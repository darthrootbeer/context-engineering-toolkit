---
name: docs-pipeline
description: Guided docs improvement pipeline — walks through audit, split (if needed), style passes, reviews, decision checkpoint, and publish in sequence. Loads one stage at a time to preserve context quality. Use when processing a doc end-to-end.
argument-hint: <ticket-id> <slug>
allowed-tools: [Read, Write, Edit, Glob, Grep, Bash, Agent]
---

# docs-pipeline

Guided end-to-end pipeline for improving a documentation page. Runs each stage sequentially, pausing for review between stages. Loads only the context needed for the current stage to keep quality high.

## Arguments

The user provided: $ARGUMENTS

- `$ARGUMENTS[0]` — Ticket ID (e.g., `TICKET-1801`) OR path to an existing workspace directory
- `$ARGUMENTS[1]` — Guide slug (e.g., `webhooks`, `backend-integration`) — required if arg 0 is a ticket ID, ignored if arg 0 is a workspace path

**Required.** If missing, stop: `"Usage: /docs-pipeline TICKET-1801 webhooks"`

If a single path is provided that looks like a workspace (contains `docs/input/`), use it directly. Otherwise, derive the workspace path from the ticket ID and slug.

---

## Pipeline Overview

```
Stage 0: Workspace           → create or reuse the workspace directory
Stage 1: Audit               → classify the doc, determine if split is needed
Stage 2: Split               → extract into typed docs (skip if not needed)
Stage 3: Style passes        → structure → voice → human → readability → proofread (sequential)
Stage 4: Reviews             → visuals → links → SME review → changes summary
Stage 5: Decision checkpoint → resolve all recommendations before publish
Stage 6: Publish             → branch, PR, verify
```

Each stage ends with a summary and a prompt: **"Proceed to Stage N?"** The user can:
- **proceed** — continue to the next stage
- **skip** — jump past the current stage
- **stop** — end the pipeline here (work so far is saved)
- **redo** — re-run the current stage with adjustments

---

## Stage 0: Workspace Setup

**Goal:** Ensure a workspace exists with the source doc ready.

### 0a. Determine workspace path

```
TICKET_ID = first argument (e.g., TICKET-1801)
SLUG = second argument (e.g., webhooks)
TICKET_NUM = numeric portion of TICKET_ID
PROJECT_NAME = "workspace_doc-{TICKET_NUM}_{SLUG}"
PROJECT_PATH = ~/projects/{PROJECT_NAME}
```

### 0b. Check for existing workspace

If `PROJECT_PATH` already exists:
1. Print: `"Workspace found at {PROJECT_PATH}, reusing it."`
2. Verify the directory tree exists (`docs/input/`, `docs/output/`, etc.). Create any missing subdirectories.
3. Check if a source doc exists in `docs/input/`. Print the filename if yes, warn if no.
4. Check if an audit already exists in `docs/output/_process/diataxis-audit/`. If yes, note it.
5. Skip to the workspace summary below.

If `PROJECT_PATH` does not exist:
1. Run the full `/docs-workspace-setup` process: create directory, git init, directory tree, shared resource symlinks, CLAUDE.md, README.md, .gitignore.
2. Search `{YOUR_DOCS_REPO_PATH}` for a file matching the slug and copy it to `docs/input/`.

### 0c. Workspace summary

```
## Stage 0 Complete: Workspace

Path:       {PROJECT_PATH}
Source doc:  {filename in docs/input/ or "missing — copy manually"}
Audit:      {exists / not yet}

→ Next: Stage 1 (audit).
Proceed to Stage 1?
```

**Wait for user response before continuing.**

---

## Stage 1: Diataxis Audit

**Goal:** Classify the doc's content and determine whether it needs splitting.

### 1a. Check for existing audit

Check `docs/output/_process/diataxis-audit/` for an existing audit report and JSON mapping.

If both exist:
- Read the audit report
- Read the JSON mapping
- Skip to the audit summary below
- Note: "Audit already completed. Using existing results."

### 1b. Run the audit

**Follow the complete `/docs-diataxis-audit` process** (`docs-diataxis-audit.md`). Read that skill file and execute all steps. Do not abbreviate or skip steps.

The audit skill produces three mandatory outputs — all three must exist before Stage 1 is complete:

1. **Audit report** (`{GUIDE_NAME}_audit-report.md`) — full analysis with content breakdown, boundary violations, and restructuring recommendations
2. **JSON mapping** (`{GUIDE_NAME}_mapping.json`) — section-level mapping with hash IDs following the schema at `_shared/schemas/diataxis-audit-mapping/schema.json`
3. **SVG visualizations** (`{GUIDE_NAME}_00-overview.svg`, `{GUIDE_NAME}_01-*.svg`, ...) — generated via `node _shared/tools/diataxis-mapper/generate-svg.js --multi`

