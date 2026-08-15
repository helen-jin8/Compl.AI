# PRD — Compl.AI GTM Agent

**Owner:** Gaurang Sumra (product) · **Build owner:** GTM agent engineer
**Status:** Draft for team build · **Last updated:** 15 Aug 2026

This PRD specifies the **go-to-market agent** — the system that finds pre-launch
hardware companies about to miss a certification deadline, verifies the device
with a human panel, scopes the standards they need, and reaches out with the
answer already attached. The compliance scoping is the payload; the GTM loop is
the product.

It is written to be built by one engineer. Where a design choice is already
settled, it is stated as a decision, not an option. Where it is open, it is
listed under **Open questions**. The tactical spine — tiering, deliverability
gating, warm sourcing, multichannel sequencing, and the engagement feedback loop
— is lifted directly from the deplace outbound motion that worked (see
[§9 What we are copying from deplace](#9-what-we-are-copying-from-deplace)).

---

## 1. Problem & why now

A pre-launch hardware founder must clear FCC and UL certification before they can
legally ship in the US. The process is opaque: they do not know which standards
apply, which lab to call, what it costs, or how long it takes. Scoping alone runs
$10k–$15k before any physical test, and the consultancies who do this work reject
small founders outright — their economics require a minimum engagement size this
segment sits below.

Meanwhile, thousands of funded crowdfunding campaigns publish a ship date and a
device with a radio or a battery, and never file with the FCC. That is a dated,
public, verifiable trigger event. Nobody is serving them.

**Why now:** LLMs can read a campaign page and classify a device; a human panel
API (Terac) can verify the reading in minutes; a rules table maps attributes to
standards deterministically. The scoping work that justified a $12k consultant is
now a model call plus a lookup. The firm that serves this segment can run with no
compliance staff.

## 2. Goal & success metrics

**Goal:** an autonomous GTM loop that turns a public ship-date trigger into a
qualified, personalized outreach containing a real piece of the deliverable, and
converts a fraction to a paid signed review — with a human in the loop only where
one is actually needed (perception).

**North star:** *qualified replies per 100 sourced prospects.* A reply from a
real hardware founder is the one asset that cannot be manufactured, and it is the
top of every downstream funnel (paid report, lab routing).

| Metric | Definition | Launch target |
| --- | --- | --- |
| Trigger coverage | Funded campaigns sourced with ship date ≤ 6 mo | 500 / week |
| Tier-A rate | Sourced → radio/battery + no FCC grant + shipping soon | ≥ 25% |
| Deliverable accuracy | Model attributes vs. Terac panel consensus | ≥ 90% pre-panel; 100% post |
| Deliverability | Sends that inbox (not spam/bounce) | ≥ 95% |
| Reply rate | Replies / sends | ≥ 4% (cold), ≥ 12% (warm/engaged) |
| Enhance conversion | Paid signed-review / free reports delivered | ≥ 2% |
| Human cost per prospect | Terac panel spend per qualified prospect | ≤ $2 |

Guardrail metrics (must not regress): spam-complaint rate < 0.1%, zero reports
that claim we certify, zero unlabeled simulations reaching a screen.

## 3. Users & ICP

**Primary ICP — the buyer.** Pre-launch hardware founder, small team, no
compliance function, a public and dated ship commitment, and nothing on file with
the FCC.

**Qualification signal (writes the subject line):** absence from the FCC
Equipment Authorization database. A funded campaign shipping in four months with a
radio or a lithium pack and no grant on file has a problem it has not priced.
*Absence is a strong signal, not a proof* — a grant can sit under a contract
manufacturer's grantee code. Every piece of copy must keep that caveat.

**Primary source:** Kickstarter and Indiegogo, hardware/technology, funded, ship
date inside six months.

**Not the ICP:** enterprise manufacturing / supply-chain contacts (the deplace
lists). Wrong segment for this product — but the *motion* those lists were run
through is exactly what we are reusing.

## 4. The one idea everything hangs on

**The outbound email is a free sample of the deliverable.** The prospecting agent
and the compliance agent are the same agent, so the cold email contains the actual
standards list for that specific device with clause citations, the recommended
lab, the cost band, and the weeks. That is why it converts and why it is not spam:
we do a piece of the work and send it, rather than pitching a service.

Everything in this PRD serves that idea. The GTM agent is not a sequencer bolted
onto a product — the product *is* the message.

## 5. System overview

```
 SOURCE ─▶ ENRICH ─▶ QUALIFY ─▶ PERCEPTION ─▶ SCOPE ─▶ OUTREACH ─▶ ENGAGE ─▶ RE-ENGAGE
 (Apify)   (Apollo/  (FCC +     (Terac panel, (rules   (LGM multi-  (reply/   (expert
           Clay)     tiering)   BLOCKING)     engine)  channel)     signal)   comment)
                                    │                                             │
                                    ▼                                             ▼
                            measurable before/after                       degrade honestly
                            (mandatory Terac criteria)                     (refund at deadline)
```

Each stage reads and writes one shared prospect record (§6) and appends to an
event log. State is the single source of truth; the dashboard reads only state.
Every external call is cached so a full run can replay offline — do not let a live
demo depend on venue wifi.

## 6. Data model — the prospect record

One record per prospect, merged by `url`. Fields group by stage. This merges the
deplace LGM import schema (contact/deliverability fields) with the compliance
state shape.

```jsonc
{
  // identity (sourcing)
  "url": "https://kickstarter.com/projects/...",   // merge key
  "company": "Lumen Labs",
  "product": "Lumen Pack",
  "source": "kickstarter | indiegogo | linkedin_engagement | referral",
  "pledged": 184000, "backers": 2100,
  "ship_month": "2026-11",

  // contact (enrichment — from deplace schema)
  "first_name": "", "last_name": "", "full_name": "",
  "job_title": "Founder", "linkedin_url": "",
  "email": "", "has_email": true,          // deliverability gate
  "email_status": "valid | risky | invalid | unknown",

  // qualification
  "fcc": { "grants": 0, "checked": true, "source": "fcc_eas" },
  "months_to_ship": 3,
  "tier": "A | B | C",                     // urgency tier (contact-worthiness)
  "reasons": ["transmitter on board, Part 15 Subpart C required", "..."],

  // perception (Terac, human panel — BLOCKING)
  "model_attributes": { "intentional_radiator": true, "lithium_cell": null },
  "panel_attributes": { "lithium_cell": { "value": true, "agreement": 0.8, "n": 5 } },
  "attributes": { /* merged, panel overrides model */ },
  "attributes_corrected": ["lithium_cell"],   // only overrides that change standards
  "panel_source": "terac | mock",             // 'mock' must never reach a slide

  // scope (deterministic rules engine)
  "standards_before": ["47 CFR Part 15 Subpart C"],
  "standards_after": ["47 CFR Part 15 Subpart C", "UN 38.3", "..."],
  "determination": { "standards": [...], "cost_band": [lo, hi], "weeks": 12 },
  "lab": { "name": "...", "accreditations": [...], "one_stop": true },

  // offer + outreach
  "offer_tier": "free | enhanced",
  "report_v1": "…markdown free report…",
  "variant": "A | B", "subject": "...", "body": "...",
  "channel_plan": ["linkedin_view", "linkedin_connect", "email_1", "email_2"],
  "outreach": "drafted | sent | bounced",
  "sent_pre_label": false,     // sent before panel returned — badge it

  // engagement + expert loop
  "engagement": { "opened": true, "replied": false, "linkedin_accepted": true },
  "expert_job_id": null, "expert_posted_at": null,
  "expert_state": "empty | pending | signed",
  "expert_name": null, "expert_credential": null, "expert_comments": [],
  "report_v2": null,           // signed version
  "approval_simulated": false, // only true under SIMULATED_APPROVAL=1, badged
  "refund_deadline": null, "expert_outcome": null,  // 'not_found' triggers refund

  "stage": "sourced | qualified | labelled | analyzed | contacted | ..."
}
```

## 7. Stage specifications

Each stage is an idempotent command. Re-running a stage on an unchanged record is
a no-op. Every stage is safe to run repeatedly (the deplace lists were re-imported
constantly; assume the same here).

### 7.1 Source
Pull funded hardware/technology campaigns with a ship date ≤ 6 months. Primary:
Apify actor over Kickstarter/Indiegogo. Fallback: hand-filled seed list. Normalize
to the record shape. **Warm source (high-value, from deplace):** people who
engaged with our LinkedIn content are their own segment — sourced with
`source: linkedin_engagement` and routed to a warmer sequence (§7.6).
*Acceptance:* N normalized records with a `url`, `ship_month`, and `page_text`.

### 7.2 Enrich
Fill contact + deliverability fields. Apollo/Clay for founder name, title,
LinkedIn, and a verified email. **Deliverability gate (from deplace):** set
`has_email` and `email_status`; a `risky`/`invalid` email never gets an email
send — it routes to LinkedIn-only. In deplace, ~55% of a raw list had a usable
email; design for that, do not assume full coverage.
*Acceptance:* every record has `has_email` set and, if true, a syntactically
valid address with a status.

### 7.3 Qualify
Check the FCC Equipment Authorization database for a grant under the company name
(two strategies: EAS search, then fccid.io mirror; never guess — mark
`checked: false` on failure). Compute `months_to_ship`. Assign the urgency
**tier**:
- **A** — (radio or battery) **and** no FCC grant **and** shipping ≤ 6 mo. The
  only tier contacted today.
- **B** — has radio or battery but misses one of the above.
- **C** — everything else.

*Acceptance:* tier distribution printed; tier-A records carry human-readable
`reasons`.

### 7.4 Perception panel (Terac) — BLOCKING, mandatory
Every tier-A prospect goes to a Terac general-population panel *before* scoping.
Five questions any literate adult can answer from a product page (battery? radio?
ship month? for children? plugs into the wall?). Panel consensus **overrides** the
model. This is the eligibility floor and the mandatory external-input criteria —
it always fills, in minutes.

The measurable **before/after** is model-only attribute accuracy vs. panel
consensus, plus the standards list that changed downstream. A panel catching a
missed battery moves the list from ~2 entries to ~6 by adding UN 38.3. That delta
is the hero of the demo — do not bury it.

`--mock` fakes the panel for dev and stamps `panel_source: mock` so it can never
reach a slide unnoticed.
*Acceptance:* panel consensus written with agreement rates; a correction event
logged when the panel overrides the model on a standards-changing attribute.

### 7.5 Scope (deterministic rules engine)
Map merged attributes → standards via `data/standards.yaml` (auditable, cited),
pick a lab via `data/labs.yaml` (prefer one-stop, prefer startup-friendly — the
big labs decline this segment, which is the whole thesis). **The model classifies
and writes prose; the YAML decides which standards apply.** A standard not in the
YAML does not go in a report. Render `report_v1` (free tier) with an empty,
upgrade-linked expert signature block.
*Acceptance:* a free report renders end to end with clause citations and zero
occurrences of "certified" about our own output.

### 7.6 Outreach (multichannel — the deplace engine)
The email carries the actual scope (§4). Two variants (absence hook / cost hook),
plain text only, no tracking pixel, CAN-SPAM footer (physical address +
unsubscribe) on every send. **Execution runs through La Growth Machine**, the same
engine deplace used: a record becomes an LGM import row and is sequenced across
**LinkedIn + email** per its `channel_plan`:
- **Cold, has_email:** LinkedIn profile view → email 1 (the scope) → LinkedIn
  connect → email 2 (the sleeper standard).
- **Cold, no email:** LinkedIn-only path (view → connect + note → message).
- **Warm (`linkedin_engagement`):** open on the engagement — "picking this back
  up" — shorter, no re-introduction.

**Send discipline (non-negotiable):** nothing sends without an explicit `--send`;
default writes drafts to an outbox. A hard `MAX_SENDS` cap per cold domain — cold
volume lands in spam and a spam-foldered demo shows zero replies. Warm up the
domain before scaling.
*Acceptance:* drafts render for every tier-A record; `--send` gated; caps
enforced; every draft has the caveat + footer.

### 7.7 Engage
Track reply / open / LinkedIn-accept back onto the record. A reply is the north
star — surface it immediately. **Never simulate a reply from a stranger.**
*Acceptance:* engagement fields update; replies appear on the dashboard.

### 7.8 Re-engage (highest-value message)
When an expert has reviewed a report, draft a follow-up that **quotes the expert
verbatim** — never "an expert reviewed your report" when you can paste the actual
sentence. Variants by prior state (never replied / went quiet / already paid).
This puts the human panel inside the GTM loop, not only in delivery.
*Acceptance:* the draft contains the expert's real sentence, not a paraphrase.

### 7.9 Enhance & degrade (the paid loop)
On enhance (paid via Stripe Payment Link), post the job **plus the finished draft**
to Terac's expert pool — the draft turns hours of unknown work into twenty minutes
of review, which raises acceptance. On acceptance → `pending` → signed `report_v2`
ships. **If no expert accepts by `refund_deadline`, refund automatically and send
the honest "no reviewer found" note** — the same honesty the founder was denied by
the consultancy. Demo this screen on purpose.

The approval step may be simulated for a demo **only** behind
`SIMULATED_APPROVAL=1`, which sets `approval_simulated: true` and forces a visible
badge on the row. With the flag off, no code path can set the flag. Never simulate
a Stripe charge, a stranger's reply, or a panel result.

## 8. The accuracy chain (why there is no compliance expert on payroll)

| Layer | Question | Who answers | Cost of being wrong |
| --- | --- | --- | --- |
| **Perception** | battery? radio? ship date? child audience? | Terac general population, blocking | wrong standards list — caught by panel |
| **Rules** | which standards those attributes trigger | `standards.yaml`, deterministic | auditable, fixable in the file |
| **Authority** | is the scope right, what does it cost | accredited-lab quote requests | the lab's accreditation is on the line, not ours |

Only perception needs a human, and reading a product page is a general-population
task — which is why the absence of compliance specialists never mattered. The
verification is *structural*: we send the scope to three labs as quote requests;
their quotes confirm or correct it, and they are free because labs want qualified
inbound.

## 9. What we are copying from deplace

The deplace outbound motion is proven; reuse it, do not reinvent it. What worked,
and how it maps here:

1. **A/B/C tiering.** Every list was tiered by fit/urgency and worked top-down.
   → our `tier` field; only tier-A is contacted today.
2. **Deliverability gating.** `has_email` was a first-class column; no-email
   contacts went LinkedIn-only. ~55% email coverage was normal.
   → §7.2 gate; channel plan branches on it.
3. **Warm sourcing from content engagement.** The best-performing segment was
   *people who engaged with a LinkedIn post* — re-imported as its own tiered list.
   → `source: linkedin_engagement`, warmer sequence (§7.6).
4. **Multichannel via La Growth Machine.** LinkedIn + email sequenced together,
   CSV import schema (name, title, company, domain, LinkedIn, email, tier,
   source). → §6 record maps 1:1 to an LGM import row; §7.6 runs on LGM.
5. **Engagement feedback loop.** Engaged contacts were re-segmented and re-worked,
   not dropped after one touch. → §7.7 → §7.8; records are long-lived and
   re-runnable.
6. **Small, clean lists beat big dirty ones.** deplace ran ~60-row tiered lists,
   not 10k blasts. → cap tier-A volume; protect deliverability over reach.

**LGM import contract (reuse deplace's columns):**
`firstname, lastname, company_name, job_title, linkedin_url, email, tier, source`
plus our payload columns (`subject`, `body`, `channel_plan`). The GTM agent's job
is to produce this row correctly and hand it to LGM; LGM owns delivery + inbox.

## 10. Tooling & integrations

| Capability | Tool | Notes |
| --- | --- | --- |
| Sourcing | Apify | pick actor at runtime; seed-list fallback |
| Contact enrichment | Apollo, Clay | name/title/LinkedIn/verified email |
| FCC lookup | apps.fcc.gov EAS → fccid.io | browser UA; honest failure, never guess |
| Perception + expert | Terac | blocking panel (mandatory) + best-effort expert pool |
| Outreach execution | La Growth Machine | multichannel sequencing + deliverability |
| Payment | Stripe Payment Link | no gated app; enhanced report emails on confirmation |
| Model | Anthropic (Claude) | classify device + write prose; **not** the standards decision |

**Model note:** use a current Claude model id (e.g. `claude-sonnet-4-6` for the
extraction/classification task; `claude-opus-4-8` where deeper reasoning helps).
The old `claude-opus-4-20250514`-style ids in the scaffold are stale — fix them.

## 11. Guardrails (bugs if violated)

- **Never claim we certify anything.** "Reviewed and signed by a named expert."
  Certification authority is the lab's. Assert on this in the renderer.
- **Never send without `--send`; `MAX_SENDS` is a hard cap.** Default is drafts.
- **Every external call is cached; `OFFLINE=1` replays a full run with no network.**
- **Never simulate** a Stripe charge, a stranger's reply, or a panel result. The
  expert approval may be simulated only behind `SIMULATED_APPROVAL=1`, always
  badged.
- **FCC absence is a signal, not a proof** — a grant can sit under a contract
  manufacturer's grantee code. Copy that drops this caveat is a bug.
- **A standard not in `standards.yaml` does not go in a report.** Add it with a
  citation or leave it out.
- **CAN-SPAM:** physical address + unsubscribe on every send; no tracking pixel on
  a technical audience.

## 12. Milestones (build order for the teammate)

- **M0 — Skeleton (½ day):** record model, state store with offline cache, stage
  runner. A run replays offline end to end on a seed row.
- **M1 — Source → Qualify:** Apify/seed sourcing, enrichment stub, FCC + tiering.
  Output: tier-A list with reasons.
- **M2 — Perception + Scope:** Terac panel (with `--mock`), rules engine,
  `report_v1`. Output: the before/after correction + a free report.
- **M3 — Outreach on LGM:** variants, deliverability gate, channel plan, LGM
  import contract, send rails. Output: drafts + one warm-source sequence.
- **M4 — Enhance loop:** Stripe link, expert job with draft attached, poll,
  degrade + refund, re-engagement. Output: paid path + honest degradation screen.
- **M5 — Dashboard + metrics:** panel-correction lead, funnel tiles, revenue,
  simulated/pre-label badges.

Ship in order; stop when the clock says stop, not when the list ends.

## 13. Open questions

- **Terac payload shapes** for the panel and the expert job are unconfirmed —
  pin field names against sponsor docs; everything downstream needs only a task/job
  id back.
- **LGM API vs. CSV import** — start with CSV import (proven at deplace); move to
  API only if volume needs it.
- **Warm-source supply** — how fast can LinkedIn content generate an engaged
  segment at useful volume? deplace got ~35 engaged contacts per post.
- **Enhance pricing** — $19 is a demo price to make a charge plausible in-event;
  the real price is a separate decision.
- **Lab routing economics** — labs paying for qualified inbound is the year-3
  business (see VISION.md); out of scope for v1 but shapes the data we keep.

## 14. Non-goals (v1)

No physical testing, no certification, no compliance web app, no reply-handling
agent, no gated paywall build. We scope and route. Moving up the chain to testing
is the year-three story, not this build.
