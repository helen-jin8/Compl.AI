"""FCC Equipment Authorization lookup.

This is the qualification signal. If a company has no grant on file and their
device has a radio, and they are shipping soon, they have a problem they have not
priced.

Honest limits, and these must survive into the outbound copy:
  - A grant can be filed under a contract manufacturer's grantee code rather than
    the brand name. Absence is a strong signal, not a proof.
  - apps.fcc.gov sits behind bot protection. It returned 403 to a datacenter IP
    during development. It will probably work from a laptop with a browser user
    agent. Strategy 2 exists for when it does not.

Strategies, in order:
  1. FCC EAS generic search with a browser user agent.
  2. fccid.io, a third party mirror, as a fallback.
  3. Return `unknown` and mark the record `fcc_checked: false`. Never guess.
"""
from __future__ import annotations

import re
import urllib.parse

import requests

from .store import cached

UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
)
EAS = "https://apps.fcc.gov/oetcf/eas/reports/GenericSearchResult.cfm"
TIMEOUT = 20


def _try_eas(company: str) -> dict | None:
    params = {"RequestTimeout": "500", "calledFromFrame": "N", "applicant": company}
    url = f"{EAS}?{urllib.parse.urlencode(params)}"
    r = requests.get(url, headers={"User-Agent": UA}, timeout=TIMEOUT)
    if r.status_code != 200:
        return None
    body = r.text
    if re.search(r"no records|0 records", body, re.I):
        return {"source": "fcc_eas", "grants": 0, "checked": True}
    ids = re.findall(r"[A-Z0-9]{3,5}-[A-Z0-9\-]{2,14}", body)
    return {"source": "fcc_eas", "grants": len(set(ids)), "sample": sorted(set(ids))[:5], "checked": True}


def _try_fccid_io(company: str) -> dict | None:
    slug = urllib.parse.quote(company)
    r = requests.get(
        f"https://fccid.io/search.php?q={slug}", headers={"User-Agent": UA}, timeout=TIMEOUT
    )
    if r.status_code != 200:
        return None
    hits = len(re.findall(r'href="/[A-Z0-9\-]{5,}"', r.text))
    return {"source": "fccid_io", "grants": hits, "checked": True}


def lookup(company: str) -> dict:
    """Return {'grants': int|None, 'source': str, 'checked': bool}."""

    def fetch() -> dict:
        for strategy in (_try_eas, _try_fccid_io):
            try:
                out = strategy(company)
            except Exception:
                out = None
            if out is not None:
                return out
        return {"source": "none", "grants": None, "checked": False}

    return cached("fcc", company.lower().strip(), fetch)


def urgency(prospect: dict, months_to_ship: float | None) -> tuple[str, list[str]]:
    """Tier a prospect. Returns (tier, reasons).

    Tier A is the only tier we contact today. Twenty tier A rows beat two hundred
    of anything else.
    """
    reasons: list[str] = []
    a = prospect.get("attributes", {})
    fcc = prospect.get("fcc", {})

    has_radio = a.get("intentional_radiator") is True
    has_batt = a.get("lithium_cell") is True
    no_grant = fcc.get("grants") == 0
    unchecked = not fcc.get("checked")

    if has_radio:
        reasons.append("transmitter on board, Part 15 Subpart C certification required")
    if has_batt:
        reasons.append("lithium pack, UN 38.3 required before any carrier will fly it")
    if no_grant:
        reasons.append("no FCC grant found under this company name")
    if unchecked:
        reasons.append("FCC database not reachable, signal unverified")
    if months_to_ship is not None and months_to_ship <= 6:
        reasons.append(f"ship date roughly {months_to_ship:.0f} months out")

    near = months_to_ship is not None and months_to_ship <= 6
    if (has_radio or has_batt) and no_grant and near:
        return "A", reasons
    if has_radio or has_batt:
        return "B", reasons
    return "C", reasons
