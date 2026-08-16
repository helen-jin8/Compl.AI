# Outbound, a two-step sequence

The first email is a single human ask, not a scope dump. Dumping the whole
standards list in a cold email reads like an agent and asks for too much at once.
So Email 1 notices what they are building and makes one soft ask. Email 2 carries
the real deliverable (the scoped standards list), sent once they reply. See
docs/PRD.md §7.5. Plain text, no tracking pixel, CAN-SPAM footer on cold sends.
Every send passes the house-style guard (docs/STYLE.md): no em dashes, no AI tells.

Code: `src/outreach.py` -> `first_touch()` (Email 1), `variant_a`/`variant_b` (Email 2).

## Email 1, first touch (single ask)

```
Subject: Hardware certifications for {product}

Hey {first_name},

How's it going? Saw you're building {product}, {one_line}. The early build looks very cool.

Quick one: have you thought about FCC and UL certification for it yet? Anything
with WiFi and a battery has to clear a handful of tests before it can ship, and
most hardware founders find out how involved that is pretty late.

That's what we built Compl.AI for. You tell us what you're making, and we come back
with the exact certifications you need and what they cost, reviewed and signed off
by hardware compliance experts who help you get there with the right labs.

Worth me putting together a quick certification scope for {product}?

Best,
{sender}
Compl.AI
```

### Worked example, Kitiki (Ravi)

```
Subject: Hardware certifications for Kitiki

Hey Ravi,

How's it going? Saw you're building Kitiki, the open-source e-ink laptop. The early build looks very cool.

Quick one: have you thought about FCC and UL certification for it yet? Anything
with WiFi and a battery has to clear a handful of tests before it can ship, and
most hardware founders find out how involved that is pretty late.

That's what we built Compl.AI for. You tell us what you're making, and we come back
with the exact certifications you need and what they cost, reviewed and signed off
by hardware compliance experts who help you get there with the right labs.

Worth me putting together a quick certification scope for Kitiki?

Best,
Gaurang
Compl.AI
```

## Email 2, the scope (send on reply)

This is the deliverable: the actual standards for their device, clause-cited, with
a lab and a cost band. Fill the {braces} from the scoped record.

```
Subject: {product}, the certification scope

Hi {first_name},

Here's the scope I promised. Based on {product} having WiFi and a lithium battery
(tell me if that's wrong):

{standards_block}   # one line per standard: ID: name  [clause cite]

{lab} covers that in one booking. Rough band is ${cost_low} to ${cost_high} and
about {weeks} weeks. Book late and {ship_month} slips.

One shortcut: if your WiFi module is already certified, you can file under FCC
modular approval and skip the radio testing, usually the most expensive line.

The full version is reviewed and signed by a named compliance professional, with
three lab quotes requested for you: {payment_link}. You can also edit your details
and regenerate the scope here: {compl_ai_link}

If I got the device wrong, reply and I'll fix the whole list, free.

{sender}
{physical_address}
Unsubscribe: {unsubscribe_url}
```

Keep the caveat: not finding an FCC grant is a signal, not a guarantee, because a
grant can sit under a contract manufacturer's grantee code.

### Worked example (Email 2), Beni by Mondo Robotics

Real lead from `data/prospects.csv`. Verifiable at
https://www.kickstarter.com/projects/mondorobotics/beni-all-terrain-camera-robot

```
  47 CFR Part 15 Subpart C: the auto-following radio      [15.247 / 15.249]
  FCC KDB 447498: RF exposure evaluation                  [KDB 447498 D01]
  UN 38.3: lithium battery transport testing              [UN 38.3]
  UL 2054 / IEC 62133-2: battery pack safety              [IEC 62133-2:2017]
  UL 62368-1: product electrical safety                   [UL 62368-1]
```

A robot that ships with a lithium pack can't go by air freight until UN 38.3 is
done. Recommended lab (F2 Labs) and reviewers come from `data/experts.csv`.
