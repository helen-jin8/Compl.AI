"""Offline evaluation harness for the outreach learning loop.

  python -m src.evalsim

WARNING — TEST ONLY. This file simulates reply outcomes to prove the learning
policy in `src/learning.py` actually learns. It is firewalled from the live
pipeline and the dashboard on purpose: the real reply signal comes from Gmail
threads, never from here. `docs/PRD.md` §11 forbids simulating a stranger's reply
in anything a judge or customer sees. This is a unit test, not a demo.

What it shows
-------------
A ground-truth environment (which the agent never sees) where the better email
framing *depends on the segment*: battery devices reply more to the cost hook (B),
non-battery to the absence hook (A), and warm leads reply more across the board.
We run the bandit round by round against a fixed 50/50 A/B baseline and check that:

  1. the learned policy's reply rate beats the baseline, and
  2. for every segment, the policy converges on the truly-better arm.
"""
from __future__ import annotations

import random

from .learning import Policy, VARIANTS

# Every segment the sourcing/scoping stage can produce (warm|batt|radio).
SEGMENTS = [
    f"{w}|{b}|{r}"
    for w in ("cold", "warm")
    for b in ("batt", "nobatt")
    for r in ("radio", "noradio")
]


def true_reply_prob(seg: str, variant: str) -> float:
    """Hidden ground truth. The agent must discover this from outcomes alone.

    The right hook roughly doubles reply rate for its segment — the realistic case
    where framing matters and the whole point of learning which one to send.
    """
    warm, batt, radio = seg.split("|")
    base = 0.10 if warm == "warm" else 0.04          # warm leads reply more
    if batt == "batt":
        lift = 0.14 if variant == "B" else 0.0        # cost hook wins for battery
    else:
        lift = 0.12 if variant == "A" else 0.0        # absence hook wins otherwise
    if radio == "radio":
        base += 0.01                                  # small radio bump, hook-neutral
    return min(base + lift, 0.95)


def better_arm(seg: str) -> str:
    return max(VARIANTS, key=lambda v: true_reply_prob(seg, v))


def run(rounds: int = 20, batch: int = 400, seed: int = 7) -> dict:
    rng = random.Random(seed)
    policy = Policy()

    learned_hist: list[float] = []
    baseline_hist: list[float] = []

    for _ in range(rounds):
        l_rep = l_sent = b_rep = b_sent = 0
        for _ in range(batch):
            seg = rng.choice(SEGMENTS)

            # learned agent: pick a variant via Thompson sampling, observe, update
            v = policy.choose(seg, VARIANTS, rng)
            replied = rng.random() < true_reply_prob(seg, v)
            policy.update(seg, v, replied)
            l_sent += 1
            l_rep += int(replied)

            # baseline: fixed 50/50, no learning (same segment, independent draw)
            vb = rng.choice(VARIANTS)
            b_replied = rng.random() < true_reply_prob(seg, vb)
            b_sent += 1
            b_rep += int(b_replied)

        learned_hist.append(l_rep / l_sent)
        baseline_hist.append(b_rep / b_sent)

    # did the policy land on the truly-better arm in each segment?
    converged = {seg: policy.best_variant(seg) == better_arm(seg) for seg in SEGMENTS}

    return {
        "policy": policy,
        "learned_hist": learned_hist,
        "baseline_hist": baseline_hist,
        "converged": converged,
    }


def main() -> int:
    res = run()
    learned, baseline = res["learned_hist"], res["baseline_hist"]

    def avg(xs):
        return sum(xs) / len(xs)

    early = avg(learned[:2])
    late = avg(learned[-5:])
    base_late = avg(baseline[-5:])

    print("round  learned  baseline")
    for i, (l, b) in enumerate(zip(learned, baseline)):
        mark = "  <- learning" if i in (0, len(learned) - 1) else ""
        print(f"{i:>5}   {l:6.3f}   {b:6.3f}{mark}")

    print()
    print(f"learned reply rate  early(3): {early:.3f}   late(5): {late:.3f}")
    print(f"baseline reply rate late(5): {base_late:.3f}")
    uplift = (late - base_late) / base_late * 100
    print(f"uplift over fixed 50/50 baseline: {uplift:+.1f}%")

    n_seg = len(res["converged"])
    n_ok = sum(res["converged"].values())
    print(f"segments converged to the better arm: {n_ok}/{n_seg}")
    print()
    print("segment            best  rate_A  rate_B   nA   nB")
    for row in res["policy"].summary():
        print(
            f"{row['segment']:<18} {row['best']:>4}  "
            f"{row['rate_A']:.3f}   {row['rate_B']:.3f}  "
            f"{row['n_A']:>3}  {row['n_B']:>3}"
        )

    # assertions — this is a test
    assert late > early, f"policy did not improve: early {early:.3f} late {late:.3f}"
    assert late > base_late, f"policy no better than baseline: {late:.3f} vs {base_late:.3f}"
    assert n_ok == n_seg, f"only {n_ok}/{n_seg} segments converged"
    print("\nPASS: learning loop improves reply rate and converges per segment.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
