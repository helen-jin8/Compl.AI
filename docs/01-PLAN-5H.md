# Plan to submission lock

Submissions lock 6:45 PM. Work backwards from that, not forwards from now.
T+0 is the moment you start. Budget assumes roughly five hours.

## Governing principle

The only assets you cannot manufacture in the last hour are a reply from a
stranger, a Terac panel result, and a Stripe charge. All three need wall clock
time to arrive. So all three get triggered inside the first 90 minutes, and the
engineering gets built while they cook.

Everything else can be built, cached, or narrated.

## Cut list

**Cut.** LinkedIn and La Growth Machine. A separate reply-handling agent. Lab
routing beyond `data/labs.yaml`. A compliance web app. Human expert sign-off,
which is a strategy change rather than a scope cut, see D1. Linq, Superserve,
Replay and Band tracks unless a teammate is idle.

**Keep.** Terac message ranking. Stripe payment link. FCC qualification. The
compliance preview payload. One live end to end run on stage. The scoreboard.
The rejection email cold open. Render Workflows deploy.

## Schedule

### T+0 to T+20 — humans only, three things in parallel

These block everything downstream and none of them are code.

**a. Stripe.** Personal account, one Payment Link with customer chooses price,
restricted key with Balance and Charges set to Read and everything else None.
Submit team name, link, and `rk_` key to organizers. Fifteen minutes, gates the
$2,500 prize.

**b. Rejection bait.** Email four hardware compliance consultancies asking for
help with a small pre-launch device. Copy in `04-OUTREACH-COPY.md`. You need one
written rejection for the opening slide and there is a chance it lands in time.

**c. Terac smoke test.** Launch one throwaway labeling task against a single
hand-picked campaign URL right now, before the pipeline exists. You need to know
the panel turnaround time before you design around it, and you need to find the
auth and payload problems while they are cheap. Design is in
`05-TERAC-INTEGRATION.md`.

### T+20 to T+1:00 — sourcer and qualifier

Twenty tier A prospects. Kickstarter and Indiegogo hardware and technology,
funded, ship date inside six months, cross-checked against the FCC Equipment
Authorization database. No grant on file plus a battery or a radio equals tier A.

    python -m src.pipeline source --limit 60
    python -m src.pipeline qualify

If the Apify actor stalls, stop and hand-collect twenty campaign URLs into
`data/seed_prospects.json`. Twenty good rows beat a broken scraper, and the
scraper is not what is being judged.

### T+1:00 to T+1:20 — Terac attribute labeling, launch and do not wait

Every qualified prospect goes to a panel for attribute labels. Five questions,
all answerable by anyone who can read. This is blocking by design but not by
schedule: launch the batch, then keep building.

    python -m src.pipeline terac-label
    python -m src.pipeline terac-pull      # run again later, it is idempotent

If the panel is slow, run the analyst with `--terac-async` so it proceeds on
model attributes and patches records when labels land. Log which prospects went
out pre-label. Never let a slow panel eat the send window.

### T+1:20 to T+1:45 — analyst

Compliance preview per prospect, built from panel-corrected attributes where
available. Device class, standards with clause citations, one recommended lab,
cost band, week count. This is the payload and it is what makes the outreach
defensible rather than spam.

    python -m src.pipeline analyze

Record `standards_before` and `standards_after` on every prospect the panel
corrected. That pair is the mandatory before and after and it is a product
metric, not a marketing one.

### T+1:45 to T+2:15 — send generation 1

Twenty emails, ten per variant, plain text, real mailbox, unsubscribe line, $19
payment link inline. Replies now have four hours.

    python -m src.pipeline outreach --send

Do not exceed twenty from a cold domain.

### T+2:15 to T+2:45 — comprehension gate

Second Terac panel reads the generated report and answers what the company should
do next. Majority naming the correct action is a pass. Below that, the agent
rewrites and re-tests.

    python -m src.pipeline terac-comprehend
    python -m src.pipeline rewrite-report

Two rounds is enough. Round 1 versus round 2 pass rate is the second before and
after.

### T+2:45 to T+3:30 — harness

Wire the subagents so the system survives inspection. Target is a live run on one
fresh prospect, sourcing through drafted email, on stage. Cache every external
call so the stage run is deterministic.

This is the block that gets poked by judges. Protect it.

### T+3:30 to T+4:00 — scoreboard and Render

`dashboard/index.html` against `data/state.json`. Deploy to Render Workflows for
the second track.

### T+4:00 to T+4:20 — submit

Submit early. The form closes hard at 6:45 and the queue will be slow at 6:40.

### T+4:20 to T+4:50 — rehearse twice, timed
### T+4:50 to T+5:00 — buffer

## Revenue, the thing most likely to go wrong

Best Overall Agent-Run Company is scored on money that actually moved. Twenty
cold emails to Kickstarter founders may produce zero charges in four hours.

Mitigations, cheapest first:

1. Price at $19. Impulse range, no procurement, no call.
2. Put the payment link in the first email, not after a reply.
3. Add one inbound post. A Show HN or an r/hardware comment offering a free
   compliance scope, with the paid package one click away. Fifteen minutes of
   work and it widens the funnel past your twenty sends.
4. Accept a charge from anyone who counts as a customer, including a hardware
   person at the venue who buys a scope for their side project. It is a charge
   and the agent produced the deliverable.

## Parallelization

With two other builders: one owns sourcer and qualifier, one owns scoreboard and
Render, you own the analyst, the outreach copy, and the Terac studies. The
analyst and the Terac loop are the critical path and should sit with whoever
writes best.
