---
name: docs-diataxis-create-overview
description: Create an overview entry-point doc for a Diataxis split guide set. Reads the output docs in a folder, extracts titles/types/summaries, and generates an index.md following the established format. Use after a split is complete, before audit-links.
argument-hint: [docs-folder] [area-prefix]
allowed-tools: [Read, Write, Glob, Bash]
---

# docs-diataxis-create-overview

Create a standalone overview doc for a Diataxis guide set. The overview is the entry point and navigation hub — it does not contain conceptual explanation, steps, or API specs.

## Arguments

The user provided: $ARGUMENTS

- `$ARGUMENTS[0]` — Path to the docs folder containing output docs (e.g., `docs/output/docs`)
- `$ARGUMENTS[1]` — Area prefix for the filename (e.g., `webhooks`) — optional

**Required:** At least the docs folder path. If missing, stop:
`"Please provide the docs folder: /docs-diataxis-create-overview [docs-folder] [area-prefix]"`

## Constants

```
REFERENCE_DOC=./_knowledge/style-guides/diataxis/style-guide_guide-set-overview.md
```

---

## Steps

### 1. Validate inputs and discover docs

**Parse arguments:**
- `DOCS_DIR = $ARGUMENTS[0]` (strip trailing slash)
- `AREA_PREFIX = $ARGUMENTS[1]` (optional)

**Find output docs:**
```bash
ls {DOCS_DIR}/*.md 2>/dev/null
```
If zero `.md` files found: stop — `"No docs found in {DOCS_DIR}. Run the split first."`

If an overview doc already exists in the folder (any file with `diataxis_type: overview` in frontmatter), stop:
`"Overview doc already exists: {filename}. Delete it first if you want to regenerate."`

**Auto-detect area prefix (if not provided):**
Extract the filename stems of all docs in `DOCS_DIR`. Find the most common leading segment (everything before the first `-`). If all files share the same prefix, use it. If ambiguous, prompt:
`"Could not infer area prefix from filenames. Enter it (e.g., 'webhooks'):"`

Store as `AREA_PREFIX`.

---

### 2. Read all output docs

Read each `.md` file in `DOCS_DIR`. For each doc, extract:

- **H1 title**: First `# ` heading (or frontmatter `title:` if no H1)
- **`diataxis_type`**: From frontmatter. If absent, infer from filename prefix as fallback:
  - `explanation-*` → `explanation`
  - `how-to-*` → `how-to`
  - `reference-*` → `reference`
  - `tutorial-*` → `tutorial`
- **First paragraph**: First substantive prose paragraph after the H1 (skip blockquotes, callouts, and blank lines)

Store as `OUTPUT_DOCS` — a list of `{filename, title, type, summary}`.

---

### 3. Check for source doc

Look for a source document in `docs/input/`:
```bash
ls docs/input/*.md 2>/dev/null
```

If found, read it and extract:
- **Guide title**: H1 heading or frontmatter `title:`
- **Opening paragraph**: First substantive prose paragraph after the H1
- **Audience section**: Content of any section titled "Audience", "Who this is for", or similar
- **Prerequisites section**: Content of any section titled "Prerequisites", "Before you start", or similar

If no source doc exists, synthesize these from the output docs:
- **Guide title**: Humanize the area prefix (e.g., `webhooks` → "Webhooks", `configure-webhooks` → "Configure Webhooks")
- **Opening paragraph**: Synthesize from the typed docs' titles and purposes: `"This guide covers everything you need to [action implied by how-to title] using the product API."`
- **Audience**: `"Integration engineers and product managers integrating with the Acme Orders API."`
- **Prerequisites**: `"An active Acme Orders integration. If you haven't set that up yet, start with [getting started with Acme Orders](https://docs.example.com/docs/get-started)."`

---

### 4. Build "What's in this guide" list

For each entry in `OUTPUT_DOCS`, generate a bullet:

```markdown
- **[{title}](./{filename})**. {One sentence describing what this doc contains and when to read it.}
```

**Order:** Explanation → How-to → Reference → Tutorial (Diataxis reading order)

