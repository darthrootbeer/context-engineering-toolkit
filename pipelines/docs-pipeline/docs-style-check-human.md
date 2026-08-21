---
name: docs-style-check-human
description: Final prose polish — detect and rewrite AI writing patterns using the Write Like a Human style guide. Catches em dashes, banned words, filler phrases, uniform sentence length, bold-label lists, and other AI tells. Edits docs in place. Run last, after diataxis and general style passes.
argument-hint: [folder-or-file]
allowed-tools: [Read, Write, Edit, Glob, Bash]
---

# docs-style-check-human

Final editing pass on one or more docs to detect and rewrite AI writing patterns. Applies every rule from the "Write Like a Human" style guide. Edits docs in place. Produces an audit report summarizing findings and fixes.

This is the last style pass in the pipeline. Run it after `/docs-style-check-structure` (structure) and `/docs-style-check-voice` (The Product conventions) so it operates on settled prose.

## Arguments

The user provided: $ARGUMENTS

This should be a path to a **folder** (all `.md` files inside) or a single `.md` **file**.

**Required.** If missing, stop: `"Please provide a folder or file path: /docs-style-check-human [path]"`

---

## Constants

```
STYLE_GUIDE=~/projects/example-docs-repo/_extras/style-guides/write-like-a-human/style-guide_write-like-a-human.md
```

---

## Steps

### 1. Validate input

- Check that $ARGUMENTS is provided. If not, stop with usage message.
- Resolve whether the path is a directory or single file:
  - **Directory**: Glob all `.md` files inside it. Abort if zero found.
  - **File**: Use that single file. Abort if it doesn't exist.
- Store the full file list.

### 2. Read the style guide

Read `STYLE_GUIDE` using the Read tool. Internalize the full guide — every section matters. Pay particular attention to:

- The **Quick reference: editing pass order** at the bottom (section headings 1-15 — this is the check order)
- The **hard-ban word list** (section 3)
- The **phrases to cut** (section 4)

### 3. Read all docs

Read each doc in full using the Read tool. Read in parallel where possible.

### 4. Check each doc using the editing pass order

For each doc, work through the checks in the exact order specified by the style guide's Quick Reference. This order is deliberate — earlier passes change structure that later passes depend on.

#### Pass 1: Bold-label lists

**What to find:** Bullet lists where every item starts with `**Label:** description`.

**Fix:** Convert to plain prose or varied lists. Options:
- Remove the bold labels entirely if the list reads fine without them
- Convert to a table if the labels genuinely serve as lookup keys
- Keep bold on the first word only if it's a proper noun or API field name

**Exception:** Definition-style lists where the bold term IS the content being defined (e.g., a glossary) can stay. The pattern is only a problem when it's decorative structure.

#### Pass 2: Em dashes

**What to find:** Every `—` (em dash) in the doc.

**Fix:** Apply the replacement table:

| Em dash is doing this | Replace with |
|---|---|
| Connecting two independent clauses | Period. Start a new sentence. |
| Connecting two closely related clauses | Semicolon |
| Setting off parenthetical info (not for emphasis) | Commas or parentheses |
| Introducing a list or explanation | Colon |
| Adding emphasis to a final clause or aside | Keep it, but only once per paragraph |

**Limits:** Maximum one em dash per paragraph. Maximum one per sentence. When in doubt, replace with a period.

#### Pass 3: Hard-ban words

**What to find:** Any word from the hard-ban list. Scan the full doc.

**Banned — vague buzzwords:** delve, tapestry, landscape (metaphorical), realm, paradigm, transformative, groundbreaking, revolutionary, unprecedented, game-changer, testament, pioneering, trailblazing, cutting-edge, next-gen, next-generation, future-proof, state-of-the-art, leading-edge, disruptive, visionary, ever-evolving, multifaceted

**Banned — empty intensifiers:** crucial, pivotal, vital, seamless, robust, scalable, comprehensive, optimal, frictionless, effortless, adaptive, dynamic, immersive, intuitive, proactive, predictive, insightful, mission-critical, compelling, straightforward

