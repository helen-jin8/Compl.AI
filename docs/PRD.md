# PRD — Compl.AI GTM Agent

**Owner:** Gaurang Sumra (product) · **Build owner:** GTM agent engineer
**Status:** Draft for team build · **Last updated:** 15 Aug 2026

This PRD specifies the **go-to-market agent** — the system that finds pre-launch
hardware companies about to miss a certification deadline, scopes the standards
they need, and reaches out with the answer already attached. The compliance
scoping is the payload; the GTM loop is the product.

**Where Terac fits:** the GTM engine has **no human in the loop**. Terac is used
only on the *deliverable* — the paid expert review that signs a report (§7.8).
The measurable human-input before/after (draft vs. signed report) lives there,
not in prospecting or scoping.

It is written to be built by one engineer. Where a design choice is already
settled, it is stated as a decision, not an option. Where it is open, it is
listed under **Open questions**. The tactical spine — tiering, deliverability
gating, warm sourcing, and the engagement feedback loop — is lifted directly from
the deplace outbound motion that worked, adapted to email-only execution (see
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

**Why now:** LLMs can read a campaign page and classify a device, with each
attribute backed by a quote from the page as its audit trail; a rules table maps
attributes to standards deterministically. The scoping work that justified a $12k
consultant is now a model call plus a lookup. The firm that serves this segment
can run with no compliance staff — human judgment is bought once, at the end, to
review and sign the deliverable.

## 2. Goal & success metrics

**Goal:** an autonomous GTM loop that turns a public ship-date trigger into a
qualified, personalized outreach containing a real piece of the deliverable, and
converts a fraction to a paid signed review — with a human in the loop only on the
final deliverable (the expert review), never in prospecting or scoping.

**North star:** *qualified replies per 100 sourced prospects.* A reply from a
real hardware founder is the one asset that cannot be manufactured, and it is the
top of every downstream funnel (paid report, lab routing).

| Metric | Definition | Launch target |
| --- | --- | --- |
| Trigger coverage | Funded campaigns sourced with ship date ≤ 6 mo | 500 / week |
| Tier-A rate | Sourced → radio/battery + no FCC grant + shipping soon | ≥ 25% |
| Extraction quality | Attributes carrying a valid page `evidence` quote | ≥ 95% |
| Deliverability | Sends that inbox (not spam/bounce) | ≥ 95% |
| Reply rate | Replies / sends | ≥ 4% (cold), ≥ 12% (warm/engaged) |
| Enhance conversion | Paid signed-review / free reports delivered | ≥ 2% |
| Review turnaround | Enhance paid → signed report shipped | ≤ 4 days |

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
 SOURCE ─▶ ENRICH ─▶ QUALIFY ─▶ SCOPE ─▶ OUTREACH ─▶ ENGAGE ─▶ RE-ENGAGE
 (Apify)   (Apollo/  (FCC +     (model    (Gmail    (reply    (expert
           Clay)     tiering)   + rules)  MCP)      tracking) comment)
                                                                   │
        ENHANCE (paid, Stripe) ─▶ Terac expert review ─▶ signed report_v2
                                                                   │
                                                                   ▼
                                         degrade honestly (refund at deadline)
```

The **GTM engine (source → re-engage) has no human in the loop** — model
extraction feeds a deterministic rules table, and outreach runs on the Gmail MCP.
Terac enters once, on the **deliverable**, when a paid report is reviewed and
signed. That review is the sole human-input step and where the measurable
before/after (draft `report_v1` → signed `report_v2`) lives.

Each stage reads and writes one shared prospect record (§6) and appends to an
event log. State is the single source of truth; the dashboard reads only state.
Every external call is cached so a full run can replay offline — do not let a live
demo depend on venue wifi.

## 6. Data model — the prospect record

One record per prospect, merged by `url`. Fields group by stage. Contact and
deliverability fields carry over from the deplace list schema; the rest is the
compliance state.

```jsonc
{
  // identity (sourcing)
  "url": "https://kickstarter.com/projects/...",   // merge key
  "company": "Lumen Labs",
  "product": "Lumen Pack",
  "source": "kickstarter | indiegogo | linkedin_engagement | referral",
  "pledged": 184000, "backers": 2100,
  "ship_month": "2026-11",

  // contact (enrichment — deplace contact/deliverability fields)
  "first_name": "", "last_name": "", "full_name": "",
  "job_title": "Founder", "linkedin_url": "",
  "email": "", "has_email": true,          // deliverability gate
  "email_status": "valid | risky | invalid | unknown",

  // qualification
  "fcc": { "grants": 0, "checked": true, "source": "fcc_eas" },
  "months_to_ship": 3,
  "tier": "A | B | C",                     // urgency tier (contact-worthiness)
  "reasons": ["transmitter on board, Part 15 Subpart C required", "..."],

  // attributes (model read from the page — no human panel; evidence is the audit trail)
  "attributes": { "intentional_radiator": true, "lithium_cell": true },
  "evidence": { "lithium_cell": "…quote from the page justifying it…" },
  "attributes_confidence": { "lithium_cell": 0.9 },  // low/uncertain → leave null

  // scope (deterministic rules engine)
  "determination": { "standards": [...], "cost_band": [lo, hi], "weeks": 12 },
  "standards": ["47 CFR Part 15 Subpart C", "UN 38.3", "..."],
  "lab": { "name": "...", "accreditations": [...], "one_stop": true },

  // offer + outreach (Gmail MCP)
  "offer_tier": "free | enhanced",
  "report_v1": "…markdown free report…",
  "variant": "A | B", "subject": "...", "body": "...",
  "gmail_thread_id": null,      // set on send; native reply tracking
  "outreach": "drafted | sent | bounced",

  // engagement + expert loop
  "engagement": { "opened": null, "replied": false, "reply_snippet": null },
  "expert_job_id": null, "expert_posted_at": null,
  "expert_state": "empty | pending | signed",
  "expert_name": null, "expert_credential": null, "expert_comments": [],
  "report_v2": null,           // signed version
  "approval_simulated": false, // only true under SIMULATED_APPROVAL=1, badged
  "refund_deadline": null, "expert_outcome": null,  // 'not_found' triggers refund

  "stage": "sourced | qualified | scoped | contacted | replied | enhanced | signed"
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
`source: linkedin_engagement` and routed to a warmer email (§7.5).
*Acceptance:* N normalized records with a `url`, `ship_month`, and `page_text`.

### 7.2 Enrich
Fill contact + deliverability fields. Apollo/Clay for founder name, title,
LinkedIn, and a verified email. **Deliverability gate (from deplace):** set
`has_email` and `email_status`; a `risky`/`invalid`/missing email is not
contacted (email-only channel — no address, no send). In deplace, ~55% of a raw
list had a usable email; design for that, and treat finding the founder's address
as part of enrichment, not an assumption.
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

### 7.4 Scope (deterministic rules engine)
Map the model's attributes → standards via `data/standards.yaml` (auditable,
cited), pick a lab via `data/labs.yaml` (prefer one-stop, prefer startup-friendly
— the big labs decline this segment, which is the whole thesis). **The model
classifies and writes prose; the YAML decides which standards apply.** Every
attribute the scope relies on must carry an `evidence` quote from the page — that
is the audit trail in place of a human panel, and low-confidence reads are left
`null` rather than guessed. A standard not in the YAML does not go in a report.
Render `report_v1` (free tier) with an empty, upgrade-linked expert signature block.
*Acceptance:* a free report renders end to end with clause citations, every
asserted attribute has an `evidence` quote, and zero occurrences of "certified"
about our own output.

### 7.5 Outreach (email-only, Gmail MCP)
The email carries the actual scope (§4). Two variants (absence hook / cost hook),
plain text only, no tracking pixel, CAN-SPAM footer (physical address +
unsubscribe) on every send. **Execution runs on the Gmail MCP** — send the message
and let Gmail own the thread; no separate sequencer or API setup. Store the
returned `gmail_thread_id` so replies can be tracked natively (§7.6). Path by
segment:
- **Cold (`has_email`):** one send now (the scope); one follow-up later on the
  sleeper standard if no reply. Keep touches minimal — this is a technical
  audience, not a drip.
- **Warm (`linkedin_engagement`):** open on the engagement — "picking this back
  up" — shorter, no re-introduction.

**Send discipline (non-negotiable):** nothing sends without an explicit `--send`;
default writes drafts to an outbox. A hard `MAX_SENDS` cap — cold volume from a
single Gmail address lands in spam and a spam-foldered demo shows zero replies.
Warm the address and keep volume low.

**Variant selection is a learning loop.** Which of the two hooks to send is not
fixed — a contextual bandit (`src/learning.py`) picks per segment and shifts toward
whatever earns replies, folding in each observed outcome via `pipeline learn`. It
is **built and tested** (≈+49% reply rate vs. fixed 50/50 on the eval; converges
per segment). Full design and the one integration point the team owns (Gmail reply
polling → `engagement.replied`) are in `docs/LEARNING-LOOP.md`.
*Acceptance:* drafts render for every tier-A record; `--send` gated; caps
enforced; every draft has the caveat + footer; variant chosen by the policy.

### 7.6 Engage
Reply tracking is native: poll the `gmail_thread_id` for a reply and write
`engagement.replied` + a `reply_snippet` onto the record. A reply is the north
star — surface it immediately. **Never simulate a reply from a stranger.** This is
also the reward signal that closes the learning loop (`docs/LEARNING-LOOP.md`):
once `engagement` is observed, `pipeline learn` folds the outcome into the variant
policy.
*Acceptance:* engagement fields update from real Gmail threads; replies appear on
the dashboard; observed outcomes are learnable exactly once.

### 7.7 Re-engage (highest-value message)
When an expert has reviewed a report, draft a follow-up that **quotes the expert
verbatim** — never "an expert reviewed your report" when you can paste the actual
sentence. Variants by prior state (never replied / went quiet / already paid).
This puts the human review inside the GTM loop, not only in delivery.
*Acceptance:* the draft contains the expert's real sentence, not a paraphrase.

### 7.8 Enhance & degrade (the paid loop — the one human-input step)
On enhance (paid via Stripe Payment Link), post the job **plus the finished draft**
to Terac's expert pool — the draft turns hours of unknown work into twenty minutes
of review, which raises acceptance. On acceptance → `pending` → signed `report_v2`
ships. This review is Compl.AI's **single human-in-the-loop** and the measurable
before/after (`report_v1` → `report_v2`) that satisfies the external-input
criteria. **If no expert accepts by `refund_deadline`, refund automatically and
send the honest "no reviewer found" note** — the same honesty the founder was
denied by the consultancy. Demo this screen on purpose.

The approval step may be simulated for a demo **only** behind
`SIMULATED_APPROVAL=1`, which sets `approval_simulated: true` and forces a visible
badge on the row. With the flag off, no code path can set the flag. Never simulate
a Stripe charge, a stranger's reply, or an expert review.

## 8. The accuracy chain (why there is no compliance expert on payroll)

| Layer | Question | Who answers | Cost of being wrong |
| --- | --- | --- | --- |
| **Perception** | battery? radio? ship date? child audience? | the model, from the page; each attribute carries an `evidence` quote | mitigated by cited evidence + the paid expert review |
| **Rules** | which standards those attributes trigger | `standards.yaml`, deterministic | auditable, fixable in the file |
| **Authority** | is the scope right, what does it cost | accredited-lab quotes + the signed Terac expert review | the lab's accreditation is on the line, not ours |

Reading a product page is not expert work, so the model does it and every
attribute it relies on is backed by a quote from the page — the read is auditable
without trusting the model. Human judgment enters once, at the **deliverable**: the
paid Terac expert review signs the report. Verification of the scope is otherwise
*structural* — we send it to three labs as quote requests; their quotes confirm or
correct it, and they are free because labs want qualified inbound.

## 9. What we are copying from deplace

The deplace outbound *tactics* are proven; reuse them, do not reinvent them.
Execution is simplified to email-only on the Gmail MCP (no LGM, no LinkedIn
automation, no separate API to stand up), but the playbook is the same:

1. **A/B/C tiering.** Every list was tiered by fit/urgency and worked top-down.
   → our `tier` field; only tier-A is contacted today.
2. **Deliverability gating.** `has_email` was a first-class column. Email-only
   here makes it stricter: no valid address → not contacted. ~55% coverage was
   normal, so treat finding the address as enrichment work. → §7.2 gate.
3. **Warm sourcing from content engagement.** The best-performing segment was
   *people who engaged with a LinkedIn post* — its own tiered segment. → source
   them as `linkedin_engagement`, email a warmer opener (§7.5).
4. **Engagement feedback loop.** Engaged contacts were re-worked, not dropped
   after one touch. → §7.6 → §7.7; records are long-lived and re-runnable, and
   Gmail threads make reply state native.
5. **Small, clean lists beat big dirty ones.** deplace ran ~60-row tiered lists,
   not 10k blasts. → cap tier-A volume; protect deliverability over reach. This
   matters more from a single Gmail address than it did from a warmed LGM pool.

The deplace list columns (`firstname, lastname, company_name, job_title,
linkedin_url, email, tier, source`) still define enrichment output — the GTM agent
produces that row, then hands the email body to the Gmail MCP to send and track.

## 10. Tooling & integrations

| Capability | Tool | Notes |
| --- | --- | --- |
| Sourcing | Apify | pick actor at runtime; seed-list fallback |
| Contact enrichment | Apollo, Clay | name/title/LinkedIn/verified email |
| FCC lookup | apps.fcc.gov EAS → fccid.io | browser UA; honest failure, never guess |
| Expert review | Terac | best-effort expert pool that reviews + signs the deliverable (paid enhance only — not in the GTM loop) |
| Outreach + reply tracking | Gmail MCP | send + native thread tracking; no separate sequencer/API |
| Payment | Stripe Payment Link | no gated app; enhanced report emails on confirmation |
| Model | Anthropic (Claude) | classify device + write prose; **not** the standards decision |

**Model note:** use a current Claude model id (e.g. `claude-sonnet-4-6` for the
extraction/classification task; `claude-opus-4-8` where deeper reasoning helps).
The old `claude-opus-4-20250514`-style ids in the scaffold are stale — fix them.

## 11. Guardrails (bugs if violated)

- **Never claim we certify anything.** "Reviewed and signed by a named expert."
  Certification authority is the lab's. Assert on this in the renderer.
- **Never send without `--send`; `MAX_SENDS` is a hard cap.** Default is drafts.
  Cold volume from one Gmail address burns deliverability — keep it low, warm the
  address first.
- **Every external call is cached; `OFFLINE=1` replays a full run with no network.**
- **Never simulate** a Stripe charge, a stranger's reply, or an expert review. The
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
- **M1 — Source → Qualify:** Apify/seed sourcing, enrichment (with email gate),
  FCC + tiering. Output: tier-A list with reasons.
- **M2 — Scope:** model extraction with `evidence`, rules engine, `report_v1`.
  Output: a free report with cited standards and an evidence trail.
- **M3 — Outreach on Gmail MCP:** two variants, deliverability gate, warm vs. cold
  opener, send rails, `gmail_thread_id` capture + reply polling. Output: drafts +
  one warm-source send.
- **M4 — Enhance loop:** Stripe link, expert job with draft attached, poll,
  degrade + refund, re-engagement. Output: paid path + honest degradation screen.
- **M5 — Dashboard + metrics:** funnel tiles, replies, revenue, review before/after,
  simulated badge.

Ship in order; stop when the clock says stop, not when the list ends.

## 13. Open questions

- **Terac payload shapes** for the expert job are unconfirmed — pin field names
  against sponsor docs; everything downstream needs only a job id back.
- **Gmail deliverability + limits** — cold sending from a Gmail address risks spam
  foldering and per-day send limits (~500). Fine at demo scale; before scaling,
  warm the address or move to a dedicated sending domain.
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
