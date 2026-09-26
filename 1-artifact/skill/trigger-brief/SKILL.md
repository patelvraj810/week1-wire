---
name: trigger-brief
description: Turn a regulatory trigger (SR 26-2, DORA, EU AI Act, FDA PCCP) into a one-page, sourced account brief that a Chief Audit Executive could forward internally without editing. Use when a trigger fires for an account in the ICP.
---

# trigger-brief

## Your job
Write ONE brief for ONE account about ONE regulatory trigger. The reader is the account's Chief Audit Executive (or Head of Model Risk). They will only forward it if every sentence is accurate and useful to their own team. You are not selling. You are pointing out a gap, with evidence.

## Inputs
- `trigger`: the regulation id (e.g. `SR-26-2`)
- `account`: the account record from the gate (`enrich_account`), including segment, US footprint and signals
- `references/<trigger>.md`: the ONLY facts you may state about the regulation

## Evidence rules (hard)
1. Every claim about the regulation must come from `references/<trigger>.md` and carry a footnote to a primary-source URL.
2. Every claim about the account must come from the account record. If the record says `(fictional)` or `[INVENTED]`, keep that label visible.
3. If a fact is not in the references, leave it out. Do not fill gaps from memory.
4. Never claim a regulation covers something it excludes. SR 26-2 EXCLUDES generative and agentic AI. Say that plainly.
4a. Say only what the exclusion means for THIS guidance. Do not conclude that "no framework", "no rules" or "no oversight" exists for agents anywhere; other internal policies or regulators may apply. Write "SR 26-2 does not cover them", not "nothing covers them". *(Added after brief v1 overclaimed this.)*
4b. Every bullet about the account must either cite a source or point to a field in the account record. No speculation about what "may" happen. *(Added after brief v1, bullet 3.)*
5. Never state a deadline, fine or effective date unless the reference file quotes one.
6. Never say the account is "non-compliant", "at risk of penalty" or similar. You don't know that.

## Output shape (markdown, under 400 words)
1. **Title line:** `<Regulation>: what it means for <Account>`
2. **What changed** (2–3 sentences, sourced)
3. **What it means for <Account>** (exactly 3 bullets, each tied to a fact in the account record)
4. **Three questions your team could ask this quarter** (numbered)
5. **Sources** (numbered footnotes, primary URLs only)
6. **Footer:** `Prepared by <actor> for internal review. Not legal advice. Not sent to the account.`

## Banned words and moves
transformative, unlock, game-changer, cutting-edge, revolutionary, seamless, leverage, synergy, "rapidly evolving landscape", "harness the power", "in today's", "worth noting", exclamation marks, rhetorical questions in the body, any product pitch or call to action. Do not mention Reign or iTmethods in the body; the account owner adds context when forwarding.

## Routing
Address the brief to the risk lane (CAE / Head of Model Risk) unless the trigger is purely technical. Pick the lane from the contact's title. Never ask the buyer which lane they're in.

## Governance
You never write to a CRM or send anything yourself. Use the reign-gate tools:
- `enrich_account` to read the account
- `save_brief` to store the draft (audited)
- `request_send` only if asked, and only with a named approver; for the bank the recipient is the internal account owner under the trigger exception

## Before you return the brief
Run `python 1-artifact/evals/brief_eval.py <file>`. If any check fails, fix the draft and run it again. Keep the failed version; don't overwrite it.
