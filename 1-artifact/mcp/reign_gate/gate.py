"""reign_gate: the R-17 gate.

Every agent action that touches a prospect goes through `Gate.run()`.
The gate writes an audit record FIRST. If the record can't be written,
or a rule fails, the action does not happen.

Rules come from three places in the packet:
- R-17: FS actions (create, update, enrich, score, message) need a full
  audit record; a send needs a named human approver and must be blockable.
- Paul's notes: "Everything that sends needs a named human." (all segments)
- Paul's notes: no outbound to the bank until a briefing is booked, except a
  regulatory trigger, where the brief goes to the internal account owner.
"""
from __future__ import annotations

import json
import datetime as dt
from pathlib import Path
from typing import Any, Callable

R17_ACTIONS = {"create", "update", "enrich", "score", "message"}
R17_FIELDS = ("actor", "principal", "action", "object", "purpose", "sources", "send")
VAGUE_PURPOSES = {"engagement", "outreach", "follow up", "follow-up", "marketing", "nurture", "touch"}
NOT_HUMANS = {"", "agent", "system", "bot", "auto", "automation", "claude"}


class Blocked(Exception):
    """Raised when the gate refuses an action. The action did not happen."""


class Gate:
    def __init__(self, playbook: dict, audit_path: str | Path):
        self.playbook = playbook
        self.audit_path = Path(audit_path)

    # ---------- audit ----------
    def _write(self, record: dict) -> None:
        """Append one JSON line. Any failure propagates: no record, no action."""
        self.audit_path.parent.mkdir(parents=True, exist_ok=True)
        with self.audit_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

    # ---------- rules ----------
    def _check(self, req: dict, account: dict) -> list[str]:
        problems: list[str] = []
        fs = bool(account.get("financial_services"))
        policy = self.playbook["audit"]["policy"]  # {"fs": "required", "non_fs": "on_by_default"}

        if self.playbook.get("kill_switch"):
            problems.append("kill switch is on: CRO stopped this motion")

        if req.get("action") not in R17_ACTIONS:
            problems.append(f"unknown action '{req.get('action')}'")

        # R-17 fields: required for FS; for non-FS they are recorded but only warned
        missing = [k for k in R17_FIELDS if req.get(k) in (None, "", [])]
        if missing and (fs or policy["non_fs"] == "required"):
            problems.append(f"R-17 fields missing: {', '.join(missing)}")

        purpose = (req.get("purpose") or "").strip().lower()
        if fs and (purpose in VAGUE_PURPOSES or len(purpose.split()) < 6):
            problems.append("purpose must be one specific sentence, not 'engagement'")

        principals = self.playbook["approval"]["principals"]
        if fs and req.get("principal") not in principals:
            problems.append(f"principal '{req.get('principal')}' is not an authorized human for this motion")

        # Sends: Paul's rule applies to every segment
        if req.get("send"):
            approver = (req.get("approver") or "").strip()
            if approver.lower() in NOT_HUMANS:
                problems.append("send=true needs a named human approver")
            elif approver not in self.playbook["approval"]["approvers"]:
                problems.append(f"approver '{approver}' is not on this playbook's approver list")

            # Bank gate: no outbound until briefing booked; trigger exception = internal only
            if fs and not account.get("briefing_booked"):
                if req.get("trigger_exception") and req.get("recipient") == account.get("internal_owner"):
                    pass  # brief goes to our own Forge account owner, not the bank
                else:
                    problems.append("bank outbound blocked: no Executive Assurance Briefing booked "
                                    "(trigger exception only allows the internal account owner)")
        return problems

    # ---------- entry point ----------
    def run(self, req: dict, account: dict, do: Callable[[], Any] | None = None) -> dict:
        """Check rules, write the audit record, then (only if allowed) do the action."""
        problems = self._check(req, account)
        record = {
            "ts": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
            "playbook_id": self.playbook["playbook_id"],
            "playbook_version": self.playbook["version"],
            "segment": account.get("segment"),
            "financial_services": bool(account.get("financial_services")),
            **{k: req.get(k) for k in R17_FIELDS},
            "approver": req.get("approver"),
            "recipient": req.get("recipient"),
            "outcome": "blocked" if problems else "allowed",
            "reasons": problems,
        }
        # Audit FIRST. If this raises, we never reach the action.
        try:
            self._write(record)
        except Exception as e:  # noqa: BLE001
            raise Blocked(f"audit record could not be written ({e}); action not performed") from e

        if problems:
            raise Blocked("; ".join(problems))

        result = do() if do else None
        return {"outcome": "allowed", "record": record, "result": result}
