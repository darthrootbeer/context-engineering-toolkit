# SETUP.md — docs-pipeline

This is a set of Claude Code skills that takes existing documentation through a structured improvement pipeline: audit → split → style passes → reviews → publish. Each skill is a markdown instruction file. Claude Code reads the file and executes the steps when you invoke the corresponding `/skill-name` command.

This guide is for you, or an AI agent working for you, setting up the pipeline for a new documentation project. Read it top to bottom before running anything.

---

## 1. Prerequisites

Before running any skill:

- **Claude Code** installed and available as `claude` in the terminal
- **GitHub CLI** (`gh`) installed and authenticated for the org that owns the docs repo (`gh auth login`)
- **Git** installed
- **Node.js** with `markdownlint-cli` available (`npm install -g markdownlint-cli`) — required by `docs-publish`
- A docs repository with markdown files to improve
- A published docs site (or a staging environment) that the repo syncs to
- A docs platform that matches the skills' assumption. Stages 2, 4b and 6 assume a git repo that syncs to ReadMe (readme.com): flat slugs, ReadMe frontmatter, blockquote callouts. Other platforms need those three skills adapted.

---

## 2. Configuration — replace all placeholders

Every skill file contains placeholder values in `{CURLY_BRACES}`. Replace the ones you need before you install the skills in section 3 (the install step copies the files, so a change made later needs a re-install). Do a find-and-replace across all `.md` files in this directory.

Which placeholders you need depends on the stages you use. The smoke test in section 4 needs none of them. Stages 4b (links), 4c (the naming-collision part only), 6 (publish) and the post-merge check need the docs-repo placeholders.

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

Three more placeholders are optional. Leave them as they are unless you want the feature:

| Placeholder | What it is | If you leave it unset |
|-------------|-----------|-----------------------|
| `{SHARED_CONFIG_DIR}` | A folder of your own shared tools (for example a JSON schema or a diagram generator) | The steps that need it are skipped |
| `{NOTES_DIR}` | A notes folder (for example an Obsidian vault) where Stage 0 writes a project note | No project note is written |
| `{YOUR_PIPELINE_DIR}` | The path of this folder | You do not set this by hand: the install loop in section 3 fills it in |

**One-liner to find all remaining `{YOUR_` placeholders**, run from inside this folder:

```bash
grep -rl '{YOUR_' . --include='*.md'
```

`{YOUR_PIPELINE_DIR}` will still show up in the source files. That is expected: it is filled in on the installed copies, not here.

---

## 3. Install the skills

Claude Code loads a skill from `<skills folder>/<name>/SKILL.md`. The files in this folder are flat (`docs-pipeline.md`, `docs-sme-review.md`, ...), so copying the folder as it is will not register them. This loop makes one folder per skill and fills in `{YOUR_PIPELINE_DIR}` on the way.

Run it from inside this folder (`pipelines/docs-pipeline/` in your clone of the repo):

```bash
PIPELINE_DIR="$PWD"
SKILLS_DIR="$HOME/.claude/skills"   # use ./.claude/skills instead to install for one project only

for f in docs-*.md; do
  name="${f%.md}"
  mkdir -p "$SKILLS_DIR/$name"
  sed "s|{YOUR_PIPELINE_DIR}|$PIPELINE_DIR|g" "$f" > "$SKILLS_DIR/$name/SKILL.md"
done

# the readability stage (3d) lives in the repo's skills/ folder
mkdir -p "$SKILLS_DIR/docs-readability-check"
cp ../../skills/docs-readability-check/SKILL.md "$SKILLS_DIR/docs-readability-check/SKILL.md"
```

This installs 17 skills: the 16 `docs-*.md` files here plus `docs-readability-check`. Run it again any time you edit a file. Keep your clone where it is: the skills read `_knowledge/` and `workspace-gitignore.template` from `PIPELINE_DIR`.

**Check that they registered.** Start a new Claude Code session and type `/docs-`. The list should show all 17 names. Or run this from the shell and count the lines (it should print 17):

```bash
claude -p "hi" --model haiku --output-format stream-json --verbose | grep -o '"docs-[a-z-]*"' | sort -u | wc -l
```

If the count is lower, the loop wrote to a different folder than the one Claude Code reads: check `SKILLS_DIR`, and start a fresh session.

---

## 4. Smoke test

