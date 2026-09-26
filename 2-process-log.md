# Process log

> RAW NOTES, written during the run. Trim to one page in the last block.

## Timeline

| Block | What happened |
|---|---|
| Decide | Reconciled Paul's notes into `decisions.md`; wrote the living ICP; added a "why the bank, not pharma or defense" table. |
| Learn | ChatGPT overview of the four regulations → Fed primary source for SR 26-2 → found GenAI and agentic AI are excluded (see `3-learned.md`). Ran over time here. |

## Design decisions I rethought

**One ICP, or one per motion?**
- *Question I hit:* Paul wants "one playbook we can reuse on the next product launch." Should each motion's playbook carry its own copy of the ICP, so a launch only touches one file?
- *What I noticed:* the Campaign Manager stub already has `audience: { icp_id, segment }`. The playbook is meant to **point to** an ICP, not contain one.
- *Call:* one shared, versioned `icp.yaml` (who we sell to) and one playbook per motion (how this motion runs). A new launch = a new playbook that points at a different segment. The ICP only changes when leadership changes who we target.
- *Why it matters:* copying the ICP into every playbook means a rule change (e.g., Rob's risk-committee gate) has to be edited in every file, and motions drift apart on who counts as a target.

## What failed / where I got stuck

-

## Prompts, skills and configs

- See `1-artifact/skill/trigger-brief/prompts/`.

## With another 3 hours

- Check OSFI E-23's treatment of GenAI for the Canadian angle.
- Verify FDA PCCP scope against FDA's own guidance before building the pharma swap.
