# Outbound template, the email carries the deliverable

The cold email carries the actual scope for that specific device, with clause
citations, a recommended lab, cost band, and weeks. A founder can read a piece of
the real work before they pay for anything, and a reply corrects it. See
docs/PRD.md §4. Plain text only, no tracking pixel, CAN-SPAM footer on every send.
The variant is chosen by the learning loop (docs/LEARNING-LOOP.md). Every send
passes the house-style guard (docs/STYLE.md): no em dashes, no AI tells.

## Template (absence hook, fill the {braces})

```
Subject: no FCC grant on file for {product}?

Hi {first_name},

You're shipping {product} in {ship_month} and I couldn't find an equipment
authorization under {company} in the FCC database. If your contract manufacturer
filed under their own grantee code, ignore this email.

If they didn't, here's what I read off your campaign page:

{standards_block}   # one line per standard: ID: name  [clause cite]

{lab} covers that in one booking. Rough band is ${cost_low} to ${cost_high} and
about {weeks} weeks. Book late and {ship_month} slips.

That scope took about ninety seconds, which is how much of this work is mechanical.
For the full version, reviewed and signed by a named compliance professional with
three lab quotes requested for you: {payment_link}

You can also edit your device details and regenerate the whole scope here:
{compl_ai_link}

Or just reply with your BOM and I'll fix anything I got wrong, free.

{sender}
{physical_address}
Unsubscribe: {unsubscribe_url}
```

Keep the caveat in every send: not finding an FCC grant is a signal, not a
guarantee, because a grant can sit under a contract manufacturer's grantee code.

---

## Worked example, Beni by Mondo Robotics (Palo Alto, CA)

Real lead from `data/prospects.csv` (source: kickstarter). Funded $2.87M, 4,578
backers, verifiable at
https://www.kickstarter.com/projects/mondorobotics/beni-all-terrain-camera-robot

```
Subject: no FCC grant on file for Beni?

Hi there,

You're shipping Beni in September 2026 and I couldn't find an equipment
authorization under Mondo Robotics in the FCC database. If your contract
manufacturer filed under their own grantee code, ignore this email.

If they didn't, here's what I read off your campaign page:

  47 CFR Part 15 Subpart C: the auto-following radio      [15.247 / 15.249]
  FCC KDB 447498: RF exposure evaluation                  [KDB 447498 D01]
  UN 38.3: lithium battery transport testing              [UN 38.3]
  UL 2054 / IEC 62133-2: battery pack safety              [IEC 62133-2:2017]
  UL 62368-1: product electrical safety                   [UL 62368-1]

F2 Labs covers the FCC and the safety testing in one booking. Rough band is
$18,000 to $35,000 and about 12 weeks. A robot that ships with a lithium pack
can't go by air freight until UN 38.3 is done, so book early or September slips.

That scope took about ninety seconds, which is how much of this work is mechanical.
For the full version, reviewed and signed by a named compliance professional with
three lab quotes requested for you: {payment_link}

You can also edit your device details and regenerate the whole scope here:
{compl_ai_link}

Or just reply with your BOM and I'll fix anything I got wrong, free.

Gaurang Sumra
655 Bryant St, San Francisco, CA 94107
Unsubscribe: {unsubscribe_url}
```

Why Beni is a strong lead: funded and dated (a hard trigger), a radio and a lithium
pack (the full standards story, including the UN 38.3 catch), a Palo Alto team with
no compliance function, and nothing on file with the FCC. The recommended lab
(F2 Labs) is a real accredited lab from `data/experts.csv`.
