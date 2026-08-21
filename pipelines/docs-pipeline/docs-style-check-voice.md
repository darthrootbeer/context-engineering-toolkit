---
name: docs-style-check-voice
description: Apply the general style guide to docs — voice, tone, list formatting, callouts, tables, terminology, addressing conventions, and structure rules. Edits docs in place. Run after diataxis style pass, before human style pass.
argument-hint: [folder-or-file]
allowed-tools: [Read, Write, Edit, Glob, Bash]
---

# docs-style-check-voice

Apply the general style guide to one or more docs. Reads each doc, checks against every rule in the general style guide, and edits in place. Produces an audit report summarizing findings and fixes.

This pass enforces product voice, tone, and formatting conventions. It runs after the structural pass (`/docs-style-check-structure`) and before the AI cleanup pass (`/docs-style-check-human`).

## Arguments

The user provided: $ARGUMENTS

This should be a path to a **folder** (all `.md` files inside) or a single `.md` **file**.

**Required.** If missing, stop: `"Please provide a folder or file path: /docs-style-check-voice [path]"`

---

## Constants

```
STYLE_GUIDE=./_knowledge/style-guides/style-guide.md
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

Read `STYLE_GUIDE` using the Read tool. Internalize every rule — the checks below reference specific sections but the full guide is the authority.

### 3. Read all docs

Read each doc in full using the Read tool. Read in parallel where possible.

### 4. Check each doc against the style guide

For each doc, work through these check categories in order. Record findings as **Fix** (will be applied) or **Flag** (reported only).

#### 4a. Voice and tone

| Check | Rule | Action |
|---|---|---|
| Marketing language | No marketing, hype, or sales language. Be technically honest. | Fix: rewrite to be direct and factual |
| Robotic style | No stiff, formal prose. Write like a technically sharp teammate. | Flag if detected |
| Chatty tone | "Let's go ahead and..." or exclamation marks in technical content | Fix: rewrite to be direct |

#### 4b. Structure

| Check | Rule | Action |
|---|---|---|
| Paragraph length | 1-3 lines per paragraph. No walls of text. | Fix: break up paragraphs >3 lines where natural breaks exist |
| Key idea first | Each section/paragraph should lead with the key idea. | Flag if buried |
| Title case | Titles and callouts must use sentence case (capitalize first word only, plus proper nouns). | Fix: convert to sentence case |

#### 4c. Lists — procedural (numbered)

This is the most enforcement-heavy section. The general style guide has strict rules about numbered lists.

| Check | Rule | Action |
|---|---|---|
| Usage | Numbered lists MUST be used for procedural instructions where actions are performed in order. | Flag bullets that should be numbered |
| Imperative verbs | Every numbered step must start with an imperative verb. | Fix: rewrite step to start with imperative |
| Lead-in required | Every numbered list MUST be introduced with bold text starting with "To" and ending with `:`. E.g., `**To configure webhooks:**` | Fix: add lead-in if missing. If a heading already serves as the lead-in, add the "To" lead-in between the heading and the list. |
| Outcome sentence | Every numbered list MUST be followed by a sentence confirming successful completion. | Fix: add outcome sentence if missing |
| Outcome phrasing | Outcome sentence must NOT start with "After completing these steps" or similar. Use "This will..." or state the outcome directly. | Fix: rewrite if it starts with "After completing..." |

#### 4d. Lists — conceptual (bulleted)

| Check | Rule | Action |
|---|---|---|
| Usage | Bulleted lists MUST be used for conceptual/descriptive explanations of behavior, flow, states, or properties. | Flag numbered lists that describe behavior (not steps) |
| No implied order | Bulleted lists must not imply required execution order. | Flag if order matters — should be numbered |
| Flat indentation | All items in a conceptual list must be at the same indentation level. No nested bullets in conceptual lists. | Fix: flatten nested bullets or restructure |
| Describe, don't instruct | Bulleted items describe what happens, not what the reader does. | Flag any bullet starting with an imperative verb in a conceptual list |

#### 4e. Tables

| Check | Rule | Action |
|---|---|---|
| Separator rows | Use `\|---\|` per column, not padded dashes | Fix: remove padding from separator rows |
| Cell padding | Do not pad cells with extra spaces | Fix: remove extra whitespace |
| Empty cells | Must contain a single space (`\| \|`), not be empty (`\|\|`) | Fix: add space to empty cells |
| Standard markdown | Use standard markdown tables, not ReadMe `[block:parameters]` JSON blocks | Flag — requires manual conversion |

#### 4f. Callouts

| Check | Rule | Action |
|---|---|---|
| Allowed types only | Only Info (📘), Warning (⚠️), Error/Critical (🛑), Okay (✅). No other callout types. | Fix: convert unsupported types to nearest allowed type |
| Required syntax | Line 1: `> ` + emoji + space + `**bold title**`. Line 2: `> ` (empty). Line 3+: `> ` + body text. | Fix: restructure callouts to match required format |
| No inline prefixes | No `INFO:`, `WARNING:`, `CRITICAL:`, `NOTE`, `TIP`, `RELATED` prefixes | Fix: convert to proper callout format |
| No bolded emojis | Bold the title text, not the emoji | Fix: move bold to title only |
| Semantic usage | Info for optional context, Warning for issues/limitations, Error for blocking/required, Okay for success confirmation (sparingly) | Flag if semantic mismatch detected |

#### 4g. Addressing the reader

| Check | Rule | Action |
|---|---|---|
| "You" in prose | Use "you" to address the reader in sentences and paragraphs | Flag passive constructions that should use "you" |
| Imperative in lists | Use imperative form (without "you") in list items | Fix: remove "You" from list item starts |
| Imperative in headings | Use imperative form in headings and subheadings — no "you" | Fix: remove "You" from heading starts |
| Customer reference | Use "customers" not "your customers" | Fix: remove "your" before "customers" |
| Active voice | Prefer active voice. Avoid passive. | Flag passive voice sentences |
| "We" usage | Only use "we" when the system is the actor ("We return a 200 OK"). Never "we" as guide author. | Fix: rewrite "we" to "you" or imperative when it's the guide author speaking |

#### 4h. Terminology

| Check | Rule | Action |
|---|---|---|
| Exact API field names | Use exact field names from the API. Don't rename. | Flag if a renamed field is detected |
| Consistent naming | Same term used the same way throughout the doc | Flag inconsistencies |

#### 4i. Cross-referencing

| Check | Rule | Action |
|---|---|---|
| Inline links | Use inline links, not bare URLs | Fix: convert bare URLs to inline links |
| No link dumps | Don't list multiple links in one sentence | Flag if detected |

#### 4j. General principles

| Check | Rule | Action |
|---|---|---|
| No filler | "In this guide, we will discuss..." and similar filler intros | Fix: delete filler and start with the point |
| No redundant intros | Sections that restate what's obvious from the heading | Fix: trim redundant opening |
| Every element has purpose | Check that every paragraph, list, and section earns its place | Flag padding that could be cut |

### 5. Apply fixes

For each **Fix** finding, edit the doc in place using the Edit tool. Work through one doc at a time, top to bottom.

**Important:** When making multiple edits to the same doc, re-read the file between major edit batches to avoid stale content references.

Track every edit: `{filename}: {what changed}`.

### 6. Write audit report

Write to the `_process/style-audit/` directory relative to the project's output root. Resolve the output root by walking up from the input path until you find a directory containing `_process/` (or create `_process/style-audit/` as a sibling of the docs folder).

**Filename:** `style-audit-general-{folder-name}.md` (where `{folder-name}` is the input folder's basename, e.g. `caper-refunds`)

For a single file input, use the filename without extension instead of folder name.

**Format:**

```markdown
# General Style Audit: {folder-name}

