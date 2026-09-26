# Eval results

## Governance (`test_governance.py`): 10/10 pass
Every test tries to break an R-17 or Paul rule and checks the gate blocks it: missing R-17 field, vague purpose, audit write failure, send with no/non-human approver, approver not on the playbook, bank outbound before briefing, kill switch, unauthorized principal. Plus: the audit record exists before the action runs, and the trigger exception only reaches the internal owner.

## Brief (`brief_eval.py`)

| Check | v1 | v2 |
|---|---|---|
| Under 400 words | PASS (362) | PASS (357) |
| Exactly 3 "what it means" bullets | PASS | PASS |
| Sources are primary URLs | PASS | PASS |
| "What changed" is footnoted | PASS | PASS |
| No banned words / no pitch | **FAIL** ("worth noting") | PASS |
| No exclamation marks | PASS | PASS |
| No false or overreaching claims | **FAIL** (after eval fix, see below) | PASS |
| Fictional labels kept | PASS | PASS |
| Marked not sent / internal | PASS | PASS |
| **Total** | **7/9** | **9/9** |

### What happened
1. First run on v1: 8/9. The eval caught a banned phrase.
2. Reading v1 myself, I found a worse problem the eval **missed**: bullet 2 said "there is no supervisory framework for them." That's an overclaim. We only know SR 26-2 excludes agents, not that nothing governs them. The regex only matched "no framework exists."
3. Fixed the **eval** first (widened the regex), re-ran on v1: 7/9, now catching both.
4. Fixed the **prompt** (`SKILL.md` rules 4a and 4b), not just the draft, then wrote v2: 9/9.

Lesson: a regex eval is only as good as the phrasings I thought of. A human read still caught something the automated check didn't. Next step would be an LLM-as-judge check for overclaims, with the regex kept as the fast first pass.
