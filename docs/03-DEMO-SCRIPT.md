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

## The Terac layer, 60 seconds

This is the mandatory criteria and it is also the best idea in the project, so
give it real time. Show the standards-before against standards-after comparison
for one prospect the panel corrected.

> The obvious question with a compliance product is who checks the work. So we
> split it into three layers and looked at which one actually needs a person.
>
> Perception. Does this thing have a battery, does it have a radio, when does it
> ship. Rules. Which standards those attributes trigger. Authority. Is the scope
> right and what does it cost.
>
> Rules are a lookup table. It's in the repo, it's deterministic, you can read it.
> Authority comes from accredited labs, and no consultant has that authority
> anyway. Perception is the only layer that needs a human, and reading a product
> page is not expert work.
>
> So every prospect goes to a Terac panel before the analysis runs. Five
> questions, anyone can answer them. On this one the panel spotted a rechargeable
> pack our model missed. That added UN 38.3, which is the transport standard, and
> without it no carrier will fly the product. The model would have sent this
> founder a report that let them miss their ship date.
>
> The company has no employees. It hires perception by the task through an API.

If the panel caught nothing, say so and show the agreement rate instead. A high
agreement rate is still a measurement, and claiming a catch you did not get is
the one thing that will lose you the room.

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
- Do not run out of time before the Terac chart. It is the mandatory criteria and
  a project that skips it is not eligible.
