---
title: "Style Guide: Write Like a Human"
purpose: >-
  Applied by AI agents editing or generating prose content in this repository.
  Follow all rules during writing, not as a separate editing pass.
scope: >-
  All prose content: documentation, guides, concept notes, spec docs,
  narrative descriptions. Does not apply to code, YAML, or structured data.
instructions: >-
  Read this guide before editing or generating prose. Apply all rules inline
  as you write. When reviewing existing content, use the Quick Reference
  checklist (bottom of this file) as your editing pass order. Do not mention
  this style guide, its rules, or the fact that you are following it in your
  output.
research_basis:
  - "Reddit r/ChatGPT"
  - "Wikipedia: Signs of AI Writing"
  - "Max Planck Institute (2025) — word frequency study"
  - "Northeastern University (2025) — human writing fingerprints"
  - "Johns Hopkins University (2024) — AI writing fingerprints"
  - "University College Cork (2025) — AI stylistic clustering"
  - "Search Engine Journal — AI writing fingerprints"
  - "Microsoft Style Guide"
  - "Mashable, Substack (Ruben Hassid, enkla), humanizeai.now"
last_updated: "2026-03-03"
---

# Style Guide: Write Like a Human

AI-generated prose follows predictable patterns in formatting, punctuation, word choice, structure, and tone. These patterns are individually minor but collectively unmistakable. This guide addresses every documented category.

---

## 1. Formatting

Formatting tells are the most visually obvious AI signals. A reader can spot them before reading a single sentence.

### Bold-label + colon lists

The single strongest AI formatting tell. AI produces bullet lists where every item starts with a **bolded label** followed by a colon and description. Humans almost never write lists this way unprompted.

```text
AI PATTERN:
- **Scalability:** The system handles increasing loads efficiently.
- **Security:** All data is encrypted at rest and in transit.
- **Performance:** Response times remain under 200ms.

HUMAN ALTERNATIVE:
- The system handles increasing loads without degradation.
- All data is encrypted at rest and in transit.
- Response times stay under 200ms.
```

If a list genuinely needs labels, use a table or a definition list. Don't bold the first word of every bullet.

### Heading inflation

AI creates H2s and H3s every few paragraphs, even when the content doesn't warrant a section break. Let paragraphs breathe. Not every topic shift needs a heading.

### Colon-heavy titles

"Topic: A Complete Guide" or "Authentication: Getting Started" correlates strongly with AI. Use simpler titles. "How authentication works" or just "Authentication."

### Emoji decoration

AI chatbots decorate headings and bullets with emoji. No emoji in technical writing.

### Over-structured output

AI defaults to structured output (headers, bullets, numbered lists) even when prose would be better. A question that warrants a two-sentence answer doesn't need an H2, three bullets, and a summary sentence. Match the format to the content.

---

## 2. Punctuation

### Em dashes: ration, don't ban

Em dashes are overused by AI at roughly 2x the rate of human writers. They are not wrong; they are a signal when frequent.

**Limits:**
- Maximum one em dash per paragraph.
- Maximum one em dash per sentence.
- Use only when no other punctuation achieves the same effect.

**Replacement table:**

| The em dash is doing this | Replace with |
|---|---|
| Connecting two independent clauses | Period. Start a new sentence. |
| Connecting two closely related clauses | Semicolon |
| Setting off parenthetical info (not for emphasis) | Commas or parentheses |
| Introducing a list or explanation | Colon |
| Adding emphasis to a final clause or aside | Keep it, but only once per paragraph |

When in doubt, replace with a period (new sentence) or a comma (continue sentence). This resolves ~90% of cases.

```text
BEFORE: The system handles routing automatically — it never interrupts the player — and recovers silently.
AFTER:  The system handles routing automatically. It never interrupts the player and recovers silently.

BEFORE: There are three modes — play, pause, and edit.
AFTER:  There are three modes: play, pause, and edit.
```

### Semicolons: less mechanical

AI uses semicolons to connect simple phrases where "and" or "but" would read better. Human semicolons feel like a deliberate choice; AI semicolons feel equidistant and formulaic.

Use "and," "but," "so" most of the time. Reserve semicolons for when two closely related clauses genuinely benefit from the tighter connection.

### Colons: not just list launchers

AI uses colons almost exclusively to introduce lists. Humans also use them for dramatic effect, emphasis, or explanation.

```text
AI PATTERN:   Here are the key factors:
HUMAN:        There was only one problem: nobody had tested it.
```

Vary colon usage. Sometimes flow into a list without announcing it.

### Parentheses: use more of them

AI underuses parentheses. Humans use parentheses for personal asides, self-deprecation, secondary context, and humor. AI prefers em dashes for the same job.

```text
AI:    The migration took longer than expected — about three weeks.
HUMAN: The migration took longer than expected (about three weeks).
HUMAN: The migration took longer than expected. (Don't ask.)
```

Use parentheses for personality. They signal a human aside.

---

