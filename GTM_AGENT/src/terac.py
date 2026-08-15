"""Terac panel client. The perception layer of the pipeline.

Design rationale is in docs/05-TERAC-INTEGRATION.md. Short version: the accuracy
chain splits into perception, rules and authority. Only perception needs a human,
and reading a product page is a general population task, so the absence of
hardware compliance specialists on the panel does not matter.

IMPORTANT, read before running.
The exact Terac request and response shapes are not pinned here because the API
surface was not available at authoring time. Two adapters are provided:

  TeracHTTP  - fill in ENDPOINT and the two payload builders from the sponsor
               docs or the booth. Everything else stays the same.
  TeracMock  - deterministic fake panel. Lets the whole pipeline run end to end
               before the credentials work. Never demo from this. It is labelled
               in state.json as `panel_source: mock` on purpose so you cannot
               show it by accident.

Escalation ladder, do not invert it:
  Tier 1, blocking, general population, five perception questions.
  Tier 2, non-blocking, filtered for hardware or electronics experience if the
          pool fills. One question. Bonus slide if it lands, no impact if not.
"""
from __future__ import annotations

import os
import time
from collections import Counter

import requests

from .store import cached

ENDPOINT = os.environ.get("TERAC_API", "https://api.terac.com/v1")
TOKEN = os.environ.get("TERAC_API_KEY", "")

# Five questions any literate adult can answer from a product page.
# Keys match the attribute names in data/standards.yaml so the analyst can
# consume panel output directly with no translation layer.
PERCEPTION_QUESTIONS = [
    {
        "key": "lithium_cell",
        "text": "Does this product contain a rechargeable battery?",
        "options": ["yes", "no", "cannot tell"],
    },
    {
        "key": "intentional_radiator",
        "text": "Does it connect wirelessly to a phone, computer or the internet?",
        "options": ["yes", "no", "cannot tell"],
    },
    {
        "key": "ship_month",
        "text": "What month and year does the page say it will ship?",
        "type": "text",
    },
    {
        "key": "sold_to_children",
        "text": "Is this product intended for children under 12?",
        "options": ["yes", "no", "cannot tell"],
    },
    {
        "key": "external_power_supply",
        "text": "Does it plug into a wall outlet?",
        "options": ["yes", "no", "cannot tell"],
    },
]

COMPREHENSION_QUESTIONS = [
    {"key": "next_action", "text": "What is this company supposed to do next?", "type": "text"},
    {
        "key": "confidence",
        "text": "How confident are you that you could act on this?",
        "options": ["1", "2", "3", "4", "5"],
    },
    {"key": "confusing", "text": "What is confusing or missing?", "type": "text"},
]


class TeracHTTP:
    source = "terac"

    def __init__(self, panel: str = "general_population", n: int = 5):
        self.panel = panel
        self.n = n

    def _post(self, path: str, body: dict) -> dict:
        r = requests.post(
            f"{ENDPOINT}{path}",
            json=body,
            headers={"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"},
            timeout=30,
        )
        r.raise_for_status()
        return r.json()

    def launch(self, stimulus: str, questions: list[dict], title: str) -> str:
        # TODO confirm field names against sponsor docs. Everything downstream
        # only needs a task id back.
        out = self._post(
            "/studies",
            {
                "title": title,
                "audience": self.panel,
                "respondents": self.n,
                "stimulus": stimulus,
                "questions": questions,
            },
        )
        return out.get("id") or out.get("study_id")

    def results(self, task_id: str) -> list[dict] | None:
        r = requests.get(
            f"{ENDPOINT}/studies/{task_id}/responses",
            headers={"Authorization": f"Bearer {TOKEN}"},
            timeout=30,
        )
        if r.status_code == 404:
            return None
        r.raise_for_status()
        payload = r.json()
        rows = payload.get("responses", payload if isinstance(payload, list) else [])
        return rows or None


class TeracMock:
    """Deterministic stand-in so the pipeline runs before credentials work.

    Mirrors the model's own guess with one deliberate disagreement seeded per
    batch, which lets you exercise the correction path in dev. Marked as mock in
    state so it cannot reach a slide unnoticed.
    """

    source = "mock"

    def __init__(self, panel: str = "general_population", n: int = 5):
        self.panel, self.n = panel, n

    def launch(self, stimulus: str, questions: list[dict], title: str) -> str:
        return f"mock-{abs(hash(stimulus)) % 10**8}"

    def results(self, task_id: str) -> list[dict]:
        seed = int(task_id.split("-")[-1])
        rows = []
        for i in range(self.n):
            rows.append(
                {
                    "lithium_cell": "yes" if (seed + i) % 3 else "no",
                    "intentional_radiator": "yes" if (seed + i) % 2 else "cannot tell",
                    "ship_month": "November 2026",
                    "sold_to_children": "no",
                    "external_power_supply": "no" if (seed + i) % 4 else "yes",
                }
            )
        return rows


