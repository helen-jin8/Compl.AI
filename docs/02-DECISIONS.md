# Decisions

## D1. No human expert on our side. The lab quote is the oracle.

**Problem raised by the team.** Terac has no hardware compliance specialists, so
nobody can sign off on the agent's output.

**Why the premise was wrong twice.** First, no consultant certifies anything in
this industry. Authority sits with accredited bodies: NRTLs for product safety
(UL Solutions, Intertek, TÜV, CSA and roughly a dozen others) and TCBs for FCC
equipment authorization. A human expert on our side was buying trust, not
authority. The legal signature was never ours to give. Second, Terac's criteria
never asked for domain experts. See D8.

**Decision.** Verify the agent's scope by sending it to three NRTLs as a quote
request. Quotes come back from accredited bodies naming standards and price.
Three-way agreement verifies the scope. Disagreement catches the error before the
client pays. The oracle is free, more authoritative than any contractor we could
hire, and labs want the inbound.

**Second layer.** Every claim cites its clause. UL 62368-1 with section, 47 CFR
15.247, IEC 62133-2 with section. The reader verifies without trusting us.

**Pitch consequence.** This is an advantage, not a patch. Competitors keep humans
in the loop. We do not need one because verification is structural.

**Liability line.** We never certify. We scope and route. That goes in the terms
and it is the answer when a judge asks who is liable.

## D2. The outbound message is a free sample, not a pitch.

The prospecting agent and the delivery agent are the same agent. The email
carries actual work product: standards for their specific device, the lab that
covers all of them in one pass, cost band, week count. This is why it converts,
why it is not spam, and why the system reads as one coherent thing rather than an
outbound bot bolted to a consulting bot.

## D3. The GTM loop is the hero. The compliance product is the payload.

Five hours buys one impressive thing. The hackathon judges whether the business
runs itself. Build the loop. Do not build a web app.

## D4. Kickstarter and Indiegogo over Apollo or Clay for sourcing.

Firmographic databases do not know who is about to ship hardware. A crowdfunding
campaign publishes the trigger event: funded, dated, public. Apollo and Clay
enrich the contact after the trigger is found. They do not find the trigger.

## D5. FCC absence as the qualification signal.

The FCC Equipment Authorization System is a public database of every device
authorized for sale in the US. A funded campaign shipping in four months with a
radio inside and no grant on file has a problem it has not priced.

Honest caveat to state on stage: a grant may sit under a contract manufacturer's
grantee code rather than the brand name, so absence is a strong signal and not a
proof. The email is phrased as a question for that reason. Saying this out loud
is a credibility gain, not a loss.

## D6. Cache every external call. Replay offline.

Any live stage run that depends on a third party API is a coin flip. Every fetch
writes to `data/cache/`. `--offline` replays. Rehearse online, demo from cache if
venue wifi is bad, and say so if asked.

## D7. Twenty emails, not two hundred.

A cold domain sending volume lands in spam and the demo shows zero replies.
Twenty targeted sends with a specific payload outperform, and the story is
better. Unsubscribe line and physical address included. When a judge asks whether
this is spam, the answer is the payload.

## D8. Terac is the perception layer inside the service, not a dev loop.

Full design in `05-TERAC-INTEGRATION.md`.

**The blocker.** Terac has no hardware compliance experts, so nobody can validate
the output.

**Why it dissolves.** Split the accuracy chain. Perception asks whether the
device has a battery, a radio, a ship date, a child audience. Rules map those
attributes to standards. Authority confirms the scope and the price. Rules are a
deterministic table we already wrote. Authority comes from accredited lab quotes
and no consultant has it anyway. Perception is the only layer that needs a human,
and reading a product page is a general population task.

We never needed a compliance expert. We needed eyes.

**Decision.** Terac panels label device attributes for every prospect, blocking,
in production, between the sourcer and the analyst. Panel consensus overrides the
model. Wrong attributes produce a wrong standards list, so the humans are
load-bearing for correctness. Remove Terac and output accuracy drops measurably.

**Second use.** A comprehension gate before delivery. A report ships only once a
non-expert panel can read it and name the correct next action. A first-time
hardware founder is functionally a non-expert reading a compliance document, so
the general population panel is a better customer proxy than an expert would be.

**Measured before and after.** Model-only attribute accuracy against panel
consensus, and the standards list that changed as a result. The best single
artifact is one prospect where the panel caught a battery the model missed and
the report gained UN 38.3.

**Rejected alternative.** Ranking outbound email variants. It satisfies the
letter of the requirement but it optimises the marketing rather than the company,
and in a hackathon judging whether a business runs itself that distinction is the
whole point. Kept as a bonus if time remains.

**Pitch line.** The company has no employees. It hires perception by the task
through an API, applies deterministic rules, and takes authority from accredited
labs.

## D9. Price at $19 and put the link in the first email.

Best Overall Agent-Run Company is scored on revenue earned during the event. A
$2,000 consulting engagement will not close in four hours. A $19 impulse purchase
might. The email already carries most of the value, so the charge buys the full
scoped package plus three lab quote requests sent on their behalf.

One charge beats zero. The judges are scoring whether money moved.

## D10. Track selection under time pressure.

Render is scored by the same panel as Best Agent-Run Company, so deploying the
pipeline to Render Workflows buys a second track for roughly thirty minutes.
Pioneer is cheap because GLiNER2 is an extraction model and pulling device
attributes out of campaign text is an extraction task.

Band, Linq, Superserve and Replay are skipped unless a teammate is idle. Band in
particular requires that removing it breaks the project, which is not something
to retrofit at hour four.
