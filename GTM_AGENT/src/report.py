"""Report renderer. Task 1 in docs/07-BUILD-SPEC.md.

Wording discipline enforced here and asserted at the bottom: we never say we
certify. Reviewed and signed by a named expert. Certification authority is the
lab's and the whole trust argument depends on being precise about that.
"""
from __future__ import annotations

from datetime import datetime

EMPTY_BLOCK = """---

## Expert review

Not yet reviewed.

This report is the output of a published rules table applied to the attributes of
your device. Every standard below cites its clause so you can verify it without
trusting us.

For a version reviewed and signed by a named compliance professional, plus three
lab quotes requested on your behalf: {payment_link}

If no reviewer picks it up inside 48 hours, that fee is refunded automatically.
"""

PENDING_BLOCK = """---

## Expert review

**Accepted by {expert_name}{cred}** on {accepted_at}. Review in progress,
typically three to four days.{sim}
"""

SIGNED_BLOCK = """---

## Expert review

**Reviewed and signed by {expert_name}{cred}** on {signed_at}.{sim}

{comments}

Note on scope: this is a professional review of the scoping work. It is not a
certification. Certification is issued by an accredited NRTL for product safety
and an FCC-recognised TCB for equipment authorization, and no consultant can
issue it.
"""


def _signature_block(p: dict, payment_link: str) -> str:
    state = p.get("expert_state", "empty")
    cred = f", {p['expert_credential']}" if p.get("expert_credential") else ""
    sim = (
        "\n\n> Approval simulated for demo. Live SLA is three to four days."
        if p.get("approval_simulated")
        else ""
    )
    if state == "pending":
        return PENDING_BLOCK.format(
            expert_name=p.get("expert_name", "a reviewer"),
            cred=cred,
            accepted_at=p.get("expert_accepted_at", "today"),
            sim=sim,
        )
    if state == "signed":
        comments = "\n".join(f"- {c}" for c in p.get("expert_comments", [])) or "- No changes."
        return SIGNED_BLOCK.format(
            expert_name=p.get("expert_name", "a reviewer"),
            cred=cred,
            signed_at=p.get("expert_signed_at", "today"),
            comments=comments,
            sim=sim,
        )
    return EMPTY_BLOCK.format(payment_link=payment_link)


def render(p: dict, payment_link: str = "") -> str:
    det = p.get("determination") or {}
    lab = p.get("lab") or {}
    attrs = p.get("attributes") or {}
    panel = p.get("panel_attributes") or {}

    lines = [
        f"# Compliance scope: {p.get('product','your device')}",
        f"Prepared for {p.get('company','you')} on {datetime.now():%d %B %Y}.",
        "",
        "## What we understand this device to be",
        "",
        p.get("one_line", "") or "See attributes below.",
        "",
    ]

    for k, v in attrs.items():
        if v is not True:
            continue
        src = "human panel" if k in panel else "automated read"
        ev = (p.get("evidence") or {}).get(k, "")
        lines.append(f"- **{k.replace('_',' ')}** ({src}){f': {ev}' if ev else ''}")
    if p.get("attributes_corrected"):
        lines += [
            "",
            f"A human panel corrected our automated read on: "
            f"{', '.join(p['attributes_corrected'])}. "
            "Those corrections changed the standards list below.",
        ]

    lines += ["", "## Standards that apply", ""]
    for s in det.get("standards", []):
        lines.append(f"### {s['id']} — {s['name']}")
        lines.append(f"Clause: `{s['cite']}`")
        lines.append(f"Applies because: {s['because']}")
        if s.get("note"):
            lines.append(f"Note: {s['note']}")
        lines.append("")

    if det.get("out_of_scope"):
        lines += [
            "## Outside our scope",
            "",
            "We do not scope the following and you should engage a specialist:",
            "",
            *[f"- {x}" for x in det["out_of_scope"]],
            "",
        ]

    band = det.get("cost_band", [0, 0])
    lines += [
        "## Where to take it",
        "",
        f"**{lab.get('name','See lab directory')}** holds "
        f"{', '.join(lab.get('accreditations', []))} and covers "
        f"{', '.join(lab.get('covers', []))}"
        f"{' in a single booking' if lab.get('one_stop') else ''}.",
        "",
        f"Order of magnitude: ${band[0]:,} to ${band[1]:,}. "
        f"Roughly {det.get('weeks','?')} weeks once booked. "
        "These are scoping numbers for planning, not a price. The quote is the number.",
        "",
        "## What to do this week",
        "",
        "1. Ask your cell vendor for their existing certificates before paying to repeat that testing.",
        "2. Confirm whether your contract manufacturer has already filed with the FCC under their own grantee code.",
        f"3. Request a quote from {lab.get('name','an accredited lab')} against the standards listed above.",
        "",
        "## Limits of this document",
        "",
        det.get("disclaimer", ""),
        "",
        "Absence of an FCC grant under your company name is a strong signal that "
        "authorization has not been filed. It is not proof, because a grant can sit "
        "under a contract manufacturer's grantee code.",
        "",
        _signature_block(p, payment_link),
    ]

    out = "\n".join(lines)
    lowered = out.lower()
    for bad in ("we certify", "our certification", "certified by us"):
        assert bad not in lowered, f"report claims certification: {bad}"
    return out


def degradation_message(p: dict) -> str:
    """The honest 'no reviewer found' note. docs/04-OUTREACH-COPY.md section 8.

    Sent rather than going silent. It is the same honesty the founder was denied
    by a consultancy that would not work with a company that size, and it is
    demoed on purpose. Refund is automatic at the deadline.
    """
    product = p.get("product", "your device")
    first = p.get("first_name") or "there"
    lab = (p.get("lab") or {}).get("name", "an accredited lab")
    return (
        f"Subject: no reviewer found for {product}, refunding\n\n"
        f"Hi {first},\n\n"
        f"We couldn't find a qualified reviewer for {product} inside the window "
        "we promised, so your enhance fee is refunded, nothing owed.\n\n"
        "The scoping report stands on its own and I've attached it again. Here is "
        "what it is worth: it is the output of a rules table you can read, sourced "
        "from published standards with the clause cited on every line. It is not a "
        "signature and we have never claimed it is.\n\n"
        "We'll keep looking for a reviewer. If one picks it up I'll send their "
        f"notes, free. If you want to move now, {lab} will quote the scope above "
        "directly."
    )