`{GUIDE_NAME}` is the slug from the workspace folder name (e.g., `configure-webhooks` from `workspace-doc-1318-configure-webhooks`). All output files in the workspace (except `docs/input/`) must be prefixed with this guide name.

**Do not proceed to the audit summary until all three outputs exist.** If SVG generation fails, note the error but still require the report and mapping before continuing.

After the audit, determine the split recommendation:
- **No split needed** — the doc is cleanly one Diataxis type
- **Split recommended** — the doc contains content belonging to 2+ types

### 1c. Audit summary

Present the result clearly:

**If no split needed:**
```
## Stage 1 Complete: Audit

This doc is a clean [type]. No split needed.

Current issues found:
- [list any structural issues, missing sections, etc.]

→ Skipping Stage 2 (split). Next: Stage 3 (style passes).
Proceed to Stage 3?
```

**If split recommended:**
```
## Stage 1 Complete: Audit

This doc should split into:
- [type]: [description of what goes in this doc]
- [type]: [description]
- Overview: entry-point page linking the set

→ Next: Stage 2 (split).
Proceed to Stage 2?
```

**Wait for user response before continuing.**

---

## Stage 2: Diataxis Split (conditional)

**Skip this stage entirely if the audit determined no split is needed.**

### 2a. Execute the split

Follow the same process as `/docs-diataxis-split`:
- Read the audit report and JSON mapping
- Extract content from the source doc into typed output files
- Create an overview doc

### 2b. Generate overview

Follow the same process as `/docs-diataxis-create-overview`:
- Read the split output docs
- Generate the overview entry-point page

### 2c. Split summary

```
## Stage 2 Complete: Split

Created [N] docs:
- [filename] (type: [type]) — [one-line summary]
- [filename] (type: [type]) — [one-line summary]
- overview.md — entry-point linking the set

Files are in: [output path]

→ Next: Stage 3 (style passes).
Proceed to Stage 3?
```

**Wait for user response before continuing.**

---

## Stage 3: Style Passes

Run three passes sequentially on the output docs (or the single doc if no split happened). Each pass loads its own style guide fresh.

**Target files:** If a split happened, process all docs in the output folder. If no split, process the single source doc.

### 3a. Structure check

**Follow the complete `/docs-style-check-structure` process** (`docs-style-check-structure.md`). Read that skill file and execute all steps against the output docs.

Present summary:
```
### Stage 3a: Structure check complete

[N] files checked, [M] edits made:
- [filename]: [brief description of changes]
- [filename]: no changes needed

Proceed to voice check (3b)?
```

**Wait for user response.**

### 3b. Voice check

**Follow the complete `/docs-style-check-voice` process** (`docs-style-check-voice.md`). Read that skill file and execute all steps against the output docs.

Present summary:
```
### Stage 3b: Voice check complete

[N] files checked, [M] edits made:
- [filename]: [brief description of changes]

Proceed to human check (3c)?
```

**Wait for user response.**

### 3c. Human check (de-AI)

**Follow the complete `/docs-style-check-human` process** (`docs-style-check-human.md`). Read that skill file and execute all steps against the output docs.

Present summary:
```
### Stage 3c: Human check complete

[N] files checked, [M] edits made:
- [filename]: [brief description of changes]

Proceed to readability check (3d)?
```

**Wait for user response.**

### 3d. Readability check (sentence complexity)

**Follow the complete `/docs-readability-check` process.** The skill file ships in this repo at `skills/docs-readability-check/SKILL.md`. Read it and execute all steps against the output docs.

Present summary:
```
### Stage 3d: Readability check complete

[N] files checked, [M] edits made:
- [filename]: grade level [before] → [after] ([status: within target / improved / still above target])
- Wall paragraphs flagged for manual review: [K]

Proceed to proofread check (3e)?
```

**Wait for user response.**

### 3e. Proofread check (grammar, spelling, terminology)

**Follow the complete `/docs-grammar-spelling` process** (`docs-grammar-spelling.md`). Read that skill file and execute all steps against the output docs.

Present summary:
```
### Stage 3e: Proofread check complete

[N] files checked, [M] fixes applied, [K] flags for review:
- Terminology: [N]
- Spelling: [N]
- Grammar: [N]
- Punctuation: [N]
- Consistency: [N]

→ Stage 3 complete. Next: Stage 4 (reviews).
Proceed to Stage 4?
```

**Wait for user response.**

---

## Stage 4: Reviews

Pre-publish quality checks. These produce recommendations, not edits.

