# Process log

**Build clock:** started 2:00 p.m. · stopped [fill in] · I paired with Claude throughout (see README, "Tools used").

## What I did, in order

| Block | What happened |
|---|---|
| Decide | Reconciled Paul's notes (`decisions.md`): the bank is armed, not contacted; 40 meetings vs precision is sequencing; defense waits for Rob. Wrote the shared ICP and a "why the bank, not pharma or defense" table. |
| Learn | ChatGPT for the map of 4 regulations, then the Fed's primary source for SR 26-2. Found GenAI and agents are **excluded** (`3-learned.md`). Ran ~12 min over. |
| Build: gate | `reign_gate` MCP server: audit first, named human for sends, bank blocked until briefing. 10 governance tests; 7 real MCP calls through it (4 allowed, 3 blocked). |
| Build: skill | `SKILL.md` + brief eval. v1 failed, v2 passed 9/9, saved through the gate. |
| Playbook | Full Campaign Manager JSON with a `_guess` on every undefined field; `schema-guesses.md`. The gate reads it; tests still pass. |
| Docs | Day-one wiring, would-not-ship, this log, README. |
| HubSpot | Connected with ~55 min left: sandbox company + 3 fictional contacts; the gate now reads from HubSpot and writes the brief as a note and the approval as a task. Verified in HubSpot. |

## Design calls I rethought

- **One ICP or one per motion?** The stub's `audience.icp_id` says a playbook *points to* an ICP. Call: one shared, versioned ICP; one playbook per motion. A new launch changes two fields. Copies would drift.
- **Why build a gate instead of using HubSpot's or Slack's MCP?** Vendor MCPs give the agent abilities but can't write an R-17 record first. R-17: "wrap it or don't send." So vendor tools go *behind* the gate.

## What failed / where I got stuck

- **Ran ~12 min over in Learn.** Reading the primary source took longer than planned. Worth it, since it flipped my assumption. Made it back by building the gate before anything else.
- **The MCP server wouldn't start.** The client only said `McpError: Connection closed`. Next experiment: run the server by hand. The real error was a folder-path bug (`parents[2]` instead of `parents[3]`). One-line fix. Lesson: when an MCP client says "connection closed," run the server directly first.
- **Brief v1 failed, and so did my eval.** The eval caught "worth noting" (banned). Reading it myself, I found a worse problem it missed: "there is no supervisory framework for them" overclaims, since SR 26-2 only excludes agents from *its* scope. Fixed the eval, re-ran v1 (7/9), then fixed the **prompt** (`SKILL.md` rules 4a, 4b), not just the draft. v2: 9/9.
- **Lost the link to my laptop twice.** Claude builds on my machine through a desktop bridge; when it dropped, it built and tested in its cloud workspace and copied the files over later.
- **IDE showed missing imports** on the tests (pytest not installed; the gate's path added at runtime). Installed requirements, added `pyrefly.toml`. Tests: 10 passed on my Mac.
- **HubSpot moved private apps mid-run.** "Private Apps" now redirects to "Legacy Apps", which pushes you to Service Keys. Used a Service Key. Notes and tasks have no scopes of their own; they ride on `crm.objects.contacts.write` / `companies.write`.
- **MCP SDK version mismatch.** My Mac installed MCP 2.x, which renamed `FastMCP`; the client again only said "Connection closed". Pinned `mcp<2` in `requirements.txt`.
- **Key set, lookup worked, but the gate still wrote locally.** The MCP stdio client only forwards an allow-list of environment variables to the server it launches, so the server never saw `HUBSPOT_TOKEN`. Passed the environment through explicitly. Worth knowing: that default is a safety feature, and it's why secrets didn't leak into the server by accident.
- **Pasted the HubSpot key into my AI chat while debugging.** Sandbox only, but rotated it afterwards.
- **Pushing:** the AI has no GitHub login (I'm not handing it a token). It commits; I push.

## Prompts and configs

- Real prompts I used: `1-artifact/skill/trigger-brief/prompts/`
- The skill itself (the agent's instructions): `1-artifact/skill/trigger-brief/SKILL.md`
- Gate config: `1-artifact/playbook/reign-bank-sr26-2.json`

## With another 3 hours

1. **Slack approval loop:** `request_send` posts to the approver, waits for Approve / Reject, and logs who decided and when.
2. **HubSpot's own MCP behind the gate** instead of the direct API call; `briefing_booked` read from HubSpot meetings.
3. **LLM-judge overclaim check** on top of the regex, since the regex missed a real one.
4. **Verify FDA PCCP scope**, then run the pharma swap (change `audience` + `trigger`).
5. **OSFI E-23:** check how Canada's guideline treats GenAI.
