"""Learning loop for outreach — a contextual multi-armed bandit.

The agent has more than one way to say the same true thing: variant A opens on the
absence hook (no FCC grant on file), variant B on the cost hook (weeks of testing
vs. the ship date). Which one earns a reply is not fixed — it depends on the
prospect. A founder with a lithium pack and a hard carrier deadline reacts to the
cost framing; one without reacts to the absence framing. We do not know the mapping
up front, so we learn it.

This is the continuous version of the generation-1 → generation-2 idea already in
`docs/04-OUTREACH-COPY.md`: send both framings, watch what replies, and let future
sends drift toward what works *for that kind of prospect*.

Design
------
- **Context (segment).** A low-cardinality key built from the features that plausibly
  change which hook lands: warm vs. cold source, battery, radio. `segment_of()`.
- **Arms.** The outreach variants (currently "A" and "B"; extensible).
- **Policy.** One Beta(alpha, beta) posterior per (segment, arm) on P(reply).
  Selection is **Thompson sampling** — sample a reply-rate from each arm's
  posterior and send the winner. That explores uncertain arms early and exploits
  the better arm as evidence accumulates, with no epsilon to tune.
- **Update.** Each observed outcome (replied / didn't) bumps that arm's posterior.

The reply signal in production is real: it comes from Gmail threads (see
`docs/PRD.md` §7.6), never from a simulator. The simulator in `src/evalsim.py` is a
test harness only and is firewalled from the live pipeline.
"""
from __future__ import annotations

import json
import random
from pathlib import Path

VARIANTS = ["A", "B"]


def segment_of(prospect: dict) -> str:
    """Context key for the bandit. Keep cardinality low so arms get enough data.

    Uses only features that plausibly change which framing converts. Attributes are
    the model's read (post-scope), so call this after the device is scoped.
    """
    a = prospect.get("attributes", {}) or {}
    warm = "warm" if prospect.get("source") == "linkedin_engagement" else "cold"
    batt = "batt" if a.get("lithium_cell") else "nobatt"
    radio = "radio" if a.get("intentional_radiator") else "noradio"
    return f"{warm}|{batt}|{radio}"


class Policy:
    """Beta-Bernoulli Thompson-sampling bandit, one posterior per (segment, arm)."""

    def __init__(self, arms: dict | None = None):
        # key "segment||arm" -> [alpha, beta]; Beta(1,1) uniform prior when absent
        self.arms: dict[str, list[float]] = arms or {}

    # -- posterior bookkeeping -------------------------------------------------
    @staticmethod
    def _key(seg: str, arm: str) -> str:
        return f"{seg}||{arm}"

    def _ab(self, seg: str, arm: str) -> list[float]:
        return self.arms.setdefault(self._key(seg, arm), [1.0, 1.0])

    def rate(self, seg: str, arm: str) -> float:
        """Posterior mean P(reply) for this arm."""
        a, b = self._ab(seg, arm)
        return a / (a + b)

    def trials(self, seg: str, arm: str) -> int:
        """Observed sends for this arm (priors excluded)."""
        a, b = self._ab(seg, arm)
        return int((a - 1) + (b - 1))

    # -- decisions -------------------------------------------------------------
    def choose(self, seg: str, variants: list[str] | None = None, rng: random.Random | None = None) -> str:
        """Thompson sampling: draw a rate from each arm's posterior, send the max."""
        variants = variants or VARIANTS
        rng = rng or random
        best, best_sample = variants[0], -1.0
        for v in variants:
            a, b = self._ab(seg, v)
            sample = rng.betavariate(a, b)
            if sample > best_sample:
                best_sample, best = sample, v
        return best

    def best_variant(self, seg: str, variants: list[str] | None = None) -> str:
        """The arm we'd exploit now (greedy, for reporting/dashboards).

        Restricted to arms that have data, so an untried arm sitting at its 0.5
        prior can't spuriously outrank an arm with a real, lower observed rate.
        Selection under uncertainty still explores untried arms — that is
        `choose()`'s job, via Thompson sampling.
        """
        variants = variants or VARIANTS
        tried = [v for v in variants if self.trials(seg, v) > 0]
        pool = tried or variants
        return max(pool, key=lambda v: self.rate(seg, v))

    def update(self, seg: str, arm: str, replied: bool) -> None:
        ab = self._ab(seg, arm)
        ab[0 if replied else 1] += 1.0

    # -- persistence -----------------------------------------------------------
    def to_dict(self) -> dict:
        return {"arms": self.arms}

    @classmethod
    def from_dict(cls, d: dict) -> "Policy":
        return cls(d.get("arms", {}))

    def save(self, path: str | Path) -> None:
        Path(path).write_text(json.dumps(self.to_dict(), indent=2))

    @classmethod
    def load(cls, path: str | Path) -> "Policy":
        p = Path(path)
        return cls.from_dict(json.loads(p.read_text())) if p.exists() else cls()

    def totals(self) -> dict:
        """Overall replies / sends / reply-rate across all arms (priors excluded)."""
        replies = sends = 0.0
        for a, b in self.arms.values():
            replies += a - 1
            sends += (a - 1) + (b - 1)
        return {
            "replies": int(replies),
            "sends": int(sends),
            "reply_rate": (replies / sends) if sends else None,
        }

    def summary(self, variants: list[str] | None = None) -> list[dict]:
        """Per-segment view for the dashboard / logs: chosen arm, rates, trials."""
        variants = variants or VARIANTS
        segs = sorted({k.split("||")[0] for k in self.arms})
        out = []
        for seg in segs:
            row = {"segment": seg, "best": self.best_variant(seg, variants)}
            for v in variants:
                row[f"rate_{v}"] = round(self.rate(seg, v), 3)
                row[f"n_{v}"] = self.trials(seg, v)
            out.append(row)
        return out
