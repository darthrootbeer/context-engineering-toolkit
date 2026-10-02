# docs-pipeline

**What this is.** A chain of Claude Code skills that takes a documentation change from a rough draft to a published pull request, one stage at a time. Each stage has one job: classify the content, split mixed docs apart, fix structure and voice, check readability and grammar, recommend diagrams and links, review accuracy. Nothing moves to the next stage until a person says so. Before anything is published, every open recommendation gets an explicit apply, skip, or defer decision.

**Why it is the best thing in this repo.** I used a version of it every working day on real documentation, and no other piece here has had that much real use. What makes it work is that the order and the gates are fixed. Style passes run before reviews, so the reviewers never read prose that still needs cleaning. Each stage commits its output, so every change can be traced to the stage that made it. And the human decision comes last, where it counts. The reason to read it is the structure, which you can copy to other kinds of work, more than any single skill.

**How it was built, and what it does not claim.** Claude Code wrote these skills under my direction. I set the requirements, ran them on real documentation, read what came out, and corrected what was wrong. I did not type them by hand. This is prompts, ordering, and checks. There is no model training, no machine-learning pipeline, no retrieval system, and no claim to production ML experience. The copy here is a generic export of the version I used: you fill in the placeholders and the knowledge files before it fits your docs, and the publish and verify stages assume a git-based docs repo. I can vouch for how it behaved on my own docs, not on yours.

Each skill is a markdown file that Claude Code loads when you run the matching `/skill-name` command.

## Skills in this export

| File | Slash command | Stage | What it does |
|------|--------------|-------|--------------|
| `docs-pipeline.md` | `/docs-pipeline` | Orchestrator | Runs the full pipeline end-to-end, stage by stage |
| `docs-workspace-setup.md` | `/docs-workspace-setup` | 0 | Creates the workspace directory, copies in the knowledge files, and writes the starter files |
| `docs-diataxis-audit.md` | `/docs-diataxis-audit` | 1 | Classifies doc content by Diataxis type, produces audit report + JSON mapping |
| `docs-diataxis-split.md` | `/docs-diataxis-split` | 2 | Extracts content into typed output files (how-to, explanation, reference, tutorial) |
| `docs-diataxis-create-overview.md` | `/docs-diataxis-create-overview` | 2b | Creates the overview/index entry-point doc after a split |
| `docs-style-check-structure.md` | `/docs-style-check-structure` | 3a | Checks required sections, headings, and Diataxis structural rules |
| `docs-style-check-voice.md` | `/docs-style-check-voice` | 3b | Applies general style guide voice, tone, list formatting, and terminology rules |
| `docs-style-check-human.md` | `/docs-style-check-human` | 3c | Removes AI writing patterns (em dashes, filler phrases, uniform sentences) |
| `../../skills/docs-readability-check/SKILL.md` | `/docs-readability-check` | 3d | Estimates reading grade level, finds dense sentence patterns, and rewrites them to the target level for the doc type |
| `docs-grammar-spelling.md` | `/docs-grammar-spelling` | 3e | Grammar, spelling, and domain terminology check |
| `docs-visuals-review.md` | `/docs-visuals-review` | 4a | Recommends diagrams and visual aids; Mermaid-first |
| `docs-links-review.md` | `/docs-links-review` | 4b | Finds cross-link candidates against the full docs corpus |
| `docs-sme-review.md` | `/docs-sme-review` | 4c | Domain accuracy, reader journey, naming collisions, technical clarity |
| `docs-changes-list.md` | `/docs-changes-list` | 4d | Generates `editorial-changes.md` summarising everything done |
| `docs-decision-checkpoint.md` | `/docs-decision-checkpoint` | 5 | Walks through every open recommendation: apply / skip / defer |
| `docs-publish.md` | `/docs-publish` | 6 | Copies output to docs repo, adds frontmatter, creates branch + PR |
| `docs-work-verify.md` | `/docs-work-verify` | Post | Verifies the PR merged and changes are live |

## Quick start

1. Install the skills with the loop in section 3 of [SETUP.md](./SETUP.md).
2. Run the smoke test in section 4 of [SETUP.md](./SETUP.md). It uses the sample doc in [`sample/`](./sample/acme-orders-cancellations.md) and needs no configuration.
3. Replace the made-up product knowledge in `_knowledge/` with your own (next section), then fill in the placeholders under Configuration.

## Knowledge sources

The pipeline loads three knowledge sources at runtime. They ship as working starters, so it runs from a fresh clone. The product knowledge base describes a made-up product (the "Acme Orders API"), so replace it with your own before you trust Stage 4c on real docs:

| Path | What it needs |
|------|--------------|
| `_knowledge/glossary.yaml` | Your domain terminology, canonical forms, and common mistakes |
| `_knowledge/product-kb/` | Your product model: integration types, API endpoints, domain objects, webhooks, error codes |
| `_knowledge/style-guides/general/style-guide_general.md` | Your voice, tone, and formatting rules |