The one-sentence description names the reader's purpose, not just the doc type:
- **Explanation**: Draw from the doc's first paragraph. Pattern: "[Topic]. [What the reader will understand.]"
- **How-to**: Draw from the doc's first paragraph. Pattern: "Step-by-step instructions for [action]."
- **Reference**: Draw from the doc's first paragraph. Pattern: "Complete specs for [what's covered]."
- **Tutorial**: Draw from the doc's first paragraph. Pattern: "Hands-on walkthrough to [outcome]."

---

### 5. Write the overview doc

**Filename:** `{GUIDE_PREFIX}_overview.md` during drafting (in the workspace), where `GUIDE_PREFIX` is the guide name slug from the workspace folder name (e.g., `intro-to-billing` from `workspace_doc-1318_intro-to-billing`). At publish time, `/docs-publish` renames this to `index.md` in the guide's subdirectory.

If no workspace context exists (standalone run), fall back to `index.md`.

**Frontmatter:**

```yaml
---
diataxis_type: overview
hidden: true
robots: noindex
---
```

**Body:**

```markdown
# {Guide Title}

{Opening orientation paragraph — 1–3 sentences. What this guide covers and what capability it enables. Draw from source doc if available.}

## Audience

{1–2 sentences. Who this is for. Assumed background.}

## Prerequisites

{2–4 sentences. What must already be in place before starting. Include links to upstream docs where appropriate.}

## What's in this guide

{Bulleted list from step 4, in Diataxis reading order}
```

**Quality checks before writing:**
- 15–25 body lines (after frontmatter). Route, don't inform.
- Bullet descriptions name the reader's purpose, not just the doc type.
- No original content — everything draws from existing docs or the source.
- Audience names a role + assumed baseline.
- Prerequisites are specific and link to upstream docs.
- No conceptual explanation (that's the explanation doc).
- No numbered steps (that's the how-to doc).
- No field tables or API specs (that's the reference doc).

Write to `{DOCS_DIR}/index.md`.

---

### 6. Display summary

```
Created: {DOCS_DIR}/index.md

  Title:      {Guide Title}
  Type:       overview
  Body lines: {N}

  Links to:
    - {filename} [{type}]
    - {filename} [{type}]
    - ...

  Source doc used: {yes/no — path if yes}
```

---

## Error Handling

| Situation | Behavior |
|-----------|----------|
| Missing docs folder argument | Stop, show usage |
| Docs folder empty or not found | Stop: "No docs found in {path}. Run the split first." |
| Overview doc already exists | Stop: "Overview doc already exists: {filename}. Delete it first." |
| Area prefix not provided and not inferrable | Prompt for it |
| Source doc not found | Continue — synthesize from output docs |
| Output file already exists | Stop: "File already exists: {path}. Delete it first." |

---

## Reference

The overview doc follows the rules in `REFERENCE_DOC` (`_knowledge/style-guides/diataxis/style-guide_guide-set-overview.md`). Key characteristics:

- Short (15–25 body lines). Its job is to route, not inform.
- Opening paragraph orients the reader to the product capability, not to the docs themselves.
- Audience and Prerequisites are factual and direct — no marketing language.
- "What's in this guide" bullets are linked and describe the reader's *purpose* in going to that doc, not just what the doc contains.
- Nothing in the overview doc is original content — it draws from the source doc's existing orientation language and from the typed docs' titles/purposes.

---

## Notes

- The overview doc does NOT include orientation callouts or a "Related documentation" section — those are for typed docs that need cross-navigation. The overview IS the navigation.
- If the folder already has an overview doc (detected by `diataxis_type: overview` in frontmatter), the skill stops. Delete the existing one first if regenerating.
- This skill is standalone — it does not depend on `/docs-diataxis-audit` or `/docs-diataxis-split` having been run, only on output docs existing in the folder.
- At publish time, `/docs-publish` merges the overview doc's body into `index.md` so the guide's landing page renders the overview content directly. The overview is not published as a separate child page.
- Trigger: after the split is complete, before `/docs-links-review`.
