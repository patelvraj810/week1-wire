"""Drive the reign-gate MCP server over stdio, the same way an agent would.
Writes real records to 1-artifact/audit/audit-log.jsonl.  Run: python 1-artifact/evals/demo_mcp_calls.py"""
import asyncio
import os
import json
import sys
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

ART = Path(__file__).resolve().parents[1]
SRC = ["https://www.federalreserve.gov/supervisionreg/srletters/SR2602a1.pdf"]
P = "Paul (CEO)"
OWNER = "Dana Whitfield (iTmethods account owner, fictional)"
PURPOSE = "Draft an SR 26-2 brief on the agentic-AI scope gap for the bank's CAE"

CALLS = [
    ("enrich_account", dict(account_id="acct-northmere", principal=P, purpose=PURPOSE, sources=SRC)),
    ("score_account", dict(account_id="acct-northmere", principal=P, purpose=PURPOSE, sources=SRC)),
    ("score_account", dict(account_id="acct-northmere", principal=P, purpose="engagement", sources=SRC)),
    ("save_brief", dict(account_id="acct-northmere", principal=P, purpose=PURPOSE, sources=SRC,
                        brief_markdown="(placeholder until the skill drafts it)")),
    ("request_send", dict(account_id="acct-northmere", principal=P, purpose=PURPOSE, sources=SRC,
                          approver="agent", recipient=OWNER, trigger_exception=True)),
    ("request_send", dict(account_id="acct-northmere", principal=P, purpose=PURPOSE, sources=SRC,
                          approver=OWNER, recipient="Priya Raman (fictional)")),
    ("request_send", dict(account_id="acct-northmere", principal=P, purpose=PURPOSE, sources=SRC,
                          approver=OWNER, recipient=OWNER, trigger_exception=True)),
]


async def main():
    server = StdioServerParameters(command=sys.executable, args=[str(ART / "mcp" / "reign_gate" / "server.py")],
                                    env=dict(os.environ))  # MCP stdio only forwards an allow-list of env vars by default; pass HUBSPOT_TOKEN through
    async with stdio_client(server) as (r, w), ClientSession(r, w) as s:
        await s.initialize()
        print("tools:", [t.name for t in (await s.list_tools()).tools])
        for name, args in CALLS:
            res = await s.call_tool(name, args)
            out = json.loads(res.content[0].text)
            print(f"{name:15} -> {out['outcome']:8} {out.get('reasons', '')}")

asyncio.run(main())
