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

Three knowledge sources live in `_knowledge/`. They are loaded by the accuracy-sensitive pipeline stages. The pipeline will run without them, but Stages 3b, 3e, and 4c will produce shallow or incorrect results.

Populate all three before running a full pipeline on any real docs.

---

### 3.1 Glossary — `_knowledge/glossary.yaml`

**Loaded by:** `docs-grammar-spelling` (Stage 3e)

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

### Prompt for your AI model

Paste this into any AI model, together with this document and the files it describes.

```text
I have attached the setup guide for "docs-pipeline" and its placeholder file `_knowledge/glossary.yaml`. Below is some text from my own documentation.

[PASTE two or three paragraphs from your docs that use your product's own terms.]

Following section 3.1 of the guide and the structure in the placeholder file, draft a first `glossary.yaml` with the 10 most important terms from my text. For every entry give the canonical form, the aliases only if my text shows them, and the docs_facing flag. Where my text does not show a capitalization rule or a common mistake, leave that field out and write "needs review" instead of inventing one. Do not infer a capitalization rule from how a word happens to be capitalized in my text.

A good answer uses the field names from the placeholder file exactly, has no more than 10 entries, and marks everything it could not know as "needs review".
```

**How this prompt was checked.** On 2026-10-01 I ran it against Claude Sonnet and Claude Haiku, attaching this guide and `_knowledge/glossary.yaml`, with a made-up paragraph of product text. Sonnet passed. The first version made Haiku invent capitalization rules from how words happened to be capitalized in my sample. The prompt now forbids that, and both models passed on the rerun.

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
| 3d — Readability | In-place sentence rewrites, grade level before and after, wall paragraphs flagged | Check the rewrites kept your meaning; split the flagged wall paragraphs yourself |
| 3e — Grammar | In-place fixes + flags for manual review | Review the flags — these need judgment |
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

---

### Prompt for your AI model

Paste this into any AI model, together with this document and the files it describes.

**Understand and teach**

```text
I have attached the setup guide for "docs-pipeline". Teach it to me as if I am an engineer who has never used it.

1. Turn the guide into a numbered checklist in the order I should do things, with one sentence on why each step exists.
2. Say which steps I can skip for a first trial and which I cannot.
3. Then ask me three questions to check that I understood, one at a time. Wait for my answer before the next one, and correct me where I am wrong.

A good answer follows the guide's order, covers the prerequisites, the placeholders, the knowledge sources, and running the pipeline, and does not add a step the guide does not contain.
```

**Review against your own setup**

```text
I have attached the setup guide for "docs-pipeline". Below is the output of the commands I ran on my machine.

[PASTE the output of: claude --version, gh auth status, git --version, node --version, markdownlint --version]

Compare my output with the "Prerequisites" section. For each prerequisite, say whether it is met, missing, or impossible to tell from my output, and quote the line of my output that shows it. Then say what I must do before the first run.

A good answer has one line per prerequisite, never marks something as met without a line of output to show it, and does not guess about anything my output does not cover.
```

**Adapt and test**

```text
I have attached the setup guide for "docs-pipeline". I want to run the smallest possible test before I use it on real documentation.

Write me a smoke test that uses one short markdown file and stops before anything is published. Say which placeholders in section 2 I can fill with dummy values for this test and which need real values, following the guide's own rule about placeholders. List the exact commands, what proves the test worked, and how to undo everything afterwards. Use only commands that appear in the guide. Where the guide has no command for something, say so and do not write one.

A good answer respects what the guide says about replacing placeholders, uses only commands the guide contains, stops before the publish stage, and says so where the guide does not give an undo step.
```

**How these prompts were checked.** On 2026-10-01 I ran every prompt in this document through the Claude Code command line, once against Claude Sonnet and once against Claude Haiku (the `sonnet` and `haiku` model names in Claude Code 2.1.287). Each run was a fresh session with no tools and no other instructions. I attached this document and any other file the prompt names, replaced each bracketed input with a made-up sample, and read every answer against that prompt's "good answer" list. I have not run them against models from other vendors, so "any AI model" means "should work", not "verified".

| Prompt | Sonnet | Haiku |
| --- | --- | --- |
| Understand and teach | Pass | Pass. It contradicted itself on whether a stage stops when a knowledge file is missing. |
| Review against your own setup | Pass | Pass |
| Adapt and test | Pass, on both runs | Fail, on both runs. It wrote its own shell commands (creating files, search and replace, deleting a folder) although the prompt says to use only commands from the guide. Use a stronger model for this one. |

