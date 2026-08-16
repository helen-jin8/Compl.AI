"""Outreach. The email is a free sample of the deliverable, not a pitch.

Both variants open with a fact about the recipient they cannot dismiss, give away
the answer before asking for money, and end by inviting correction. The invitation
to correct is what converts skeptics into repliers, and a reply is the most
valuable thing today because it is the one asset that cannot be manufactured.

Safety rails:
  - Nothing sends without --send. Default writes to data/outbox/.
  - MAX_SENDS is hard. A cold domain sending volume lands in spam and the demo
    shows zero replies.
  - Unsubscribe line and physical address on every send. Legal requirement, and
    also the answer when a judge asks whether this is spam.
"""
from __future__ import annotations

import os
import smtplib
from email.mime.text import MIMEText

from . import style
from .store import OUTBOX

MAX_SENDS = int(os.environ.get("MAX_SENDS", "20"))
FROM = os.environ.get("SEND_FROM", "")
PHYSICAL_ADDRESS = os.environ.get("PHYSICAL_ADDRESS", "")
UNSUB = os.environ.get("UNSUBSCRIBE_URL", "")
PAYMENT_LINK = os.environ.get("STRIPE_PAYMENT_LINK", "")

FOOTER = "\n\n{sender}\n{addr}\nUnsubscribe: {unsub}\n"


def variant_a(p: dict, det: dict, lab: dict, sender: str) -> tuple[str, str]:
    a = p.get("attributes", {})
    radio = "Bluetooth or Wi-Fi" if a.get("intentional_radiator") else "wireless"
    ship = p.get("ship_month_label", "your stated ship month")
    subject = f"no FCC grant on file for {p.get('product','your product')}?"
    body = f"""Hi {p.get('first_name','there')},

You're shipping {p.get('product')} in {ship} and I couldn't find an equipment authorization under {p.get('company')} in the FCC database. If your contract manufacturer filed under their own grantee code, ignore this email.

If they didn't, here's what I read off your campaign page:

{_standards_block(det)}

{lab['name']} covers that in one booking. Rough band is ${det['cost_band'][0]:,} to ${det['cost_band'][1]:,} and about {det['weeks']} weeks. Book late and {ship} slips.

That took about ninety seconds, which tells you how much of this work is mechanical.

Full scope with clause citations, plus three lab quotes requested on your behalf: $19, {PAYMENT_LINK}

Or just reply with your BOM and I'll correct anything I got wrong, free."""
    return subject, body + FOOTER.format(sender=sender, addr=PHYSICAL_ADDRESS, unsub=UNSUB)


def variant_b(p: dict, det: dict, lab: dict, sender: str, sleeper: str | None) -> tuple[str, str]:
    ship = p.get("ship_month_label", "your ship month")
    subject = f"{ship} ship date and {det['weeks']} weeks of testing"
    body = f"""Hi {p.get('first_name','there')},

{det['weeks']} weeks is a normal lead time at {lab['name']} for the tests {p.get('product')} needs. Counting back from {ship}, that booking should already be placed.

From your campaign page:

{_standards_block(det)}

The one people miss is {sleeper or det['standards_ids'][0]}. Finding out late is what turns a delay into a refund wave.

I'll send the full scope with clause citations and get three labs to quote you directly. $19, {PAYMENT_LINK}

If I've got the device wrong, reply and tell me. I'd rather be corrected than confident."""
    return subject, body + FOOTER.format(sender=sender, addr=PHYSICAL_ADDRESS, unsub=UNSUB)


def _standards_block(det: dict) -> str:
    lines = []
    for s in det["standards"][:5]:
        lines.append(f"  {s['id']} - {s['name']}  [{s['cite']}]")
    return "\n".join(lines)


def first_touch(p: dict, sender: str) -> tuple[str, str]:
    """Email 1 of the sequence. One human, single-ask opener. No scope dump.

    A cold first email that dumps the whole standards list reads like an agent and
    asks for too much at once. The opener notices what they are building, names the
    one thing they will hit (WiFi + battery means certifications), says who reviews
    it (real experts + labs), and makes a single soft ask. The full scoped report
    (variant_a / variant_b) is Email 2, sent once they reply. See docs/PRD.md §7.5.
    """
    product = p.get("product", "your device")
    one_line = p.get("one_line") or "the hardware you're building"
    subject = f"Hardware certifications for {product}"
    body = f"""Hey {p.get('first_name','there')},

How's it going? Saw you're building {product}, {one_line}. The early build looks very cool.

Quick one: have you thought about FCC and UL certification for it yet? Anything with WiFi and a battery has to clear a handful of tests before it can ship, and most hardware founders find out how involved that is pretty late.

That's what we built Compl.AI for. You tell us what you're making, and we come back with the exact certifications you need and what they cost, reviewed and signed off by hardware compliance experts who help you get there with the right labs.

Worth me putting together a quick certification scope for {product}?

Best,
{sender}
Compl.AI"""
    return subject, body


def render(p: dict, det: dict, lab: dict, variant: str, sender: str, sleeper=None):
    # Sequence: 'first_touch' is Email 1 (single ask). 'A'/'B' carry the full
    # scope and are the reply/follow-up once the prospect bites.
    if variant == "first_touch":
        return first_touch(p, sender)
    if variant == "A":
        return variant_a(p, det, lab, sender)
    return variant_b(p, det, lab, sender, sleeper)


def deliver(to: str, subject: str, body: str, send: bool) -> str:
    """Write to outbox always. Send only when explicitly told to.

    House-style guard runs first: em dashes and AI tells never leave the building.
    assert_clean humanizes mechanical punctuation and hard-fails on rhetoric a human
    must rewrite (docs/STYLE.md). Same discipline as report.py refusing 'certified'.
    """
    subject = style.assert_clean(subject, where="subject")
    body = style.assert_clean(body, where="body")
    safe = to.replace("@", "_at_").replace("/", "_")
    (OUTBOX / f"{safe}.txt").write_text(f"To: {to}\nSubject: {subject}\n\n{body}")
    if not send:
        return "drafted"

    host = os.environ["SMTP_HOST"]
    msg = MIMEText(body, "plain", "utf-8")
    msg["Subject"] = subject
    msg["From"] = FROM
    msg["To"] = to
    with smtplib.SMTP(host, int(os.environ.get("SMTP_PORT", "587"))) as s:
        s.starttls()
        s.login(os.environ["SMTP_USER"], os.environ["SMTP_PASS"])
        s.send_message(msg)
    return "sent"
