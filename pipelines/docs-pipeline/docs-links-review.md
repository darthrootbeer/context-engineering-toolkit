---
name: docs-links-review
description: Cross-link check for draft docs — scans a file or folder against the full docs corpus to surface content overlaps and missing cross-link candidates. Use when finishing a new or restructured doc before review/PR.
allowed-tools: [Read, Write, Bash, Glob]
---

# docs-links-review

Scan one or more draft markdown files against the full docs corpus to find: (1) content that already exists elsewhere and shouldn't be duplicated, and (2) existing pages that should be linked from the draft. Fires after Diátaxis work, before review/PR.

## Arguments

The user provided: $ARGUMENTS

This should be a path to a **folder** or a single `.md` **file**, with an optional Linear ticket ID:

```
/docs-link-check docs/output/split/
/docs-link-check docs/output/split/ TICKET-1232
```

- **Path** (required): folder or single file to analyze
- **Ticket ID** (optional): Ticket tracking this work (e.g., `TICKET-1232`). If provided, the skill will post a comment with one-line link summaries after writing the reports.

## Usage

`/docs-link-check [folder-or-file-path]`

**Required:** The `[folder-or-file-path]` parameter is mandatory. If not provided, stop and ask: "Please provide a folder or file path: `/docs-link-check [path]`"

**Primary use case:** folder path — when a large guide has been split into multiple pieces (e.g., `output/acmepay/`), run against the directory and the skill discovers all `.md` files automatically.

---

## Steps

### 1. Validate input

- Check that `$ARGUMENTS` is provided. If not, stop with usage message above.
- Parse arguments: first token is the path, second token (if present, matches `[A-Z]+-[0-9]+`) is the ticket ID.
- Resolve whether the path is a directory or a single file:
  - **Directory**: Glob all `.md` files inside it (non-recursive is fine; use `**/*.md` if subdirs are expected). Abort if zero `.md` files found: "No markdown files found in: [path]"
  - **File**: Use that single file. Abort if it doesn't exist: "File not found: [path]"
- For each draft file, derive `INPUT_BASENAME`:
  - Get filename stem (no extension, no leading path): e.g., `acmepay-overview.md` → `acmepay-overview`
- Store the full draft file list and their basenames.

### 2. Read draft files

- Read each draft file in full using `Read` tool.
- If any single file exceeds 1500 lines, note it in the report header: "⚠️ Large file ([N] lines) — analysis may be incomplete for deeply nested sections." Continue anyway.
- Parse each draft for:
  - H1, H2, H3 headings (these become anchor points for citing overlap/link locations)
  - Approximate line numbers for each heading

### 3. Build corpus index

Do a fresh shallow clone of the docs repo so the corpus is always at HEAD, not whatever state the local clone happens to be in.

Create a temp directory (separate Bash call):
```bash
mktemp -d /tmp/docs-corpus-XXXXXX
```
Store the output path as `CORPUS_TMP`. Then clone into it:
```bash
gh repo clone {YOUR_ORG}/{YOUR_DOCS_REPO} CORPUS_TMP_PATH -- --depth 1 --quiet
```
Replace `CORPUS_TMP_PATH` with the actual path from mktemp.

