# Day-one wiring: Clay, ZoomInfo, HubSpot, Slack

I didn't have Clay, ZoomInfo or a HubSpot workflow tier for this run. Here's what's mocked today and what I'd wire on day one. The rule doesn't change: **every vendor tool sits behind `reign_gate`.** The agent never gets direct access to a vendor's API or MCP, because none of them can write an R-17 record before acting ("wrap it or don't send").

| Tool | Today (mocked) | Day one | Gate tool it sits behind |
|---|---|---|---|
| **Clay** | `fixtures/bank-account.json` | A Clay table keyed on account domain: employee count, US footprint, agents-in-production signals, risk-committee flag (from 10-K / proxy / careers pages). The gate calls Clay's HTTP API; each enrichment is one audited `enrich` action. | `enrich_account` |
| **ZoomInfo** | Fictional contacts in the fixture | Pull contacts by title for the two lanes (risk: CAE, Head of MRM, CRO; engineering: VP Eng, Head of AI Platform). Store title + lane only; no personal email is used, because nothing emails the bank. | `enrich_account` |
| **HubSpot** | **Live in a sandbox.** Gate reads the company + contacts; brief = note, send = task. Local fallback without a key. | System of record, as Paul wants. The brief is a note on the company; the send is a task assigned to the approver; `briefing_booked` comes from a meeting on the deal. Put HubSpot's own MCP **behind** the gate instead of calling the API directly. | `save_brief`, `request_send` |
| **Slack** | Approval = a task file | `request_send` posts the brief to the approver in Slack with Approve / Reject. The gate waits for the reply and writes the decision (who, when) into the audit record. Only an approved task can move forward. | `request_send` |

## What stays the same when a tool is swapped

- The audit record is written first, and a failed write stops the action.
- Sends need a named human from the playbook.
- The bank stays blocked until a briefing is booked.

Swapping HubSpot for Salesforce, or Clay for another enrichment tool, only changes the small adapter behind the gate, not the rules.