The starter `_knowledge/product-kb/index.md` ships with an `extracted:` date. Once that date is more than 90 days old, Stage 4c reports a staleness warning on the starter data. Update the date to today when you replace the starter KB (section 5).

First, an offline check that needs no model. From the root of your clone, run `python3 pipelines/docs-pipeline/tests/check_pipeline.py`. It confirms that every knowledge file the skills name exists and that the folder holds no private paths. It should print `check_pipeline: clean`.

Then the real test. This runs the pipeline on a short sample doc that ships in this folder (`sample/acme-orders-cancellations.md`, a made-up doc about a made-up product). It stops before anything is published and needs no placeholders. Run these in Claude Code:

1. `/docs-workspace-setup TICKET-1 smoke-test` and answer `y`. This creates `~/projects/workspace_doc-1_smoke-test/` with a copy of `_knowledge/`.
2. In that folder, copy the sample in: `cp "<path to this folder>/sample/acme-orders-cancellations.md" docs/output/docs/`
3. `/docs-style-check-voice docs/output/docs/` (Stage 3b). It edits the sample in place and writes a report to `docs/output/_process/style-audit/`.
4. `/docs-sme-review docs/output/docs/` (Stage 4c). It writes `acme-orders-cancellations-sme-review.md` and a summary into a `_process/sme-review/` folder (the model may place it under `docs/output/` or at the workspace root).

**What proves it worked.** Stage 3b does not stop with "Style guide not found". The sample has a casual opener, so the voice report lists at least one tone fix. Stage 4c does not stop with "Product KB not found". Its report lists at least these three HIGH domain findings, because the sample contradicts `_knowledge/product-kb/`: a paid order cannot be canceled, the hosted order form does not receive webhooks, and the rate limit is 100 a minute, not a thousand.

**Undo.** Delete the folder `~/projects/workspace_doc-1_smoke-test/`. Nothing else was changed.

---

## 5. Knowledge sources — build before running

Three knowledge sources live in `_knowledge/`. They are loaded by the accuracy-sensitive pipeline stages. Each one ships as a working starter, so the pipeline runs from a fresh clone. The glossary and style guides are generic. The product knowledge base describes a made-up product (the "Acme Orders API") and must be replaced with your own before Stages 3e and 4c mean anything on real docs.

Stage 0 copies `_knowledge/` into every new workspace, so fill these files in once, in this folder, before you create workspaces. A workspace made earlier keeps its old copy.

Populate all three before running a full pipeline on any real docs.

---

### 5.1 Glossary — `_knowledge/glossary.yaml`

**Loaded by:** `docs-grammar-spelling` (Stage 3e)

**What it does:** The grammar skill loads this file, builds a term index, and enforces canonical forms throughout every doc — capitalization, acronym expansion, deprecated terms, API field formatting.

**Minimum viable:** 10–20 terms covering your most commonly misused or misformatted words. The skill won't flag what isn't in the glossary.

**Structure:** Each entry has a `canonical` form, optional `aliases`, `docs_facing` flag (false = internal-only; flag if found in customer docs), and a `usage` block with capitalization rules and known mistakes. See the placeholder file for the full format.

**AI prompt to populate it:**

> "List every product-specific term, acronym, API resource name, and concept name used in our docs. For each, tell me: the canonical spelling and capitalization, any aliases or alternate forms people use, whether it's customer-facing or internal, and any common mistakes you've seen."

Then translate each answer into a glossary entry following the YAML structure in `_knowledge/glossary.yaml`.

---

### 5.2 Product knowledge base — `_knowledge/product-kb/`

**Loaded by:** `docs-sme-review` (Stage 4c)

**What it does:** The SME review skill loads these files and fact-checks every claim in the draft docs against your actual product model — integration type scopes, API resource availability, webhook event mappings, error code meanings. It flags content that would mislead a customer following the docs.

**Files and what to put in each.** All seven files ship as starters with fill-in instructions at the top and a few fictional example rows (marked `FICTIONAL EXAMPLE DATA`). Delete the example rows and add yours:

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

### 5.3 Style guide — `_knowledge/style-guides/general/style-guide_general.md`

**Loaded by:** `docs-style-check-voice` (Stage 3b)

**What it does:** The voice skill reads every rule in this file and applies them to the draft docs — rewriting prose that violates voice, tone, list formatting, callout syntax, and addressing conventions.

