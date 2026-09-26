"""Save a finished brief through the reign-gate MCP server (audited), then request approval
to hand it to the internal account owner under the trigger exception. Never sends to the bank.
Run: python 1-artifact/skill/trigger-brief/save_via_gate.py 1-artifact/briefs/northmere-sr26-2-v2.md"""
import asyncio
import os
import json
import sys
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

ART = Path(__file__).resolve().parents[2]
SRC = ["https://www.federalreserve.gov/supervisionreg/srletters/SR2602.htm",
       "https://www.federalreserve.gov/supervisionreg/srletters/SR2602a1.pdf"]
OWNER = "Dana Whitfield (iTmethods account owner, fictional)"
PURPOSE = "Store the SR 26-2 agentic-AI scope-gap brief for Northmere's CAE for internal review"


async def main(brief_path: str):
    brief = Path(brief_path).read_text()
    server = StdioServerParameters(command=sys.executable, args=[str(ART / "mcp" / "reign_gate" / "server.py")],
                                    env=dict(os.environ))  # MCP stdio only forwards an allow-list of env vars by default; pass HUBSPOT_TOKEN through
    async with stdio_client(server) as (r, w), ClientSession(r, w) as s:
        await s.initialize()
        for name, args in [
            ("save_brief", dict(account_id="acct-northmere", principal="Paul (CEO)", purpose=PURPOSE,
                                sources=SRC, brief_markdown=brief)),
            ("request_send", dict(account_id="acct-northmere", principal="Paul (CEO)",
                                  purpose="Ask the account owner to approve forwarding the SR 26-2 brief internally",
                                  sources=SRC, approver=OWNER, recipient=OWNER, trigger_exception=True)),
        ]:
            out = json.loads((await s.call_tool(name, args)).content[0].text)
            print(f"{name:13} -> {out['outcome']} {out.get('result') or out.get('reasons', '')}")

asyncio.run(main(sys.argv[1]))
