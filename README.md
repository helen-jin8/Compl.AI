# GTM agent system, autonomous hardware compliance firm

Built for the Zero Human Company Hackathon, Terac, San Francisco, Aug 15 2026.

Read `CLAUDE.md` first, then `docs/` in numeric order. The design arguments live
in `docs/02-DECISIONS.md` and the Terac integration in
`docs/05-TERAC-INTEGRATION.md`.

## What it does

Finds pre-launch hardware companies about to miss a certification deadline,
verifies the device's attributes with a human panel, scopes the standards they
need, and emails them the answer with a payment link attached.

The outbound message and the product are the same artifact. That is the design.

## The accuracy chain

| Layer | Question | Who answers |
| --- | --- | --- |
| Perception | Battery, radio, ship date, child audience | Terac general population panel |
| Rules | Which standards those attributes trigger | `data/standards.yaml`, deterministic |
| Authority | Is the scope right, what does it cost | Accredited lab quote requests |

Only perception needs a human, and reading a product page is not expert work.
The company has no employees. It hires perception by the task through an API.

## Quickstart

    pip install -r requirements.txt
    cp .env.example .env        # fill in keys
    python -m src.pipeline run --mock     # end to end on the seed row, fake panel

Then, for real:

    python -m src.pipeline source --limit 60
    python -m src.pipeline qualify
    python -m src.pipeline terac-label
    python -m src.pipeline analyze --terac-async
    python -m src.pipeline outreach            # add --send when you mean it
    python -m src.pipeline terac-comprehend
    open dashboard/index.html

## Safety rails, deliberately annoying

- `--send` is required to send email. Default writes to `data/outbox/`.
- `MAX_SENDS=20`. A cold domain sending volume lands in spam and the demo shows
  zero replies.
- `--mock` fakes the Terac panel and stamps `panel_source: mock` into state so it
  cannot reach a slide unnoticed.
- `OFFLINE=1` replays every external call from `data/cache/`. Warm the cache
  before demoing and the stage run stops depending on venue wifi.

## Known gaps, do not discover these at 6:30 PM

- **Terac payload shapes are unconfirmed.** `src/terac.py` has the adapter and a
  TODO. Fix the field names from the sponsor docs or the booth, then everything
  downstream works unchanged.
- **apps.fcc.gov returned 403 to a datacenter IP** during development. It will
  probably work from a laptop with a browser user agent. `src/fcc.py` falls back
  to fccid.io and then to `checked: false`, and never guesses.
- **No Apify actor id is hardcoded.** Pick one at runtime with the Apify MCP
  search. If it stalls, hand-fill `data/seed_prospects.json` and move on.
- **`data/standards.yaml` is a scoping aid, not a legal determination.** The
  binding scope comes from the lab quote. Every generated document says so.

## What is deliberately not here

No Stripe API integration. Use a Payment Link, per the guidebook. No reply
handling agent. No compliance web app. Reasons in `docs/02-DECISIONS.md`.
