# Week-1 Wire: governed regulatory-trigger brief agent

iTmethods · Growth Engineer (AI-Native) take-home · Vraj Patel

**What this is:** a Claude skill that turns a regulatory trigger (**SR 26-2**) into a short, sourced brief a bank's Chief Audit Executive could forward internally, for one account (a fictional Canadian D-SIB).

**How it's kept safe:** every action the agent takes goes through `reign_gate`, an MCP server that enforces **R-17**. It writes the audit record first, needs a named human for any send, and blocks the bank until a briefing is booked.

```
SR 26-2 fires ──► agent (SKILL.md) drafts brief ──► reign_gate checks rules + writes audit ──► named human approves
                                                        │
                                                        └── blocked? logged with the reason, nothing happens
```

**The finding it's built on:** SR 26-2 explicitly puts generative and agentic AI *out of scope*. Banks got a new model-risk rulebook that doesn't cover their agents, so the controls have to live in the tooling.

## The four deliverables

| # | Deliverable | Where |
|---|---|---|
| 1 | Working artifact | [`1-artifact/`](1-artifact/): the skill, the gate, the brief, the evals |
| 2 | Process log | [`2-process-log.md`](2-process-log.md) |
| 3 | One thing I didn't know | [`3-learned.md`](3-learned.md) |
| 4 | What I wouldn't ship | [`4-would-not-ship.md`](4-would-not-ship.md) |

## Run it (2 commands)

```
pip install -r requirements.txt
export HUBSPOT_TOKEN=...   # optional: HubSpot service key (companies + contacts read/write); without it, local fallback
pytest 1-artifact/evals -q                                                        # 10 R-17 governance tests, all must block
python 1-artifact/evals/brief_eval.py 1-artifact/briefs/northmere-sr26-2-v2.md    # brief checks (v1 fails, v2 passes)
```

Optional: `python 1-artifact/evals/demo_mcp_calls.py` drives the MCP server like an agent would and appends to the audit log.

## What's in `1-artifact/`

| File | What it is |
|---|---|
| `decisions.md` | Paul's contradictions → my calls, what I refused, open questions for Rob and Paul |
| `icp.yaml` | Shared living ICP; guesses marked `[INVENTED]` / `[UNVETTED]` |
| `references/sr-26-2.md` | SR 26-2 facts, quoted from the Fed's own text |
| `skill/trigger-brief/SKILL.md` | The agent's instructions (evidence rules, banned words, output shape) |
| `mcp/reign_gate/` | `gate.py` = the R-17 rules; `server.py` = the MCP server (4 tools, never sends email) |
| `playbook/` | Campaign Manager playbook, a `_guess` on every undefined field; `schema-guesses.md` |
| `briefs/` | v1 (failed eval, kept on purpose) and v2 (passed) |
| `evals/` | Governance tests, brief eval, `results.md` (v1 vs v2) |
| `audit/audit-log.jsonl` | Real records from MCP tool calls, including blocked ones |
| `fixtures/` | Fictional bank and people. Nothing real, since the repo is public. |
| `day-one-wiring.md` | How Clay, ZoomInfo, HubSpot and Slack plug in behind the gate |

## Tools used

| Tool | Used for |
|---|---|
| **Claude (Cowork)** | My pair for the whole run: research, writing the code, drafting the brief as the agent (following `SKILL.md`), drafting docs. I made the calls, reviewed everything and approved each commit. |
| **ChatGPT** | First overview of the four regulations. Treated as unverified; checked against the Fed's text. |
| **MCP (Python SDK)** | `reign_gate`, the custom MCP server |
| **pytest** | Evals |
| **HubSpot** | **Live, behind the gate.** The gate reads Northmere and its contacts from HubSpot; `save_brief` wrote the v2 brief as a note on the company and `request_send` created an approval task (High priority, not started). Nothing emails anyone. Without `HUBSPOT_TOKEN` it falls back to `fixtures/` and `crm_outbox/`. |
| **Clay, ZoomInfo** | Not available; mocked with fixtures. Day-one plan in `day-one-wiring.md`. |

## Real vs mocked

- **Real:** the MCP server, the gate's rules, the tests, the audit log, the SR 26-2 research, the brief and its eval, **and the HubSpot sandbox** (fictional company + 3 contacts; brief saved as a note and approval task through the gate).
- **Mocked:** the bank and its people (fictional), enrichment (fixture instead of Clay/ZoomInfo), approvals (a HubSpot task instead of a Slack approve/reject loop).

`reign_gate` = the R-17 gate, plus Paul's rule ("everything that sends needs a named human") and the bank briefing rule.
