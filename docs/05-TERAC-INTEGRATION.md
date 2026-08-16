# Terac integration

Terac use is mandatory. This document is the design, and it is deliberately not
a bolt-on.

## The requirement, as written

> Use real human input you collect during the hackathon to make your project
> measurably better, whether that's product feedback, user testing, expert
> judgment, or labeled data. Build something real people can respond to. An app
> people can use, react to, label, rate, rank, or compare. Call the Terac API/MCP
> to bring the people. Turn that input into a better project. Show a clear before
> and after. Please launch studies geared towards the General Population.

Two things follow. Labeled data is explicitly in scope. General population is
explicitly preferred.

## The insight

The team's blocker was "Terac has no hardware compliance experts." That assumed
the human had to supply judgment. Split the accuracy chain and the assumption
falls apart.

| Layer | Question | Who answers | Cost |
| --- | --- | --- | --- |
| Perception | Does this device have a rechargeable battery, a radio, a stated ship date, a child audience | Terac general population panel | Cents per label |
| Rules | Which standards do those attributes trigger | `data/standards.yaml`, deterministic | Zero |
| Authority | Is the scope right, what does it cost, how long | Accredited lab quote requests | Zero, labs want the inbound |

Only perception needs a human, and reading a product page is not expert work.
The expertise lives in the rules table and in the lab's accreditation. We never
needed a compliance expert. We needed eyes.

This is also why the company can claim zero employees honestly. It hires
perception by the task through an API, applies deterministic rules, and takes
authority from accredited bodies. Nobody is on payroll and nobody needs to be.

## Use 1, primary. Attribute labeling, in production, per prospect

**Where it sits.** Between the sourcer and the analyst. Blocking. The analyst
does not run until labels return.

**Task shown to the panel.** The campaign page content, plus:

1. Does this product contain a rechargeable battery? (yes / no / cannot tell)
2. Does it connect wirelessly to a phone, computer or the internet?
   (yes / no / cannot tell)
3. What month and year does the page say it will ship? (free text)
4. Is this product intended for children under 12? (yes / no / cannot tell)
5. Does it plug into a wall outlet? (yes / no / cannot tell)

All five are answerable by anyone who can read. None require domain knowledge.

**Resolution.** Panel majority overrides the model. Disagreement between panel
and model gets flagged in `state.json` and shown on the dashboard, because
disagreements are the demo.

**Why it is load-bearing.** Wrong attributes produce a wrong standards list,
which produces a wrong report and a wrong lab. Remove Terac and output accuracy
drops. That is the criteria's bar, met structurally rather than cosmetically.

**Measured before and after.** Model-only attribute accuracy against panel
consensus, and the count of standards added or removed downstream. The single
best artifact is one prospect where the panel caught a battery the model missed
and the report gained UN 38.3. Put that on the slide.

## Use 2, secondary. Delivery comprehension gate

**Where it sits.** Between the analyst and the outreach agent. Blocking on the
paid report, advisory on the cold email.

**Task shown to the panel.** The generated report, plus:

1. What is this company supposed to do next? (free text)
2. How confident are you that you could act on this? (1 to 5)
3. What is confusing or missing? (free text)

**Pass condition.** A majority of panelists name the correct next action. Below
that, the agent rewrites and re-tests.

**Why general population is right here.** A first-time hardware founder is
functionally a non-expert reading a compliance document. The panel is a better
proxy for the customer than an expert would be. An expert would rate the document
on correctness, which is the layer the lab already covers.

**Measured before and after.** Comprehension pass rate, generation 1 versus the
rewrite.

## Use 3, bonus only if time remains. Outbound message ranking

Two cold email variants, general population, which would you reply to, which
reads like spam, trust and clarity on a five point scale, and one open text
question on what would make you delete it. The open text drives the rewrite.

This is a marketing optimisation rather than a production loop, so it ranks
third. Copy is in `04-OUTREACH-COPY.md`.

## What to log for the judges

`data/state.json` carries, per prospect:

    terac_task_id
    model_attributes
    panel_attributes
    panel_agreement            float, 0 to 1
    attributes_corrected       list of field names the panel overrode
    standards_before           list, from model attributes alone
    standards_after            list, after panel correction
    comprehension_pass         bool
    comprehension_round        int

The dashboard renders `standards_before` against `standards_after`. That
comparison is the mandatory before and after, and it is a product metric rather
than a marketing one.

## Failure plan

If the Terac panel is slow, run the pipeline with `--terac-async` so the analyst
proceeds on model attributes and patches the record when labels land. Never let a
slow panel block the send window. Log which prospects were sent pre-label and say
so on stage if asked. Being straight about it costs nothing and hiding it costs
the room.
