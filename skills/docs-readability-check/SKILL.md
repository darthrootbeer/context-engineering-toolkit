---
name: docs-readability-check
description: Readability pass on one or more docs. Estimates reading grade level, detects dense sentence patterns (stacking, information pile-up, jargon-then-clause, wall paragraphs), and rewrites them to hit target levels by doc type. Edits in place. Run standalone or after the style pipeline. Never touches tables, code blocks, or callouts.
argument-hint: [folder-or-file]
allowed-tools: [Read, Write, Edit, Glob, Bash]
---

# docs-readability-check

Readability pass on one or more docs. Detects and rewrites the sentence-level patterns that make technical writing feel dense or overwhelming, without changing vocabulary, structure, or voice. Edits in place. Produces an audit report with before/after grade level scores in plain language (e.g. "10th grade", "college level").

Run this standalone on any doc or folder, or as the final step in the style pipeline after `/docs-style-check-human`.

## Arguments

The user provided: $ARGUMENTS

This should be a path to a **folder** (all `.md` files inside) or a single `.md` **file**.

**Required.** If missing, stop: `"Please provide a folder or file path: /docs-readability-check [path]"`

---

## Target reading levels

| Doc type | Target grade level | Prose model |
|---|---|---|
| `overview`, `explanation` | 10th–11th grade | Atlantic / Wired feature article |
| `how-to`, `tutorial` | 11th–12th grade | Good technical blog post |
| `reference` | 12th grade–college freshman | Technical blog / API docs |
| Vault notes (no diataxis_type) | 11th–12th grade | Technical blog post |

**Grade level scale reference:**
- 8th–9th grade: Easy. Most adults breeze through this.
- 10th–11th grade: Standard. Smart general audience.
- 12th grade: Upper secondary. Good for technical blogs.
- College freshman (grade 13): Dense but accessible to practitioners.
- College sophomore+ (grade 14+): Specialist. Rarely appropriate for docs.

The goal is never to dumb down content. It's to remove unnecessary friction — the sentence constructions that make a reader work harder than the ideas require.

---

## Steps

### 1. Validate input

- Check that $ARGUMENTS is provided. If not, stop with usage message.
- Resolve whether the path is a directory or single file:
  - **Directory**: Glob all `.md` files inside it. Abort if zero found.
  - **File**: Use that single file. Abort if it doesn't exist.
- Exclude files in `_archive/`, `_templates/`, `_attachments/` — skip with a note.
- Store the full file list.

### 2. Read all docs

Read each doc in full using the Read tool. Read in parallel where possible.

### 3. For each doc: determine type and target

Check frontmatter for `diataxis_type`. Use the target table above to set the FK target range for this doc. If no type is present, use the vault note target (60–70).

### 4. For each doc: extract prose sample and estimate FK score

#### 4a. Extract prose

Strip the following before scoring — they skew the count and aren't prose:

- YAML frontmatter (between `---` delimiters)
- Fenced code blocks (` ``` ` to ` ``` `)
- Inline code (backtick-wrapped text) — remove the backticks and treat as a placeholder word
- Table rows (lines containing `|`)
- Callout lines (lines starting with `>`)
- Mermaid diagrams
- Wikilinks `[[...]]` — treat as one word
- URLs and file paths — treat as one word each
- Markdown headings (`#`, `##`, etc.) — strip the `#` markers, keep the text
- Bullet/number list markers — keep the text

