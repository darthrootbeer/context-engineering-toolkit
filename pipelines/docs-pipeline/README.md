# docs-pipeline — Skill Export

Exported Claude Code skills for a Diataxis-based docs improvement pipeline.

Each file is a `SKILL.md` — a prompt-based instruction set loaded by Claude Code when you invoke the corresponding `/skill-name` command.

## Skills in this export

| File | Slash command | Stage | What it does |
|------|--------------|-------|--------------|
| `docs-pipeline.md` | `/docs-pipeline` | Orchestrator | Runs the full pipeline end-to-end, stage by stage |
| `docs-workspace-setup.md` | `/docs-workspace-setup` | 0 | Creates the workspace directory, symlinks, and project note |
| `docs-diataxis-audit.md` | `/docs-diataxis-audit` | 1 | Classifies doc content by Diataxis type, produces audit report + JSON mapping |
| `docs-diataxis-split.md` | `/docs-diataxis-split` | 2 | Extracts content into typed output files (how-to, explanation, reference, tutorial) |
| `docs-diataxis-create-overview.md` | `/docs-diataxis-create-overview` | 2b | Creates the overview/index entry-point doc after a split |
| `docs-style-check-structure.md` | `/docs-style-check-structure` | 3a | Checks required sections, headings, and Diataxis structural rules |
| `docs-style-check-voice.md` | `/docs-style-check-voice` | 3b | Applies general style guide voice, tone, list formatting, and terminology rules |
| `docs-style-check-human.md` | `/docs-style-check-human` | 3c | Removes AI writing patterns (em dashes, filler phrases, uniform sentences) |
| `docs-grammar-spelling.md` | `/docs-grammar-spelling` | 3d | Grammar, spelling, and domain terminology check |
| `docs-visuals-review.md` | `/docs-visuals-review` | 4a | Recommends diagrams and visual aids; Mermaid-first |
| `docs-links-review.md` | `/docs-links-review` | 4b | Finds cross-link candidates against the full docs corpus |
| `docs-sme-review.md` | `/docs-sme-review` | 4c | Domain accuracy, reader journey, naming collisions, technical clarity |
| `docs-changes-list.md` | `/docs-changes-list` | 4d | Generates `editorial-changes.md` summarising everything done |
| `docs-decision-checkpoint.md` | `/docs-decision-checkpoint` | 5 | Walks through every open recommendation: apply / skip / defer |
| `docs-publish.md` | `/docs-publish` | 6 | Copies output to docs repo, adds frontmatter, creates branch + PR |
| `docs-work-verify.md` | `/docs-work-verify` | Post | Verifies the PR merged and changes are live |

## Knowledge sources

The pipeline loads three knowledge sources at runtime. Populate these before running:

| Path | What it needs |
|------|--------------|
| `_knowledge/glossary.yaml` | Your domain terminology, canonical forms, and common mistakes |
| `_knowledge/product-kb/` | Your product model: integration types, API endpoints, domain objects, webhooks, error codes |
| `_knowledge/style-guides/style-guide.md` | Your voice, tone, and formatting rules |

Placeholder files with structure and instructions are already in `_knowledge/`. Fill them in before running `docs-grammar-spelling`, `docs-sme-review`, or `docs-style-check-voice`.

## Pipeline order

```
workspace → audit → split → structure → voice → human → grammar
         → visuals → links → SME → changes → decisions → publish → verify
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
