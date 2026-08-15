# Product spec, two tiers

Supersedes the single-report model in earlier docs. Decided Aug 15 afternoon.

## Shape

    outbound  ->  context  ->  FREE REPORT  ->  [Enhance]  ->  expert loop  ->  signed report
                                   |                              |
                            perception panel              accepted or not
                            (Terac, blocking)             (Terac, best effort)

**Free tier.** The agent accepts any job it believes its own models plus the
rules table can handle. Generates the scoping report immediately. Ships same day.
Contains standards with clause citations, a recommended lab, cost band, weeks.
The expert signature block is present and empty, with the upgrade link where the
signature would go.

**Enhance, paid.** Optional. Posts the job plus the finished draft to Terac.
On acceptance, the expert reviews, marks it up, and the signed version ships.
Live SLA three to four days.

## Why the free tier does not cannibalise the paid one

One sentence, and it needs to survive a judge asking it in these words:

> The free report tells you what you need. The paid one is signed by a named
> human and comes with three lab quotes already requested on your behalf. You
> are not buying more information, you are buying accountability and legwork.

**Wording discipline.** Reviewed and signed by a named expert. Never certified.
Certification authority is the lab's and always will be. A judge with industry
background will catch the wrong word, and the whole trust argument rests on us
being precise about who holds what authority.

## Why the draft goes out before the expert accepts

Earlier plan gated generation on acceptance. Inverted, deliberately.

Generation costs one model call. Expert time is the scarce input. An expert
asked to "review a hardware compliance case" is being offered hours of unknown
work. An expert shown a finished draft is being offered twenty minutes. The draft
is the recruitment asset, not just the deliverable, and attaching it should raise
acceptance rather than waste effort.

## Graceful degradation, and put it in the demo

If no expert accepts inside the window, the agent tells the client the truth:

> We could not find an expert for this right now. This is our verdict and here is
> what it is worth. Finding a reviewer may take longer, and we will keep looking.

Refund the enhance fee automatically at the deadline. This is the same honesty
the founder was denied when a consultancy said they do not work with companies
that size, and it closes the demo back to the cold open. Show this screen on
purpose rather than hiding it.

## Terac is used in two places, and only one of them is guaranteed

| Use | Tier | Fills | Purpose |
| --- | --- | --- | --- |
| Perception panel, attribute labels | Free, blocking | Minutes, general population | Eligibility floor. Produces the measurable before and after. |
| Expert review | Paid, best effort | Hours to days, may not fill | Upside. Produces the signed report and the re-engagement hook. |

**Do not drop the perception panel.** If the expert pool never fills, it is the
only thing standing between this project and a weak reading of the mandatory
criteria. It is the floor. The expert loop is the ceiling.

## Re-engagement, the highest value use of the expert output

An expert comment is a re-open hook no cold sequence can imitate. Quote the
expert verbatim. Never write "an expert reviewed your report" when you can paste
what they actually said. Copy is in `04-OUTREACH-COPY.md` section 7.

This puts Terac inside the go-to-market loop rather than only in delivery, which
is what the team wanted from the start.

## Payment

Stripe Payment Link. No auth, no gated app, no paywall build. The enhanced report
emails on payment confirmation. Delivery on email and in the platform record.

## Demo simulation policy

The approval step after expert acceptance may be simulated, because the live SLA
does not fit inside the event.

It must be labelled on screen. `SIMULATED_APPROVAL=1` sets
`approval_simulated: true` in state and the dashboard renders a visible badge.
An unlabelled simulation that a judge uncovers costs the track. A labelled one
costs nothing and reads as discipline.

Never simulate: a Stripe charge, a reply from a stranger, a panel result.