### 4a. Visuals review

**Follow the complete `/docs-visuals-review` process** (`docs-visuals-review.md`). Read that skill file and execute all steps against the output docs folder.

Present recommendations (do not auto-create diagrams):
```
### Stage 4a: Visuals review

[filename]:
- [location]: Recommend [type] diagram showing [what]
- [location]: Recommend [type] showing [what]

[filename]:
- No visual aids recommended

Proceed to links review (4b)?
```

**Wait for user response.**

### 4b. Links review

**Follow the complete `/docs-links-review` process** (`docs-links-review.md`). Read that skill file and execute all steps against the output docs folder.

Present candidates:
```
### Stage 4b: Links review

Cross-link candidates:
- [doc]: consider linking to [existing doc] re: [topic]
- [doc]: overlaps with [existing doc] — deduplicate or cross-reference

Proceed to SME review (4c)?
```

**Wait for user response.**

### 4c. SME review

**Follow the complete `/docs-sme-review` process** (`docs-sme-review.md`). Read that skill file and execute all steps against the output docs folder.

Present findings:
```
### Stage 4c: SME review

Domain accuracy: [N] HIGH, [N] MEDIUM
Reader journey: [N] findings
Naming collisions: [N] findings
Component opportunities: [N] suggestions
Technical clarity: [N] findings
Proofreading: [N] findings

Reports: _process/sme-review/

Proceed to changes summary (4d)?
```

**Wait for user response.**

### 4d. Changes summary

**Follow the complete `/docs-changes-list` process** (`docs-changes-list.md`). Read that skill file and execute all steps. It reads the original doc, output docs, audit report, and visual audit to auto-fill all sections and writes `editorial-changes.md` to the `_process/` directory.

```
### Stage 4d: Changes summary written

→ editorial-changes.md created at [path]
→ Stage 4 complete. Next: Stage 5 (decision checkpoint).
Proceed to Stage 5?
```

**Wait for user response.**

---

## Stage 5: Decision Checkpoint

**Goal:** Resolve every open recommendation before publishing. Nothing goes to Stage 6 with unresolved items.

**Follow the complete `/docs-decision-checkpoint` process** (`docs-decision-checkpoint.md`). Read that skill file and execute all steps against the output docs folder.

The skill collects all unresolved flags from the style audit and all recommendations from the reviews (visuals, links), writes a `recommendations.md` document to `_process/`, and walks the user through apply/skip/defer decisions for each item.

```
### Stage 5 complete

Applied: {N} items
Skipped: {N} items
Deferred: {N} items

→ Next: Stage 6 (publish).
Proceed to Stage 6?
```

**Wait for user response.**

---

## Stage 6: Publish

### 6a. Pre-publish validation

Before publishing, run quick checks:
- All docs have required docs platform frontmatter (`title`, `slug`, `excerpt`, `hidden`, `createdAt`, `updatedAt` — adjust fields for your platform)
- No unescaped curly braces or dollar signs outside code fences
- All internal links resolve

Report any issues. If issues found, fix them before proceeding.

### 6b. Publish

Follow the `/docs-publish` process:
- Copy output docs to `{YOUR_DOCS_REPO}`
- Add/update docs platform frontmatter
- Create `_order.yaml` if needed (platform-specific)
- Create a feature branch
- Open a draft PR

### 6c. Pipeline complete

```
## Pipeline Complete

**Source:** [original file]
**Output:** [N] docs published
**PR:** [link to PR]

Stages completed:
✓ Audit — [result summary]
✓ Split — [split/skipped]
✓ Style — structure, voice, human, readability, grammar
✓ Reviews — visuals, links, SME review, changes
✓ Decisions — [N] applied, [N] skipped, [N] deferred
✓ Publish — PR #[N] opened

Next: ask reviewer to check the PR, then run `/docs-work-verify` after merge.
```

---

## Important Rules

- **One stage at a time.** Never load multiple style guides simultaneously. Read the guide for the current pass, complete the pass, then move on.
- **Always pause between stages.** Show the summary, ask to proceed. Never auto-advance.
- **Track all changes.** Every edit made during style passes should be noted for the changes summary in Stage 4c.
- **Workspace-aware.** If running in a `/docs-workspace-setup` workspace, use its directory structure. If running on a standalone file, create output artifacts alongside the file.
- **Respect exit points.** If the user says "stop", end gracefully. Summarize what was completed and what remains.
- **No duplicate work.** If a stage was already completed (e.g., audit exists from a previous run), skip it and note that it was pre-completed.
- **No unresolved recommendations at publish.** Stage 5 must complete before Stage 6. Every flag and recommendation gets an explicit apply/skip/defer decision.