**Minimum viable:** The shipped file already contains a working baseline (imperative steps, sentence-case headings, "you" for the reader, no marketing language, numbered lists with lead-ins and outcome sentences). Its examples use the made-up Acme Orders product. This is enough to run Stage 3b on any docs. Stages 3a, 3c and the Diataxis audit read the other folders under `_knowledge/style-guides/` the same way.

**To make it yours:** Add or override rules for your specific conventions. Common additions:
- Product name capitalization and formatting
- Preferred terminology for your domain ("customers" vs. "developers" vs. "clients")
- Callout syntax for your docs platform (if different from the ReadMe defaults in the baseline)
- Any structural patterns your team has agreed on (e.g. always include a Prerequisites section)

**AI prompt to populate it:**
> "What are the voice, tone, and formatting conventions we follow in our docs? Cover: how we address the reader, how we write steps vs. concepts, how we use callouts, any words or phrases we avoid, how we capitalize product names, and any patterns we always or never do."

### Prompt for your AI model

Paste this into any AI model, together with this document and the files it describes.

```text
I have attached the setup guide for "docs-pipeline" and its placeholder file `_knowledge/glossary.yaml`. Below is some text from my own documentation.

[PASTE two or three paragraphs from your docs that use your product's own terms.]

Following section 5.1 of the guide and the structure in the placeholder file, draft a first `glossary.yaml` with the 10 most important terms from my text. For every entry give the canonical form, the aliases only if my text shows them, and the docs_facing flag. Where my text does not show a capitalization rule or a common mistake, leave that field out and write "needs review" instead of inventing one. Do not infer a capitalization rule from how a word happens to be capitalized in my text.

A good answer uses the field names from the placeholder file exactly, has no more than 10 entries, and marks everything it could not know as "needs review".
```

**How this prompt was checked.** On 2026-10-01 this prompt was run under my direction against Claude Sonnet and Claude Haiku, with this guide and `_knowledge/glossary.yaml` attached and a made-up paragraph of product text. A Claude model (Sonnet 5.5) graded each answer against the prompt's "good answer" line; I have not re-read every answer. Sonnet passed. The first version made Haiku invent capitalization rules from how words happened to be capitalized in my sample. The prompt now forbids that, and both models passed on the rerun.

---

## 6. Running the pipeline

### Full pipeline

```
/docs-pipeline TICKET-ID slug
```

Example:
```
/docs-pipeline TICKET-1234 order-cancellations
```

The pipeline creates a workspace at `~/projects/workspace_doc-1234_order-cancellations/`, copies the source doc(s) into `docs/input/`, and walks through each stage. It pauses between stages and asks to proceed. You can say `proceed`, `skip`, `stop`, or `redo`.

### Individual skills

Any skill can be run standalone on a file or folder:

```
/docs-diataxis-audit docs/input/order-cancellations.md
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

## 7. Skill-to-knowledge dependency map

| Skill | Knowledge file(s) loaded | If missing or empty |
|-------|--------------------------|---------------------|
| `docs-style-check-voice` | `_knowledge/style-guides/general/style-guide_general.md` | Skill stops: "Style guide not found" |
| `docs-grammar-spelling` | `_knowledge/glossary.yaml` | Skill stops: "Glossary not found" |
| `docs-sme-review` | `_knowledge/product-kb/index.md` + relevant sub-files | Skill stops: "Product KB not found" |
| `docs-diataxis-audit` | `_knowledge/style-guides/diataxis/README.md` | Skill stops if the framework file is missing |
| `docs-style-check-structure` | `_knowledge/style-guides/diataxis/` | Skill stops: "Style guide not found" |
| `docs-style-check-human` | `_knowledge/style-guides/write-like-a-human/` | Skill stops: "Style guide not found" |
| `docs-diataxis-split` | Audit report + JSON mapping from Stage 1 | Requires Stage 1 output |
| `docs-links-review` | Live docs corpus (cloned from `{YOUR_DOCS_REPO}`) | Stops if clone fails |
| `docs-sme-review` naming-collision check | Live docs corpus (same clone) | Skipped with a note, the rest of the review runs |
| All others | None | Run without external knowledge sources |

---

## 8. Keeping knowledge current

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
| `style-guides/general/style-guide_general.md` | Style decision changes; new convention agreed; platform callout syntax changes | Voice audit flags the same pattern as wrong repeatedly |

When you update any `product-kb/` file, update the `extracted:` date in `product-kb/index.md`.

---

## 9. Troubleshooting

| Error | Cause | Fix |
|-------|-------|-----|
| `Style guide not found at _knowledge/style-guides/general/style-guide_general.md` | You are not running from inside a workspace, or the workspace has no `_knowledge/` copy | Run from the workspace folder, or copy `_knowledge/` into it. Check the `STYLE_GUIDE` constant in `docs-style-check-voice.md` |
| `Glossary not found at _knowledge/glossary.yaml` | File missing or path wrong | Check `GLOSSARY` constant in `docs-grammar-spelling.md` |
| `Product KB not found at _knowledge/product-kb/` | You are not running from inside a workspace, or the workspace has no `_knowledge/` copy | Run from the workspace folder, or copy `_knowledge/` into it |
| `PIPELINE_DIR is not set` | The skills were copied without the install loop | Re-run the loop in section 3 |
| `Failed to clone docs repo` | `gh` not authenticated or repo name wrong | Run `gh auth login`; check `{YOUR_ORG}/{YOUR_DOCS_REPO}` |
| `No output docs found in docs/output/docs/` | Split hasn't run yet | Run Stage 2 first |
| `Branch already exists` | Previous partial run | Delete the branch: `git branch -D {branch-name}` |
| `Product KB last extracted >90 days ago` | Staleness warning, not a stop | Update KB files and refresh `extracted:` date in `index.md` |
| Placeholders like `{YOUR_ORG}` still appearing in output | Configuration incomplete | Run the grep one-liner from section 2 to find remaining placeholders |

---

### Prompt for your AI model

Paste this into any AI model, together with this document and the files it describes.

**Understand and teach**

```text
I have attached the setup guide for "docs-pipeline". Teach it to me as if I am an engineer who has never used it.