def client(mock: bool = False, **kw):
    if mock or not TOKEN:
        return TeracMock(**kw)
    return TeracHTTP(**kw)


def consensus(rows: list[dict], questions: list[dict]) -> dict:
    """Majority vote per question. 'cannot tell' does not win, it abstains.

    Returns {key: {'value': ..., 'agreement': float, 'n': int}}.
    Agreement is the winning share among panelists who committed to an answer.
    A low agreement number is a signal worth showing, not a number to hide.
    """
    out: dict = {}
    for q in questions:
        k = q["key"]
        votes = [str(r.get(k, "")).strip().lower() for r in rows if r.get(k) not in (None, "")]
        committed = [v for v in votes if v != "cannot tell"]
        if not committed:
            out[k] = {"value": None, "agreement": 0.0, "n": len(votes)}
            continue
        top, count = Counter(committed).most_common(1)[0]
        value = {"yes": True, "no": False}.get(top, top)
        out[k] = {"value": value, "agreement": count / len(committed), "n": len(votes)}
    return out


def label_prospect(prospect: dict, mock: bool = False, n: int = 5) -> dict:
    """Tier 1. Blocking. General population attribute labels."""
    c = client(mock=mock, panel="general_population", n=n)
    stimulus = (
        f"Product page for {prospect.get('product','a product')} "
        f"by {prospect.get('company','a company')}.\n\n"
        f"{prospect.get('page_text','')[:4000]}"
    )

    def go():
        tid = c.launch(stimulus, PERCEPTION_QUESTIONS, f"Product attributes: {prospect.get('product')}")
        for _ in range(60):
            rows = c.results(tid)
            if rows:
                return {"task_id": tid, "rows": rows, "source": c.source}
            time.sleep(10)
        return {"task_id": tid, "rows": [], "source": c.source}

    raw = cached("terac_label", prospect.get("url", prospect.get("company", "")), go)
    return {
        "terac_task_id": raw["task_id"],
        "panel_source": raw["source"],
        "panel_raw": raw["rows"],
        "panel_attributes": consensus(raw["rows"], PERCEPTION_QUESTIONS),
    }


def comprehension_gate(report_text: str, key: str, mock: bool = False, n: int = 5) -> dict:
    """Tier 1b. A report ships only once non-experts can name the next action."""
    c = client(mock=mock, panel="general_population", n=n)
    stimulus = (
        "Below is a compliance scoping report produced for a small hardware "
        "company. You are not expected to understand the technical standards.\n\n"
        + report_text[:6000]
    )

    def go():
        tid = c.launch(stimulus, COMPREHENSION_QUESTIONS, "Report comprehension")
        for _ in range(60):
            rows = c.results(tid)
            if rows:
                return {"task_id": tid, "rows": rows, "source": c.source}
            time.sleep(10)
        return {"task_id": tid, "rows": [], "source": c.source}

    raw = cached("terac_comprehend", key, go)
    rows = raw["rows"]
    conf = [int(r["confidence"]) for r in rows if str(r.get("confidence", "")).isdigit()]
    return {
        "comprehension_task_id": raw["task_id"],
        "comprehension_mean_confidence": (sum(conf) / len(conf)) if conf else None,
        "comprehension_pass": bool(conf) and (sum(conf) / len(conf)) >= 3.5,
        "comprehension_freetext": [r.get("confusing") for r in rows if r.get("confusing")],
        "panel_source": raw["source"],
    }


def expert_second_opinion(prospect: dict, standards: list[str], mock: bool = False, n: int = 3) -> dict | None:
    """Tier 2. NON-BLOCKING. Only runs if a filtered pool actually fills.

    Ask the booth first whether they can fill 3+ years electronics or hardware
    within two hours. If they cannot, skip this entirely. It is a bonus slide,
    never a dependency, and it is not the verification. The lab quote is the
    verification, because the lab's accreditation is what is legally on the line.
    """
    try:
        c = client(mock=mock, panel="hardware_electronics_3yr", n=n)
        stimulus = (
            f"Device: {prospect.get('product')}. "
            f"Attributes: {prospect.get('attributes')}.\n"
            f"Proposed standards list: {', '.join(standards)}"
        )
        q = [
            {
                "key": "looks_right",
                "text": "Does this standards list look correct for this device?",
                "options": ["yes", "no", "unsure"],
            },
            {"key": "missing", "text": "Anything obviously missing?", "type": "text"},
        ]
        tid = c.launch(stimulus, q, "Standards sanity check")
        rows = c.results(tid)
        if not rows:
            return None
        return {"expert_task_id": tid, "expert_rows": rows, "panel_source": c.source}
    except Exception:
        return None


