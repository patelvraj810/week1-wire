"""MCP server exposing the R-17 gate as the ONLY way the agent can touch an account.

Run:  python 1-artifact/mcp/reign_gate/server.py
Tools: enrich_account, score_account, save_brief, request_send

Nothing here ever sends an email. `request_send` creates an approval task for a
named human. That is what "the send must be blockable" means in practice.

CRM: if HUBSPOT_TOKEN is set, accounts are read from HubSpot (overriding the fixture where
HubSpot has a value), briefs become notes and send requests become tasks on the company.
Otherwise everything uses fixtures/ and crm_outbox/ (local stand-in, stated in README).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

from mcp.server.fastmcp import FastMCP

sys.path.insert(0, str(Path(__file__).parent))
from gate import Blocked, Gate  # noqa: E402
import hubspot  # noqa: E402

ROOT = Path(__file__).resolve().parents[3]          # repo root (reign_gate → mcp → 1-artifact → root)
ART = ROOT / "1-artifact"
PLAYBOOK = json.loads((ART / "playbook" / "reign-bank-sr26-2.json").read_text())
ACCOUNTS = {a["id"]: a for a in json.loads((ART / "fixtures" / "bank-account.json").read_text())["accounts"]}
gate = Gate(PLAYBOOK, ART / "audit" / "audit-log.jsonl")
OUTBOX = ART / "crm_outbox"
ACTOR = "trigger-brief-agent@0.1.0"

mcp = FastMCP("reign-gate")


def _req(action, account_id, principal, purpose, sources, send=False, **extra):
    return {"actor": ACTOR, "principal": principal, "action": action, "object": account_id,
            "purpose": purpose, "sources": sources, "send": send, **extra}


def _account(account_id: str) -> dict | None:
    """Fixture first; if HubSpot is connected, HubSpot values win where they exist."""
    acct = dict(ACCOUNTS[account_id]) if account_id in ACCOUNTS else None
    if acct and hubspot.enabled():
        try:
            hs = hubspot.find_company(acct["name"])
        except Exception as e:  # noqa: BLE001  keep working on the fixture, but say so
            acct["source"] = f"fixture (HubSpot read failed: {str(e)[:120]})"
            hs = None
        if hs:
            acct.update({k: v for k, v in hs.items() if v not in (None, [], "")})
            acct["source"] = "hubspot"
    return acct


def _crm_write(kind: str, account: dict, body: dict) -> str:
    if hubspot.enabled() and account.get("hubspot_id"):
        if kind == "brief":
            return hubspot.add_note(account["hubspot_id"], body["brief"])
        return hubspot.add_task(account["hubspot_id"],
                                f"Approve: forward SR 26-2 brief ({account['name']})",
                                json.dumps(body, indent=2))
    OUTBOX.mkdir(parents=True, exist_ok=True)
    p = OUTBOX / f"{account['id']}.{kind}.json"
    p.write_text(json.dumps(body, indent=2))
    return f"local:{p.relative_to(ROOT)}"


def _call(req: dict, account_id: str, do=None) -> dict:
    acct = _account(account_id)
    if not acct:
        return {"outcome": "blocked", "reasons": [f"unknown account {account_id}"]}
    try:
        out = gate.run(req, acct, (lambda: do(acct)) if do else None)
        return {"outcome": "allowed", "result": out["result"]}
    except Blocked as e:
        return {"outcome": "blocked", "reasons": str(e)}


@mcp.tool()
def enrich_account(account_id: str, principal: str, purpose: str, sources: list[str]) -> dict:
    """Enrich an account (Clay/ZoomInfo stand-in: reads the fixture). Audited first."""
    return _call(_req("enrich", account_id, principal, purpose, sources), account_id,
                 lambda a: {k: a.get(k) for k in ("name", "segment", "contacts", "signals", "source")})


@mcp.tool()
def score_account(account_id: str, principal: str, purpose: str, sources: list[str]) -> dict:
    """Check the account against the ICP gates (e.g. risk committee). Audited first."""
    return _call(_req("score", account_id, principal, purpose, sources), account_id,
                 lambda a: {"fit": bool(a.get("has_risk_committee")) and a.get("employees", 0) >= 5000,
                            "has_risk_committee": a.get("has_risk_committee")})


@mcp.tool()
def save_brief(account_id: str, principal: str, purpose: str, sources: list[str], brief_markdown: str) -> dict:
    """Save a drafted brief to the CRM as a note. Does not send anything."""
    req = _req("create", account_id, principal, purpose, sources)
    return _call(req, account_id, lambda a: _crm_write("brief", a,
                                                      {"brief": brief_markdown, "sources": sources}))


@mcp.tool()
def request_send(account_id: str, principal: str, purpose: str, sources: list[str], approver: str,
                 recipient: str, trigger_exception: bool = False) -> dict:
    """Ask a named human to approve sending the brief. Creates an approval task; never sends."""
    req = _req("message", account_id, principal, purpose, sources, send=True, approver=approver,
               recipient=recipient, trigger_exception=trigger_exception)
    return _call(req, account_id, lambda a: _crm_write("send-task", a,
                                                      {"status": "awaiting_approval", "approver": approver,
                                                       "recipient": recipient}))


if __name__ == "__main__":
    mcp.run()
