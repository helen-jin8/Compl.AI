# Demo script

Judging runs 7:00 to 8:00 PM with eleven judges. Assume they circulate and you
deliver this repeatedly, not once from a stage. Optimize for a three minute
version that survives interruption.

## Cold open, 20 seconds

Put the rejection email on screen before you say anything.

> I emailed a compliance consultant this morning asking what it takes to certify
> a small hardware product. This is what came back. They don't work with
> companies that size.
>
> There are thousands of funded hardware campaigns with ship dates and no
> certification plan, and the people who could help them have all moved upmarket.
> So we built the firm that serves them, and it has no employees.

If the rejection has not landed by 7:00, use the cheapest quote you received
instead and say "twelve thousand dollars to be told which forms to fill in."

## The loop, 90 seconds, run it live

One fresh prospect, sourcing through drafted email, on stage.

Narrate the four beats as they happen:

1. **Sourced.** Funded campaign, ship date inside six months.
2. **Qualified.** No grant under this company in the FCC authorization database.
   Device has a radio and a lithium pack. Tier A.
3. **Scoped.** These standards, this clause, this lab, this cost band, this many
   weeks.
4. **Contacted.** Here is the email it wrote, and here is the payment link inside
   it.

The line to land on beat 3:

> The outbound email and the product are the same artifact. We don't pitch the
> service, we do a piece of the work and send it. That is why this isn't spam.

If wifi is bad, run `--offline` and say you are replaying from cache. Judges
respect the engineering decision more than they penalize the replay.

## The accuracy chain and the human review, 60 seconds

This is where the mandatory human-input criteria lives, so give it real time.

> The obvious question with a compliance product is who checks the work. We split
> it into three layers and asked which one actually needs a person.
>
> Perception. Does it have a battery, a radio, when does it ship. The model reads
> the page, and every attribute it uses quotes the exact line it came from, so you
> can check the read instead of trusting it. Rules. Which standards those trigger.
> That's a deterministic table in the repo, you can read it. Authority. Is the
> scope right and what does it cost. That comes from accredited labs, and from a
> named expert who reviews and signs the finished report.
>
> So the engine runs with no human in the loop. The one place a person adds
> something a model can't is signing the deliverable, and that's the paid tier.
> Here's a report before review, and here's the same report after a named reviewer
> marked it up and signed it. That draft-to-signed diff is the human input, and
> it's what turns a good scope into one a founder will pay to stand behind.

Show the expert-review section on the dashboard: draft `report_v1` → signed
`report_v2`, the reviewer's name, and their verbatim notes. If the approval was
simulated for the event, the row carries a visible "approval simulated" badge —
point at it. A labelled simulation reads as discipline; an unlabelled one a judge
uncovers costs the track.

If no reviewer accepted in time, show the honest degradation screen: we refund
automatically and say so. That is the same honesty the founder was denied by the
consultancy, and it closes the demo back to the cold open.

## The learning loop, 30 seconds

Open the dashboard's learning section.

> The email is the product, so we optimize the email the way you'd optimize a
> product. There are two framings, one opens on the missing FCC grant, one on the
> testing weeks against the ship date. We don't guess which works. A bandit sends
> both, watches which one earns replies for each kind of device, and shifts the
> next batch toward the winner. Battery devices with a hard carrier deadline reply
> to the cost framing; the others to the absence framing. It learned that from
> replies, not from us.
>
> On our own eval that's about a fifty percent lift in reply rate over sending the
> two at random. And the reward is a real reply from a real founder, the one
> signal in this whole funnel we refuse to fake.

The per-segment table shows the winning hook and the reply rate it's converging
on. Reply rate is the north-star number.

## Revenue, 30 seconds

Show the Stripe dashboard, not a screenshot of it.

> Nineteen dollars, N charges, and the agent produced the deliverable for each
> one. Small number. It is a number that moved without a person in the path.

If revenue is zero at 7:00, do not hide it. Say:

> Zero charges so far, N replies. The funnel is real and the conversion window
> for a four hour cold email test is what it is. Here's what came back.

Showing three thoughtful replies from actual hardware founders beats a fake
charge, and the panel includes people who will spot a fake charge.

## The hard question, 25 seconds, volunteer it before they ask

> The obvious hole is who signs off. Nobody on our side, and that's deliberate.
> No consultant can certify a product. That authority sits with accredited labs.
> So instead of hiring an expert, the agent sends its scope to three of them as
> quote requests. Their quotes either confirm the scope or correct it, and
> they're free because labs want the work. Our competitors keep a human in the
> loop. We don't need one, because the verification is structural.

Volunteering this is worth more than answering it. It signals you found the hole
yourself.

## Q and A prep

**Is this spam?**
Twenty sends. Every one contains a specific technical answer about their device.
Unsubscribe line, physical address, no tracking pixel. Every email invites
correction. Spam does not ask to be told it is wrong.

**What if the FCC lookup is wrong?**
It can be. A grant can sit under a contract manufacturer's grantee code rather
than the brand. That is why the subject line is a question and the email says to
ignore it if their CM filed. Absence is a strong signal, not a proof.

**What stops UL or Intertek from doing this?**
Nothing, and they should. They will not, because their economics require a
minimum engagement size and this segment is below it. That is the same reason the
rejection email exists.

**Is this a business after today?**
The scoping layer is a wedge, not the business. The business is being the routing
layer between thousands of small hardware companies and a dozen labs that want
qualified inbound. Labs pay for that. Same structure works for SOC 2 next.

**How much of this is the model versus your code?**
Point at `data/standards.yaml` and `data/labs.yaml`. The domain mapping is
deterministic. The model classifies the device and writes the email. Say that
plainly, because the judges will find out anyway and honesty here reads as
engineering maturity.

**What breaks at scale?**
Deliverability, and lab quote turnaround. Both are solvable and neither is
solvable in five hours.

## Do not

- Do not claim you certify anything.
- Do not claim more sends than you made.
- Do not show a slide with an unlabeled y-axis to a Google DeepMind PM.
- Do not run out of time before the human-review before/after. It is the mandatory
  human-input criteria and a project that skips it is not eligible.
