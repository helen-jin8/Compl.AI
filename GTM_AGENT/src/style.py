"""House style guard. Keeps AI tells out of anything the company sends.

Two jobs:
  humanize(text)  -> mechanical fixes (em/en dashes, smart quotes) applied in place.
  lint(text)      -> a list of remaining AI-tell hits the author must rewrite by hand.
  assert_clean()  -> raises if any tell survives. Wired into outreach so no message
                     ships with an em dash or a "not just X, it's Y" flourish.

Why: a cold email that reads like it came out of a chatbot gets deleted, and a
technical founder is exactly the reader who notices. Rules distilled from how
people actually spot AI writing (see docs/STYLE.md). The point is not to pass a
detector, it is to sound like a person wrote it. Full rationale in docs/STYLE.md.
"""
from __future__ import annotations

import re

# --- mechanical fixes: safe to apply automatically --------------------------
_DASHES = {"—": ", ", "–": "-", "―": ", ", "−": "-"}
_SMART = {"“": '"', "”": '"', "‘": "'", "’": "'", "…": "..."}


def humanize(text: str) -> str:
    """Replace em/en dashes and smart punctuation. Collapse the doubled spaces
    that leaves. This is the auto-fixable layer; rhetoric it cannot fix, see lint()."""
    for bad, good in {**_DASHES, **_SMART}.items():
        text = text.replace(bad, good)
    text = re.sub(r" {2,}", " ", text)
    text = re.sub(r" ,", ",", text)
    return text


# --- rhetorical tells: flagged for a human rewrite, not auto-fixed ----------
# Each entry is (compiled regex, human-readable label). Kept deliberately tight
# so it does not fire on ordinary compliance prose.
_TELLS = [
    (r"\bnot only\b[^.?!]{0,60}\bbut also\b", "'not only X but also Y'"),
    (r"\bit'?s not (just |merely |simply )?[^.,;?!]{1,40},?\s+(it'?s|but)\b", "antithesis \"it's not X, it's Y\""),
    (r"\bisn'?t just\b", "\"isn't just X\""),
    (r"\bnot just\b[^.?!]{1,40}\bbut\b", "\"not just X but Y\""),
    (r"\bmore than just\b", "\"more than just\""),
    (r"\bi hope this (e-?mail|message|note|finds?)\b[^.?!]{0,30}\bwell\b", "\"I hope this finds you well\""),
    (r"\bat the end of the day\b", "\"at the end of the day\""),
    (r"\bin today'?s (fast[- ]paced|digital|modern|ever[- ]changing)\b", "\"in today's ... world\""),
    (r"\blet'?s (dive|unpack|explore|delve)\b", "\"let's dive/unpack\""),
    (r"\b(leverage|seamless(ly)?|robust|elevate|unlock|supercharge|game[- ]?chang\w*|"
     r"revolutioniz\w*|cutting[- ]edge|delve|realm|tapestry|testament|synergy|paradigm|"
     r"holistic|plethora|myriad|embark|bustling|vibrant|streamline\w*|empower\w*|"
     r"unparalleled|effortless\w*|supercharged)\b", "AI buzzword"),
    (r"[\U0001F000-\U0001FAFF☀-➿←-⇿⬀-⯿]", "emoji/symbol"),
    (r"—|–|―", "em/en dash (run humanize first)"),
]
_TELLS = [(re.compile(p, re.I), label) for p, label in _TELLS]


def lint(text: str) -> list[dict]:
    """Return remaining AI tells as [{label, match}]. Run humanize() first so the
    dash check only fires on genuinely un-fixed input."""
    hits = []
    for rx, label in _TELLS:
        for m in rx.finditer(text):
            hits.append({"label": label, "match": m.group(0).strip()})
    return hits


def assert_clean(text: str, where: str = "message") -> str:
    """Humanize, then hard-fail on any surviving tell. Mirrors report.py's refusal
    to ship the word 'certified': a guardrail, not a suggestion. Returns the
    humanized text so callers can use it directly."""
    cleaned = humanize(text)
    hits = lint(cleaned)
    if hits:
        detail = "; ".join(f"{h['label']} ({h['match']!r})" for h in hits[:6])
        raise AssertionError(f"AI tell in {where}: {detail}. Rewrite by hand. See docs/STYLE.md.")
    return cleaned
