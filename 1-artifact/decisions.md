# Decisions: reconciling Paul's notes

Paul's notes contradict themselves in places. I didn't execute every sentence. Here is what I decided, what I refused, and what I left open for someone else to decide.

## The one-line plan

Go deep on one account type (the D-SIB bank), one trigger (SR 26-2), one artifact: an agent that turns the trigger into a short, sourced brief a CAE can forward, where every action runs through an R-17 audit gate and nothing sends without a named human.

## Why the bank, not pharma or defense

| | D-SIB bank | Biopharma quality | Defense supplier |
|---|---|---|---|
| Paul's priority | "The one that matters this month" | Asked about PCCP last week | "Forge-first, Reign later… check with Rob" |
| R-17 audit | **Required** (financial services) | Recommended only | Recommended only |
| Can we act today? | Yes, through Paul's exception: a regulatory trigger → a brief the CAE can forward, via the existing Forge relationship | Yes, unblocked | No, waiting on Rob |
| Trigger on the brief's list | SR 26-2, DORA | FDA PCCP | None |
| What it proves | Agent + governance under the strictest rule | Agent, with lighter governance | — |

**Call:** the bank. It's the account Paul cares most about, and the only one where R-17 is mandatory, so it's the only place I can prove the governance works where it has to. Pharma is unblocked and a real opportunity, so it's the next swap in the same playbook (change `audience` + `trigger`, keep the gate and evals). Defense waits for Rob.

## Contradictions → my call

| Paul's notes say | Conflict | My call | Why |
|---|---|---|---|
| "Bank buyer is the one that matters this month." / "Do not outbound to the bank until an Executive Assurance Briefing is on the calendar." | The priority account is also the blocked one. | The bank is **armed, not contacted**. The agent drafts the brief, writes the audit record, and hands it to the internal Forge account owner. Nothing goes to the bank. | Paul's own exception: if SR 26-2 or DORA hits, "we should already be in the thread with a brief that a CAE can forward." The bank already runs Forge, so "the thread" is an existing relationship, not cold outbound. |
| CRO: "40 first meetings this quarter." / Paul: "No spray. Precision." | Volume vs precision. | **Sequencing, not a real conflict.** Precision on the bank now. The CRO keeps control through `kill_criteria` in the playbook, which is how he stops a motion that goes sloppy. | 40 generic sequences into CISO inboxes is exactly what Paul says will kill the motion. |
| Defense: "Do not lead Reign there. I think. Check with Rob. Actually lead with the substrate story…" | Paul changes his mind mid-sentence and defers to Rob. | **Forge-first, Reign as the assurance reason.** I'm not building a defense motion this round. | His last sentence wins, but "check with Rob" is an open question, not mine to settle. |
| Pharma: "They asked about FDA PCCP last week… Do not write a blog. Build the trigger." | Pharma is unblocked; the bank is gated. Which goes first? | **No blog. Pharma is the next swap**, not built today. | The brief says "pick one, go deep, do not spray." R-17 is only *required* for financial services, so the bank is where the governance has to be proven. Pharma reuses the same playbook: swap `audience` and `trigger`. |
| Bank buyer: "Risk and engineering will not sit in the same meeting if we make them declare which one they are. Route them without asking." | We need to know the lane without asking. | **Infer the lane from title and department.** Never ask the buyer to pick. | Direct instruction. |
| "Everything that sends needs a named human… If you cannot leave an audit trail, it does not send." vs R-17: "Non-FS segments: recommended, not required." | Paul's rule covers every segment; R-17 only requires FS. | **The stricter rule wins for sends, in every segment.** Full R-17 records are required for FS and switched on by default everywhere else. | It costs nothing to audit everything, and it's the rule Paul actually wrote for the company. |

## ICP cleanup (details in `icp.yaml`)

- **Removed:** AI startups (Paul: "Remove them"), mid-market SaaS (Paul: "Do not include").
- **Parked:** hospitals (website copy, but "do not spray hospitals this month"), "Canada federal" (unvetted Slack note), semiconductor (only with a US export-control problem, no trigger defined yet).
- **Added as a hard gate:** Rob's "if they do not have a risk committee we are wasting the briefing." Unvetted, but cheap to enforce and it protects the briefing.

## What I refused to build

- **A pharma blog.** Paul said no.
- **A generic "AI governance" sequence** to CISOs. Paul said he'd kill the motion.
- **Any cold outbound to the bank** before a briefing is booked.
- **High-volume anything.** One account, one trigger, one brief.
- **A defense or pharma motion this round.** Depth over breadth.

## Open questions (not mine to decide)

- **Rob:** Forge-first or Reign-first for the defense supplier?
- **Paul:** does "Canada federal" belong in the ICP?
- **Paul / Rob:** is the risk-committee requirement a real rule or a Slack opinion?

## R-17 vs Paul's send rule, in the code

- The gate covers all five R-17 actions: **create, update, enrich, score, message**, not just sends.
- The audit record is written **before** the action. If it can't be written, the action doesn't happen.
- `send: true` requires a named `approver`, and the send is a blockable task, never an automatic email.
- Bank sends are also refused until a briefing is booked, unless the trigger exception applies (and even then, the brief goes to the internal account owner).
- Policy: `fs: required`, `non_fs: on_by_default`.