**Date:** {YYYY-MM-DD}
**Style guide:** General Style Guide
**Docs audited:** {N}
**Scope:** {path relative to project root}

---

## Summary

{1-2 sentences: overall compliance, most common issue category}

Fixes applied: {N}
Flags for review: {N}

---

## Fixes applied

### {filename}

- {Description of fix applied}

### {filename}

- {Description of fix applied}

---

## Flags (manual review needed)

### {filename}

- ⚠ {Description of issue and suggested fix}

---

## Passed — no issues

- {filename}
```

### 7. Display summary

```
General style audit complete.

Docs audited: {N}
Fixes applied: {N}
Flags for review: {N}

Audit report: {path}/_process/style-audit/style-audit-general-{folder-name}.md

What's next:
  /docs-style-check-human {path}  → AI pattern cleanup (final pass)
```

---

## Error Handling

| Situation | Behavior |
|---|---|
| No argument provided | Stop: show usage message |
| Path doesn't exist | Stop: "File not found: [path]" or "Directory not found: [path]" |
| No `.md` files in directory | Stop: "No markdown files found in: [path]" |
| Style guide not found | Stop: "General style guide not found at [path]. Check STYLE_GUIDE constant." |

---

## Notes

- This skill edits docs **in place**. The audit report records what was changed.
- Run this **after** `/docs-style-check-structure` (structural compliance), **before** `/docs-style-check-human` (AI pattern cleanup).
- The numbered list rules (lead-in, outcome sentence) are the most common violations. Pay close attention to these.
- The callout format rules are strict and specific to ReadMe's rendering. Get the syntax exactly right.
- Don't over-fix voice and tone — if the prose is clear and direct, leave it alone. The goal is consistency with the product voice, not rewriting everything.
- Tables that use `[block:parameters]` JSON format require manual conversion to standard markdown tables. Flag these but don't attempt auto-conversion.
