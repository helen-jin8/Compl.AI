# Demo — 2 minutes

The full talk track is `03-DEMO-SCRIPT.md`. This is the 2-minute version. Have
these open: the dashboard (`GTM_AGENT/dashboard/index.html`), the prospect list
(`GTM_AGENT/data/prospects.csv`), the outreach example
(`GTM_AGENT/templates/outreach_template.md`), and the rejection email.

| Time | Beat | Say / show |
| --- | --- | --- |
| 0:00 | **Cold open** | Rejection email on screen: "I asked a compliance consultant to certify a small device. They don't work with companies that size. So we built the firm that serves them — no employees." |
| 0:20 | **Real pipeline** | Open `prospects.csv`. 38 US pre-launch hardware companies, 33 tier-A, sourced live from Kickstarter + Bay/Berkeley accelerators. Every row is verifiable — click a campaign URL or a founder's LinkedIn. |
| 0:40 | **The email is the product** | Open `outreach_template.md` → the Beni example. "The prospecting agent and the compliance agent are the same agent, so the cold email *is* a piece of the deliverable — the actual standards for their device, clause-cited. Ninety seconds of work. That's why it converts and isn't spam." |
| 1:00 | **It learns** | Dashboard → Learning loop. "Two hooks; a bandit sends both and shifts to whatever earns replies per segment. ~50% lift over sending at random on our eval. The reward is a real reply." |
| 1:20 | **Who signs it** | Dashboard → Terac expert review (draft → signed, badge if simulated). "Human input enters once, on the deliverable. If Terac's pool doesn't fill, we fall back to real accredited labs — `experts.csv`, e.g. Atlas Compliance in San Jose. That's the Authority layer; the lab's accreditation is what's on the line, never us." |
| 1:40 | **Revenue + close** | Show the Stripe link / number. "Nineteen dollars, N charges, deliverable produced with no person in the path. We scope and route. We never certify — that's the lab's. That precision is the whole trust argument." |

**Two lines to land:** "The outbound email and the product are the same artifact."
· "The company has no employees. It buys human judgment by the task."

**If asked, reference:** ICP + qualification → `PRD.md §3`; why not spam →
`PRD.md §11` + the caveat in every email; how it learns → `LEARNING-LOOP.md`;
the standards mapping is a readable table → `GTM_AGENT/data/standards.yaml`.

**Do not:** claim we certify anything · claim more sends than made · show the
learning eval as if it were real replies (it's a firewalled test — say so).
