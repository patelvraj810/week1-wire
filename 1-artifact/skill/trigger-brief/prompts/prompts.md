# Prompts I actually used

Copied exactly as I wrote them (typos included). Tools: **Claude (Cowork)** as my build partner, **ChatGPT** for one research overview. The agent's own prompt is [`../SKILL.md`](../SKILL.md).

## 1. Decisions + ICP (Claude)
> Can you write them for me based on what we have decided so far?

"Them" = `decisions.md` and `icp.yaml`. I made the calls first, then had Claude write them up, and reviewed before committing.

## 2. Learning the regulations (ChatGPT)
> Give me details about the following acts and how they would affect a company that is selling secured AI to banks, pharma, and defence: EU AI Act, SR 26-2, DORA, or FDA PCCP) on marketing perspective

Used for the map only. I then checked the key SR 26-2 claim against the Federal Reserve's own text (`references/sr-26-2.md`).

## 3. Questioning the design (Claude)
> I want to understand something about the MCP server. They're asking if we really need to make our own MCP server. Can we not just use an app that has their own MCP? ... Also, what this exactly does—the one you have created—is it just helping us connect to HubSpot? Can we not just do it via HubSpot's MCP or HubSpot's connector or API?

Answer that shaped the build: vendor MCPs give the agent abilities, but can't write an R-17 record first. So vendor tools go *behind* the gate.

## 4. Pushing for honesty in the log (Claude)
> All right, let's get onto block three. And also let's focus on what failed and where I got stuck as well.

## 5. Choosing HubSpot over mock data (Claude)
> Now that we still have 55 minutes, do you think it's better to connect HubSpot instead of having JSON files for the bank account and this stuff? I would prefer HubSpot over anything, right? Or what would they prefer? They really don't want anyone who is just marketing or just technical. They want a mixture of both, right?

Result: HubSpot connected with a 25-minute timebox and a local fallback.

## 6. The agent's prompt (SKILL.md, excerpt)
The rule added after brief v1 overclaimed:
```
4a. Say only what the exclusion means for THIS guidance. Do not conclude that
"no framework", "no rules" or "no oversight" exists for agents anywhere; other
internal policies or regulators may apply. Write "SR 26-2 does not cover them",
not "nothing covers them".
```