**Banned — business-speak:** leverage, synergy, foster, empower, streamline, optimize, holistic, align, showcase, garner, underscore, accentuate, elevate, democratize, accelerate, data-driven, results-driven, agile, plug-and-play, turnkey, AI-powered, hyper-personalized, cloud-native, harness, navigate (metaphorical), bolstered

**Banned — prose padding:** meticulously, vibrant, intricate, nestled, breathtaking, stunning, renowned, versatile, unparalleled, nuanced, grappling, endeavour

**Fix:** Rewrite the sentence with a specific, concrete alternative. Use the replacement table in the style guide. Don't just swap one word — the sentence structure often needs to change to sound natural.

**Flag words (not banned, but note if frequent):** utilize (→ use), commence (→ start), various (→ several/some), in-depth (→ detailed), typically (→ usually/often), certainly, additionally, furthermore

#### Pass 4: Opening phrases to cut

**What to find:** Paragraphs that start with any of these:

"Let me explain...", "In essence...", "Indeed...", "Interestingly...", "It's worth noting that...", "It should be noted that...", "It's important to note...", "It's important to consider...", "Let's explore...", "Let's break this down...", "When it comes to...", "One key aspect is...", "A significant factor is...", "This approach offers...", "From a [X] perspective...", "At its core...", "At the end of the day...", "The reality is...", "The truth is...", "In today's ever-evolving...", "Here is a summary...", "Below is..."

**Fix:** Delete the phrase and start with the actual sentence.

#### Pass 5: Sycophantic openers

**What to find:** "Great question!", "That's an excellent point!", "Absolutely!", "Certainly!", "Sure!"

**Fix:** Delete. (Rare in docs, more common in conversational content.)

#### Pass 6: Heading inflation

**What to find:** H2s and H3s that don't warrant a section break. Every few paragraphs getting a heading when the content flows naturally.

**Fix:** Remove unnecessary headings and let paragraphs flow. Only flag — don't auto-remove headings, as this changes doc structure.

#### Pass 7: Transition word density

**What to find:** moreover, furthermore, additionally, consequently, as a result, in contrast, therefore, in addition, to summarize, to conclude, in conclusion, it is worth noting, this means that, in other words, to put it simply, essentially, fundamentally

**Fix:** If any transition word appears more than once in 3 consecutive paragraphs, rewrite to remove the extras. Let sentence structure carry the reader.

#### Pass 8: Sentence length uniformity

**What to find:** Runs of 4+ sentences that are all roughly the same length (18-27 words each).

**Fix:** Vary deliberately. Break one sentence short for emphasis. Combine two short ones if they flow together. The goal is natural rhythm, not mechanical regularity.

#### Pass 9: Rule of threes

**What to find:** Groups of three adjectives, three examples, or three bullets that feel reflexive rather than content-driven.

**Fix:** If two things are enough, use two. If four are needed, use four. The number should come from the content.

#### Pass 10: Contrast framing and short-sentence stacking

**What to find:**
- "It's not X. It's Y." / "Not a rule, but a principle."
- Fragments stacked for drama: "You're not just building. You're creating."

**Fix:** Flatten. "This is a design philosophy, not just a feature." One sentence, not three.

#### Pass 11: Synonym cycling

**What to find:** The same concept referred to by a different synonym in each paragraph (the "researcher → scientist → academic → scholar" pattern).

**Fix:** Use pronouns. Repeat the same noun when it's clear. Don't force variation.

#### Pass 12: Bullet overuse

**What to find:** Ideas in bullet lists that would read better as prose.

**Fix:** Convert to prose when the items flow naturally as a sentence or short paragraph. Keep lists for items that genuinely don't flow.

#### Pass 13: Adjective audit

**What to find:** significant, crucial, essential, effective, optimal, comprehensive, important, powerful, key, major, fundamental, core