1. Turn the guide into a numbered checklist in the order I should do things, with one sentence on why each step exists.
2. Say which steps I can skip for a first trial and which I cannot.
3. Then ask me three questions to check that I understood, one at a time. Wait for my answer before the next one, and correct me where I am wrong.

A good answer follows the guide's order, covers the prerequisites, the placeholders, the install loop, the smoke test, the knowledge sources, and running the pipeline, and does not add a step the guide does not contain.
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
I have attached the setup guide for "docs-pipeline". Section 4 is a smoke test on a sample doc. I want to run the same test on one of my own short docs instead.

[PASTE the file name of your doc and a one-line description of what it is about.]

Rewrite the smoke test in section 4 for my doc. Change only what has to change for my file. Keep every command the guide gives, in the guide's order. In the copy command, write my doc's location as `<path to my doc>`. Say which placeholders in section 2 I still do not need to fill in for this test. Do not invent a command or a file path. Do not predict what any stage will find in my doc. If my doc cannot be checked the way section 4 describes (for example because it is not about a product the knowledge files describe), say so plainly.

A good answer keeps the guide's commands and order, changes only the file name and where the guide's expected results depend on the sample doc, stops before the publish stage, repeats the guide's undo step, and says that Stage 4c checks my doc against the knowledge files, which describe a made-up product until I replace them.
```

**How these prompts were checked.** On 2026-10-01 every prompt in this document was run under my direction through the Claude Code command line, once against Claude Sonnet and once against Claude Haiku (the `sonnet` and `haiku` model names in Claude Code 2.1.287). Each run was a fresh session with no tools and no other instructions. This document and any other file the prompt names were attached, each bracketed input was replaced with a made-up sample, and a Claude model (Sonnet 5.5) graded each answer against that prompt's "good answer" list, which was written before the run. I have not re-read every answer. One run per prompt per model: a Pass means that run met the list, not that the prompt always does. I re-ran all four prompts after the fresh-clone fixes on the same day, and the answers are saved in [`tests/prompt-runs/`](./tests/prompt-runs/README.md). I have not run them against models from other vendors, so "any AI model" means "should work", not "verified".

| Prompt | Sonnet | Haiku |
| --- | --- | --- |
| Glossary (section 5.1) | Pass | Pass |
| Understand and teach | Pass | Pass. It told me to replace every placeholder before the smoke test, although section 4 says the smoke test needs none. |
| Review against your own setup | Pass | Pass |
| Adapt and test | Pass | Pass on the third version of the prompt. The earlier version of this prompt, which asked the model to write a smoke test from nothing, failed on Haiku on both runs because it wrote its own shell commands. The guide now has a smoke test, so the prompt adapts that one. Two further wording fixes were needed: forbid predictions about the reader's doc, and write the doc's location as `<path to my doc>`. |
