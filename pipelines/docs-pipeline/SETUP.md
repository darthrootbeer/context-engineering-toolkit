# SETUP.md — docs-pipeline

This is a set of Claude Code skills that takes existing documentation through a structured improvement pipeline: audit → split → style passes → reviews → publish. Each skill is a markdown instruction file. Claude Code reads the file and executes the steps when you invoke the corresponding `/skill-name` command.

This guide is for an AI agent setting up the pipeline for a new documentation project. Read it top to bottom before running anything.

---

## 1. Prerequisites

Before running any skill:

- **Claude Code** installed and available as `claude` in the terminal
- **GitHub CLI** (`gh`) installed and authenticated for the org that owns the docs repo (`gh auth login`)
- **Git** installed
- **Node.js** with `markdownlint-cli` available (`npm install -g markdownlint-cli`) — required by `docs-publish`
- A docs repository with markdown files to improve
- A published docs site (or a staging environment) that the repo syncs to

---

## 2. Configuration — replace all placeholders

Every skill file contains placeholder values in `{CURLY_BRACES}`. Replace them before running any skill. Do a find-and-replace across all `.md` files in this directory.

| Placeholder | What it is | Example |
|-------------|-----------|---------|
| `{YOUR_ORG}` | GitHub organization name | `acme-corp` |
| `{YOUR_DOCS_REPO}` | Docs repository name | `acme-docs` |
| `{YOUR_DOCS_SITE}` | Published docs domain | `docs.acme.com` |
| `{YOUR_DOCS_REPO_PATH}` | Local filesystem path to the docs repo clone | `~/projects/acme-docs` |
| `{YOUR_ISSUE_TRACKER}` | Ticket tool URL base | `linear.app/acme/issue` |
| `{YOUR_TICKET_URL}` | Full base URL for tickets | `https://linear.app/acme/issue` |
| `{YOUR_USERNAME}` | Git username for branch naming | `jsmith` |
| `{YOUR_DEFAULT_OG_IMAGE_URL}` | Default Open Graph image for published pages | `https://cdn.acme.com/og-default.png` |

**One-liner to find all remaining placeholders after replacement:**

```bash
grep -r '{YOUR_' ~/Downloads/docs-pipeline/ --include="*.md" -l
```

---

## 3. Knowledge sources — build before running

Three knowledge sources live in `_knowledge/`. They are loaded by the accuracy-sensitive pipeline stages. The pipeline will run without them, but Stages 3b, 3d, and 4c will produce shallow or incorrect results.

Populate all three before running a full pipeline on any real docs.

---

### 3.1 Glossary — `_knowledge/glossary.yaml`

**Loaded by:** `docs-grammar-spelling` (Stage 3d)

**What it does:** The grammar skill loads this file, builds a term index, and enforces canonical forms throughout every doc — capitalization, acronym expansion, deprecated terms, API field formatting.

**Minimum viable:** 10–20 terms covering your most commonly misused or misformatted words. The skill won't flag what isn't in the glossary.

**Structure:** Each entry has a `canonical` form, optional `aliases`, `docs_facing` flag (false = internal-only; flag if found in customer docs), and a `usage` block with capitalization rules and known mistakes. See the placeholder file for the full format.

**AI prompt to populate it:**

> "List every product-specific term, acronym, API resource name, and concept name used in our docs. For each, tell me: the canonical spelling and capitalization, any aliases or alternate forms people use, whether it's customer-facing or internal, and any common mistakes you've seen."

Then translate each answer into a glossary entry following the YAML structure in `_knowledge/glossary.yaml`.

---

### 3.2 Product knowledge base — `_knowledge/product-kb/`

**Loaded by:** `docs-sme-review` (Stage 4c)

**What it does:** The SME review skill loads these files and fact-checks every claim in the draft docs against your actual product model — integration type scopes, API resource availability, webhook event mappings, error code meanings. It flags content that would mislead a customer following the docs.

**Files and what to put in each:**

