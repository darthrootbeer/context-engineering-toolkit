---
name: docs-style-check-structure
description: Apply Diataxis structural style rules to docs based on their diataxis_type frontmatter. Checks required sections, heading format, opening structure, conclusion, content boundaries, and the closing prompt block for the reader's AI model. For notes inside a vault, it can also run an optional Pass 0 note-standard check (title heading, orienting summary, required frontmatter fields). Edits docs in place. Run after split, before general and human style passes.
argument-hint: [folder-or-file]
allowed-tools: [Read, Write, Edit, Glob, Bash]
---

# docs-style-check-structure

Apply Diataxis structural style rules to one or more docs. Reads each doc's `diataxis_type` from frontmatter, loads the matching style guide, checks structural compliance, and edits the doc in place. Produces an audit report summarizing findings and fixes.

This is a structural pass — it fixes sections, headings, and content boundaries. It does not touch prose style (that's `/docs-style-check-voice`) or AI pattern cleanup (that's `/docs-style-check-human`).

## Arguments

The user provided: $ARGUMENTS

This should be a path to a **folder** (all `.md` files inside) or a single `.md` **file**.

**Required.** If missing, stop: `"Please provide a folder or file path: /docs-style-check-structure [path]"`

---

## Constants

```
STYLE_GUIDES_DIR=./_knowledge/style-guides/diataxis
```

| `diataxis_type` | Style guide file |
|---|---|
| `overview` | `style-guide_guide-set-overview.md` |
| `how-to` | `style-guide_diataxis-type_how-to-guides.md` |
| `reference` | `style-guide_diataxis-type_reference.md` |
| `explanation` | `style-guide_diataxis-type_explanation.md` |
| `tutorial` | `style-guide_diataxis-type_tutorials.md` |

---

## Steps

### 1. Validate input

- Check that $ARGUMENTS is provided. If not, stop with usage message.
- Resolve whether the path is a directory or single file:
  - **Directory**: Glob all `.md` files inside it. Abort if zero found.
  - **File**: Use that single file. Abort if it doesn't exist.
- Store the full file list.

### 1b. Pass 0 — Note standard check (optional, Obsidian-style vault notes only)

This pass is optional. Run it only when the input sits inside a notes vault, detected by a `.obsidian/` directory in a parent folder. Skip it for docs headed to a published docs site. Treat the field list below as a default and change it to match your own vault's standard.

For each note, check the following. Fix where noted and flag the rest.

#### Frontmatter fields

| Field | Rule | Action if missing |
|---|---|---|
| `title` | Must be present and match the `#` heading in the body | Flag and suggest a value |
| `tags` | Must have at least one tag | Flag |
| `created` | Must be present (date string) | Flag |
| `status` | Must be one of `current`, `draft`, `archived` | Flag and suggest `current` |

#### Body structure

| Element | Rule | Action if missing or wrong |
|---|---|---|
| `#` title heading | Must be the first non-frontmatter, non-blank line in the body | Fix: add `# {frontmatter title}` at the top |
| Orienting summary | 1 to 3 sentences right after the `#` heading, before any `##` section or callout, with no heading of its own. It says what the note is, who it is for, and what it covers. | Flag. The skill cannot write it without knowing the note, so report it as needing a summary |

**What counts as a summary:** a paragraph that answers "what is this note and why would I read it?" If the first content after the `#` heading is a `##` section, a `> [!...]` callout, or a `---` divider, the summary is missing.

**Do not flag** notes in `_archive/`, `_templates/`, or `_attachments/`. They are exempt.

Record every fix and flag in the audit report under a **Pass 0: Note Standard** section.

---

### 2. Read all docs and determine types

Read each doc using the Read tool. For each doc, determine its Diataxis type using this fallback chain:

#### 2a. Check frontmatter

Look for `diataxis_type` in the YAML frontmatter. If present and matches a known type (overview, how-to, reference, explanation, tutorial), use it.

#### 2b. Check filename

If frontmatter has no `diataxis_type`, infer from the filename:

| Filename pattern | Inferred type |
|---|---|
| `index.md` | `overview` |
| `*-overview.md` | `overview` |
| `*-reference.md` or `*-ref.md` | `reference` |
| Starts with `how-to-*` | `how-to` |
| Starts with `tutorial-*` or contains `your-first` | `tutorial` |

#### 2c. Stop if unresolvable

If neither frontmatter nor filename provides a type, collect those files into an `untyped` list. After checking all files:

- If **all** files are typed: proceed to step 3.
- If **any** files are untyped: STOP and report:

```
Cannot determine diataxis_type for:
  - {filename} (no frontmatter type, no recognizable filename pattern)
  - {filename}

These docs need a diataxis_type before the style pass can run.

Want me to read each doc and assess its type first? I'll propose a type for each one based on the content, and you can confirm before I proceed.
```

Wait for the user's response. If they say yes, read each untyped doc in full, classify it using the Diataxis decision tree (is it steps? → how-to. Is it facts for lookup? → reference. Is it conceptual "why"? → explanation. Is it guided learning? → tutorial. Is it a routing page? → overview), and propose the type. After the user confirms, add `diataxis_type` to the doc's frontmatter and continue.

