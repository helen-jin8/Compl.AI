# Build spec for Claude Code

What exists, what to build, in order, with acceptance criteria. Read
`CLAUDE.md`, `06-PRODUCT-SPEC.md` and `02-DECISIONS.md` before starting.

Submissions lock 6:45 PM. Ship in the order below and stop when the clock says
stop rather than when the list ends.

## Already working, do not rebuild

- `src/store.py` cache and state, with `OFFLINE=1` replay
- `src/fcc.py` FCC absence lookup with two strategies and honest failure
- `src/analyst.py` deterministic attribute-to-standards determination
- `src/terac.py` perception panel, consensus, comprehension gate, mock adapter
- `src/outreach.py` two cold variants with hard send rails
- `src/sourcer.py` seed and Apify paths
- `src/pipeline.py` source, qualify, terac-label, analyze, outreach
- `data/standards.yaml` and `data/labs.yaml`
- `dashboard/index.html`

Verified: a perception panel catching a missed battery moves the standards list
from two entries to six, adding UN 38.3. That is the before and after.

## Task 1. Report renderer, blocking everything else

`src/report.py`, function `render(prospect) -> str` returning markdown.

Sections in order: what this device is, standards that apply with clause
citations, recommended lab and why, cost band and weeks, what to do this week,
and an expert signature block.

The signature block renders one of three states: `empty` with the upgrade link,
`pending` with the accepted expert's name and an ETA, `signed` with the name,
credential and their comments inline.

Acceptance: renders for the sample prospect in `data/state.json` with the block
in `empty` state, and no line anywhere says the word "certified".

## Task 2. Expert loop

Add to `src/terac.py`:

    post_expert_job(prospect, report_md) -> job_id
    poll_expert_job(job_id) -> {'status': 'open'|'accepted'|'returned',
                                'expert': {...}, 'comments': [...]}

The job posting must include the rendered draft. That is the point, see
`06-PRODUCT-SPEC.md`.

Add to `src/pipeline.py`: `post-expert-job`, `pull-expert-review`.

New state fields per prospect: `tier` as `free` or `enhanced`, `expert_job_id`,
`expert_posted_at`, `expert_accepted_at`, `expert_name`, `expert_credential`,
`expert_comments`, `report_v1`, `report_v2`, `approval_simulated`,
`refund_deadline`.

Acceptance: `post-expert-job` writes a job id into state and is idempotent on
re-run. `pull-expert-review` is safe to call when nothing has changed.

## Task 3. Simulated approval, labelled

`SIMULATED_APPROVAL=1` lets `poll_expert_job` return an accepted-and-returned
result after a short delay, and sets `approval_simulated: true`.

The dashboard must render a visible badge on any prospect carrying that flag.
Not a footnote, a badge on the row.

Acceptance: with the flag off, no path can set `approval_simulated`. With it on,
the badge appears. This is the one place where being caught undermines the whole
project, so make the flag impossible to forget.

## Task 4. Degradation path

If `now > refund_deadline` and status is still `open`, mark
`expert_outcome: not_found`, render the honest message from
`06-PRODUCT-SPEC.md`, and log a refund action.

Acceptance: the message renders and appears on the dashboard. This screen is
demoed on purpose.

## Task 5. Re-engagement

`src/pipeline.py reengage`. For every prospect with `expert_comments`, draft the
follow-up from section 7 of `04-OUTREACH-COPY.md`, quoting the expert verbatim.

Acceptance: the draft contains the expert's actual sentence, not a paraphrase and
not the phrase "an expert reviewed your report". Writes to `data/outbox/`, sends
only under `--send`.

## Task 6. Dashboard additions

Tiles for free reports shipped, enhance conversions, expert jobs posted, expert
jobs accepted, revenue. Badges for `approval_simulated` and `sent_pre_label`.
Keep the existing panel-correction section as the lead, because it is the
mandatory criteria.

## Task 7, only if time remains

Render Workflows deploy. Same judging panel as Best Agent-Run Company, so it is
the cheapest second track available.

## Standing rules

- Never emit the word "certified" about our own output. Reviewed and signed.
- Never send without `--send`. `MAX_SENDS=20` is hard.
- Every external call goes through `store.cached`. `OFFLINE=1` must replay a full
  demo run with no network.
- Never simulate a Stripe charge, a reply from a stranger, or a panel result.
- Absence from the FCC database is a signal, not a proof. Any copy that forgets
  the contract manufacturer caveat is a bug.
- If a standard is not in `data/standards.yaml`, it does not go in a report. Add
  it to the file with a citation or leave it out.

## Definition of done for the submission

1. `OFFLINE=1 python -m src.pipeline run` completes with no network.
2. Dashboard shows at least one panel correction with standards before and after.
3. At least one free report rendered end to end.
4. Twenty cold emails in `data/outbox/`, however many actually sent.
5. One expert job posted to Terac with the draft attached.
6. Stripe Payment Link live and submitted to organizers with the `rk_` key.
7. Nothing on screen claims we certify anything.
