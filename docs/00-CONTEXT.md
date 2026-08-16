# Context log

Everything below is carried over from the Cowork session so a fresh Claude Code
instance starts with full context.

## Sources

1. Granola note "Zero-Human Company Hackathon - Initial Scoping", Aug 15 2026,
   8:30 AM PDT, captured by Gaurang Sumra. Full transcript reviewed.
2. Zero Human Company Hackathon guidebook, pasted by the user.
3. Two CSVs in `~/Downloads` reviewed and ruled out of scope.

## Event logistics

Humanmade, 655 Bryant St, San Francisco. Aug 15 2026, 8:30 AM to 9:00 PM.
Hacking opened 10:45 AM. **Submissions lock 6:45 PM.** Judging 7:00 to 8:00 PM.
Winners 8:20 PM.

## Rules, verbatim intent

Build an agent, or several working in unison, that run a company autonomously.
Named surfaces: building the product, marketing and outbound, selling to
customers, handling payments, legal and compliance, making hard decisions.

All projects must use the Terac MCP. Criteria as written:

> Use real human input you collect during the hackathon to make your project
> measurably better, whether that's product feedback, user testing, expert
> judgment, or labeled data. Build something real people can respond to. Call the
> Terac API/MCP to bring the people. We handle recruiting and incentives. Turn
> that input into a better project. Show a clear before and after. Please launch
> studies geared towards the General Population, so you get the fastest and best
> results.

Note for the team: this does not require domain experts. The instruction to aim
at the general population is explicit. See D8 in `02-DECISIONS.md`.

## Tracks in priority order for this team

| Track | Prize | Our position |
| --- | --- | --- |
| Best Overall Agent-Run Company | $2,500 | Primary. Requires revenue earned today via Stripe. |
| Best Overall Project | $2,500 | Secondary, same build. |
| Best use of Render | $500 / $300 / $100 credits | Same judging panel as agent-run company. Cheap second track. |
| Best use of Pioneer | $500 | GLiNER2 for attribute extraction. Cheap third track. |
| Best use of Band | $500 | Only if a teammate is free. Coordination must happen in Band or it does not count. |
| Best use of Linq | $1,500 | Highest tool prize but cold iMessage to strangers is a bad fit. Skip unless time is left over. |
| Best use of Superserve | $1,000 | Skip unless the scraper needs a sandbox anyway. |
| Best use of Replay | $1,000 | Only if the dashboard becomes a real app worth QA-ing. |

## Judging panel

Best Overall Project: Ilia Bolgov and Roman Yanushevskyi (Touchmark, YC S26),
Om Buddhdev and Shreshth Sharma (Olam Labs, YC S26), Shubh Mittal (xAI).

Best Overall Agent-Run Company and Render: Sarthak Ahuja and Arhan Singhal
(Brekfuz), **Tosh Rayadhurgam, Head of Advanced AI at Stripe**, **Shriram
Bagavathyappan, Group PM at Google DeepMind**, Erin Meryl McGurk (Egoist
Machines, YC S26), Harry Kapoor.

Design implication. Tosh will look at the payment path. Shriram will probe
product reasoning and the ICP logic. The YC founders will ask whether this is a
business after today.

## Mentor feedback from the scoping session

- Two existing players (hardwarecompliance.com, Noetic YC 2026) are validation,
  not a threat. Our angle differs from both.
- Open the pitch with the rejection email. It is the emotionally legible hook.
- Do not tackle the whole value chain. Physical lab testing is a later phase, and
  saying so out loud is itself part of the pitch.
- Build the outbound loop: ICP list, enrich via Apify and Clay MCP and LinkedIn,
  reach out by email or LinkedIn, and on response close async. The audience is
  technical and does not need a pitch call, which is unusual for consulting.
- After winning a client, build the delivery workflow, watch turnaround time,
  deliver, then collect via Stripe.
- Closing the loop, in the mentor's words: "whatever client you were able to win
  and deliver well to, that goes into the loop and the go-to-market agent learns
  from it. This is working, this is not, do more of what works, scrap the rest.
  Which is how we do go-to-market anyway."
- The team's own read, and the reason this idea won over the alternatives:
  "being able to demonstrate that the business can run itself is going to be more
  interesting and more novel than whatever solution or product we do."

## Ideas considered and dropped

Meal planning and nutrition with a dietitian in the loop. Dropped for being
crowded and for a forced-feeling go-to-market. An agentic creative agency with
human-ranked ad variants. Dropped, but note it is structurally similar to how we
now use Terac. An autonomous research firm. Dropped, already being done by a
Berkeley-funded startup.

## Adjacent context on the founder

Runs contract engineering and enterprise AI agent deployment. Also automating his
own job search with an agent that sources roles, tailors a resume, runs an ATS
check, and keeps a manual submission gate. That manual gate is a good analogue
for the accountability gate in this product and can be referenced on stage.
