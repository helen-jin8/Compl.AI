"""Pipeline runner.

    python -m src.pipeline source     --limit 60
    python -m src.pipeline qualify
    python -m src.pipeline terac-label            # tier 1, launch and walk away
    python -m src.pipeline terac-pull             # idempotent, run again later
    python -m src.pipeline analyze [--terac-async]
    python -m src.pipeline outreach [--send]
    python -m src.pipeline terac-comprehend
    python -m src.pipeline run                    # one prospect, end to end, for stage

OFFLINE=1 replays every external call from data/cache/. Warm the cache before
you demo and the stage run stops depending on venue wifi.
"""
from __future__ import annotations

import argparse
import os

from . import analyst, fcc, outreach, sourcer, terac
from .store import load_state, log, save_state, upsert

SENDER = os.environ.get("SENDER_NAME", "")


def cmd_source(args, state):
    rows = sourcer.from_seed()
    if args.actor:
        rows += sourcer.from_apify(args.actor, {"category": "technology"}, args.limit)
    for r in rows[: args.limit]:
        if not r.get("url"):
            continue
        if not r.get("page_text"):
            r["page_text"] = sourcer.fetch_page(r["url"])
        upsert(state, {**r, "stage": "sourced"})
    log(state, "source", f"{len(rows)} rows")
    print(f"sourced {len(state['prospects'])}")


def cmd_qualify(args, state):
    for p in state["prospects"]:
        info = analyst.extract(p.get("page_text", ""), p["url"])
        p.update(
            {
                "product": info.get("product") or p.get("product"),
                "company": info.get("company") or p.get("company"),
                "one_line": info.get("one_line"),
                "ship_month": info.get("ship_month"),
                "model_attributes": info.get("attributes", {}),
                "evidence": info.get("evidence", {}),
                "attributes": info.get("attributes", {}),
            }
        )
        p["fcc"] = fcc.lookup(p.get("company") or "")
        m = sourcer.months_until(p.get("ship_month"))
        p["months_to_ship"] = m
        p["tier"], p["reasons"] = fcc.urgency(p, m)
        p["stage"] = "qualified"
    tiers = [p["tier"] for p in state["prospects"]]
    print(f"tier A {tiers.count('A')}  B {tiers.count('B')}  C {tiers.count('C')}")


def cmd_terac_label(args, state):
    n = 0
    for p in state["prospects"]:
        if p.get("tier") != "A":
            continue
        p.update(terac.label_prospect(p, mock=args.mock))
        p["stage"] = "labelled"
        n += 1
    log(state, "terac", f"labelled {n}")
    print(f"labelled {n}")


cmd_terac_pull = cmd_terac_label  # cached, so pulling again is the same call


def cmd_analyze(args, state):
    for p in state["prospects"]:
        if p.get("tier") != "A":
            continue
        panel = p.get("panel_attributes")
        if not panel and not args.terac_async:
            print(f"skip, awaiting panel: {p.get('company')}")
            continue

        before = analyst.determine(p.get("model_attributes", {}))
        merged, corrected = analyst.merge_attributes(p.get("model_attributes", {}), panel)
        after = analyst.determine(merged)

        p["attributes"] = merged
        p["attributes_corrected"] = corrected
        p["standards_before"] = before["standards_ids"]
        p["standards_after"] = after["standards_ids"]
        p["determination"] = after
        p["lab"] = analyst.pick_lab(merged)
        p["sleeper"] = analyst.sleeper_standard(after)
        p["sent_pre_label"] = panel is None
        p["stage"] = "analyzed"

        if corrected:
            gained = sorted(set(after["standards_ids"]) - set(before["standards_ids"]))
            log(
                state,
                "panel_correction",
                f"{p.get('company')}: panel overrode {corrected}",
                gained=gained,
            )
            print(f"panel corrected {p.get('company')}: {corrected} -> gained {gained}")


def cmd_outreach(args, state):
    sent = 0
    for i, p in enumerate(state["prospects"]):
        if p.get("tier") != "A" or not p.get("determination"):
            continue
        if sent >= outreach.MAX_SENDS:
            print(f"stopping at MAX_SENDS={outreach.MAX_SENDS}")
            break
        variant = "A" if i % 2 == 0 else "B"
        subject, body = outreach.render(
            p, p["determination"], p["lab"], variant, SENDER, p.get("sleeper")
        )
        to = p.get("email") or f"unknown+{i}@example.com"
        status = outreach.deliver(to, subject, body, send=args.send and bool(p.get("email")))
        p.update({"variant": variant, "subject": subject, "body": body, "outreach": status})
        p["stage"] = "contacted" if status == "sent" else "drafted"
        sent += 1
    log(state, "outreach", f"{sent} messages, send={args.send}")
    print(f"{sent} messages, send={args.send}")


def cmd_terac_comprehend(args, state):
    for p in state["prospects"]:
        if not p.get("body"):
            continue
        p.update(terac.comprehension_gate(p["body"], p["url"], mock=args.mock))
        p["comprehension_round"] = p.get("comprehension_round", 0) + 1
    passes = [p.get("comprehension_pass") for p in state["prospects"] if "comprehension_pass" in p]
    if passes:
        print(f"comprehension pass rate {sum(1 for x in passes if x)}/{len(passes)}")


def cmd_run(args, state):
    """One prospect end to end. This is the stage demo."""
    for fn in (cmd_source, cmd_qualify, cmd_terac_label, cmd_analyze, cmd_outreach):
        fn(args, state)


COMMANDS = {
    "source": cmd_source,
    "qualify": cmd_qualify,
    "terac-label": cmd_terac_label,
    "terac-pull": cmd_terac_pull,
    "analyze": cmd_analyze,
    "outreach": cmd_outreach,
    "terac-comprehend": cmd_terac_comprehend,
    "run": cmd_run,
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("command", choices=COMMANDS)
    ap.add_argument("--limit", type=int, default=60)
    ap.add_argument("--actor", default=os.environ.get("APIFY_ACTOR", ""))
    ap.add_argument("--send", action="store_true", help="actually send email")
    ap.add_argument("--mock", action="store_true", help="fake Terac panel, never demo this")
    ap.add_argument("--terac-async", action="store_true", help="do not block on panel")
    args = ap.parse_args()

    state = load_state()
    try:
        COMMANDS[args.command](args, state)
    finally:
        save_state(state)


if __name__ == "__main__":
    main()