## 3. Hard-ban word list

These words appear in AI output at far higher frequency than in human writing. Do not use them. If a sentence seems to require one, rewrite the sentence with a specific, concrete alternative.

### Vague buzzwords

delve, tapestry, landscape (metaphorical), realm, paradigm, transformative, groundbreaking, revolutionary, unprecedented, game-changer, testament, pioneering, trailblazing, cutting-edge, next-gen, next-generation, future-proof, state-of-the-art, leading-edge, disruptive, visionary, ever-evolving, multifaceted

### Empty intensifiers

crucial, pivotal, vital, seamless, robust, scalable, comprehensive, optimal, frictionless, effortless, adaptive, dynamic, immersive, intuitive, proactive, predictive, insightful, mission-critical, compelling, straightforward

### Business-speak

leverage, synergy, foster, empower, streamline, optimize, holistic, align, showcase, garner, underscore, accentuate, elevate, democratize, accelerate, data-driven, results-driven, agile, plug-and-play, turnkey, AI-powered, hyper-personalized, cloud-native, harness, navigate (metaphorical), bolstered

### Prose padding

meticulously, vibrant, intricate, nestled, breathtaking, stunning, renowned, versatile, unparalleled, nuanced, grappling, endeavour

### Filler words (not banned, but flag when frequent)

utilize (use "use"), commence (use "start"), various (use "several" or "some"), in-depth (use "detailed"), typically (use "usually" or "often"), certainly, additionally, furthermore

### Replacement table

| Banned | Use instead |
|---|---|
| leverage | use, apply, take advantage of |
| seamless | smooth, uninterrupted, invisible to the user |
| robust | reliable, stable, handles edge cases |
| crucial / pivotal | say why it matters, not that it matters |
| innovative | describe what it actually does differently |
| transformative | say what specifically changes |
| foster | build, grow, create |
| empower | let, allow, give the ability to |
| delve | look at, dig into, explore |
| landscape | be specific: "the current state of X" or "how X works" |
| navigate | deal with, work through, handle |
| harness | use, tap into |
| nuanced | subtle, detailed, complicated |
| utilize | use |
| commence | start, begin |
| straightforward | simple, clear, easy |

---

## 4. Phrases to cut

AI defaults to these as paragraph openers. They add no meaning. Delete them and start with the actual sentence.

### Delete on sight

- "Let me explain..."
- "In essence..."
- "Indeed..."
- "Interestingly..."
- "It's worth noting that..."
- "It should be noted that..."
- "It's important to note..."
- "It's important to consider..."
- "Let's explore..."
- "Let's break this down..."
- "When it comes to..."
- "One key aspect is..."
- "A significant factor is..."
- "This approach offers..."
- "From a [X] perspective..."
- "At its core..."
- "At the end of the day..."
- "The reality is..."
- "The truth is..."
- "In today's ever-evolving..."
- "Here is a summary..."
- "Below is..."

### Sycophantic openers (conversational contexts)

Delete these when they appear at the start of a response or paragraph:
- "Great question!"
- "That's an excellent point!"
- "Absolutely!"
- "Certainly!"
- "Sure!"

Just answer the question.

---

## 5. Sentence and paragraph patterns

### Uniform sentence length

AI sentences cluster around 18-27 words. Human writing swings between 5-word fragments and 40-word constructions. This uniformity is one of the strongest statistical signals of AI authorship.

Vary sentence length deliberately. Short sentences for emphasis. Longer ones when the thought demands it. A single short sentence after a long one creates emphasis. That's the only version of short-sentence stacking that works.

### Rule of threes

AI defaults to groups of three: three adjectives, three examples, three bullet points. Sometimes two things are enough. Sometimes four. The number should come from the content, not from a pattern.

```text
AI:    It's fast, reliable, and scalable.
HUMAN: It's fast and reliable.
```

### Synonym cycling

AI uses a different synonym each time it refers to the same thing. A person becomes "the researcher," then "the scientist," then "the academic," then "the scholar" across four paragraphs. Pronouns exist. Use them. Repeating the same noun is fine when it's clear.

### "And honestly?" pattern

Fake conversational punches. Also: "The result?" / "The best part?" / "The worst part?"

```text
BEFORE: The system is fast. And honestly? That matters.
AFTER:  The system is fast, and that matters.
```

### Short-sentence stacking for drama

Fragments piled up to create emotional weight. Fine once; not as a habit.

```text
BEFORE: You're not just building. You're creating. I see it. Others see it. And that's rare.
AFTER:  You're building something worth noticing.
```

### Contrast framing ("It's not X. It's Y.")

```text
BEFORE: This is not a feature. It's a philosophy. Not a rule, but a principle.
AFTER:  This is a design philosophy, not just a feature.
```

### Paragraph symmetry

AI writes paragraphs of identical length. Human writing is uneven. A one-sentence paragraph is fine. A six-sentence paragraph is fine.

### Bullet list overuse