If the user says no or wants to handle it themselves, stop the skill.

#### 2d. Group by type

Group all docs by their resolved `diataxis_type` (whether from frontmatter, filename, or user-confirmed assessment).

### 3. Load the style guide for each type

For each unique `diataxis_type` found in the doc set (all types are resolved by this point), read the matching style guide from `STYLE_GUIDES_DIR`. Read these in parallel.

If a `diataxis_type` value doesn't match any known guide (not in the constants table above), report and skip: `"⚠ Unknown diataxis_type '{type}' in {filename} — skipping."`

### 4. Check each doc against its style guide

For each doc, run the checks defined below for its type. Record every finding as either:

- **Fix** — a concrete structural change to make (will be applied)
- **Flag** — something worth noting but not auto-fixable (reported only)

#### 4a. Overview docs (`diataxis_type: overview`)

| Check | Rule | Fix if violated |
|---|---|---|
| Title format | Must follow `[Product/Feature] [Guide Type]` pattern. Not "Introduction to..." or "Getting Started with..." | Flag — suggest corrected title |
| Lead paragraph | Must exist below H1, before any `##` heading. 1-2 sentences. No section heading on it. | Flag if missing |
| `## Audience` section | Must be present. Must name a role and assumed baseline. | Fix: add placeholder section if missing |
| `## Prerequisites` section | Must be present. Must be specific and actionable. | Fix: add placeholder section if missing |
| `## What's in this guide` | Must be present. Must list every doc in the guide set. Each bullet: `**[Linked title]**. One sentence.` Order: Explanation → How-to → Reference → Tutorial. | Fix: reorder if wrong. Flag if docs appear missing. |
| No duplicated content | Overview must not reproduce content from the typed docs. | Flag any section >5 lines that looks like how-to steps, reference tables, or detailed explanation |
| Length | As long as needed to orient, no more. If any section would be more useful in a typed doc, it should be there. | Flag if >50 body lines |

#### 4b. How-to docs (`diataxis_type: how-to`)

| Check | Rule | Fix if violated |
|---|---|---|
| Title format | Must be "How to [accomplish goal]" or "[Action] [object]". Imperative. | Flag — suggest corrected title |
| Opening section | Must include problem/goal statement (1-2 sentences). Must include prerequisites (brief, not tutorial-level). | Flag if missing |
| Step headings | Major steps should use `###` or `##` headings with action verbs. Steps should be numbered lists for sequential actions. | Flag if steps use bullets instead of numbers for sequential actions |
| Procedural list lead-in | Every numbered list must be introduced with bold text starting with "To" and ending with `:` (e.g., `**To configure webhooks:**`). | Fix: add lead-in if missing |
| Outcome sentence | Every numbered list must be followed by a plain-language sentence confirming completion. Must NOT start with "After completing these steps". | Fix: flag if missing |
| No tutorial teaching | No foundational concepts, no learning exercises, no hand-holding. | Flag any paragraph >3 sentences of conceptual explanation without a signpost link to an explanation doc |
| No comprehensive reference | No full parameter lists or API specs — link to reference doc instead. | Flag any table with >5 rows of parameters |

#### 4c. Reference docs (`diataxis_type: reference`)

| Check | Rule | Fix if violated |
|---|---|---|
| Title format | Must be "[Object/Feature] Reference" or object name. Not "How to..." or "Understanding..." | Flag — suggest corrected title |
| Voice | Third person, neutral, present tense. No imperative instructions. No opinions or recommendations. | Flag sentences starting with imperative verbs ("Create...", "Use...", "Run...") |
| Structure | Organized for lookup (alphabetical, logical grouping, or hierarchical). Consistent ordering within entries. | Flag if inconsistent |
| Exhaustiveness | All parameters, values, errors, constraints should be documented. | Flag — can't auto-fix, but note if a table seems incomplete |
| No instructions | No "First do X, then Y" procedural content. | Flag any numbered list >2 steps |
| No explanations | No "why" content or design rationale. | Flag paragraphs discussing rationale or trade-offs |

#### 4d. Explanation docs (`diataxis_type: explanation`)

