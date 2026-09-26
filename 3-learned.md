# One thing I did not know

**SR 26-2, and that it deliberately leaves AI agents out.**

## At 0:00

I knew nothing about bank regulation. I'd never heard of SR 26-2, and I assumed any new 2026 banking guidance would *add* rules for AI.

## How I got dangerous in it

1. **Got the map fast.** Asked ChatGPT to explain the EU AI Act, SR 26-2, DORA and FDA PCCP from the angle of a company selling secure AI to banks, pharma and defense. Useful for orientation; I treated all of it as unverified.
2. **Went to the primary source for the one I was building on.** Read the Federal Reserve's SR 26-2 cover letter and guidance attachment, and wrote down only what I could quote (`1-artifact/references/sr-26-2.md`).
3. **Cross-checked.** The key point matched the Fed's text: *"Generative AI and agentic AI models are novel and rapidly evolving. As such, they are not within the scope of this guidance."* (SR 26-2 attachment, p. 3)
4. **Used it right away.** Rewrote the brief's angle and added evals so the agent can't repeat the mistake I almost made.

## What changed in my head

My assumption was backwards. SR 26-2 (April 17, 2026; Fed, OCC and FDIC; replaces SR 11-7; mostly for banks over $30B) refreshes model-risk management for **traditional** models and puts GenAI and agents **out of scope**.

That flips the pitch. It isn't "new AI rules are coming." It's "the new rulebook doesn't cover your agents, so who in audit is testing them, and against what?" The honest answer for most banks is "an internal policy we still have to write." That's the gap a CAE would forward internally, and the reason controls like the R-17 gate have to live in the tooling.

## How it changed what I built

- The brief's angle: from "new rules for your AI" to "the new guidance carves agents out; here's the audit gap and three questions to ask."
- A new eval: fail any brief that says SR 26-2 covers GenAI or agents, or that states a deadline.
- After brief v1, a stricter rule: say "SR 26-2 doesn't cover them", never "nothing covers them."

## What I can do now

- Explain in one sentence what SR 26-2 covers, who it's for and what it excludes.
- Separate a quotable claim from a plausible one, and keep the plausible ones out of anything an auditor reads.

## Still open

- ChatGPT said the guidance tells banks to use their existing governance for tools outside its scope. I haven't found that sentence in the Fed text yet.
- OSFI E-23: does Canada's model-risk guideline treat GenAI differently?
- FDA PCCP scope (from the ChatGPT overview, not verified): it seems to apply to AI-enabled medical devices, not pharma broadly.