| File | Minimum viable content |
|------|----------------------|
| `index.md` | Update `extracted: YYYY-MM-DD` to today. This date drives the staleness warning (fires if >90 days old). |
| `integration-types.md` | Table: each integration type or product tier → what it supports, what it doesn't |
| `endpoints.md` | Each API endpoint: path, parameters, response shape, which integration types can call it |
| `domain-models.md` | Each core API object: key fields, lifecycle states and transitions, relationships |
| `error-codes.md` | Each error code: meaning, when it fires, how docs should describe it |
| `webhooks.md` | Each webhook event: payload shape, which integration types receive it |
| `recent-changes.md` | Any API or product changes in the last 90 days that might make existing docs inaccurate |

**AI prompts to populate each file:**

For `integration-types.md`:
> "Describe every integration type or product tier we offer. For each: what it is, what API resources are available, what features are built-in vs. manual, and what a developer using it can and cannot do."

For `endpoints.md`:
> "List every API endpoint. For each: the HTTP method and path, required and optional request parameters, the response object and key fields, and any restrictions on which integration types can call it."

For `domain-models.md`:
> "Describe every core object in the API. For each: what it represents, its key fields and types, the states it can be in and how it moves between them, and which other objects it relates to."

For `error-codes.md`:
> "List every error code or error type the API returns. For each: the code, when it fires, what it means to a developer, and how our docs should describe it."

For `webhooks.md`:
> "List every webhook event. For each: the event name, when it fires, the payload structure, and which integration types or product tiers receive it."

For `recent-changes.md`:
> "What has changed in the API or product in the last 90 days? List anything that might make existing documentation inaccurate — deprecated fields, renamed resources, new required parameters, changed behavior."

---

### 3.3 Style guide — `_knowledge/style-guides/style-guide.md`

**Loaded by:** `docs-style-check-voice` (Stage 3b)

**What it does:** The voice skill reads every rule in this file and applies them to the draft docs — rewriting prose that violates voice, tone, list formatting, callout syntax, and addressing conventions.

**Minimum viable:** The placeholder file already contains a working baseline (imperative steps, sentence-case headings, "you" for the reader, no marketing language, numbered lists with lead-ins and outcome sentences). This is enough to run Stage 3b on any docs.

**To make it yours:** Add or override rules for your specific conventions. Common additions:
- Product name capitalization and formatting
- Preferred terminology for your domain ("customers" vs. "developers" vs. "merchants")
- Callout syntax for your docs platform (if different from the ReadMe defaults in the baseline)
- Any structural patterns your team has agreed on (e.g. always include a Prerequisites section)

**AI prompt to populate it:**
> "What are the voice, tone, and formatting conventions we follow in our docs? Cover: how we address the reader, how we write steps vs. concepts, how we use callouts, any words or phrases we avoid, how we capitalize product names, and any patterns we always or never do."

---

## 4. Running the pipeline

### Full pipeline

```
/docs-pipeline TICKET-ID slug
```

Example:
```
/docs-pipeline TICKET-1234 payment-methods
```

The pipeline creates a workspace at `~/projects/workspace_doc-1234_payment-methods/`, copies the source doc(s) into `docs/input/`, and walks through each stage. It pauses between stages and asks to proceed. You can say `proceed`, `skip`, `stop`, or `redo`.

### Individual skills

Any skill can be run standalone on a file or folder:

```
/docs-diataxis-audit docs/input/payment-methods.md
/docs-style-check-human docs/output/docs/
/docs-sme-review docs/output/docs/ TICKET-1234
```

### What to do at each pause

