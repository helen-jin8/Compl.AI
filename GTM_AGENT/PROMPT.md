# Kickoff prompt for Claude Code

Paste everything below the line into a fresh Claude Code session in `GTM_AGENT/`.

---

You are picking up a hackathon build already in progress. Submissions lock at
6:45 PM PDT today, Aug 15 2026. Optimise for shipping, not for elegance.

**Read these first, in this order, before writing any code:**
`CLAUDE.md`, `../docs/06-PRODUCT-SPEC.md`, `../docs/07-BUILD-SPEC.md`,
`../docs/02-DECISIONS.md`. Then skim `../docs/03-DEMO-SCRIPT.md` so you know what the
build has to produce on stage.

**What this is.** A go-to-market agent system for an autonomous hardware
compliance consulting firm, built for the Zero Human Company Hackathon hosted by
Terac. Pre-launch hardware founders must clear UL and FCC certification before
they can ship legally, the process is opaque, and consultancies reject small
founders. We scope and route. We never test and we never certify.

**The one design idea everything hangs on.** The outbound email is a free sample
of the deliverable. The prospecting agent and the compliance agent are the same
agent, so the cold email contains the actual standards list for that specific
device with clause citations. That is why it converts and why it is not spam.

**The accuracy chain, and why there is no expert on our payroll.** Perception
asks whether the device has a battery, a radio, a stated ship date, a child
audience. Rules map those attributes to standards and live in
`data/standards.yaml`, deterministic and auditable. Authority confirms the scope
and price and comes from accredited lab quote requests. Only perception needs a
human, and reading a product page is a general population task, which is why the
absence of compliance experts on the Terac panel never mattered.

**Two tiers.** Free report ships same day, gated by the Terac perception panel
which fills in minutes. Paid enhance posts the job plus the finished draft to
Terac for expert review and signature, three to four day SLA, refunded
automatically if nobody accepts. The draft goes out before the expert accepts,
deliberately: expert time is the scarce input and a finished draft turns hours of
unknown work into twenty minutes of review.

**Your task list is `../docs/07-BUILD-SPEC.md`.** Task 1, the report renderer, is
already done in `src/report.py`. Start at Task 2, the expert loop. Work down the
list in order and stop when the clock says stop rather than when the list ends.

**Standing rules you must not break:**

- Never say we certify anything. Reviewed and signed by a named expert.
  Certification authority is the lab's. `src/report.py` asserts on this.
- Never send email without `--send`. `MAX_SENDS=20` is hard. A cold domain
  sending volume lands in spam and the demo shows zero replies.
- Every external call goes through `store.cached`. `OFFLINE=1` must replay a full
  run with no network, because venue wifi decides whether the stage demo works.
- Never simulate a Stripe charge, a reply from a stranger, or a Terac panel
  result. The expert approval step may be simulated, but only behind
  `SIMULATED_APPROVAL=1`, and the dashboard must render a visible badge on any
  record carrying that flag.
- Absence from the FCC database is a signal, not a proof, because a grant can sit
  under a contract manufacturer's grantee code. Any copy that drops that caveat
  is a bug.
- If a standard is not in `data/standards.yaml` it does not go in a report. Add it
  to the file with a citation or leave it out.
- Do not drop the Terac perception panel in favour of the expert loop. Terac use
  is mandatory for eligibility, the panel always fills, and the expert pool may
  never accept a hardware job today.

**Known gaps, do not discover these at 6:30:** Terac request and response shapes
are unconfirmed and `src/terac.py` has the adapter plus a TODO. `apps.fcc.gov`
returned 403 from a datacenter IP during development and may work from a laptop
with a browser user agent, with a fccid.io fallback already wired. No Apify actor
is hardcoded, so pick one at runtime or hand-fill `data/seed_prospects.json`.

**Definition of done, all seven:**

1. `OFFLINE=1 python -m src.pipeline run` completes with no network.
2. Dashboard shows at least one panel correction with standards before and after.
3. At least one free report rendered end to end.
4. Twenty cold emails in `data/outbox/`.
5. One expert job posted to Terac with the draft attached.
6. Stripe Payment Link live and submitted to organizers with the `rk_` key.
7. Nothing on screen claims we certify anything.

Start by running `OFFLINE=0 python -m src.pipeline run --mock` to confirm the
existing pipeline works on the sample row, then read Task 2 and begin. Tell me
what you find broken before you fix it.
