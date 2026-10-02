# README-review on sonnet

Prompt (inputs filled with made-up samples):

```text
I have attached the README for "docs-pipeline". Below is a description of my own documentation setup.

My docs are markdown files in a GitHub repository called acme-docs. A static site generator publishes them to docs.acme.example. I track work in Jira. One senior writer reviews every change. I use Claude Code.

Using only the README, tell me:
1. Which stages I can use as they are.
2. Which stages I would have to adapt, and what I would change.
3. Which stages I should skip, and why.
4. Every placeholder in the README's Configuration table, with the value from my setup that should replace it. If my description does not give a value, write "not in my description" instead of guessing.

A good answer covers all four points, uses the README's own stage names, and never invents a value for a placeholder.
```

Answer:

# docs-pipeline fit for acme-docs

## 1. Stages you can use as they are

These don't depend on your platform, only on the knowledge files and placeholders being filled in:

- **Orchestrator** (`/docs-pipeline`). Its example ticket `TICKET-1319` is the same shape as a Jira key.
- **Stage 0**, `/docs-workspace-setup`
- **Stage 1**, `/docs-diataxis-audit`
- **Stage 2**, `/docs-diataxis-split`
- **Stage 3a-3e**, the structure, voice, human, readability and grammar checks
- **Stage 4a**, `/docs-visuals-review`. Mermaid-first, which fits markdown files, though the README doesn't say whether your site generator renders Mermaid.
- **Stage 4b**, `/docs-links-review`
- **Stage 4c**, `/docs-sme-review`
- **Stage 4d**, `/docs-changes-list`
- **Stage 5**, `/docs-decision-checkpoint`

Before 3b, 3e and 4c are trustworthy, replace the starter `_knowledge/` files (style guide, glossary, product KB). The README says the product KB describes a made-up "Acme Orders API".

## 2. Stages to adapt

- **Stage 6, `/docs-publish`.**
  - It copies output to the docs repo, adds frontmatter, and creates a branch and PR. That matches a GitHub-hosted markdown repo.
  - Check that the frontmatter it adds matches what your static site generator expects. The README doesn't list the fields, so read the skill file.
  - Check how it names branches (`{YOUR_USERNAME}`) and links tickets, so Jira keys and URLs come out right.
  - Check whether the PR is assigned to your senior writer. The README doesn't say.
- **Post stage, `/docs-work-verify`.** It verifies the PR merged and the changes are live. Point its "live" check at docs.acme.example. Your description doesn't say whether the generator deploys on merge, so confirm that.
- **Stage 5, the decision checkpoint.** The README says a person decides apply, skip or defer. Your description doesn't say who that is, so decide whether it is you, with the senior writer reviewing the PR, or the senior writer at this stage.

## 3. Stages to skip

Nothing in your description requires skipping a stage. Two are conditional:

- **Stage 2 (split) and Stage 2b (`/docs-diataxis-create-overview`).** Skip them for a change whose audit shows a single doc type. 2b exists only to create an overview after a split.

## 4. Configuration table placeholders

| Placeholder | Value from your setup |
|---|---|
| `{YOUR_ORG}` | not in my description |
| `{YOUR_DOCS_REPO}` | `acme-docs` |
| `{YOUR_DOCS_SITE}` | `docs.acme.example` |
| `{YOUR_ISSUE_TRACKER}` | not in my description (the tool is Jira, but no URL base is given) |
| `{YOUR_TICKET_URL}` | not in my description |
| `{YOUR_USERNAME}` | not in my description |
| `{YOUR_DOCS_REPO_PATH}` | not in my description |
| `{YOUR_DEFAULT_OG_IMAGE_URL}` | not in my description |

Three placeholders sit outside the table. `{SHARED_CONFIG_DIR}` and `{NOTES_DIR}` are optional, and any step that needs them is skipped if you leave them. `{YOUR_PIPELINE_DIR}` is filled in by the SETUP.md install loop.