Not every idea needs a list. Use prose for ideas that flow; use lists for items that don't.

```text
BEFORE: There are several reasons this works:
        - It handles routing
        - It recovers silently
        - It never interrupts the player

AFTER:  It works because it handles routing and recovers silently,
        without ever interrupting the player.
```

### Excessive bold

Bold is for one or two critical terms per section, not every interesting phrase. If everything is emphasized, nothing is.

---

## 6. Structure

### Five-paragraph essay

AI defaults to: introduction paragraph, three body sections, conclusion. This structure appears even when it's not appropriate. Start with the point. Skip the introduction when the reader already has context. End when you're done; don't wrap up with "In conclusion."

### Front-loaded comprehensiveness

AI covers every angle in a single response. Human writers are comfortable being incomplete, opinionated, or focused. Have a point of view. Omit what's not relevant.

### Signposting everything

Announcing structure instead of letting it emerge.

```text
BEFORE: There are three things to know. Firstly... Secondly... The key takeaway is...
AFTER:  [Just write the three things. Number them if needed.]
```

### Generic engagement closers

```text
BEFORE: I'm curious what others think about this approach.
AFTER:  [Delete it. Link to a related doc if follow-up is needed.]
```

---

## 7. Tone and voice

### Be specific, not impressive

AI writing tries to impress. Human writing tries to communicate. Choose the word that is accurate, not the word that sounds authoritative.

### Hedging overload

AI over-qualifies statements with "typically," "might," "can," "some," "often," "generally." This makes everything tentative. Commit to the statement. If there's a genuine caveat, state it directly.

```text
BEFORE: This can typically help in some cases where users might need to configure...
AFTER:  This helps when users need to configure...
```

### Passive voice

AI defaults to passive constructions more than human writers. Use active voice unless the actor is genuinely unknown or unimportant.

```text
BEFORE: The request is validated by the server.
AFTER:  The server validates the request.
```

### State opinions directly

```text
BEFORE: It's worth considering that this approach may have certain advantages.
AFTER:  This approach is faster and easier to debug.
```

### Use contractions in casual contexts

Formal docs (spec docs, system architecture) can be more formal. Guides, concept docs, and narrative writing should use contractions naturally.

### Write for one reader

AI writes for an imagined audience. Write as if explaining to one specific person, the person most likely to read this doc.

### Generic-positive bias

AI replaces specific details with vague praise. "Inventor of the first coupling device" becomes "a revolutionary titan of industry." Be specific. "Fixed a race condition in the token refresh logic" reads more human than "resolved a critical authentication issue."

### Monotonous person

AI sticks to one grammatical person throughout a piece. Human writers naturally shift between "you," "we," and "they" depending on context. Mix naturally when it fits.

---

## 8. Adjective audit

Before using any of these adjectives, ask: what specifically makes this [word]? If you can't answer, replace the adjective with the specific answer.

Flag list: significant, crucial, essential, effective, optimal, comprehensive, important, powerful, key, major, fundamental, core

```text
BEFORE: This is a significant part of the system.
AFTER:  This is what determines whether the player hears music or silence.
```

---

## 9. Transition words

These are not banned. They are overused. Flag any transition word used more than once in three consecutive paragraphs.

Watch list: moreover, furthermore, additionally, consequently, as a result, in contrast, therefore, in addition, to summarize, to conclude, in conclusion, it is worth noting, this means that, in other words, to put it simply, essentially, fundamentally

Let sentence structure carry the reader. If the relationship between ideas is clear, no signpost is needed.

---

## Quick reference: editing pass order

When reviewing existing content, check in this order:

1. **Bold-label lists** — convert `**Label:** text` bullets to plain prose or varied lists
2. **Em dashes** — find every `—`, apply the replacement table
3. **Hard-ban words** — grep for the list; rewrite any sentence containing one
4. **Opening phrases** — find and delete at paragraph starts
5. **Sycophantic openers** — delete "Great question!" and friends
6. **Heading inflation** — remove unnecessary H2s and H3s
7. **Transition word density** — check for moreover/furthermore/additionally pileups
8. **Sentence length uniformity** — vary short and long; break up medium-only runs
9. **Rule of threes** — check if groups of three are genuine or reflexive
10. **Contrast framing and short-sentence stacking** — read for rhythm; flatten
11. **Synonym cycling** — replace unnecessary variation with pronouns or repetition
12. **Bullet overuse** — ask if this should be prose
13. **Adjective audit** — flag the adjective list; replace with specifics
14. **Passive voice** — flip to active where the actor is known
15. **Hedging** — remove unnecessary "typically," "might," "can"

---

## What this guide is not

It is not a ban on formal writing. Formal is fine. Vague is not.

It is not a ban on punctuation variety. Semicolons, colons, dashes are all fine when used correctly and sparingly.

It is not a call for casual or sloppy writing. Specific and direct is the goal, not breezy.

It is not about passing AI detection tools. It is about writing that communicates clearly.
