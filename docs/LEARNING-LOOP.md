# Learning loop — outreach variant optimization

> **Code location.** Lives in [`GTM_AGENT/`](../GTM_AGENT/). Run from there
> (`cd GTM_AGENT`); `src/…` and `data/…` paths below are relative to it.

The agent does not send a fixed email. It learns which framing earns a reply *for
each kind of prospect*, and shifts future sends toward what works. This is the
continuous version of the generation-1 → generation-2 test in
`04-OUTREACH-COPY.md`: instead of one A/B study and a manual rewrite, the policy
updates every time a reply does or doesn't come in.

## Why a bandit and not an A/B test

An A/B test splits traffic 50/50 until it reaches significance, then you pick a
winner — and you've spent half your sends on the losing arm the whole time. A
**contextual multi-armed bandit** starts exploring, then concentrates sends on the
better arm *as evidence accumulates*, and keeps a separate winner per segment. On
our own eval that is a **~49% higher reply rate** than fixed 50/50 (see below).

Reply rate is the north-star metric (`docs/PRD.md` §2). The learning loop optimizes
it directly.

## How it works (`src/learning.py`)

- **Context / segment.** `segment_of(prospect)` → a low-cardinality key from the
  features that plausibly change which hook lands: `warm|batt|radio` etc. (warm vs.
  cold source, battery, radio). Low cardinality so each arm gets enough data.
- **Arms.** The outreach variants — today `A` (absence hook) and `B` (cost hook).
  Add a third and it self-balances; no other change needed.
- **Policy.** One `Beta(α, β)` posterior over P(reply) per `(segment, arm)`.
- **Selection — Thompson sampling.** `choose()` draws a sample reply-rate from each
  arm's posterior and sends the argmax. Uncertain arms get explored; as data
  accumulates the better arm wins almost every draw. No epsilon to tune.
- **Update.** `update(segment, arm, replied)` bumps `α` on a reply, `β` on silence.
- **Persistence.** `data/policy.json` (gitignored; it is learned state, like
  `state.json`). Carries across runs, so learning compounds.

## The loop, end to end

```
outreach ─▶ Gmail send ─▶ (reply or silence) ─▶ engage polls the thread ─▶ learn
   ▲                                                                          │
   └──────────────────  updated policy picks the next variant  ◀─────────────┘
```

1. `pipeline outreach` — `policy.choose(segment)` selects the variant per prospect;
   records `segment` + `variant` on the record; persists the policy.
2. `pipeline engage` (team's Gmail wiring) — polls `gmail_thread_id`, writes
   `engagement.replied` once the outcome is observed (reply, or silence past the
   window). **Real signal only** — never a simulated reply.
3. `pipeline learn` — folds each newly observed outcome into the policy exactly
   once (guarded by `outcome_learned`), then prints the per-segment table.

## The reply signal is real; the test signal is firewalled

Production learns from **Gmail threads only**. `docs/PRD.md` §11 forbids simulating
a stranger's reply in anything a customer or judge sees, and the pipeline honors
that: `learn` reads `engagement.replied`, which is set only by real thread polling.

`src/evalsim.py` is a **test harness**, not part of the pipeline. It invents a
hidden ground truth (battery devices reply more to the cost hook, non-battery to
the absence hook, warm leads more across the board) and checks the policy discovers
it. It never touches `state.json`, the dashboard, or a real send.

## Proof it learns

```
python -m src.evalsim
```

Runs the bandit against a fixed 50/50 baseline over 20 rounds and asserts:

1. learned reply rate improves from early to late rounds,
2. it beats the baseline (**~+49%** on the seeded run), and
3. **all 8 segments** converge to the truly-better arm.

Representative output:

```
learned reply rate  early(2): 0.185   late(5): 0.201
baseline reply rate late(5): 0.135
uplift over fixed 50/50 baseline: +49.4%
segments converged to the better arm: 8/8

segment            best  rate_A  rate_B   nA   nB
cold|batt|noradio     B  0.086   0.196   68  922   # piled sends onto B (cost hook)
cold|nobatt|noradio    A  0.150   0.043  954   44   # piled sends onto A (absence hook)
...
PASS: learning loop improves reply rate and converges per segment.
```

## What the team plugs in

Only step 2. The bandit and the `learn` fold-in are done. Wire `pipeline engage` to
the Gmail MCP: for each contacted prospect, poll `gmail_thread_id`, and set
`engagement = {"replied": <bool>, "observed": true}` once the reply window has
elapsed. `learn` does the rest. Do not count "no reply yet" as a rejection — only
fold in a prospect once its outcome is actually observed (that is why `learn` skips
records whose `engagement` is still absent).

## Extending it

- **More arms.** Add subject-line or CTA variants — same `choose`/`update`, more
  arms per segment.
- **Richer context.** Add features to `segment_of` (e.g. ship-window urgency), but
  watch cardinality: every new split divides the data and slows learning. Keep
  segments coarse until volume justifies more.
- **Non-reply rewards.** Today the reward is a reply. Swap in a paid-enhance reward
  to optimize for revenue instead of replies once conversion volume exists.
