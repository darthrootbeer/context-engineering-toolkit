---
name: docs-sme-review
description: >-
  Product knowledge review for docs — checks domain accuracy, reader journey,
  naming collisions, and technical clarity against the product knowledge base.
  Read-only. Use after links-review, before changes summary.
allowed-tools: [Read, Write, Bash, Glob]
---

# docs-sme-review

Scan one or more draft markdown files against the product knowledge base to catch domain accuracy errors, reader journey gaps, naming collisions, technical clarity issues, and typos. This skill is product-knowledge-aware: it knows which features belong to which integration type, which API resources exist for each product, and which webhook events fire for which integrations.

Run this **after** `/docs-links-review` and **before** `/docs-changes-list`.

## Arguments

The user provided: $ARGUMENTS

This should be a path to a **folder** or a single `.md` **file**, with an optional Linear ticket ID:

```
/docs-sme-review docs/output/split/
/docs-sme-review docs/output/split/ TICKET-1801
```

- **Path** (required): folder or single file to analyze
- **Ticket ID** (optional): Ticket tracking this work (e.g., `TICKET-1801`)

## Usage

`/docs-sme-review [folder-or-file-path]`

**Required:** The `[folder-or-file-path]` parameter is mandatory. If not provided, stop and ask: "Please provide a folder or file path: `/docs-sme-review [path]`"

---

## Steps

### 1. Validate input

- Check that `$ARGUMENTS` is provided. If not, stop with usage message above.
- Parse arguments: first token is the path, second token (if present, matches `[A-Z]+-[0-9]+`) is the ticket ID.
- Resolve whether the path is a directory or a single file:
  - **Directory**: Glob all `.md` files inside it (non-recursive is fine; use `**/*.md` if subdirs are expected). Abort if zero `.md` files found: "No markdown files found in: [path]"
  - **File**: Use that single file. Abort if it doesn't exist: "File not found: [path]"
- For each draft file, derive `INPUT_BASENAME`:
  - Get filename stem (no extension, no leading path): e.g., `webhooks-concepts.md` → `webhooks-concepts`
- Store the full draft file list and their basenames.

### 2. Read draft files

- Read each draft file in full using `Read` tool.
- If any single file exceeds 1500 lines, note it in the report header: "Large file ([N] lines) — analysis may be incomplete for deeply nested sections." Continue anyway.
- Parse each draft for:
  - H1, H2, H3 headings (these become anchor points for citing locations)
  - Approximate line numbers for each heading
  - `diataxis_type` from frontmatter (if present)

### 3. Load product knowledge base

- Read `./_knowledge/product-kb/index.md` first.
- If the file is missing, stop with error: "Product KB not found at _knowledge/product-kb/ — populate the placeholder files before running SME review."
- Check the `extracted:` frontmatter date. If it is more than 90 days old, include a warning in every report header: "Product KB last extracted [date] (>90 days ago) — findings may be stale. Re-run extraction before acting on domain accuracy flags."
- Then load the three core KB files for domain accuracy checks:
  - `./_knowledge/product-kb/integration-types.md` (scopes, capabilities, limits)
  - `./_knowledge/product-kb/endpoints.md` (API surface, params, responses)
  - `./_knowledge/product-kb/domain-models.md` (objects, lifecycles, relationships)
- Load additional KB files based on what the draft content covers:
  - Draft mentions error codes or error handling → load `error-codes.md`
  - Draft mentions webhooks → load `webhooks.md`
  - Draft mentions SDK methods or components → load `domain-models.md`
  - Unsure if a recent API change affects the draft → load `recent-changes.md`

### 4. Build title index

Build a lightweight index of all published doc titles to check for naming collisions.

**Optional step.** If `{YOUR_ORG}` or `{YOUR_DOCS_REPO}` still reads as a placeholder (it starts with `{`), or `gh` is not installed or not logged in, skip this whole step. Set `CORPUS_TMP` to unset, print "Naming-collision check skipped: no docs repo configured" in the report header, and skip Category C in step 5.

Otherwise do a fresh shallow clone of the docs repo:

```bash
mktemp -d /tmp/docs-corpus-XXXXXX
```
Store the output path as `CORPUS_TMP`. Then clone:
```bash
gh repo clone {YOUR_ORG}/{YOUR_DOCS_REPO} CORPUS_TMP_PATH -- --depth 1 --quiet
```

- Set `CORPUS_ROOT="CORPUS_TMP_PATH/docs"`.
- Glob all `.md` files under `$CORPUS_ROOT`.
- For each corpus file, read the **first 15 lines** only.
- Extract `title:` from frontmatter.
- Skip files where `hidden: true` or `deprecated: true`.
- Exclude any corpus file whose filename matches a draft file's basename.
- Store as title index: `[{ path, title }]`
- Note the count of indexed titles for the report header.