| Stage | What Claude produces | Your job |
|-------|---------------------|----------|
| 1 — Audit | Classification of each doc section by Diataxis type; split recommendation | Confirm whether to split or not |
| 2 — Split | 2–5 typed output docs + overview | Skim the split; confirm filenames and content placement look right |
| 3a — Structure | In-place edits for structural compliance | Review the audit report; approve or adjust |
| 3b — Voice | In-place edits for voice/tone/formatting | Review flags; approve or adjust |
| 3c — Human | In-place edits removing AI writing patterns | Review; these are usually safe to approve |
| 3d — Grammar | In-place fixes + flags for manual review | Review the flags — these need judgment |
| 4a — Visuals | Recommendations only (no edits) | Decide which diagrams to create |
| 4b — Links | Cross-link candidates (no edits) | Decide which links to add |
| 4c — SME | Domain accuracy findings by severity | HIGH findings need your attention; verify against source of truth |
| 5 — Decisions | Interactive apply/skip/defer for all open items | Work through each one |
| 6 — Publish | Branch + PR | Review the PR description before confirming push |

---

## 5. Skill-to-knowledge dependency map

| Skill | Knowledge file(s) loaded | If missing or empty |
|-------|--------------------------|---------------------|
| `docs-style-check-voice` | `_knowledge/style-guides/style-guide.md` | Skill stops: "Style guide not found" |
| `docs-grammar-spelling` | `_knowledge/glossary.yaml` | Skill stops: "Glossary not found" |
| `docs-sme-review` | `_knowledge/product-kb/index.md` + relevant sub-files | Skill stops: "Product KB not found" |
| `docs-diataxis-audit` | None | Runs fully on built-in Diataxis knowledge |
| `docs-diataxis-split` | Audit report + JSON mapping from Stage 1 | Requires Stage 1 output |
| `docs-links-review` | Live docs corpus (cloned from `{YOUR_DOCS_REPO}`) | Stops if clone fails |
| All others | None | Run without external knowledge sources |

---

## 6. Keeping knowledge current

| File | Update when | How to know it's stale |
|------|------------|----------------------|
| `glossary.yaml` | New term added to the product; wrong capitalization found in published docs; term deprecated | Proofread reports flag the same non-glossary terms repeatedly |
| `product-kb/index.md` | Any KB file is updated | `extracted:` date >90 days → SME review reports show a staleness warning |
| `product-kb/integration-types.md` | New integration type; capability added or removed | SME review flags features as "unverified against product model" |
| `product-kb/endpoints.md` | API change; new endpoint; parameter renamed or removed | SME review flags API claims as potentially inaccurate |
| `product-kb/domain-models.md` | Object renamed; field added or removed; lifecycle changed | SME review flags object references |
| `product-kb/error-codes.md` | New error code; code meaning changed | SME review flags error handling sections |
| `product-kb/webhooks.md` | New event; event renamed; payload changed | SME review flags webhook sections |
| `product-kb/recent-changes.md` | Continuous — update as changes ship; clear entries older than 90 days | This file is meant to be a rolling window, not a permanent log |
| `style-guides/style-guide.md` | Style decision changes; new convention agreed; platform callout syntax changes | Voice audit flags the same pattern as wrong repeatedly |

When you update any `product-kb/` file, update the `extracted:` date in `product-kb/index.md`.

---

## 7. Troubleshooting

| Error | Cause | Fix |
|-------|-------|-----|
| `Style guide not found at _knowledge/style-guides/style-guide.md` | File missing or path wrong | Check `STYLE_GUIDE` constant in `docs-style-check-voice.md` |
| `Glossary not found at _knowledge/glossary.yaml` | File missing or path wrong | Check `GLOSSARY` constant in `docs-grammar-spelling.md` |
| `Product KB not found at _knowledge/product-kb/` | `index.md` missing | Populate `_knowledge/product-kb/index.md` |
| `Failed to clone docs repo` | `gh` not authenticated or repo name wrong | Run `gh auth login`; check `{YOUR_ORG}/{YOUR_DOCS_REPO}` |
| `No output docs found in docs/output/docs/` | Split hasn't run yet | Run Stage 2 first |
| `Branch already exists` | Previous partial run | Delete the branch: `git branch -D {branch-name}` |
| `Product KB last extracted >90 days ago` | Staleness warning, not a stop | Update KB files and refresh `extracted:` date in `index.md` |
| Placeholders like `{YOUR_ORG}` still appearing in output | Configuration incomplete | Run the grep one-liner from Section 2 to find remaining placeholders |
