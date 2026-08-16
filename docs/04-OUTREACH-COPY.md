# Copy

## 1. Rejection bait, send yourself, T+0

Goal is one written rejection for the opening slide. Send four so one lands.

Targets: boutique hardware compliance consultancies, not labs. Labs will just
send you a quote, which is useful but is not a rejection. Search
`"hardware compliance consulting" small business` and
`"regulatory compliance consultant" consumer electronics startup`, and include
hardwarecompliance.com and Noetic since they are the named competitors.

Send from a personal address, not a company one. Keep it small and unimpressive
on purpose. That is the point.

> Subject: help scoping certification for a small device
>
> Hi,
>
> I'm building a small connected device on my own, Bluetooth plus a lithium pack,
> and I'm trying to work out what certification I need before I can sell it in
> the US. First hardware product, no compliance background.
>
> Rough volume is a few hundred units to start. Is this something you'd help with,
> and what does engagement usually cost?
>
> Thanks,
> Gaurang

Do not dress it up. If they say no, screenshot it. If they quote you $12k, that
is nearly as good, and it goes on the same slide.

## 2. Outbound, generation 1

Twenty sends, ten per variant. Plain text only. No images, no tracking pixel, no
HTML. A tracking pixel on a cold send to a technical audience reads badly and
hurts deliverability.

Every send ends with a physical address and an unsubscribe line. This is a legal
requirement under CAN-SPAM and it is also the answer when a judge asks whether
this is spam.

### Variant A, the absence hook

> Subject: no FCC grant on file for {product}?
>
> Hi {first_name},
>
> You're shipping {product} in {ship_month} and I couldn't find an equipment
> authorization under {company} in the FCC database. If your contract
> manufacturer filed under their own grantee code, ignore this email.
>
> If they didn't: the {radio_type} radio puts you under 47 CFR Part 15 Subpart C,
> and the {battery_type} pack adds {battery_standard} plus UN 38.3 before a
> carrier will fly it. {lab_name} covers all of it in one booking, roughly
> {cost_band} and {weeks} weeks. Book late and {ship_month} slips.
>
> I scoped that from your campaign page in about ninety seconds, which tells you
> how much of this work is mechanical.
>
> Full scope with clause citations, plus three lab quotes requested on your
> behalf: {payment_link}, $19.
>
> Or just reply with your BOM and I'll correct anything I got wrong, free.
>
> {sender_name}
> {physical_address}
> Unsubscribe: {unsubscribe_link}

### Variant B, the cost hook

> Subject: {ship_month} ship date and {weeks} weeks of testing
>
> Hi {first_name},
>
> {weeks} weeks is the current lead time at {lab_name} for the tests {product}
> needs. Counting back from {ship_month}, you needed to book by roughly
> {book_by_date}.
>
> The list, from your campaign page: {standards_list}. The one people miss is
> {sleeper_standard}, and finding out late is what turns a delay into a refund
> wave.
>
> I'll send you the full scope with clause citations and get three labs to quote
> you directly. $19, {payment_link}.
>
> If I've got the device wrong, reply and tell me. I'd rather be corrected than
> confident.
>
> {sender_name}
> {physical_address}
> Unsubscribe: {unsubscribe_link}

### Why these work

Both open with a fact about the recipient that they cannot dismiss, and both
give away the answer before asking for money. The last line of each invites
correction, which converts skeptics into repliers. A reply is worth more than a
click today because it is the unfakeable demo asset.

## 3. Terac study 1

Target the general population, per Terac's guidance. Do not filter for hardware
knowledge. You are testing whether the message lands, not whether the standards
are right.

Prompt shown to panelists:

> Below are two cold emails from a company that helps small hardware startups get
> their products certified before they can legally be sold. Read both.

Questions:

1. Which email would you be more likely to reply to? (A / B / neither)
2. Which email reads more like spam? (A / B / neither)
3. How much would you trust the sender to know what they're talking about?
   (1 to 5, per email)
4. How clear was it what the sender wants you to do? (1 to 5, per email)
5. One sentence: what would make you delete this without reading it?

Question 5 is the one that produces the rewrite. Open text beats scores for
telling the agent what to change.

## 4. Terac study 2

Same five questions. Pair is the study 1 winner against the agent's rewrite of
the loser. The delta in questions 1, 3 and 4 is your measured before and after.

Chart it as generation 1 versus generation 2. That chart is the slide that
satisfies the mandatory Terac criteria, so make sure it renders.

## 5. Optional study 3, report quality

> Below is a compliance scoping report produced for a small hardware company.
> You are not expected to understand the technical standards.

1. Could you tell what the company is supposed to do next? (1 to 5)
2. Would you trust this document enough to pay $19 for it? (yes / no)
3. What is confusing or missing?

## 6. Inbound post, fifteen minutes, widens the funnel

Post once, do not spam. r/hardware, r/AskElectronics, Hacker News, or a hardware
founder Discord.

> I built an agent that reads a Kickstarter hardware campaign and tells you which
> FCC and UL certifications you need, which lab covers them in one booking, and
> what it costs. It checks the FCC authorization database to see if you've
> already filed.
>
> It's free to run against your campaign, reply or DM me a link. I built it
> because I emailed a compliance consultant about a small device and got told
> they don't work with companies my size.
>
> Caveat up front: it scopes and routes, it does not certify. Certification comes
> from an accredited lab and always will.

The caveat is not optional. It is what stops this being irresponsible, and on a
technical forum it is what makes the post credible.

## 7. Re-engagement, after an expert comments

The highest value message in the system. An expert's actual sentence is a
re-open hook no cold sequence can imitate, and it is why the expert loop belongs
in go-to-market and not only in delivery.

Rule: quote the expert verbatim. Never write "an expert reviewed your report"
when you can paste what they said. The specificity is the entire effect.

> Subject: {expert_first} flagged something in your {component}
>
> Hi {first_name},
>
> You asked for a compliance scope on {product} a while back and never came back,
> which is fine.
>
> Since then {expert_first}, who spent {years} years on FCC submissions, went
> through it. Their note:
>
> "{expert_quote}"
>
> If that's right it's a first-pass failure, and a re-test books as a new job at
> {lab_name}.
>
> Reviewed report with their name on it: {payment_link}
>
> If you already solved it, say so and I'll close the file.

Variants by prior state:

- **Never replied.** Use as written above.
- **Replied then went quiet.** Open with "picking this back up" instead of the
  never-came-back line.
- **Already paid for enhance.** No link. Deliver the signed report and ask
  whether they want the three lab quotes sent now.

## 8. No expert found, the honest degradation

Send this rather than going silent. It is the same honesty the founder was denied
by a consultancy this morning, and it is demoed on purpose.

> Subject: no reviewer found for {product}, refunding
>
> Hi {first_name},
>
> We couldn't find a qualified reviewer for {product} inside the window we
> promised, so your enhance fee is refunded, nothing owed.
>
> The scoping report stands on its own and I've attached it again. Here is what
> it is worth: it is the output of a rules table you can read, sourced from
> published standards with the clause cited on every line. It is not a signature
> and we have never claimed it is.
>
> We'll keep looking for a reviewer. If one picks it up I'll send their notes,
> free.
