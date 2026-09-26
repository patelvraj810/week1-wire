"""MCP server exposing the R-17 gate as the ONLY way the agent can touch an account.

Run:  python 1-artifact/mcp/reign_gate/server.py
Tools: enrich_account, score_account, save_brief, request_send

Nothing here ever sends an email. `request_send` creates an approval task for a
named human. That is what "the send must be blockable" means in practice.

CRM: if HUBSPOT_TOKEN is set, save_brief writes a note to HubSpot.
Otherwise it writes to 1-artifact/crm_outbox/ (local stand-in, stated in README).
"""
from __future__ import annotations

import json
import os
import sys
import urllib.request
from pathlib import Path

from mcp.server.fastmcp import FastMCP

sys.path.insert(0, str(Path(__file__).parent))
from gate import Blocked, Gate  # noqa: E402

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


def _crm_write(kind: str, account_id: str, body: dict) -> str:
    token = os.getenv("HUBSPOT_TOKEN")
    if token:  # real HubSpot note (company association left out on purpose: fictional accounts)
        data = json.dumps({"properties": {"hs_note_body": json.dumps(body)[:60000],
                                          "hs_timestamp": body.get("ts", "")}}).encode()
        r = urllib.request.Request("https://api.hubapi.com/crm/v3/objects/notes", data=data,
                                   headers={"Authorization": f"Bearer {token}",
                                            "Content-Type": "application/json"})
        with urllib.request.urlopen(r, timeout=15) as resp:
            return f"hubspot:note:{json.load(resp)['id']}"
    OUTBOX.mkdir(parents=True, exist_ok=True)
    p = OUTBOX / f"{account_id}.{kind}.json"
    p.write_text(json.dumps(body, indent=2))
    return f"local:{p.relative_to(ROOT)}"


def _call(req: dict, account_id: str, do=None) -> dict:
    acct = ACCOUNTS.get(account_id)
    if not acct:
        return {"outcome": "blocked", "reasons": [f"unknown account {account_id}"]}
    try:
        out = gate.run(req, acct, do)
        return {"outcome": "allowed", "result": out["result"]}
    except Blocked as e:
        return {"outcome": "blocked", "reasons": str(e)}


@mcp.tool()
def enrich_account(account_id: str, principal: str, purpose: str, sources: list[str]) -> dict:
    """Enrich an account (Clay/ZoomInfo stand-in: reads the fixture). Audited first."""
    return _call(_req("enrich", account_id, principal, purpose, sources), account_id,
                 lambda: {k: ACCOUNTS[account_id].get(k) for k in ("name", "segment", "contacts", "signals")})


@mcp.tool()
def score_account(account_id: str, principal: str, purpose: str, sources: list[str]) -> dict:
    """Check the account against the ICP gates (e.g. risk committee). Audited first."""
    a = ACCOUNTS[account_id] if account_id in ACCOUNTS else {}
    return _call(_req("score", account_id, principal, purpose, sources), account_id,
                 lambda: {"fit": bool(a.get("has_risk_committee")) and a.get("employees", 0) >= 5000,
                          "has_risk_committee": a.get("has_risk_committee")})


@mcp.tool()
def save_brief(account_id: str, principal: str, purpose: str, sources: list[str], brief_markdown: str) -> dict:
    """Save a drafted brief to the CRM as a note. Does not send anything."""
    req = _req("create", account_id, principal, purpose, sources)
    return _call(req, account_id, lambda: _crm_write("brief", account_id,
                                                      {"brief": brief_markdown, "sources": sources}))


@mcp.tool()
def request_send(account_id: str, principal: str, purpose: str, sources: list[str], approver: str,
                 recipient: str, trigger_exception: bool = False) -> dict:
    """Ask a named human to approve sending the brief. Creates an approval task; never sends."""
    req = _req("message", account_id, principal, purpose, sources, send=True, approver=approver,
               recipient=recipient, trigger_exception=trigger_exception)
    return _call(req, account_id, lambda: _crm_write("send-task", account_id,
                                                      {"status": "awaiting_approval", "approver": approver,
                                                       "recipient": recipient}))


if __name__ == "__main__":
    mcp.run()
