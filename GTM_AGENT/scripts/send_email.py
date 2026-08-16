"""Craft and send one outbound email per address, standalone.

This is the short path: give it email addresses, it finds what it knows about
each one in data/prospects.json, has Pioneer draft the scope email, and delivers
it. It does not need the pipeline, state.json, or a Terac panel to have run, so
it works before the rest of the system is wired.

    python scripts/send_email.py --to founder@acme.com
    python scripts/send_email.py --all --limit 5
    python scripts/send_email.py --all --send          # actually sends

Two things it inherits from the rest of the system rather than reinventing:
  - src/outreach.py `deliver()` for the outbox, SMTP, and the CAN-SPAM footer.
  - src/style.py for the house-style guard, which runs on template copy too.

Safety rails are the same as the pipeline's, deliberately:
  - Nothing sends without --send. Default writes to data/outbox/ and prints.
  - MAX_SENDS is hard, counted across this run.
  - Unknown addresses still send, with a generic scope, only if you pass
    --allow-unknown. Otherwise they are skipped, because a cold email with the
    wrong device in it is worse than no email.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))


def load_env(path: Path = ROOT / ".env") -> None:
    """Minimal .env reader so this runs without adding a dotenv dependency.
    Real environment variables win, which keeps CI and one-off overrides sane."""
    if not path.exists():
        return
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


load_env()

from src import outreach, pioneer, style  # noqa: E402  (needs env loaded first)

PROSPECTS = ROOT / "data" / "prospects.json"
PAYMENT_LINK = os.environ.get("STRIPE_PAYMENT_LINK", "")
SENDER = os.environ.get("SENDER_NAME", "")

# Cost bands and lead times by how much of the scope is RF work. Rough on
# purpose: the email says "rough band" and the paid report is what refines it.
BANDS = {
    "rf": ((8000, 15000), 6, "Intertek, Boxborough MA"),
    "safety": ((7000, 12000), 5, "TUV SUD, Wakefield MA"),
    "light": ((3000, 6000), 3, "Element Materials, San Diego CA"),
}


def normalize(p: dict) -> dict:
    """prospects.json uses founder_name/deadline; outreach copy wants a first
    name and a readable ship month. Bridge the two without mutating the file."""
    founder = (p.get("founder_name") or "").strip()
    first = founder.split()[0] if founder else "there"

    ship = p.get("deadline") or ""
    if ship:
        try:
            from datetime import date

            y, m, d = (int(x) for x in ship.split("-"))
            ship = date(y, m, d).strftime("%B %Y")
        except (ValueError, TypeError):
            pass

    details = p.get("standards_detail") or [
        {"id": s, "cite": "", "because": ""} for s in (p.get("standards") or [])
    ]
    attrs = p.get("attributes") or {}
    kind = "rf" if attrs.get("intentional_radiator") else (
        "light" if attrs.get("light_emitting") else "safety"
    )
    band, weeks, lab = BANDS[kind]

    return {
        "first_name": first,
        "founder_name": founder,
        "founder_title": p.get("founder_title", ""),
        "company": p.get("company", ""),
        "product": p.get("product", ""),
        "one_line": p.get("blurb", ""),
        "location": p.get("location", ""),
        # None, not a placeholder string. Accelerator rows have no deadline, and
        # a placeholder reads as "shipping in your stated ship date" once it
        # lands mid-sentence. The copy branches on this instead.
        "ship_month": ship or None,
        "campaign_url": p.get("campaign_url", ""),
        "funding": p.get("usd_pledged"),
        "backers": p.get("backers"),
        "fcc_status": p.get("fcc", "unchecked"),
        "standards": details,
        "lab": lab,
        "cost_band": list(band),
        "weeks": weeks,
    }


def standards_block(details: list[dict]) -> str:
    lines = []
    for s in details[:5]:
        because = f" - {s['because']}" if s.get("because") else ""
        cite = f"  [{s['cite']}]" if s.get("cite") else ""
        lines.append(f"  {s['id']}{because}{cite}")
    return "\n".join(lines) or "  (no standards scoped yet)"


def template_email(c: dict) -> tuple[str, str]:
    """Fallback copy, used when Pioneer is unavailable. Same argument as the
    Pioneer prompt: lead with a fact, give away the scope, invite correction."""
    product = c["product"] or "your device"
    subject = f"no FCC grant on file for {product}"[:60].lower()
    lo, hi = c["cost_band"]
    offer = (
        f"Full scope with clause citations, plus three lab quotes requested on your "
        f"behalf: $19, {PAYMENT_LINK}\n\n"
        if PAYMENT_LINK
        else ""
    )
    ship = c["ship_month"]
    opener = (
        f"You're shipping {product} in {ship}"
        if ship
        else f"You're building {product}"
    )
    consequence = (
        f" Book late and {ship} slips."
        if ship
        else " That lead time is the part founders discover too late."
    )
    source = "your campaign page" if c["campaign_url"] else "your site"

    body = f"""Hi {c['first_name']},

{opener} and I couldn't find an equipment authorization under {c['company']} in the FCC database. If your contract manufacturer filed under their own grantee code, ignore this email.

