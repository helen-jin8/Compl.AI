"""Pioneer AI client. Drafts the outbound copy that outreach.py used to hardcode.

Pioneer speaks the OpenAI chat-completions shape, so this is a thin requests
wrapper rather than an SDK dependency. One entry point, `craft()`, which returns
(subject, body) already run through the house-style guard.

Why a model writes the copy at all, given outreach.py has working templates: the
templates produce two fixed framings for every prospect. A model can hang the
opening line on the specific device, which is the part that decides whether a
technical founder keeps reading. The templates stay as the fallback, and the
fallback is not decorative, see `available()`.

The style guard is not advisory here. Model output goes through style.humanize()
and then style.lint(); if tells survive, we hand the lint back to the model and
ask again. Two rounds, then we give up and let the caller fall back to a
template. A model that cannot stop writing "seamlessly" does not get to send mail.
"""
from __future__ import annotations

import json
import os
import re
from typing import Any

import requests

from . import style

API = os.environ.get("PIONEER_API", "https://api.pioneer.ai/v1")
KEY = os.environ.get("PIONEER_API_KEY", "")
MODEL = os.environ.get("PIONEER_MODEL", "claude-opus-4-8")
TIMEOUT = int(os.environ.get("PIONEER_TIMEOUT", "90"))

# Raised so callers can distinguish "Pioneer is down or unpaid" from "Pioneer
# answered but wrote unusable copy". The first means fall back silently, the
# second means something is wrong with the prompt and should be loud.
class PioneerUnavailable(RuntimeError):
    pass


SYSTEM = """You write cold outbound email for a hardware-compliance firm.

The email IS the deliverable, not a pitch for it. You give away a real scope of
the certification work the recipient needs, with clause citations, before asking
for money. Then you invite correction, because a reply is worth more than a sale.

Hard rules:
- Plain text. No markdown, no headers, no bullet characters other than two spaces
  of indent.
- No em dashes or en dashes. Use a comma or a full stop.
- No exclamation marks, no emoji.
- Never write: leverage, seamless, robust, elevate, unlock, supercharge, delve,
  realm, tapestry, testament, synergy, holistic, myriad, embark, streamline,
  empower, effortless, game-changing, cutting-edge, revolutionize.
- Never write "I hope this finds you well", "not just X but Y", "it's not X,
  it's Y", or "at the end of the day".
- No filler compliments. Do not tell them their product looks exciting.
- Short sentences. A working engineer wrote this in ninety seconds, and it reads
  that way.
- 150 to 220 words in the body. Longer gets deleted.

Structure:
1. One opening fact about THIS device that they cannot dismiss as mail-merge.
2. The standards you read off their page, one per line, indented two spaces,
   formatted "  ID - why it applies  [clause cite]".
3. A lab, a cost band, a number of weeks, and what slips if they book late.
4. One line noting how mechanical the work is.
5. The paid offer with the payment link.
6. An invitation to reply and correct you, free.

Return ONLY a JSON object: {"subject": "...", "body": "..."}
The subject is lowercase, under 60 characters, and states the specific gap. No
colons in the subject. Do not wrap the JSON in code fences."""


def available() -> bool:
    """True if a key is configured. Does not prove the key is entitled to
    inference; Pioneer gates that per plan and only tells you at call time."""
    return bool(KEY)


def _post(messages: list[dict]) -> str:
    if not KEY:
        raise PioneerUnavailable("PIONEER_API_KEY is not set")
    try:
        r = requests.post(
            f"{API}/chat/completions",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {KEY}",
            },
            json={"model": MODEL, "messages": messages, "stream": False},
            timeout=TIMEOUT,
        )
    except requests.RequestException as e:
        raise PioneerUnavailable(f"network error talking to Pioneer: {e}") from e

    if r.status_code in (401, 402, 403):
        # The plan gate lives here. Surface Pioneer's own wording, it names the
        # billing page.
        raise PioneerUnavailable(f"Pioneer refused the key ({r.status_code}): {_err(r)}")
    if r.status_code == 429:
        raise PioneerUnavailable("Pioneer rate limited this key (429)")
    if r.status_code >= 500:
        raise PioneerUnavailable(f"Pioneer server error ({r.status_code})")
    if not r.ok:
        raise RuntimeError(f"Pioneer returned {r.status_code}: {_err(r)}")

    try:
        return r.json()["choices"][0]["message"]["content"]
    except (KeyError, IndexError, ValueError) as e:
        raise RuntimeError(f"unexpected Pioneer response shape: {r.text[:300]}") from e


def _err(r: requests.Response) -> str:
    try:
        return str(r.json().get("error", {}).get("message", r.text[:200]))
    except ValueError:
        return r.text[:200]


def _parse(raw: str) -> tuple[str, str]:
    """Pull {"subject","body"} out of the reply, tolerating stray prose or fences."""
    text = raw.strip()
    text = re.sub(r"^```(?:json)?\s*|\s*```$", "", text).strip()
    try:
        obj = json.loads(text)
    except ValueError:
        m = re.search(r"\{.*\}", text, re.S)
        if not m:
            raise RuntimeError(f"no JSON in Pioneer reply: {raw[:300]}")
        obj = json.loads(m.group(0))
    subject, body = obj.get("subject", "").strip(), obj.get("body", "").strip()
    if not subject or not body:
        raise RuntimeError(f"Pioneer returned an empty subject or body: {raw[:300]}")
    return subject, body


def craft(context: dict[str, Any], payment_link: str, sender: str) -> tuple[str, str]:
    """Draft one email. Returns (subject, body), style-clean, no footer attached.

    Raises PioneerUnavailable if Pioneer cannot be reached or the key is not
    entitled, which is the caller's signal to use the template instead.
    """
    brief = json.dumps(context, indent=2, default=str)
    messages = [
        {"role": "system", "content": SYSTEM},
        {
            "role": "user",
            "content": (
                f"Write the email for this prospect.\n\n{brief}\n\n"
                f"Payment link to include: {payment_link or '(none, omit the paid offer)'}\n"
                f"Sign it: {sender}\n"
                "Do not add a signature block or unsubscribe line, those are appended later."
            ),
        },
    ]

    for attempt in range(2):
        raw = _post(messages)
        subject, body = _parse(raw)
        subject, body = style.humanize(subject), style.humanize(body)
        hits = style.lint(subject) + style.lint(body)
        if not hits:
            return subject, body
        # Hand the model its own violations and make it try again.
        complaints = "; ".join(f"{h['label']} in {h['match']!r}" for h in hits[:8])
        messages += [
            {"role": "assistant", "content": raw},
            {
                "role": "user",
                "content": (
                    f"That draft broke the style rules: {complaints}. "
                    "Rewrite it with those removed. Same JSON shape."
                ),
            },
        ]

    raise RuntimeError(
        f"Pioneer could not produce style-clean copy in 2 attempts. Last hits: {complaints}"
    )
