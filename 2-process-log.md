# Process log

**Build clock:** started 2:00 p.m. · stopped [fill in]

I worked with Claude (Cowork) as my partner the whole time. I made the decisions and checked the work. Claude did a lot of the research legwork, wrote most of the code, and drafted documents for me to review. My prompts are in `1-artifact/skill/trigger-brief/prompts/prompts.md`.

## How the three hours went

**Making sense of Paul's notes.** The first thing I noticed was that the notes fight each other. The bank matters most, but I'm not allowed to contact the bank. The CRO wants 40 meetings, but Paul wants precision. I didn't try to do everything. I picked one account (the bank), one trigger (SR 26-2) and one artifact, and wrote down why in `decisions.md`. The bank won because it's the only place where R-17 is *required*, so it's where I can really prove I follow it. Pharma became "the next swap," and defense waits for Rob.

**Learning SR 26-2.** I knew nothing about it. I used ChatGPT for a quick map of the four regulations, then read the Fed's own document. That changed my plan: I expected new AI rules, but SR 26-2 actually leaves AI agents out. So the brief isn't "new rules are coming," it's "your agents aren't covered, so who is checking them?" This took longer than planned; I ran about 12 minutes over.

**Building the gate before the brief.** Since R-17 is a knockout, I built the guard first: every agent action writes an audit record before it happens, nothing sends without a named person, and the bank stays blocked until a meeting is booked. Then I wrote tests that try to break each rule. All 10 get blocked.

**Asking why, not just building.** At one point I stopped and asked why we needed our own MCP server when HubSpot and Slack already have one. The answer made the design clearer to me: their tools give the agent abilities, but they can't write an R-17 record first. So their tools sit *behind* my gate. I also asked Claude to explain every file to me in simple words, because I wanted to understand what I was shipping.

**Writing the brief.** Claude drafted it using the rules in `SKILL.md`, and my checker tested it.

**Filling in the playbook.** The Campaign Manager stub had gaps, so I marked every guess with `_guess` and answered the three open questions in `schema-guesses.md`. I also decided the playbook should point to one shared ICP instead of copying it, so the next launch only changes two fields.

**Connecting HubSpot.** With about 55 minutes left, I decided a real CRM was worth it: Paul calls HubSpot the system of record, and they grade tool range. I gave it a 25-minute limit with a fallback. It worked: the gate now reads the bank and its contacts from HubSpot, saves the brief as a note, and turns "send" into a task a person must approve. After that, I deleted the old local JSON copies of the brief and task (`crm_outbox/`), because HubSpot holds the real ones now.

## What went wrong, and what I did

1. **The first brief overclaimed, and my checker missed it.** It caught a banned phrase ("worth noting"), but not the real problem: the brief said there is "no supervisory framework" for agents. That's too strong, since SR 26-2 only leaves them out of *its own* scope. I caught it by reading. I fixed the checker first, then the agent's rules, not just the text. v1 scored 7/9, v2 passed 9/9. Lesson: an automatic check only finds what you thought to look for.
2. **The MCP server wouldn't start, twice.** Both times the error only said "Connection closed." Running the server by hand showed the real cause: first a wrong folder path, later a new version of the MCP library that renamed a class. I fixed the path and pinned the library version. Lesson: run the server directly before guessing.
3. **HubSpot had moved "Private Apps"** to a new place during the run. I switched to their Service Keys. I also learned notes and tasks don't have their own permissions; they use the contacts and companies ones.
4. **The key was set, but the gate still saved locally.** The MCP client only passes a few safe settings to the server by default, so the server never saw my key. I passed it through on purpose.
5. **I pasted my HubSpot key into the chat while debugging.** It was a test account, but I replaced the key afterwards.

## Snippets
**The rule I added to the agent after v1** (`SKILL.md`, rule 4a):
```
Do not conclude that "no framework" exists for agents anywhere.
Write "SR 26-2 does not cover them", not "nothing covers them".
```
**The config the gate enforces** (`playbook/reign-bank-sr26-2.json`):
```json
"approval": {
  "principals": ["Paul (CEO)"],
  "approvers": ["Dana Whitfield (iTmethods account owner, fictional)"],
  "send_requires_named_approver": true,
  "bank_gate": "no_outbound_until_briefing_booked"
}
```
**A prompt I gave** (cleaned up from speech):
> We have 55 minutes left. Should we connect HubSpot instead of using JSON files for the bank data?

## With another three hours
1. A Slack approve/reject step that logs who approved and when.
2. HubSpot's own MCP behind the gate, and "meeting booked" read straight from HubSpot.
3. A second, AI-based check for overclaims, since the simple one missed one.
4. Confirm FDA PCCP really applies to a pharma quality team, then run the pharma swap.
5. Look at OSFI E-23 to see how Canada treats AI agents.
