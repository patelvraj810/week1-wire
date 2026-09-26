# What I would not ship

Things I refused to build, or built and would hold back, and why. Most of these would embarrass iTmethods in front of a bank's audit team.

1. **Any outbound to the bank before the briefing is booked.** Paul said no, and a cold AI-written message to a CAE about a regulation is exactly the "generic AI governance" email he said would kill the motion. The gate blocks it, and there's a test for it.

2. **A brief with a claim I can't source to the primary text.** Brief v1 said "there is no supervisory framework" for agents. SR 26-2 only says agents are outside *its* scope. A CAE would catch that in one read, and the brief would be dead. Anything not in `references/` gets cut, not guessed.

3. **Any deadline, fine or "you're non-compliant" line.** SR 26-2 doesn't state one that I found, and we don't know the bank's compliance status. Fear-based urgency in a brief to an auditor destroys trust. The eval fails a brief that does this.

4. **Auto-send, even with a good brief.** Every send is an approval task for a named human. An agent that emails a financial institution on its own, without an audit record, is the thing R-17 exists to prevent.

5. **Vendor tools called directly by the agent.** HubSpot's, Slack's or Clay's own MCP gives the agent abilities with no R-17 record. They only get used behind the gate ("wrap it or don't send").

6. **Scraped contact data or personal emails.** For a bank, how you got a person's details is its own compliance question. Contacts would come from a licensed source (ZoomInfo), with titles only, since nothing here emails the bank.

7. **Real company or people names in a public repo.** Northmere, Ridgeway and every person in the fixtures are fictional and labeled that way.

8. **A pharma PCCP brief this round.** I'm not yet sure PCCP applies to a pharma *quality* org, since it's written for AI-enabled medical devices. Shipping that brief without checking would be the same overclaim as brief v1.

9. **The regex overclaim check on its own, at scale.** It missed a real overclaim in v1; a human caught it. Before this runs on more than a handful of accounts, it needs a second check (an LLM judge or a human review step).
