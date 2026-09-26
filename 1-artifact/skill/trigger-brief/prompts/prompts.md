# Prompts I used

Tools: **Claude (Cowork)** as my build partner, **ChatGPT** for one research overview. The agent's own prompt is [`../SKILL.md`](../SKILL.md).

> **Note:** I mostly spoke my prompts, so the originals were rough. The Claude prompts below are cleaned up for grammar and clarity; the meaning and the order are exactly what I asked. The ChatGPT prompt is word for word.

## 1. Write up my decisions (Claude)
> Based on what we've decided so far, write `decisions.md` and `icp.yaml` for me. Keep my calls as they are: bank only, pharma is the next swap, defense waits for Rob. Mark anything we invented.

I reviewed both files before committing.

## 2. Learn the regulations (ChatGPT, word for word)
> Give me details about the following acts and how they would affect a company that is selling secured AI to banks, pharma, and defence: EU AI Act, SR 26-2, DORA, or FDA PCCP) on marketing perspective

Used for the map only. I checked the key SR 26-2 claim against the Federal Reserve's own text.

## 3. Explain the code to me (Claude)
> I don't understand all of these files yet. Explain each file you created in simple English: what it does and why it's needed. Don't change anything, just explain.

I wanted to be able to defend every file myself, not just ship it.

## 4. Question the design (Claude)
> Do we really need our own MCP server? Why not use HubSpot's or Slack's MCP directly, since they already exist? Is the one you built just a HubSpot connector?

The answer shaped the build: vendor MCPs give the agent abilities but can't write an R-17 record first, so they go *behind* the gate.

## 5. Record what went wrong (Claude)
> Start the build, and keep track of what fails and where I get stuck as we go. I want that in the process log.

## 6. Decide on HubSpot (Claude)
> We have 55 minutes left. Should we connect HubSpot instead of using JSON files for the bank data? They want someone who is both technical and GTM, not just one.

Result: HubSpot connected with a 25-minute timebox and a local fallback.

## 7. The agent's prompt (`SKILL.md`, excerpt)
The rule added after brief v1 overclaimed:
```
4a. Say only what the exclusion means for THIS guidance. Do not conclude that
"no framework", "no rules" or "no oversight" exists for agents anywhere; other
internal policies or regulators may apply. Write "SR 26-2 does not cover them",
not "nothing covers them".
```