### 5. Run SME review

For each draft file, run a **single analysis pass** checking 5 categories in order. The product KB files loaded in step 3 are the authoritative reference for all domain checks.

#### Category A: Domain Accuracy (HIGH priority)

Check every claim in the draft against the product model tables:

- **Integration type scope:** If the draft or a section targets a specific integration type (identifiable from the H2 section header, e.g., "## SDK integrations"), verify that every feature, resource, and API reference mentioned in that section actually belongs to that integration type.
- **Resource scope:** Verify that every API resource mentioned in a section actually belongs to the integration type or product tier that section targets.
- **Feature attribution:** If the draft says a feature is "built-in" or "automatic," verify against the capability matrix in `_knowledge/product-kb/integration-types.md`.
- **Webhook event scope:** If the draft discusses webhook events, verify each event fires for the integration types listed in your webhook event mapping.

**Critical distinction:** Only flag when the content **implies the reader IS using** a different integration type. Mentioning another integration type **for comparison** is fine. The test: would a reader following this section's instructions be confused or misled?

Severity:
- **HIGH**: Content implies the reader has access to features/resources their integration type doesn't support.
- **MEDIUM**: Content is technically accurate but could mislead a reader who doesn't know the integration type boundaries.

#### Category B: Reader Journey

- **Assumed knowledge:** Does the draft reference concepts, resources, or processes without explaining them or linking to an explainer? Check especially for: [your product's commonly-assumed concepts — add them to this list].
- **Prerequisites:** Does the draft assume the reader has already completed a setup step without stating it? (e.g., "after you've set up your webhook endpoint" without linking to the how-to).
- **Entry point awareness:** If a reader lands on this page from search, will they understand the context? Check for missing "who this is for" signals in the first 2-3 paragraphs.
- **Cross-references to other docs in the set:** If this is part of a guide set (multiple related docs), does it link to sibling docs where relevant?

Severity:
- **HIGH**: Draft assumes knowledge that a first-time reader wouldn't have and doesn't link to the source.
- **MEDIUM**: Missing cross-reference that would help navigation but isn't strictly necessary.

#### Category C: Naming Collisions

- Compare each draft file's `title:` frontmatter (and H1 heading) against the title index built in step 5.
- Flag any exact match or near-match (same words, different order; same meaning, different phrasing).
- Include the conflicting corpus file path and its title.

Severity:
- **HIGH**: Exact title match with an existing published page.
- **MEDIUM**: Near-match that could confuse readers or search results.

#### Category D: Technical Clarity

Read as a developer encountering the concepts for the first time:

- **Backwards phrasing:** Sentences where the subject and object are swapped or the logical flow is inverted ("Pass the message as the secret" when it should be "Pass the secret as the key").
- **Odd phrasing:** Sentences that are technically accurate but read awkwardly or would confuse a developer ("A webhook is not an API call" as a standalone statement without context).
- **Unexplained jargon:** Technical terms used without definition or link, especially product-specific terms (add your product-specific terms here).
- **Non-standard spelling:** "stringify'd" instead of "stringified", inconsistent capitalization of product names.
- **Passive voice on action items:** Instructions that should be imperative but use passive voice ("The order is canceled" vs. "Cancel the order").

Severity:
- **MEDIUM**: Phrasing that would confuse or slow down a developer.
- **LOW**: Style preference that doesn't affect comprehension.

#### Category E: Proofreading

**Deferred to `/docs-grammar-spelling`.** Only flag broken markdown formatting (unclosed backticks, mismatched headers) here since those affect rendering. Spelling, grammar, terminology, and punctuation are handled by the dedicated proofread skill.

### 6. Rank and filter

- Order findings: HIGH first, then MEDIUM, then LOW.
- Within each severity, order by category: Domain Accuracy → Reader Journey → Naming Collisions → Technical Clarity → Proofreading.
- Cap LOW findings at **3 per category** to avoid noise. If more than 3, note: "[N] additional LOW findings omitted."

### 7. Validate output directory

- Check if `_process/sme-review/` exists relative to the working directory.
- If not, create it: `mkdir -p _process/sme-review/`
- If the input path contains `_process/` already (e.g., running from a workspace), create the output relative to the workspace root instead.
- Abort with error if creation fails.

### 8. Write reports

For each draft file, write one report to:
`_process/sme-review/{INPUT_BASENAME}-sme-review.md`

Also write a summary report to:
`_process/sme-review/sme-review-summary.md`

See **Report Format** below.

### 9. Clean up and display summary

Remove the temp corpus clone (only if step 4 created one):
```bash
rm -r CORPUS_TMP_PATH
```

Print the summary:

```
SME review complete.

Draft files analyzed: [N]
Corpus titles indexed: [N] (or "skipped")
Product model verified: [date]

Reports:
  _process/sme-review/{basename}-sme-review.md
  ...
  _process/sme-review/sme-review-summary.md

Findings:
  Domain Accuracy: [N] HIGH, [N] MEDIUM
  Reader Journey:  [N] HIGH, [N] MEDIUM
  Naming Collisions: [N]
  Technical Clarity: [N]
  Proofreading: [N]
  Total: [N]
```

---

## Report Format

```markdown
# SME Review: [INPUT_BASENAME]

**Draft:** `[filepath]`
**Product KB:** _knowledge/product-kb/ (extracted: [date])
**Corpus:** [N] doc titles indexed
**Generated:** YYYY-MM-DD

---

## Domain Accuracy

### HIGH: [Section heading] — [one-line summary]

**Line:** ~[N]
**Text:** "[quoted text from draft]"
**Issue:** [Why this is wrong, referencing the product model table/rule]
**Fix:** [Specific suggested change]

---

## Reader Journey

### HIGH: [Section heading] — [one-line summary]

**Line:** ~[N]
**Text:** "[quoted text]"
**Issue:** [What knowledge is assumed]
**Fix:** [Add link/context to X]

---

## Naming Collisions

### [SEVERITY]: [Draft title] conflicts with [Existing title]

**Draft:** `[draft filepath]`
**Existing:** `[corpus filepath]`
**Fix:** [Suggest alternative title]

> No collisions detected.

---

## Technical Clarity

### [SEVERITY]: [Section heading] — [one-line summary]

**Line:** ~[N]
**Text:** "[quoted text]"
**Issue:** [What's wrong with the phrasing]
**Fix:** [Suggested rewrite]

---

## Proofreading

### LOW: [Location] — [one-line summary]

**Line:** ~[N]
**Text:** "[quoted text]"
**Fix:** [Correction]

> No proofreading issues found.
```

For sections with no findings, show the `> No [category] found.` line and skip the section body.

### Summary Report Format

```markdown
# SME Review Summary

**Files reviewed:** [N]
**Product KB:** _knowledge/product-kb/ (extracted: [date])
**Generated:** YYYY-MM-DD

---

## Findings by File

| File | Domain | Journey | Naming | Clarity | Proofread | Total |
|------|--------|---------|--------|---------|-----------|-------|
| [basename] | [H/M counts] | ... | ... | ... | ... | [N] |
| **Total** | **[N]** | **[N]** | **[N]** | **[N]** | **[N]** | **[N]** |

## HIGH Priority Items

1. **[file]** ~L[N]: [one-line summary] (category)
2. ...

## MEDIUM Priority Items

1. **[file]** ~L[N]: [one-line summary] (category)
2. ...
```

---

## Error Handling

| Situation | Behavior |
|-----------|----------|
| No `$ARGUMENTS` | Stop: show usage message |
| Path doesn't exist | Stop: "File not found: [path]" or "Directory not found: [path]" |
| Directory has no `.md` files | Stop: "No markdown files found in: [path]" |
| Draft file >1500 lines | Note in report header; continue |
| Product KB missing | Stop: "Product KB not found" |
| Corpus clone fails or no docs repo configured | Skip Category C, note "Naming-collision check skipped" in the report header, continue |
| Title index file unreadable | Skip it; note count of skipped files |
| Output directory creation fails | Stop: "Cannot create output directory" |
| Report write fails | Stop: "Cannot write report: [path]" |
| Product KB >90 days old | Warning in every report header |

**Philosophy:** Stop on input/output errors. Degrade gracefully on individual corpus file failures.

---

## Notes

- This skill is **read-only** for all source files. Nothing is modified.
- Run this **after** `/docs-links-review` (cross-link check) and **before** `/docs-changes-list` (editorial summary).
- The product KB at `_knowledge/product-kb/` is the source of truth for domain accuracy checks. See `index.md` for refresh instructions.
- **Single pass, not sub-passes.** All 5 categories are checked in one read-through per file. This avoids re-reading draft content and wasting context. Categories are interconnected (a domain error IS a reader journey error).
- **"Mentioning another integration type for comparison is fine."** Only flag when the content implies the reader IS using that integration type. A comparison table contrasting different integration types is not an error.
- The corpus clone reads only the first 15 lines per file (title extraction). This is lighter than the links-review approach (40 lines) because we only need titles, not content.
- URL derivation uses the filename stem only (ReadMe flat slugs), same as links-review.