Each file has fill-in instructions at the top. Stage 0 copies the whole `_knowledge/` folder into every new workspace, so fill these in before you create one.

## Pipeline order

```
workspace → audit → split → structure → voice → human → readability
         → grammar → visuals → links → SME → changes → decisions → publish → verify
```

## Usage

Run the full pipeline with:

```
/docs-pipeline TICKET-1319 setup-and-credentials
```

Or invoke individual skills directly for targeted work:

```
/docs-diataxis-audit docs/input/authentication.md
/docs-style-check-human docs/output/docs/
```

See `ARCHITECTURE.md` for how the pipeline fits together.

## Configuration

Before using this pipeline on your docs, replace these placeholders throughout the skill files:

| Placeholder | What to replace it with |
|-------------|------------------------|
| `{YOUR_ORG}` | Your GitHub organization name |
| `{YOUR_DOCS_REPO}` | Your docs repository name |
| `{YOUR_DOCS_SITE}` | Your published docs site domain (e.g., `docs.example.com`) |
| `{YOUR_ISSUE_TRACKER}` | Your ticket tool URL base (e.g., `linear.app/yourorg/issue`) |
| `{YOUR_TICKET_URL}` | Full base URL for tickets |
| `{YOUR_USERNAME}` | Your git username for branch naming |
| `{YOUR_DOCS_REPO_PATH}` | Local filesystem path to your docs repo clone |
| `{YOUR_DEFAULT_OG_IMAGE_URL}` | Default Open Graph image URL for published docs |

Two placeholders are optional. `{SHARED_CONFIG_DIR}` (a folder of your own shared tools) and `{NOTES_DIR}` (a notes folder for a project note) can stay as they are: any step that needs them is skipped. `{YOUR_PIPELINE_DIR}` is filled in by the install loop in SETUP.md, so you do not set it by hand.

---

### Prompt for your AI model

Paste this into any AI model, together with this document and the files it describes.

**Understand and teach**

```text
I have attached the README for "docs-pipeline", a set of Claude Code skills that improve documentation in fixed stages. Teach it to me as if I am a technical writer who has never used it.

1. In plain language, say what problem it solves and what it does not do.
2. List the stages in order, one line each, and explain why the style passes come before the reviews.
3. Say exactly what the person does between every two stages, and what the AI does alone inside a stage.
4. Then ask me three questions to check that I understood, one at a time. Wait for my answer before the next one, and correct me where I am wrong.

A good answer names every stage in order, names the readability check as Stage 3d and grammar as Stage 3e, explains that nothing moves forward without a person's go-ahead (so it never says the person does not touch a stage), and repeats the limits the README states. It must not invent a stage, a command, or a file that is not in the README.
```

**Review against your own setup**

```text
I have attached the README for "docs-pipeline". Below is a description of my own documentation setup.

[PASTE a short description of your docs: where the files live, what site or platform publishes them, how you track the work, who reviews changes, and which AI coding tool you use.]

Using only the README, tell me:
1. Which stages I can use as they are.
2. Which stages I would have to adapt, and what I would change.
3. Which stages I should skip, and why.
4. Every placeholder in the README's Configuration table, with the value from my setup that should replace it. If my description does not give a value, write "not in my description" instead of guessing.

A good answer covers all four points, uses the README's own stage names, and never invents a value for a placeholder.
```

**Adapt and test**

```text
I have attached the README for "docs-pipeline". I want to try it on one short document before I trust it on a real doc set.

[PASTE a short description of the document you will try it on: its length, what it is about, and where it lives.]

Write me a trial plan that uses only the stages that do not need a docs platform: the audit, the style passes, the readability check, and the grammar check. For each stage give the exact slash command from the README, what the README says that stage produces, and one sign that the stage went wrong. Finish with the knowledge files I must fill in before I run it, and how I will know the trial worked.

A good answer uses the real command names from the README, leaves out the publish and verify stages, describes each stage's output only as the README does, and does not predict what the stage will find in my document.
```

**How these prompts were checked.** On 2026-10-01 I ran every prompt in this document through the Claude Code command line, once against Claude Sonnet and once against Claude Haiku (the `sonnet` and `haiku` model names in Claude Code 2.1.287). Each run was a fresh session with no tools and no other instructions. I attached this document and any other file the prompt names, replaced each bracketed input with a made-up sample, and read every answer against that prompt's "good answer" list. I have not run them against models from other vendors, so "any AI model" means "should work", not "verified".

| Prompt | Sonnet | Haiku |
| --- | --- | --- |
| Understand and teach | Pass | Pass |
| Review against your own setup | Pass | Pass. It credited the README with a phrase the README does not contain. |
| Adapt and test | Pass | Pass after a fix. The first version asked what I "should expect to see", and Haiku answered with confident predictions about a document it had never seen. The prompt now asks only for what the README says each stage produces. |

