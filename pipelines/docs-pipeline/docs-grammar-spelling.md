---
name: docs-grammar-spelling
description: Grammar, spelling, and domain terminology check for docs. Loads the domain glossary, checks prose for errors, and edits in place. Run last in the style chain, after the human pass.
argument-hint: [folder-or-file]
allowed-tools: [Read, Write, Edit, Glob, Bash, Grep]
---

# docs-grammar-spelling

Final correctness pass on one or more docs. Checks spelling, grammar, punctuation, and domain terminology against the canonical glossary. Edits docs in place. Produces an audit report summarizing findings and fixes.

This is the last style pass in the pipeline. Run it after `/docs-style-check-human` (AI pattern cleanup) so it operates on fully settled prose. Unlike the other style passes, this one focuses on **correctness** (right/wrong), not **style** (better/worse).

## Arguments

The user provided: $ARGUMENTS

This should be a path to a **folder** (all `.md` files inside) or a single `.md` **file**.

**Required.** If missing, stop: `"Please provide a folder or file path: /docs-grammar-spelling [path]"`

---

## Constants

```
GLOSSARY=./_knowledge/glossary.yaml
```

---

## Steps

### 1. Validate input

- Check that $ARGUMENTS is provided. If not, stop with usage message.
- Resolve whether the path is a directory or single file:
  - **Directory**: Glob all `.md` files inside it. Abort if zero found.
  - **File**: Use that single file. Abort if it doesn't exist.
- Store the full file list.

### 2. Load the glossary

Read `GLOSSARY` using the Read tool. Parse the YAML and build two internal lookup structures:

**Term index:** A map from every known form (canonical + all aliases, case-insensitive) to the canonical entry. This is used for matching terms in the doc.

**Docs-facing filter:** Note which terms have `docs_facing: false`. These are internal-only terms. If one appears in a customer-facing doc, flag it.

### 3. Read all docs

Read each doc in full using the Read tool. Read in parallel where possible.

### 4. Identify prose zones

For each doc, identify which lines are **prose** (checkable) vs **non-prose** (skip). Skip:

