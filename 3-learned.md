# One thing I did not know

> RAW NOTES, written during the run. Polish in the last block.

## What I knew at 0:00

Nothing about banking regulation. I'd never heard of SR 26-2, and I assumed any new 2026 bank guidance would add rules for AI.

## How I learned it (in order)

1. **Broad overview with ChatGPT.** I asked it to explain the EU AI Act, SR 26-2, DORA and FDA PCCP from the point of view of a company selling secure AI to banks, pharma and defense. Useful for the map, but I treated it as unverified.
2. **Went to the primary source for the one I'm using.** Read the Federal Reserve's SR 26-2 letter and guidance attachment (`1-artifact/references/sr-26-2.md`).
3. **Cross-checked.** The key nuance ChatGPT gave me (GenAI and agentic AI are out of scope) matched the Fed's own text, word for word.

## What surprised me

- **SR 26-2 explicitly excludes generative and agentic AI:** "Generative AI and agentic AI models are novel and rapidly evolving. As such, they are not within the scope of this guidance." (SR 26-2 attachment, p. 3.) My assumption was backwards. The new rulebook for large US banks refreshes model-risk management and **leaves agents out**.
- **So the gap is the trigger.** Banks running agents have no supervisory framework to point to when an auditor asks "who approved this agent action, and where's the record?" The controls have to live in the tooling. That's what the R-17 gate does.
- **FDA PCCP is narrower than I thought.** It applies to AI-enabled *medical device* software, not pharma broadly. A pharma quality org may or may not have a PCCP problem, depending on whether they ship an AI device. Another reason not to lead with pharma. *(From the ChatGPT overview; not verified against FDA's text in this run.)*
- **Defense is outside the EU AI Act** for military and national-security uses, so "AI Act compliance" is the wrong pitch there. *(ChatGPT overview; not verified.)*

## How it changed what I built

- The brief's message changed from "new AI rules for banks" to "the new guidance carves agents out, and here's the audit gap."
- I added an eval: fail any brief that claims SR 26-2 regulates GenAI or agents, or that states a deadline.
- Nothing about the gate changed. The finding made it more relevant.

## What I can do now that I couldn't at 0:00

- Explain in one sentence what SR 26-2 covers, who it's for (mostly banks over $30B in assets) and what it excludes.
- Tell a sourced claim from a plausible-sounding one, and keep the unverified ones out of anything a CAE would read.

## Still open (next 3 hours)

- ChatGPT said the guidance tells banks to use their existing governance for tools outside its scope. I haven't found that sentence in the Fed text yet.
- OSFI E-23: does the Canadian guideline treat GenAI differently?
