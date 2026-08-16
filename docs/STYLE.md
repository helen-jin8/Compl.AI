# Writing style — sound like a person

Every message the company sends (cold email, follow-up, re-engagement) has to read
like a person wrote it. Our reader is a technical founder; that is exactly the
reader who deletes anything that smells like a chatbot. This is enforced in code:
`GTM_AGENT/src/style.py` humanizes punctuation and hard-fails on the tells below
before `outreach.deliver` will send. Same discipline as refusing the word
"certified".

## Banned (the code will block these)

- **Em dashes and en dashes** (`—`, `–`). Use a comma, a period, or parentheses.
  Auto-replaced by `humanize()`.
- **Smart quotes / ellipsis characters.** Straight quotes and `...`. Auto-replaced.
- **The antithesis flourish:** "it's not X, it's Y", "isn't just X", "not just X
  but Y", "more than just", "not only X but also Y". State the point once.
- **AI buzzwords:** leverage, seamless, robust, elevate, unlock, supercharge,
  game-changer, revolutionize, cutting-edge, delve, realm, tapestry, testament,
  synergy, paradigm, holistic, streamline, empower, plethora, myriad, embark,
  effortless, unparalleled.
- **Filler openers:** "I hope this email finds you well", "in today's fast-paced
  world", "let's dive in", "at the end of the day".
- **Emoji.**

## Discouraged (won't block, but avoid)

- **Rule of three.** "Faster, cheaper, and safer." Pick the one that matters.
- **Vague "from X to Y"** ("from prototypes to production"). Say the specific thing.
- **Over-signposting** ("Firstly... Secondly... Finally").
- **Hedge stacking** ("I just wanted to quickly reach out to maybe see if...").
- **Over-bolding** and exclamation marks.

## Do instead

- Short, plain sentences. One idea per line. Aim for a grade-5 reading level.
- Say the specific, checkable thing (a clause number, a dollar band, a date).
- Write it the way you would send it to a colleague on Slack, then tighten.
- Keep the real caveats. "Not finding an FCC grant does not prove much on its own"
  is a substantive point stated plainly, not the banned rhetorical snap. Phrase
  such caveats as plain statements, not "X, not Y" constructions.

## For engineers

- `style.humanize(text)` applies the mechanical fixes.
- `style.lint(text)` returns remaining tells to rewrite.
- `style.assert_clean(text, where)` humanizes then raises on any surviving tell.
  It is called for every subject and body in `outreach.deliver`. Add it to any new
  send path (SMS, LinkedIn, notifications) so the guarantee holds everywhere.

Grounded in how people actually spot AI writing (em-dash density, the rule of
three, the "not only... but also" tic, buzzword clusters) and in plain-language
cold-email practice (short sentences, no jargon, plain text, under ~200 words).
