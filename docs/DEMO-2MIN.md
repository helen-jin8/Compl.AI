# Demo, 2 minutes

Full talk track is `03-DEMO-SCRIPT.md`. This is the 2-minute version. Have open:
the website (running locally), the prospect list (`GTM_AGENT/data/prospects.csv`),
the learning dashboard (`GTM_AGENT/dashboard/index.html`), the Ravi email, and the
rejection email.

| Time | Beat | Say / show |
| --- | --- | --- |
| 0:00 | **Cold open** | Rejection email on screen. "I asked a compliance consultant to certify a small device. They don't work with companies that size. So we built the firm that serves them, with no employees." |
| 0:20 | **Real pipeline** | Open `prospects.csv`. 38 US pre-launch hardware companies, 33 tier-A, sourced live from Kickstarter plus Bay Area accelerators. Every row is verifiable. Click a campaign URL or a founder's LinkedIn. |
| 0:35 | **Outreach that isn't a scope dump** | Show the Ravi email. "First touch is one human question. We notice what they're building and ask if certification is on their radar. No wall of text." |
| 0:50 | **The website (live)** | Run the walkthrough below. Type Kitiki in, watch it generate the scope, land on the report with a human sign-off. This is the deliverable Ravi gets when he replies. |
| 1:30 | **It learns + who signs it** | Dashboard learning section: a bandit picks the email hook per segment, ~50% lift over random on our eval. Then: "A human enters once, on the deliverable. If Terac's pool doesn't fill, we fall back to real accredited labs, see `experts.csv`, e.g. Atlas Compliance in San Jose." |
| 1:50 | **Close** | "We scope and route. We never certify, that's the lab's authority. Nineteen dollars, N charges, produced with no person in the path." |

## Website walkthrough (~40s)

1. **Landing** -> click **Start**.
2. **Form** (`/start`): Name `Ravi`, email `ravi@kitiki.computer`, and paste this
   description:
   > Kitiki, a 13.3-inch open-source e-ink Linux laptop with WiFi, a lithium
   > battery, and a USB-C charger. Shipping January 2027.
   Click **Continue**.
3. **Questions** (`/questions`): it asks the follow-ups it needs (battery type,
   wireless module). Answer one or two out loud to show it reacts, then **Generate**.
4. **Generating** (`/generating`): let the stages stream. Read one aloud:
   "parsing 3,412 pages of UL, FCC and IEC standards... queuing a human reviewer."
5. **Report** (`/report`): walk the tabs fast.
   - **Standards**: the actual certs for Kitiki (FCC Part 15, UN 38.3, UL 62368-1),
     each with a clause and a cost.
   - **Labs**: the recommended accredited lab.
   - **Expert**: the human sign-off badge. "This is the one place a person is in
     the loop."

Land it: "Same scope the email promised, generated live, signed by a real
compliance expert. That is the whole product in forty seconds."

## Notes

- The site is the demo centerpiece; the `prospects.csv` and dashboard are the
  proof behind it. If you're tight on time, cut the dashboard beat, not the site.
- Keep Kitiki as the through-line: the email, the site, and Ravi (a real person on
  the team) are the same story.

## Do not

- Claim we certify anything. We scope and route.
- Claim more sends than made.
- Show the learning eval as if it were real replies. It's a firewalled test, say so.
- Small copy fix for the team: `ui/src/api/complianceApi.ts` has an en dash in
  `eta: '2-3 hours'`. Straight hyphen keeps it consistent with `docs/STYLE.md`.