- Abort if the clone fails: "Failed to clone docs repo. Check gh auth and network."
- Set `CORPUS_ROOT="CORPUS_TMP_PATH/docs"` — all corpus file paths are relative to this.
- At the end of the skill (after all reports are written), clean up: `rm -r CORPUS_TMP_PATH` (note: no `-f` flag; if this triggers a permission prompt, that's expected)

**Build the index:**
- Glob all `.md` files under `$CORPUS_ROOT`.
- Exclude any corpus file whose filename matches a draft file's basename (skip files that are part of the draft set).
- **Exclude hidden and deprecated pages:** For each corpus file, check the frontmatter for `hidden: true` or `deprecated: true`. Skip any file where either field is `true` — these pages are not published and must not appear in overlap reports or cross-link candidates. ReadMe frontmatter uses YAML at the top of the file; check only the first ~15 lines for these fields.
  ```python
  # Example exclusion check
  with open(path) as f:
      head = f.read(500)
  if re.search(r'^hidden:\s*true', head, re.M) or re.search(r'^deprecated:\s*true', head, re.M):
      continue  # skip this file
  ```
- For each remaining corpus file:
  - Read the **first 40 lines** only (title + intro + top-level headings = enough signal without flooding context).
  - Extract: file path, H1 title (first `# ` heading), any H2 headings visible in the first 40 lines.
  - Derive the docs URL using **URL Derivation** (see below).
- Store as corpus index: `[{ path, title, headings[], url }]`
- Note the final count of indexed files (after exclusions) for the report header.
- Target: ~75 files × 40 lines ≈ 3,000 lines total (~12k tokens). This fits in a single pass.

### 4. Assess each draft file

For each draft file, run a single analysis pass using the draft content + corpus index.

For each corpus entry, assess against the draft:

**Overlap detection** — does the corpus page substantially cover the same ground as a section of the draft?
- Look for: same concept explained, same steps described, same parameters listed, same terminology defined.
- Severity:
  - **HIGH**: Draft reproduces content almost verbatim, or covers the exact same task/concept with no additive value.
  - **MEDIUM**: Draft and corpus page cover the same territory but from different angles; significant overlap but not identical.
  - **LOW**: Minor thematic overlap (e.g., both mention the same concept); not enough to cause confusion.
- For each overlap: identify the draft section (heading + approx. line range) and the corpus file.

**Cross-link candidates** — should the draft link to this corpus page?
- Link candidate criteria: the corpus page explains a concept the draft assumes, covers a prerequisite step, is the canonical reference for something the draft mentions in passing, or is the natural "next page" for a reader following this guide.
- For each candidate: identify where in the draft to add the link (section heading or specific paragraph context), suggest anchor text, and explain why in one sentence.

**Intra-guide links** (folder input only) — if the input was a folder with multiple draft files, flag where the draft files should cross-link each other.
- Only surface these if the link would be genuinely useful (not every file needs to link every other file).

### 5. Rank results

- **Overlaps**: sort HIGH → MEDIUM → LOW within each draft file's section.
- **Cross-link candidates**: sort by relevance — most tightly related corpus pages first (same product area > adjacent area > general product concepts).
- Omit LOW severity overlaps if there are more than 5 of them (cap at 5 LOW entries to avoid noise).

### 6. Validate output directory

- Check if `docs/output/_process/link-check/` exists (relative to the working directory).
- If not, create it: `mkdir -p docs/output/_process/link-check/`
- Abort with error if creation fails.

### 7. Write report

For each draft file, write one report to:
`docs/output/_process/link-check/{INPUT_BASENAME}-link-check.md`

See **Report Format** below.

### 8. Clean up temp clone

```bash
rm -r CORPUS_TMP_PATH
```
Note: `rm -rf` is blocked by the deny list. Use `rm -r` instead. A permission prompt may appear.

Run this after all reports are written, before displaying the summary.

### 9. Update tracking ticket (if ticket ID provided)

If a ticket ID was parsed from `$ARGUMENTS`, post a comment to the ticket summarising the cross-link findings. Format:

```
Link-check complete. Cross-links to add across [N] docs:

- [Doc name]: linked [page title] [where] — [one-line reason].
...

Overlaps: [N] MEDIUM. Reports: docs/output/_process/link-check/
```

Use your team's ticket tool to post the comment (Linear, Jira, GitHub Issues, etc.).

### 10. Display summary

After all reports are written (and ticket updated if applicable):

```
Cross-link check complete.

Draft files analyzed: [N]
Corpus files scanned: [N] (hidden/deprecated excluded)

Reports:
  docs/output/_process/link-check/{basename}-link-check.md
  ...

Overlaps found: [total HIGH/MEDIUM/LOW counts]
Cross-link candidates: [total count]
[Ticket updated: DOC-XXXX (comment + [N] attachments)]
```

No changes are made to any source file.

---

## URL Derivation

Convert a local corpus file path to its public docs URL.

**Rule:** Use the filename stem as the URL slug. ReadMe uses the file's slug (filename without extension), not the full directory path.

```
~/projects/{YOUR_DOCS_REPO}/docs/section/page.md
→ https://{YOUR_DOCS_SITE}/docs/page

~/projects/{YOUR_DOCS_REPO}/docs/section/subfolder/configure-webhooks.md
→ https://{YOUR_DOCS_SITE}/docs/configure-webhooks
```

**Steps:**
1. Take the filename (last path component).
2. Strip the `.md` extension.
3. Prepend `https://{YOUR_DOCS_SITE}/docs/`.

Do not use the directory path — ReadMe slugs are flat regardless of folder structure.

---

## Report Format

```markdown
# Cross-Link Report: [INPUT_BASENAME]

**Draft:** `[filepath]`
**Corpus:** [N] docs scanned (hidden/deprecated pages excluded)
**Generated:** [YYYY-MM-DD]

---

## Overlaps — Content to Remove or Summarize

Existing docs that already cover content in your draft. Avoid reproducing; link instead.

> No overlaps found.
```
*(If no overlaps, show this line and skip the section body.)*

```markdown
### HIGH: [Section heading in draft] → [Existing Doc Title](url)

**Why:** [1–2 sentences on what overlaps and where.]
**Action:** Remove or condense lines ~[N]–[N]; add a link to the existing page.

---

### MEDIUM: [Section heading in draft] → [Existing Doc Title](url)

**Why:** [1–2 sentences.]
**Action:** Keep draft's angle; add a "See also" link to the existing page.

---

### LOW: [Section heading in draft] → [Existing Doc Title](url)

**Why:** [1 sentence.]
**Action:** Optional — add inline link if context warrants it.

---

## Cross-Link Candidates — Links to Add

Existing docs your draft should reference.

> No cross-link candidates found.
```
*(If no candidates, show this line and skip the section body.)*

```markdown
### [Existing Doc Title](url)

**Link in:** [Section heading or location in draft]
**Suggested text:** `"[anchor text]"`
**Why:** [1 sentence.]

---

## Intra-Guide Links
```
*(Only include this section if input was a folder with multiple draft files AND intra-guide links were identified. If none, omit the section entirely.)*

```markdown
### [Draft File A] → [Draft File B]

**Link in:** [Section in File A]
**Suggested text:** `"[anchor text]"`
**Why:** [1 sentence.]
```

---

## Error Handling

| Situation | Behavior |
|-----------|----------|
| No `$ARGUMENTS` | Stop: show usage message |
| Path doesn't exist | Stop: "File not found: [path]" or "Directory not found: [path]" |
| Directory has no `.md` files | Stop: "No markdown files found in: [path]" |
| Draft file >1500 lines | Note in report header; continue |
| Corpus file unreadable | Skip it; note in report: "⚠️ [N] corpus files skipped (unreadable)" |
| Output directory creation fails | Stop: "Cannot create output directory: docs/output/_process/link-check/" |
| Report write fails | Stop: "Cannot write report: [path]" |

**Philosophy:** Stop on input/output errors. Degrade gracefully on individual corpus file failures.

---

## Notes

- This skill is **read-only** for all source files. Nothing is modified.
- Run this **after** `/docs-diataxis-audit` (structure), **before** submitting for review or opening a PR.
- The corpus is always a fresh shallow clone from `{YOUR_ORG}/{YOUR_DOCS_REPO}` — guaranteed to be at HEAD, not dependent on local clone state.
- The corpus index reads only the first 40 lines per file — deep section-level overlap in large corpus files may not be caught. For thorough analysis of a specific suspected overlap, read both files in full.
- URL derivation uses the filename stem only (ReadMe flat slugs). If a corpus file uses a non-default slug, the derived URL may be wrong — verify edge cases manually.
- Intra-guide links (folder input) are only surfaced when the link would be genuinely useful, not exhaustively between every pair of files.
