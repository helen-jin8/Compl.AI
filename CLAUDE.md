# CLAUDE.md

Read `docs/` before writing code. Order: 00-CONTEXT, 02-DECISIONS, 01-PLAN-5H.

## What this is

A go-to-market agent system for an autonomous hardware compliance consulting
firm. Built for the Zero Human Company Hackathon hosted by Terac, San Francisco,
Aug 15 2026. Submissions lock 6:45 PM PDT.

The GTM loop is the hero of the demo. The compliance work is the payload inside
it. Do not build a compliance web app.

## Hackathon constraints that drive architecture

**Terac MCP is mandatory.** Every project must use it. The criteria is human
input collected during the event that makes the project measurably better, with a
clear before and after. Terac says to target the General Population for speed.

Terac is the perception layer of the pipeline, in production, not a dev loop.
Full design in `docs/05-TERAC-INTEGRATION.md`.

The accuracy chain splits three ways. Perception asks whether the device has a
battery, a radio, a stated ship date, a child audience. Rules map attributes to
standards and live in `data/standards.yaml`, deterministic and auditable.
Authority confirms scope and price and comes from accredited lab quotes. Only
perception needs a human, and reading a product page is a general population
task, which is why the missing compliance experts never mattered.

Terac panels label attributes for every prospect, blocking, between the sourcer
and the analyst. Panel consensus overrides the model. Wrong attributes produce a
wrong standards list, so the humans are load-bearing. A second panel gates
delivery: a report ships only once non-experts can name the correct next action.

Before and after is model-only attribute accuracy against panel consensus, plus
the standards list that changed downstream.

**Stripe is mandatory for the main prize.** Best Overall Agent-Run Company
($2,500) goes to the company that earns actual revenue during the event. One
Payment Link, customer chooses price, restricted read-only key submitted to
organizers. Price the offer low so a charge can plausibly land inside four hours.

**Render Workflows** is scored by the same judging panel as Best Agent-Run
Company. Deploying the pipeline there is a cheap second track.

**Pioneer / Fastino** is a cheap third track. GLiNER2 is a named entity
extraction model, and pulling device attributes (battery, radio, ship date) out
of a campaign page is an extraction task. Natural fit if time allows.

## Product shape, two tiers

Decided Aug 15 afternoon, full spec in `docs/06-PRODUCT-SPEC.md`, build order in
`docs/07-BUILD-SPEC.md`.

Free tier: the agent accepts the job, generates the scoping report immediately
from its own models plus the rules table, ships same day. Expert signature block
present and empty with the upgrade link where the signature would go. Gated by
the Terac perception panel, which fills in minutes.

Enhance, paid: optional. Posts the job plus the finished draft to Terac. On
acceptance the expert reviews and signs. Live SLA three to four days. If nobody
accepts, refund automatically and say so plainly.

The draft goes out before the expert accepts, deliberately. Expert time is the
scarce input and a finished draft turns hours of unknown work into twenty minutes
of review, so attaching it raises acceptance.

Wording discipline: reviewed and signed by a named expert. Never certified.
Certification authority is the lab's. A judge with industry background will catch
the wrong word and the trust argument rests on that precision.

Do not drop the perception panel in favour of the expert loop. The panel is the
eligibility floor because it always fills. The expert loop is upside that may
never land.

## Judges worth designing for

Tosh Rayadhurgam, Head of Advanced AI at Stripe, scores the agent-run company
track. The payment path should be clean and the revenue number should be visible.

Shriram Bagavathyappan, Group PM at Google DeepMind, will probe product
reasoning. Have the ICP logic and the qualification signal ready to defend.

Multiple YC S26 founders on the panel. They will ask whether this is a business.

## The business

Autonomous hardware compliance consulting firm.

**Problem.** A pre-launch hardware founder must clear UL and FCC certification
before shipping legally. The process is opaque. They do not know which standards
apply, which lab to call, the cost, or the timeline. Scoping alone runs $10k to
$15k before any physical test, and labs bill separately.

**Wedge.** Compliance consultancies reject small founders. The lived version from
this morning's scoping session: emailed a consultant about certifying a laptop,
got told they do not work with companies that size. That rejection email opens
the pitch.

**Boundary.** No physical testing. We scope and route to accredited labs. We do
not test and we do not certify. Moving up the chain is the year-three story.

**Competitors.** hardwarecompliance.com and Noetic (YC 2026). Two players is
validation. They sell consulting to a segment above ours and reject the one we
serve.

## ICP

Pre-launch hardware founders, small teams, no compliance function, public ship
commitment, nothing on file with the FCC.

Primary source is Kickstarter and Indiegogo hardware and technology, funded, ship
date inside six months. Public, dated, and it produces a hard trigger event.

Qualification signal is absence from the FCC Equipment Authorization database. A
funded campaign shipping in four months with a radio or a battery and no grant on
file has a problem it has not priced. Free, verifiable, and it writes the subject
line.

Not the ICP: the two CSVs in Downloads are enterprise manufacturing and supply
chain contacts from separate deplace work. Wrong segment.

## Repo conventions

- Every external fetch writes to `data/cache/`. `--offline` replays from cache.
  The stage run must never depend on venue wifi.
- Pipeline state lives in `data/state.json`. The dashboard reads only that file.
- Never send email from code without `--send`. Default is dry run to
  `data/outbox/`.
- Secrets in `.env`, never committed, never printed.

## Tooling already connected in the Cowork session

Apify, Clay, Apollo, Gmail, La Growth Machine, Granola, Google Drive, Calendar.