If they didn't, here is what I read off {source}:

{standards_block(c['standards'])}

{c['lab']} covers that in one booking. Rough band is ${lo:,} to ${hi:,} and about {c['weeks']} weeks.{consequence}

That took about ninety seconds, which tells you how much of this work is mechanical.

{offer}Or just reply with your BOM and I'll correct anything I got wrong, free."""
    return subject, body


def build(c: dict, use_pioneer: bool) -> tuple[str, str, str]:
    """Returns (subject, body, how). `how` records which writer produced it, so
    the run log tells you whether Pioneer was actually in the loop.

    The footer is appended here, once, for both writers. outreach.py attaches it
    inside its own variant_a/variant_b, so neither Pioneer nor the template
    below carries it, and a send without it is a CAN-SPAM violation.
    """
    how = "template"
    if use_pioneer and pioneer.available():
        try:
            subject, body = pioneer.craft(c, PAYMENT_LINK, SENDER)
            how = "pioneer"
        except pioneer.PioneerUnavailable as e:
            print(f"  pioneer unavailable, using template: {e}")
            subject, body = template_email(c)
        except RuntimeError as e:
            print(f"  pioneer produced unusable copy, using template: {e}")
            subject, body = template_email(c)
    else:
        subject, body = template_email(c)

    return subject, body + outreach.FOOTER.format(
        sender=SENDER, addr=outreach.PHYSICAL_ADDRESS, unsub=outreach.UNSUB
    ), how


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--to", action="append", default=[], help="recipient, repeatable")
    ap.add_argument("--all", action="store_true", help="every prospect with an email")
    ap.add_argument("--limit", type=int, default=0, help="cap prospects from --all")
    ap.add_argument("--send", action="store_true", help="actually send, else draft only")
    ap.add_argument("--no-pioneer", action="store_true", help="force the template")
    ap.add_argument("--allow-unknown", action="store_true",
                    help="email addresses with no prospect record, generic scope")
    ap.add_argument("--as-prospect", metavar="NAME",
                    help="borrow this prospect's scope (company name or email) but "
                         "deliver to --to. For demoing the real copy to your own inbox.")
    args = ap.parse_args()

    if not args.to and not args.all:
        ap.error("give --to an address or pass --all")
    if args.as_prospect and not args.to:
        ap.error("--as-prospect needs --to, it redirects that prospect's email to you")

    rows = json.loads(PROSPECTS.read_text()) if PROSPECTS.exists() else []
    by_email = {r["email"].lower(): r for r in rows if r.get("email")}

    if args.all:
        targets = list(by_email)
        if args.limit:
            targets = targets[: args.limit]
    else:
        targets = [e.lower() for e in args.to]

    if args.send:
        # Everything a lawful send needs. Checked up front so a half-filled .env
        # fails before the first message rather than after the fifth.
        required = {
            "SMTP_USER": os.environ.get("SMTP_USER"),
            "SMTP_PASS": os.environ.get("SMTP_PASS"),
            "SEND_FROM": outreach.FROM,
            "SENDER_NAME": SENDER,
            "PHYSICAL_ADDRESS": outreach.PHYSICAL_ADDRESS,
            "UNSUBSCRIBE_URL": outreach.UNSUB,
        }
        missing = [k for k, v in required.items() if not v]
        if missing:
            print("Cannot send, .env is missing: " + ", ".join(missing))
            print("The last three are the CAN-SPAM footer. Sending without them is illegal.")
            return 1

    # --as-prospect: one record stands in for every recipient, so the demo shows
    # the copy a real founder would get rather than the generic fallback.
    stand_in = None
    if args.as_prospect:
        needle = args.as_prospect.lower()
        stand_in = by_email.get(needle) or next(
            (r for r in rows if needle in (r.get("company", "").lower())), None
        )
        if not stand_in:
            names = ", ".join(sorted(r["company"] for r in rows if r.get("email"))[:6])
            print(f"no prospect matches {args.as_prospect!r}. Try one of: {names}")
            return 1
        print(f"borrowing scope from {stand_in['company']}\n")

    sent = 0
    for email in targets:
        if sent >= outreach.MAX_SENDS:
            print(f"stopping at MAX_SENDS={outreach.MAX_SENDS}")
            break

        record = stand_in or by_email.get(email)
        if not record and not args.allow_unknown:
            print(f"{email}: no prospect record, skipped. Pass --allow-unknown to send anyway.")
            continue

        ctx = normalize(record or {"email": email})
        print(f"{email}  ({ctx['company'] or 'unknown company'})")
        subject, body, how = build(ctx, use_pioneer=not args.no_pioneer)

        try:
            status = outreach.deliver(email, subject, body, send=args.send)
        except AssertionError as e:
            # style.assert_clean refused it. Never silently downgrade to sending
            # copy that failed the guard.
            print(f"  blocked by style guard: {e}")
            continue

        print(f"  {status} via {how}: {subject}")
        if status == "sent":
            sent += 1

    where = "sent" if args.send else "drafted to data/outbox/"
    print(f"\n{len(targets)} target(s), {where}.")
    if not args.send:
        print("Add --send when you mean it.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
