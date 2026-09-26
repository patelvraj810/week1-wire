# Process log

**Build clock:** started 2:00 p.m. · stopped [fill in]. I paired with Claude (Cowork) the whole time. I made the calls and checked the work; Claude did research legwork, code and drafts. Prompts: `1-artifact/skill/trigger-brief/prompts/prompts.md`.

## What I did, in order

| Step | What happened |
|---|---|
| Decide | Reconciled Paul's notes (`decisions.md`). Bank = armed, not contacted. 40 meetings vs precision = sequencing. Defense waits for Rob. One shared ICP. Chose the bank because R-17 is only *required* there. |
| Learn | ChatGPT for a map of 4 regulations → Fed's own text for SR 26-2 → found AI agents are **excluded** (`3-learned.md`). |
| Gate | `reign_gate` MCP server: audit record first, named human for sends, bank blocked until briefing. 10 tests, all block. |
| Skill | `SKILL.md` + brief checker. v1 failed, v2 passed 9/9. |
| Playbook | Campaign Manager JSON with a `_guess` on every gap + `schema-guesses.md`. |
| HubSpot | With ~55 min left: sandbox company + 3 fictional contacts. Gate reads them from HubSpot; brief → **note**, send → **approval task**. Checked in HubSpot. Then deleted the old local `crm_outbox/` JSON copies, since HubSpot now holds the real ones (folder is only a fallback now, and git-ignored). |

## Calls I rethought
- **One ICP or one per motion?** The stub's `audience.icp_id` means a playbook *points to* an ICP. One shared ICP; a new launch changes two fields.
- **Why my own MCP instead of HubSpot's?** Vendor MCPs give abilities but can't write an R-17 record first. R-17: "wrap it or don't send." So HubSpot sits *behind* the gate.

## What failed / where I got stuck
1. **Ran ~12 min over on learning.** Reading the Fed's text took longer than planned, but it flipped my assumption. Made it up by building the gate first.
2. **MCP server wouldn't start.** Client only said "Connection closed." Ran the server by hand: a folder-path bug (`parents[2]` vs `parents[3]`). Lesson: run the server directly first.
3. **Brief v1 overclaimed, and my checker missed it.** It caught "worth noting" but not "there is no supervisory framework." I caught that by reading. Fixed the checker, then the **prompt** (rule below), not just the text. v1 7/9 → v2 9/9.
4. **Lost the link to my laptop twice** mid-build. Claude built in its cloud workspace and copied files over.
5. **IDE showed missing imports** on the tests. Installed requirements, added `pyrefly.toml`. 10 passed on my Mac.
6. **HubSpot moved Private Apps** to Legacy Apps during the run. Switched to Service Keys. Notes/tasks have no scopes of their own; they use the contacts/companies write scopes.
7. **MCP SDK 2.x renamed `FastMCP`.** Same "Connection closed" error. Pinned `mcp<2`.
8. **Key was set, gate still wrote locally.** The MCP client only passes an allow-list of environment variables to the server. Passed the environment through on purpose.
9. **Pasted my HubSpot key into the AI chat** while debugging. Sandbox only; rotated it.
10. **Can't push from the AI's shell** (no GitHub login, on purpose). It commits, I push.

## Snippets (the brief asks for 2–3)
**Prompt that fixed v1** (`SKILL.md`, rule 4a):
```
Do not conclude that "no framework" exists for agents anywhere.
Write "SR 26-2 does not cover them", not "nothing covers them".
```
**Config the gate enforces** (`playbook/reign-bank-sr26-2.json`):
```json
"approval": {
  "principals": ["Paul (CEO)"],
  "approvers": ["Dana Whitfield (iTmethods account owner, fictional)"],
  "send_requires_named_approver": true,
  "bank_gate": "no_outbound_until_briefing_booked"
}
```
**A prompt I gave** (cleaned up from speech; see `prompts.md`):
> We have 55 minutes left. Should we connect HubSpot instead of using JSON files for the bank data?

## With another 3 hours
1. Slack approve/reject loop, logging who decided and when.
2. HubSpot's own MCP behind the gate; `briefing_booked` read from HubSpot meetings.
3. An LLM judge for overclaims, on top of the regex (the regex missed one).
4. Check FDA PCCP scope, then run the pharma swap (change `audience` + `trigger`).
5. OSFI E-23: how Canada treats GenAI.
