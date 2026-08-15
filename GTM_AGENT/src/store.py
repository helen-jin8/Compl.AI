"""State and cache. Everything the dashboard reads comes from here.

Two rules that exist because of the stage demo:
  1. Every external fetch goes through `cached()`. No exceptions.
  2. `OFFLINE=1` replays from cache and never touches the network.
"""
from __future__ import annotations

import hashlib
import json
import os
import time
from pathlib import Path
from typing import Any, Callable

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
CACHE = DATA / "cache"
OUTBOX = DATA / "outbox"
STATE_PATH = DATA / "state.json"

for d in (DATA, CACHE, OUTBOX):
    d.mkdir(parents=True, exist_ok=True)


def offline() -> bool:
    return os.environ.get("OFFLINE") == "1"


def _key(namespace: str, ident: str) -> Path:
    h = hashlib.sha256(ident.encode()).hexdigest()[:20]
    return CACHE / f"{namespace}__{h}.json"


def cached(namespace: str, ident: str, fn: Callable[[], Any]) -> Any:
    """Return cached value, else call fn and cache it.

    In offline mode a cache miss raises rather than silently returning None,
    because a silent None on stage looks like a bug in the product.
    """
    path = _key(namespace, ident)
    if path.exists():
        return json.loads(path.read_text())["value"]
    if offline():
        raise RuntimeError(
            f"offline cache miss: {namespace} / {ident}. "
            "Run once online to warm the cache before demoing."
        )
    value = fn()
    path.write_text(json.dumps({"ident": ident, "at": time.time(), "value": value}, indent=2))
    return value


def load_state() -> dict:
    if STATE_PATH.exists():
        return json.loads(STATE_PATH.read_text())
    return {"prospects": [], "events": [], "meta": {}}


def save_state(state: dict) -> None:
    STATE_PATH.write_text(json.dumps(state, indent=2, default=str))


def upsert(state: dict, prospect: dict) -> dict:
    """Merge a prospect by url. Returns the stored record."""
    for i, p in enumerate(state["prospects"]):
        if p.get("url") == prospect.get("url"):
            state["prospects"][i] = {**p, **prospect}
            return state["prospects"][i]
    state["prospects"].append(prospect)
    return prospect


def log(state: dict, kind: str, detail: str, **extra) -> None:
    state["events"].append({"at": time.time(), "kind": kind, "detail": detail, **extra})
