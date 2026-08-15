"""Sourcer. Finds the trigger event.

Firmographic databases do not know who is about to ship hardware. A crowdfunding
campaign publishes it: funded, dated, public. Apollo and Clay enrich the contact
after the trigger is found, they do not find the trigger.

If the Apify actor stalls, stop. Hand-collect twenty campaign URLs into
data/seed_prospects.json and move on. The scraper is not what is being judged and
twenty good rows beat two hundred broken ones.
"""
from __future__ import annotations

import json
import os
import re
from datetime import datetime

import requests

from .store import DATA, cached

UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
)
APIFY_TOKEN = os.environ.get("APIFY_TOKEN", "")
SEED = DATA / "seed_prospects.json"


def from_seed() -> list[dict]:
    """Manual fallback. Shape: [{"url": ..., "company": ..., "product": ...}]"""
    if not SEED.exists():
        return []
    return json.loads(SEED.read_text())


def from_apify(actor: str, payload: dict, limit: int = 60) -> list[dict]:
    """Run an Apify actor synchronously and take the dataset items.

    Pick the actor at runtime with the Apify MCP search rather than hardcoding an
    id that may not exist on your account.
    """

    def go():
        r = requests.post(
            f"https://api.apify.com/v2/acts/{actor}/run-sync-get-dataset-items",
            params={"token": APIFY_TOKEN, "limit": limit},
            json=payload,
            timeout=180,
        )
        r.raise_for_status()
        return r.json()

    rows = cached("apify", f"{actor}:{json.dumps(payload, sort_keys=True)}", go)
    return [normalise(r) for r in rows]


def normalise(row: dict) -> dict:
    return {
        "url": row.get("url") or row.get("link") or "",
        "company": row.get("creator") or row.get("company") or row.get("author") or "",
        "product": row.get("title") or row.get("name") or "",
        "pledged": row.get("pledged") or row.get("amount_raised"),
        "backers": row.get("backers"),
        "ship_month_raw": row.get("deliveryDate") or row.get("ship_date") or "",
        "page_text": row.get("description") or row.get("text") or "",
    }


def fetch_page(url: str) -> str:
    def go():
        r = requests.get(url, headers={"User-Agent": UA}, timeout=30)
        r.raise_for_status()
        text = re.sub(r"<script.*?</script>|<style.*?</style>", " ", r.text, flags=re.S | re.I)
        text = re.sub(r"<[^>]+>", " ", text)
        return re.sub(r"\s+", " ", text)[:30000]

    return cached("page", url, go)


def months_until(ship_month: str | None) -> float | None:
    """'2026-11' or 'November 2026' to months from now."""
    if not ship_month:
        return None
    for fmt in ("%Y-%m", "%B %Y", "%b %Y", "%m/%Y"):
        try:
            d = datetime.strptime(ship_month.strip(), fmt)
            now = datetime.now()
            return (d.year - now.year) * 12 + (d.month - now.month)
        except ValueError:
            continue
    return None