# ---------------------------------------------------------------------------
# Expert review loop. Tier 2, paid, best effort. docs/06-PRODUCT-SPEC.md.
#
# The job posting carries the finished draft, deliberately. Expert time is the
# scarce input and a finished draft turns hours of unknown work into twenty
# minutes of review, so attaching it raises acceptance rather than wasting it.
#
# The hardware expert pool may never fill inside the event, so the honest
# default from a real poll is `open`, which drives the degradation path on
# purpose. A simulated acceptance is available ONLY behind SIMULATED_APPROVAL=1
# and every simulated record is tagged so the dashboard can badge it. There is
# no path to a simulated acceptance with the flag off.
# ---------------------------------------------------------------------------

EXPERT_PANEL = "hardware_electronics_3yr"
SIM_DELAY_SECONDS = int(os.environ.get("SIM_DELAY_SECONDS", "0"))

# The one place a human review is faked. Only reachable under SIMULATED_APPROVAL=1
# and always carried with simulated:true. The comments are written to read like a
# real reviewer's markup so the re-engagement copy has a verbatim sentence to
# quote, but they are never presented as a live review.
SIM_EXPERT = {
    "name": "Dana Whitfield",
    "credential": "iNARTE-certified EMC engineer, 12 years",
    "comments": [
        "The UN 38.3 call is right, but T.6 impact is the sub-test most cell "
        "vendors quietly skip. Ask for the report by section, not a summary "
        "certificate, or you will discover the gap at the carrier's dock.",
        "If the BLE module is pre-certified you can file under FCC modular "
        "approval and drop the intentional-radiator retest entirely. Worth "
        "confirming the module's grant before you budget for Part 15 testing.",
    ],
}


def _sim_enabled() -> bool:
    return os.environ.get("SIMULATED_APPROVAL") == "1"


def post_expert_job(prospect: dict, report_md: str, mock: bool = False) -> dict:
    """Post the paid enhance job to Terac with the finished draft attached.

    Returns {'job_id': str, 'source': 'terac'|'mock'}. Idempotency is the
    caller's job: skip the post when the prospect already has an expert_job_id.
    """
    if mock or not TOKEN:
        ident = prospect.get("url") or prospect.get("company", "")
        return {"job_id": f"exp-mock-{abs(hash(ident)) % 10**8}", "source": "mock"}

    body = {
        "title": f"Review hardware compliance scope: {prospect.get('product', 'a device')}",
        "audience": EXPERT_PANEL,
        "instructions": (
            "A compliance scope was drafted for a small hardware company from a "
            "published rules table. Review the standards list for this device, "
            "flag anything missing or wrong, and sign if it is correct. You are "
            "reviewing the scope, not certifying the product."
        ),
        "attachment": report_md,  # the point: the draft ships with the job
        "device_attributes": prospect.get("attributes", {}),
    }

    def go():
        r = requests.post(
            f"{ENDPOINT}/jobs",
            json=body,
            headers={"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"},
            timeout=30,
        )
        r.raise_for_status()
        out = r.json()
        return {"job_id": out.get("id") or out.get("job_id"), "source": "terac"}

    return cached("expert_post", prospect.get("url", prospect.get("company", "")), go)


def poll_expert_job(job_id: str, posted_at: float | None = None, mock: bool = False) -> dict:
    """Poll an expert job. Safe to call repeatedly when nothing has changed.

    Returns {'status': 'open'|'accepted'|'returned', 'expert': {...}|None,
             'comments': [...], 'simulated': bool}.
    """
    if _sim_enabled():
        age = (time.time() - posted_at) if posted_at else SIM_DELAY_SECONDS + 1
        if age < SIM_DELAY_SECONDS:
            return {"status": "open", "expert": None, "comments": [], "simulated": True}
        return {
            "status": "returned",
            "expert": {"name": SIM_EXPERT["name"], "credential": SIM_EXPERT["credential"]},
            "comments": list(SIM_EXPERT["comments"]),
            "simulated": True,
        }

    if mock or not TOKEN:
        # No real credentials and simulation off: we cannot invent an acceptance.
        # `open` is the truthful answer and it is what drives the refund path.
        return {"status": "open", "expert": None, "comments": [], "simulated": False}

    r = requests.get(
        f"{ENDPOINT}/jobs/{job_id}",
        headers={"Authorization": f"Bearer {TOKEN}"},
        timeout=30,
    )
    r.raise_for_status()
    out = r.json()
    return {
        "status": out.get("status", "open"),
        "expert": out.get("expert"),
        "comments": out.get("comments", []),
        "simulated": False,
    }
