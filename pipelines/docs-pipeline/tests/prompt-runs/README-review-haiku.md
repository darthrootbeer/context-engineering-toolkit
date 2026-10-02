# README-review on haiku

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

## 1. Stages you can use as they are

All stages 1–5 and most of stage 4 are pure text-analysis stages that don't depend on your specific repository structure:

- Stage 1: diataxis-audit
- Stage 2: diataxis-split
- Stage 2b: diataxis-create-overview
- Stage 3a: style-check-structure
- Stage 3b: style-check-voice
- Stage 3c: style-check-human
- Stage 3d: readability-check
- Stage 3e: grammar-spelling
- Stage 4a: visuals-review
- Stage 4b: links-review
- Stage 4c: sme-review
- Stage 4d: changes-list
- Stage 5: decision-checkpoint

You'll need to customize the knowledge files (glossary, product KB, style guide) for accuracy, but the stage logic itself works without modification.

## 2. Stages that need adaptation

- **Stage 0 (workspace-setup)**: Needs configuration (filling in placeholders), but no code changes.

- **Stage 6 (publish)**: Needs adaptation for your docs pipeline. The stage "copies output to docs repo, adds frontmatter, creates branch + PR." You must verify:
  - What frontmatter format your static site generator expects
  - Whether the branch naming and PR creation logic match your GitHub workflow for acme-docs
  - How commit messages should be constructed

- **Post stage (verify)**: Needs adaptation to your deployment process. The stage "verifies the PR merged and changes are live." You need to adapt how it checks docs.acme.example—whether it waits for a deploy trigger, polls the site, or uses another verification method specific to your static site generator.

## 3. Stages to skip

The README states "any step that needs them is skipped" if you leave the optional placeholders `{SHARED_CONFIG_DIR}` and `{NOTES_DIR}` unset. However, **the README does not list which specific stages require these optional placeholders**, so you cannot determine from the README alone which stages to skip. You would need to read the individual skill files.

## 4. Configuration placeholders

| Placeholder | Value |
|---|---|
| `{YOUR_ORG}` | not in my description |
| `{YOUR_DOCS_REPO}` | acme-docs |
| `{YOUR_DOCS_SITE}` | docs.acme.example |
| `{YOUR_ISSUE_TRACKER}` | not in my description |
| `{YOUR_TICKET_URL}` | not in my description |
| `{YOUR_USERNAME}` | not in my description |
| `{YOUR_DOCS_REPO_PATH}` | not in my description |
| `{YOUR_DEFAULT_OG_IMAGE_URL}` | not in my description |

