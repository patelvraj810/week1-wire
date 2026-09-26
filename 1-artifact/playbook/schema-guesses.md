# Campaign Manager: my guesses

The stub gave `playbook_id`, `product`, `audience`, `trigger`, `channel`, and empty `approval`, `kill_criteria` and `audit`. It listed three unknowns. Here's what I assumed and why. Every guess is also a `_guess_*` key inside `reign-bank-sr26-2.json`.

## The three unknowns

| Unknown | My guess | Why |
|---|---|---|
| **How do playbooks version?** | Semver per playbook (`0.1.0`). Every audit record stores `playbook_id` + `version`. Changing approvers or kill criteria = minor bump; changing audience or trigger = a new playbook. | An auditor needs to know which rules were live when an action happened. |
| **Can one playbook have many triggers?** | Yes: `trigger` is a list, and each entry can be switched off. | Paul names two triggers for the bank (SR 26-2, DORA). Cloning a playbook per regulation would fork the approvers and kill criteria. |
| **What does "briefing" mean as a channel?** | A sourced brief handed to the internal account owner, plus a calendar hold for the Executive Assurance Briefing. Not a cold Calendly link, not an email sequence. | Paul: no outbound to the bank until the briefing is booked. The brief is what gets the briefing booked. |

## Other decisions

- **`audience` points to the ICP instead of copying it** (`icp_id` + `segment`). A new launch changes those two fields and nothing else. See `next_swap` at the bottom of the JSON.
- **`approval` is split in two:** `principals` (who authorized this *class* of action, per R-17) and `approvers` (who approves each *send*).
- **`kill_criteria` are named rules with a set action**, owned by the CRO. Flipping `kill_switch` makes the gate block every action (tested). No bounce or open-rate metrics, because nothing here sends email.
- **Added `status`** (`armed` / `live` / `paused` / `killed`). The bank motion is `armed`: drafts and internal handoffs only.

## Not decided

- Who can flip `kill_switch` in practice (the CRO in Campaign Manager's UI, presumably).
- Whether HubSpot or Campaign Manager is the source of truth for `briefing_booked`. Today it's a field in the fixture.