- YAML frontmatter (between `---` delimiters at the top)
- Fenced code blocks (between `` ``` `` delimiters)
- Inline code (content inside backticks)
- URLs and link targets
- HTML tags
- Table separator rows (`|---|---|`)

All checks below apply only to prose zones. Never modify content inside code blocks, inline code, frontmatter, or URLs.

### 5. Check each doc

For each doc, work through the check categories below in order. Record findings as:

- **Fix** — an unambiguous correction (will be applied)
- **Flag** — judgment call or needs human review (reported only)

#### 5a. Terminology — canonical form enforcement

For every glossary term that appears in the doc's prose zones, check whether it matches the canonical form.

| Check | Rule | Action |
|---|---|---|
| Capitalization | Term must match the `canonical` field's capitalization | Fix: replace with canonical form |
| Non-canonical alias used | An alias is used instead of the canonical form | Fix: replace with canonical form (exception: if the alias is more natural in context, Flag instead) |
| Missing expansion on first use | Terms with aliases that are expansions (e.g., "Food and Nutrition Service" for FNS) should be expanded on first use in the doc | Flag if the acronym appears before any expansion |
| Internal term in customer-facing doc | A term with `docs_facing: false` appears in a doc that will be published | Flag with the canonical form and a note that it's internal-only |

**Capitalization specifics from the glossary `usage.capitalization` field:**

- Acronyms (e.g., `API`, `SDK`, `HTTP`): always fully uppercase
- Title case terms (e.g., `Payment Method`, `Authentication Token`): capitalize in prose when used as a proper concept name; lowercase when used generically
- PascalCase terms (e.g., `ProductName`, `ApiClient`): always PascalCase, never spaced or lowercased
- API field names (e.g., `field_name`, `amount`): always in backticks

**Common patterns to catch:**

| Wrong | Right | Rule |
|---|---|---|
| `Ebt`, `ebt` | `benefits-card` | Acronyms are always uppercase |
| `Product Name`, `product name` | `ProductName` | PascalCase product name example |
| `Type-A` in prose | `Type A` | Forward slash or space, not hyphen, in prose |
| `field name` | `field_name` in backticks | API fields use snake_case in backticks |
| `feature-name` | `Feature Name` | No hyphen, title case |
| `Third-Party Provider` | `Third Party Provider` | No hyphen in compound modifiers used as names |
| `deprecated-term` | `CurrentTerm` | Use current canonical form |

#### 5b. Terminology — common mistakes from glossary

Check the `usage.mistakes` field for each glossary term. These are term-specific mistakes documented in the glossary. Scan the doc for each mistake pattern.

**Fix** if the correction is unambiguous. **Flag** if context matters.

#### 5c. Spelling

Scan prose zones for common spelling errors. Focus on:

| Category | Examples | Action |
|---|---|---|
| Commonly confused words | affect/effect, its/it's, their/there/they're, then/than, complement/compliment, principal/principle | Fix if unambiguous from context; Flag if ambiguous |
| Double words | "the the", "is is", "to to" | Fix: remove duplicate |
| Technical misspellings | "authenication", "paramter", "endpoing", "webhok", "configuraton" | Fix: correct spelling |
| British vs American | "authorise" vs "authorize", "colour" vs "color", "behaviour" vs "behavior" | Fix: use American English (docs standard) |
| Hyphenation | "server side" vs "server-side" (adjective), "real time" vs "real-time" (adjective) | Fix: hyphenate compound adjectives before nouns; no hyphen after nouns ("the check runs in real time") |

**Do not flag:** intentional technical terms, API field names, code identifiers, or product names that may look like misspellings.

#### 5d. Grammar

Check prose zones for grammatical errors. Focus on high-confidence, unambiguous issues:

| Check | Rule | Action |
|---|---|---|
| Subject-verb agreement | "The endpoints returns..." → "The endpoint returns..." or "The endpoints return..." | Fix |
| Article misuse | "a endpoint" → "an endpoint"; "an HTTP" stays (correct) | Fix |
| Tense consistency | Within a section, tense should be consistent. API descriptions use present tense. Tutorials may use future tense for outcomes. | Flag if tense shifts mid-paragraph without reason |
| Sentence fragments | Incomplete sentences in prose (OK in list items, headings, table cells) | Flag |
| Run-on sentences | Two independent clauses joined without punctuation or conjunction | Flag — suggest where to split |
| Dangling modifiers | "After configuring the webhook, the server sends..." (the server didn't configure the webhook) | Flag |

**Do not over-correct.** Technical writing uses sentence fragments, imperative mood, and informal constructions intentionally. Only flag grammar issues that would confuse the reader or look unprofessional.

#### 5e. Punctuation

| Check | Rule | Action |
|---|---|---|
| Backtick consistency | API field names, file paths, HTTP methods, status codes, and code values must be in backticks | Fix: add backticks where missing |
| List punctuation | Within a single list, all items should end the same way (all periods, all no periods, etc.) | Fix: make consistent — prefer no periods for short items, periods for full sentences |
| Serial comma | Use the Oxford comma: "Type A, Type B, and Type C" not "Type A, Type B and Type C" | Fix: add serial comma |
| Colon usage | Colons introducing lists should follow a complete clause | Flag if the clause before the colon is incomplete |
| Quotation marks | Use straight quotes, not curly quotes, in technical docs | Fix: replace curly with straight |

**Backtick rules — what gets backticks:**

- API field names: `field_name`, `amount`, `status`
- HTTP methods: `POST`, `GET`, `PATCH`, `DELETE`
- HTTP status codes: `200 OK`, `400 Bad Request`, `202 Accepted`
- File paths: `/path/to/resource/`
- Endpoint paths: `/api/resource/`
- Header names: `Authorization`, `API-Version`, `Idempotency-Key`, `X-Request-ID`
- Code values: `true`, `false`, `null`
- Environment names when used as identifiers: `sandbox`

**What does NOT get backticks:**

- Product names: `ProductName` (unless in a code context)
- Concept names: `FeatureName` (unless the API resource name)
- General acronyms: `API`, `SDK`, `HTTP` (unless referring to a specific code identifier)

#### 5f. Consistency

Check within-document consistency for terms and patterns:

| Check | Rule | Action |
|---|---|---|
| Term consistency | Same concept must use the same term throughout the doc. Don't alternate between "access token" and "auth token" for the same thing. | Flag inconsistencies |
| Heading style consistency | All headings at the same level should follow the same pattern (all sentence case, all starting with verbs, etc.) | Flag if mixed |
| Code format consistency | If `POST` is backticked once, it should be backticked everywhere | Fix: backtick all instances if any are backticked |
| Number format | Consistent use of digits vs words (use digits for technical values: "15 minutes", "200 OK"; words for small counts in prose: "two types") | Flag inconsistencies |

### 6. Apply fixes

For each **Fix** finding, edit the doc in place using the Edit tool. Work through one doc at a time, top to bottom.

**Important:** Re-read the file between major edit batches to avoid stale content references. Group nearby fixes into single Edit calls where possible.

**Priority order for fixes:**
1. Terminology (canonical form) — these are the most impactful and unambiguous
2. Spelling — clear right/wrong
3. Punctuation (backticks, serial comma) — mechanical
4. Grammar — only the high-confidence ones

Track every edit: `{filename}: {what changed}`.

### 7. Write audit report

Write to the `_process/style-audit/` directory relative to the project's output root. Resolve the output root by walking up from the input path until you find a directory containing `_process/`.

**If no `_process/` directory exists** (standalone use outside a workspace), write the report to the same directory as the input file(s), in a `_proofread-report/` subdirectory.

**Filename:** `style-audit-proofread-{name}.md` (where `{name}` is the input folder's basename or filename without extension)

**Format:**

```markdown
# Proofread Audit: {name}

**Date:** {YYYY-MM-DD}
**Reference:** glossary.yaml (_knowledge/)
**Docs audited:** {N}
**Scope:** {path}

---

## Summary

{1-2 sentences: overall correctness, most common issue category}

Fixes applied: {N}
Flags for review: {N}

By category:
  Terminology: {N} fixes, {N} flags
  Spelling: {N} fixes, {N} flags
  Grammar: {N} fixes, {N} flags
  Punctuation: {N} fixes, {N} flags
  Consistency: {N} fixes, {N} flags

---

## Fixes applied

### {filename}

| Line | Category | Before | After |
|---|---|---|---|
| ~{N} | {category} | {old text} | {new text} |

---

## Flags (manual review needed)

### {filename}

- [{category}] ~line {N}: {description of issue and suggested fix}

---

## Passed — no issues

- {filename}
```

The table format for fixes makes it easy to scan what changed and verify correctness.

### 8. Display summary

```
Proofread audit complete.

Docs audited: {N}
Fixes applied: {N}
Flags for review: {N}

Top categories:
  - {Category}: {count} ({fixes} fixed, {flags} flagged)
  - {Category}: {count}
  - {Category}: {count}

Audit report: {report-path}

What's next:
  Review the {N} flags in the audit report — these need human judgment.
```

If this is running inside the pipeline (a `_process/` directory exists), also suggest:
```
  /docs-links-review {path}  → Cross-link check (next pipeline stage)
```

---

## Error Handling

| Situation | Behavior |
|---|---|
| No argument provided | Stop: show usage message |
| Path doesn't exist | Stop: "File not found: [path]" or "Directory not found: [path]" |
| No `.md` files in directory | Stop: "No markdown files found in: [path]" |
| Glossary not found | Stop: "Glossary not found at [path]. Check GLOSSARY constant." |

---

## Notes

- This skill edits docs **in place**. The audit report records what was changed.
- Run this **last** in the style pipeline — after `/docs-style-check-structure`, `/docs-style-check-voice`, and `/docs-style-check-human`.
- This pass is more mechanical than the others. Most fixes are objectively right or wrong (a typo is a typo). Use judgment only for grammar flags and terminology edge cases.
- The glossary is the single source of truth for domain terminology. If a term isn't in the glossary, don't flag it as wrong — it might just be missing from the glossary.
- **Never modify content inside code blocks, inline code, frontmatter, or URLs.** The prose zone identification in step 4 is critical.
- British spellings ("authorise", "colour") are common in engineer-written drafts. Always convert to American English.
- The backtick rules are strict. API field names without backticks are the single most common issue in engineer-written docs.
- For standalone use (outside the pipeline), this skill works on any markdown file — not just workspace output docs. Use it on PR review files, drafts, or any doc that needs a correctness check.