**Fix:** Ask what specifically makes it [adjective]. Replace with the specific answer. "This is a significant part of the system" → "This determines whether the payment captures or fails."

#### Pass 14: Passive voice

**What to find:** Passive constructions where the actor is known.

**Fix:** Flip to active voice. "The request is validated by the server" → "The server validates the request."

**Exception:** Passive is fine when the actor is genuinely unknown or unimportant.

#### Pass 15: Hedging

**What to find:** Unnecessary "typically," "might," "can," "some," "often," "generally" that make statements tentative without adding meaning.

**Fix:** Commit to the statement. "This can typically help in some cases where users might need to configure..." → "This helps when users need to configure..."

**Exception:** Genuine caveats where the hedging is factually necessary should stay.

### 5. Apply fixes

For each doc, apply all fixes using the Edit tool. Work through one doc at a time. Re-read the file between major edit batches to avoid stale content references.

**Judgment call:** This pass requires editorial judgment more than the other two passes. Not every AI pattern needs fixing — some sentences are fine even if they technically match a pattern. The goal is prose that reads naturally, not mechanical rule application.

Track every edit: `{filename}: {what changed}`.

### 6. Write audit report

Write to the `_process/style-audit/` directory relative to the project's output root. Resolve the output root by walking up from the input path until you find a directory containing `_process/` (or create `_process/style-audit/` as a sibling of the docs folder).

**Filename:** `style-audit-human-{folder-name}.md` (where `{folder-name}` is the input folder's basename, e.g. `caper-refunds`)

For a single file input, use the filename without extension instead of folder name.

**Format:**

```markdown
# Human Style Audit: {folder-name}

**Date:** {YYYY-MM-DD}
**Style guide:** Write Like a Human
**Docs audited:** {N}
**Scope:** {path relative to project root}

---

## Summary

{1-2 sentences: overall AI pattern presence, most common issue category}

Fixes applied: {N}
Flags for review: {N}

Most common fixes:
  - {Category}: {count}
  - {Category}: {count}
  - {Category}: {count}

---

## Fixes applied

### {filename}

- **[Pass N: Category]** {Description of what was changed and why}
- **[Pass N: Category]** {Description of what was changed and why}

### {filename}

- **[Pass N: Category]** {Description}

---

## Flags (manual review needed)

### {filename}

- ⚠ **[Pass N: Category]** {Description of issue}

---

## Passed — no issues

- {filename}
```

Tagging each change with the pass number and category makes it easy to see which patterns were most common.

### 7. Display summary

```
Human style audit complete.

Docs audited: {N}
Fixes applied: {N}
Flags for review: {N}

Most common fixes:
  - {Category}: {count}
  - {Category}: {count}
  - {Category}: {count}

Audit report: {path}/_process/style-audit/style-audit-human-{folder-name}.md
```

---

## Error Handling

| Situation | Behavior |
|---|---|
| No argument provided | Stop: show usage message |
| Path doesn't exist | Stop: "File not found: [path]" or "Directory not found: [path]" |
| No `.md` files in directory | Stop: "No markdown files found in: [path]" |
| Style guide not found | Stop: "Style guide not found at [path]. Check STYLE_GUIDE constant." |

---

## Notes

- This skill edits docs **in place**. The audit report records what was changed.
- Run this **last** in the style pipeline — after `/docs-style-check-structure` and `/docs-style-check-voice`.
- This is the most judgment-heavy pass. Not every pattern match needs fixing. Read the sentence in context before changing it.
- The 15-pass order from the style guide's Quick Reference is deliberate. Earlier passes change structure (bold-label lists, heading inflation) that affects what later passes see (sentence uniformity, bullet overuse).
- Don't mention this style guide, its rules, or the fact that you're following it in any output. The edits should look like natural editorial choices.
- The hard-ban word list is the most mechanical check — a word either appears or it doesn't. Start there for quick wins.
- Sentence length uniformity (pass 8) requires reading multiple sentences together. Don't check individual sentences in isolation.