| Check | Rule | Fix if violated |
|---|---|---|
| Title format | Must be "Understanding [concept]", "How [system] works", "[Concept] explained", or direct concept name. | Flag — suggest corrected title |
| Opening section | Must include context (problem domain, why it exists) and scope (what's covered, boundaries). 2-3 paragraphs. | Flag if missing or too short |
| Conclusion | Must include key insights summary and links to related docs (how-to, reference, tutorial). | Flag if missing |
| No step-by-step | No procedural "First do X, then Y" instructions. | Flag any numbered list >2 steps that reads as a procedure |
| No complete API specs | No parameter tables or full endpoint documentation. | Flag any parameter table |

#### 4e. Tutorial docs (`diataxis_type: tutorial`)

| Check | Rule | Fix if violated |
|---|---|---|
| Title format | Action-oriented: "[Verb] Your First [Thing]" or similar. | Flag — suggest corrected title |
| Opening elements | Must include all 4: what they'll learn, what they'll build, prerequisites, time estimate. | Fix: add placeholder for any missing element |
| Step structure | Each step needs: action (imperative), expected result ("You should see..."). | Flag steps missing expected results |
| Conclusion | Must include recap of accomplishments and next steps links. | Flag if missing |
| Single path | No multiple options or alternatives. One canonical path. | Flag any "Option A / Option B" pattern |
| No reference material | Only show parameters actually used. Link to reference for complete details. | Flag any comprehensive parameter table |

#### 4f. All doc types: prompt block for the reader's AI model

Run this check on every doc, whatever its type. The rule lives in the general style guide under "End every doc with a prompt for the reader's AI model". Read that section first.

Skip a doc if it is exempt: a skill file, a file under `_archive/`, `_templates/`, `_attachments/` or `_process/`, or an index or README under about 25 lines that only routes the reader elsewhere.

| Check | Rule | Action |
|---|---|---|
| Block at the end of the doc | The last heading in the doc is `### Prompt for your AI model`, followed by the sentence "Paste this into any AI model, together with this document and the files it describes." and at least one fenced `text` block | Flag if missing. Do not auto-fix. |
| Three prompts at the end | The end-of-doc block holds at least three prompts, covering understand and teach, review against the reader's own setup, and adapt and test | Flag any missing purpose |
| Block at the end of long sections | Every H2 section with more than about 40 lines of prose (code blocks and tables do not count) that stands on its own ends with a `### Prompt for your AI model` block | Flag each long section without one |
| Prompt is self-contained | Each prompt names the files to attach, says what the model must do, and says what a good answer contains | Flag prompts that only ask for a general overview, with no checkable answer |
| Tested-with statement | The doc says which models its prompts were run against and on what date, and does not claim "any AI model" without that | Flag if missing |

**Why this is a flag, not a fix:** a prompt has to be written for the doc and then run against a model before it ships. A placeholder prompt that was never run is worse than no prompt, because it claims a check that did not happen. Report the gap and let the author write and test the prompt.

Record these findings under a **Prompt block** heading in the audit report.

---

### 5. Apply fixes

For each **Fix** finding, edit the doc in place using the Edit tool. Make the minimum change needed — don't rewrite surrounding content.

Track every edit: `{filename}: {what changed}`.

### 6. Write audit report

Write to the `_process/style-audit/` directory relative to the project's output root. Resolve the output root by walking up from the input path until you find a directory containing `_process/` (or create `_process/style-audit/` as a sibling of the docs folder).

**Filename:** `style-audit-diataxis-{folder-name}.md` (where `{folder-name}` is the input folder's basename, e.g. `order-cancellations`)

For a single file input, use the filename without extension instead of folder name.

**Format:**

```markdown
# Diataxis Style Audit: {folder-name}

**Date:** {YYYY-MM-DD}
**Style guide:** Diataxis structural rules ({N} type-specific guides)
**Docs audited:** {N}
**Scope:** {path relative to project root}

---

## Summary

{1-2 sentences: overall structural compliance, most common issue category}

Fixes applied: {N}
Flags for review: {N}

---

## Fixes applied

### {filename} ({diataxis_type})

- {Description of fix applied}
- {Description of fix applied}

### {filename} ({diataxis_type})

- {Description of fix applied}

---

## Flags (manual review needed)

### {filename} ({diataxis_type})

- ⚠ {Description of issue and suggested fix}

---

## Prompt block

### {filename}

- ⚠ {Missing block, missing purpose, long section without a block, or missing tested-with statement}

---

## Passed — no issues

- {filename} ({diataxis_type})
```

If no changes were needed for any doc, still write the report with the "Passed" section.

### 7. Display summary

```
Diataxis style audit complete.

Docs audited: {N}
  overview: {N}
  how-to: {N}
  reference: {N}
  explanation: {N}
  tutorial: {N}
  skipped: {N}

Fixes applied: {N}
Flags for review: {N}

Audit report: {path}/_process/style-audit/style-audit-diataxis-{folder-name}.md
```

---

## Error Handling

| Situation | Behavior |
|---|---|
| No argument provided | Stop: show usage message |
| Path doesn't exist | Stop: "File not found: [path]" or "Directory not found: [path]" |
| No `.md` files in directory | Stop: "No markdown files found in: [path]" |
| Doc missing `diataxis_type` | Skip with warning |
| Unknown `diataxis_type` | Skip with warning |
| Style guide file not found | Stop: "Style guide not found: [path]. Check STYLE_GUIDES_DIR." |

---

## Notes

- This skill edits docs **in place**. The audit report records what was changed.
- Run this **after** `/docs-diataxis-split` (or on any docs that need structural compliance), **before** `/docs-style-check-voice` and `/docs-style-check-human`.
- Structural fixes only. Does not touch prose style, word choice, or AI patterns.
- The style guides live in the docs repo, not in the skill. If the guides are updated, this skill automatically picks up the changes.
- For docs that went through `/docs-diataxis-split`, most structural elements should already be in place. This pass catches anything the split missed.