What remains is the scorable prose. Take a 250-word sample from the **middle third** of the extracted prose (skip the opening paragraph — it's often an intentional hook — and the last paragraph — often a signpost). If the doc has fewer than 100 prose words, score the whole thing.

#### 4b. Estimate reading grade level

Use the Flesch-Kincaid Grade Level formula:

```
FKGL = (0.39 × ASL) + (11.8 × ASW) - 15.59
```

Where:
- **ASL** = Average Sentence Length (total words ÷ total sentences in the sample)
- **ASW** = Average Syllables per Word (total syllables ÷ total words in the sample)

**Counting syllables:** Use this approximation:
1. Count vowel groups (consecutive vowels = 1 syllable)
2. Subtract silent e at end of word
3. Minimum 1 syllable per word
4. Common technical suffixes: `-tion`, `-sion` = 1 syllable each; `-ity`, `-ify` = last two letters = 1 syllable; `-ing`, `-ed` don't add a syllable if they follow a vowel

This approximation is accurate to ±0.5 grade levels for technical prose, which is sufficient for our purposes.

**Counting sentences:** Split on `.`, `!`, `?` followed by a space or end of string. Don't split on abbreviations like `e.g.`, `i.e.`, `etc.`, or file extensions.

**Reporting the score:** Express as a plain-language label, not a raw number. Use this mapping:

| FKGL result | Report as |
|---|---|
| Below 9 | "8th–9th grade — easy, general audience" |
| 9–11 | "10th–11th grade — standard, smart general audience" |
| 11–12 | "11th–12th grade — upper secondary, technical blog" |
| 12–13 | "12th grade — solid technical writing" |
| 13–14 | "college freshman — dense but accessible to practitioners" |
| 14–15 | "college sophomore — specialist territory" |
| Above 15 | "graduate level — too dense for most docs" |

Always pair the label with one plain sentence of context, e.g.: "Reading at college freshman level — on the dense side for an overview doc; the technical vocabulary is driving this more than sentence length."

Record whether the doc is within target, above target (easier than needed — fine), or below target (too dense — needs work).

### 5. For each doc below target: detect problem patterns

Work through the extracted prose sentence by sentence. Identify instances of the four patterns:

#### Pattern 1: Sentence stacking

**What to find:** Three or more consecutive sentences all 25+ words long, with no short sentence (under 12 words) between them.

**Why it's a problem:** Uniform long sentences give the reader no chance to reset. The eye has nowhere to land, and the brain is still processing sentence N when sentence N+1 arrives.

**Fix:** After every 2–3 long sentences, either:
- Split one long sentence at its natural seam (often at a semicolon, a relative clause, or a list) to create a shorter follow-up
- Combine two adjacent short facts into one medium sentence to break the rhythm differently
- Keep the content — just vary the length

**Limit:** Don't create fragments. Target the short sentence at 8–15 words. It should complete a thought, not hang.

#### Pattern 2: Information pile-up

**What to find:** A single sentence containing 4 or more distinct facts, typically recognizable by:
- 3+ items in a comma-separated list within a sentence that also makes other claims
- Multiple colon-introduced clauses in the same sentence
- A sentence that, if read aloud, would require the reader to take more than two breaths

**Why it's a problem:** Working memory can hold ~3–4 items. A sentence that asks the reader to hold 5+ things simultaneously will cause re-reads or information drop.

**Fix:** Find the natural seam — usually the first comma after the second distinct fact — and split there. The second sentence picks up where the first left off. The information is identical; the cognitive load is halved.

**Exception:** Enumerated lists within a sentence are fine if the list IS the point (e.g., "The four artifacts are: game.yaml, agent.md, system.yaml, and data/tables.yaml"). Don't split these — convert to a proper bullet list if they're getting unwieldy.

#### Pattern 3: Jargon-then-clause

**What to find:** A technical term or system-specific noun introduced for the first time and immediately followed by a long qualifying clause (10+ words) before the reader has had a moment to process the term.

Pattern: `[new term] [verb] [long qualifying clause with multiple sub-clauses]`

**Why it's a problem:** The reader is still parsing the term when the clause arrives. By the end of the sentence, they've lost one or the other.

**Fix:** Introduce the term, then stop. Make the qualifying clause its own sentence. The connection is obvious without a conjunction.

```
BEFORE: The master_knowledge_document, which encodes Orbit's understanding of game design patterns across all TTRPG systems and informs how Phase 1 structures its analysis questions, lives in foundation/.

AFTER: The master_knowledge_document lives in foundation/. It encodes Orbit's understanding of game design patterns and shapes how Phase 1 structures its questions.
```

**Exception:** Short qualifying clauses (under 8 words) are fine in the same sentence. Only split when the clause itself is complex.

#### Pattern 4: Wall paragraphs

**What to find:** Paragraphs with 5+ sentences where every sentence is 20+ words and there's no visual variety (no short sentence, no sub-list, no callout that could break it up).

**Why it's a problem:** Dense paragraphs signal to the reader "this is going to be hard." Even before they read it, they're braced. That friction compounds.

**Action:** Flag these — do NOT auto-rewrite. The right fix depends on the content:
- Sometimes the content belongs in a table (if it's enumerable)
- Sometimes one idea should move to its own paragraph
- Sometimes a short summary sentence at the start ("Here's what matters:") lets the paragraph breathe
- Report the paragraph location and let the human decide

#### Pattern 5: Undefined terms

**What to find:** A project-specific noun, acronym, or technical term used in prose that has not been defined or explained earlier in the same doc. This includes:
- Acronyms used before being spelled out (e.g., "The GMA handles routing" with no prior definition)
- System-specific names introduced without a one-phrase description (e.g., "Orbit processes the schema" in a doc where Orbit hasn't been explained)
- Terms that appear to be domain jargon but have no inline definition or link to a glossary/reference doc

**Why it's a problem:** The reader hits an unknown term and has to stop. If they can't figure it out from context, they're lost — or worse, they guess wrong and carry a bad mental model through the rest of the doc.

**Fix:** At first use, add an inline definition in parentheses or a short appositive phrase. For terms that are covered in depth elsewhere, add a link to the relevant doc instead of defining inline.

```
BEFORE: Relay runs the system pack at runtime and resolves all entity lookups.

AFTER: Relay (the runtime game engine) runs the system pack at runtime and resolves all entity lookups.
```

**Exception:** Terms defined in the doc's own frontmatter glossary, or terms that were defined earlier in the same doc, do not need re-definition. Stop at first-use only.

**Limit:** Don't over-define. If a term is widely understood in the target audience (e.g., "API", "YAML", "markdown"), skip it. Apply judgment: would a smart generalist know this term without project context?

#### Pattern 6: Steps buried in prose

**What to find:** A sentence or paragraph that describes a sequence of actions using connective words ("first", "then", "next", "finally", "after that") instead of a numbered list. The giveaway is 3+ sequential actions described inline.

**Why it's a problem:** Inline step sequences are hard to follow and impossible to track. Readers lose their place, can't re-enter a sequence mid-way, and can't skim to find the step they're on.

**Fix:** Convert to a numbered list. The lead-in sentence becomes the list introduction. Each "first/then/next" clause becomes a numbered step starting with an imperative verb.

```
BEFORE: First, create the system pack file, then add the required metadata fields, and finally run the validator to confirm the structure is correct.

AFTER: **To create a system pack:**
1. Create the system pack file.
2. Add the required metadata fields.
3. Run the validator to confirm the structure is correct.
```

**Exception:** Two-step sequences ("Open the file, then save it") can stay inline. Only convert sequences of 3+ actions.

#### Pattern 7: Context-less bullets

**What to find:** A bulleted or numbered list that appears with no introductory sentence — it begins immediately after a heading or blank line, with no prose establishing what the list contains or why it exists.

**Why it's a problem:** The reader arrives at a list without knowing what question it answers. They have to read all the items and reverse-engineer the purpose. This forces more work than a single lead-in sentence would require.

**Fix:** Add a one-sentence introduction before the list. The introduction should complete the thought: "The following [noun] are/do [what]:" or similar. Keep it short — the list carries the content.

```
BEFORE:
## Supported output types

- game.yaml
- agent.md  
- session-log.json

AFTER:
## Supported output types

Orbit can generate three output file types:

- game.yaml
- agent.md
- session-log.json
```

**Exception:** Lists under a heading that is itself a complete lead-in (e.g., a heading that already says "Steps to configure webhooks") don't need a separate intro sentence. Use judgment — don't add a redundant sentence just to satisfy the pattern.

### 6. Apply fixes (Patterns 1–3, 5–7; flag Pattern 4)

For each instance of Patterns 1, 2, 3, 5, 6, and 7, apply the fix using the Edit tool. Work through one doc at a time, top to bottom. Pattern 4 (wall paragraphs) is flag-only — do not auto-fix.

**Judgment rules:**
- Read the sentence in full context before editing. If the length is serving a purpose (parallel structure, enumeration that would be worse split), leave it.
- Don't split a sentence if both halves would be under 8 words — that's choppy, not readable.
- Don't add new information. Don't remove information. Restructure only.
- After each edit, check that the surrounding sentences still flow. A fix that creates a new stacking problem isn't a fix.
- Maximum one restructuring per paragraph unless the paragraph has multiple distinct pattern violations.

Track every edit: `{filename}: {what changed and why}`.

### 7. Re-score after fixes

After applying fixes to a doc, re-estimate the FK score using the same method as Step 4. Compare before and after. If the score improved but is still below target, note it — some docs are dense by necessity (reference docs with many technical terms will always score lower). Don't over-fix to hit the number.

### 8. Write audit report

**Obsidian vault detection:** Walk up from the input path looking for a `.obsidian/` directory.

- **Obsidian vault:** Write to `{vault-root}/_system-audits/`. Filename: `style-audit — readability — {scope} — {YYYY-MM-DD}.md`
- **Non-Obsidian project:** Write to `_process/style-audit/` relative to the project root. Filename: `readability-audit-{folder-name}.md`

**Format:**

```markdown
# Readability Audit: {scope}

**Date:** {YYYY-MM-DD}
**Docs audited:** {N}
**Scope:** {path}

---

## Summary

{1–2 sentences: overall reading level, main pattern found, whether target was reached}

---

## Results by doc

### {filename}

- **Before:** {plain-language label, e.g. "college freshman — dense but accessible to practitioners"}
- **After:** {plain-language label}
- **Target:** {target label, e.g. "10th–11th grade"} ({doc type})
- **Status:** {Within target / Improved but still below / Already within target — no changes}

Fixes applied: {N}
Flags for review: {N}

**Fixes:**
- [Pattern 1: Sentence stacking] {Description of what was split and where}
- [Pattern 2: Information pile-up] {Description}
- [Pattern 3: Jargon-then-clause] {Description}
- [Pattern 5: Undefined term] {Term and where definition was added}
- [Pattern 6: Steps in prose] {What was converted to a numbered list}
- [Pattern 7: Context-less bullets] {Where a lead-in sentence was added}

**Flags (manual review needed):**
- ⚠ {Location in doc} — {1 sentence describing why it's flagged and what to consider}

---

### {filename}

...

---

## Passed — no changes needed

- {filename} — {plain-language label}, within target ({target label})
```

### 9. Display summary

```
Readability audit complete.

Docs audited: {N}
Docs improved: {N}
Docs within target: {N}
Docs still below target (dense by necessity): {N}

Wall paragraphs flagged for manual review: {N}

Audit report: {path}
```

---

## Grade level interpretation guide

| Grade level | Plain label | Example publication |
|---|---|---|
| 8th–9th | Easy, general audience | Popular science article |
| 10th–11th | Smart general audience | Wired / Atlantic feature |
| 11th–12th | Upper secondary | Good technical blog post |
| 12th–13th | Solid technical writing | API docs, technical blog |
| College freshman (13–14) | Dense but accessible | Dense API docs, spec sheets |
| College sophomore+ (14+) | Specialist territory | Academic papers, legal text |

---

## What this skill does NOT do

- Change vocabulary or word choice — that's `/docs-style-check-human`
- Change document structure or sections — that's `/docs-style-check-structure`
- Fix voice or tone — that's `/docs-style-check-voice`
- Add or remove content
- Touch tables, code blocks, callouts, or mermaid diagrams
- Process files in `_archive/`, `_templates/`, `_attachments/`

---

## Error handling

| Situation | Behavior |
|---|---|
| No argument provided | Stop: show usage message |
| Path doesn't exist | Stop: "File not found: [path]" |
| No `.md` files in directory | Stop: "No markdown files found in: [path]" |
| Doc has fewer than 50 prose words | Skip scoring; note in report |
| Doc already within target range | Report score, skip edits, mark as passed |

---

## Pipeline position

This skill runs last. The style pipeline order:

```
/docs-style-check-structure  ← sections, headings, note standard
/docs-style-check-voice      ← project voice and conventions
/docs-style-check-human      ← AI pattern cleanup
/docs-readability-check      ← sentence complexity (this skill)
```

Can also run standalone on any doc at any time.
