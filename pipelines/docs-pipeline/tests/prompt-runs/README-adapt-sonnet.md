# README-adapt on sonnet

Prompt (inputs filled with made-up samples):

```text
I have attached the README for "docs-pipeline". I want to try it on one short document before I trust it on a real doc set.

It is a 60-line markdown file about resetting an API key. It lives in docs/guides/reset-api-key.md.

Write me a trial plan that uses only the stages that do not need a docs platform: the audit, the style passes, the readability check, and the grammar check. For each stage give the exact slash command from the README, what the README says that stage produces, and one sign that the stage went wrong. Finish with the knowledge files I must fill in before I run it, and how I will know the trial worked.

A good answer uses the real command names from the README, leaves out the publish and verify stages, describes each stage's output only as the README does, and does not predict what the stage will find in my document.
```

Answer:

# Trial plan: `docs/guides/reset-api-key.md`

The README doesn't name an output file for most stages, so where it only describes what a stage does, I quote that instead of inventing an artifact.

## Before you start

1. Install the skills with the loop in section 3 of SETUP.md.
2. Run the smoke test in section 4 of SETUP.md. It uses the bundled sample doc and needs no configuration.
3. Fill in the knowledge files (listed at the end).
4. Run `/docs-workspace-setup`. The README says it creates the workspace, copies in `_knowledge/`, and writes starter files. It's Stage 0 rather than one of your five, but the knowledge files are copied into the workspace here, so it has to come after you fill them in. The README doesn't show its arguments, so check SETUP.md or the skill file.

The README says nothing moves to the next stage until a person says so, so review each stage's result before starting the next.

## Stages, in README order

| Stage | Command | What the README says it produces | One sign it went wrong |
|---|---|---|---|
| 1 | `/docs-diataxis-audit docs/guides/reset-api-key.md` | Classifies doc content by Diataxis type and produces an audit report plus a JSON mapping | Either the report or the JSON mapping is missing |
| 3a | `/docs-style-check-structure` | Checks required sections, headings, and Diataxis structural rules | The stage touches files other than your document |
| 3b | `/docs-style-check-voice` | Applies the general style guide's voice, tone, list formatting, and terminology rules | A change contradicts a rule you wrote in `style-guide_general.md` |
| 3c | `/docs-style-check-human` | Removes AI writing patterns (em dashes, filler phrases, uniform sentences) | It alters literal content such as commands, key names, or code samples |
| 3d | `/docs-readability-check` | Estimates reading grade level, finds dense sentence patterns, and rewrites them to the target level for the doc type | It rewrites sentences without ever stating a grade level estimate |
| 3e | `/docs-grammar-spelling` | Grammar, spelling, and domain terminology check | A term is changed to something that isn't in your `glossary.yaml` |

Two notes:

- **Skipped stages:** I left out split (2), overview (2b), and everything from 4a onward, including publish and verify.
- **Argument for the style stages:** The README's examples show `/docs-diataxis-audit` taking a file path and `/docs-style-check-human` taking a directory (`docs/output/docs/`). It doesn't say how a doc reaches the output folder when you skip the split. Before running 3a, check what path each skill expects.

For every stage, a general sign of trouble is that it leaves no commit. The README says each stage commits its output so changes can be traced to the stage that made them.

## Knowledge files to fill in first

Each has fill-in instructions at the top, and the README says to fill them in before creating a workspace:

- `_knowledge/glossary.yaml`: your terminology, canonical forms, and common mistakes. This is what the grammar and terminology stages rely on.
- `_knowledge/style-guides/general/style-guide_general.md`: your voice, tone, and formatting rules. This is what the voice stage applies.
- `_knowledge/product-kb/`: your product model (endpoints, domain objects, error codes, and so on). The README ties it to Stage 4c, which isn't in this trial. It ships as a made-up "Acme Orders API", and Stage 0 copies it into the workspace either way, so replace it if you want the workspace to hold only your own material.

The README's Configuration placeholders (`{YOUR_ORG}`, `{YOUR_DOCS_REPO}`, and so on) have names that point at publishing. The README doesn't say which skills contain them, so search the five trial skills for `{YOUR_` before running them.

## How you'll know the trial worked

The README doesn't define success, so these criteria are mine, built from what it promises:

1. Every stage ran in order and produced what the README says it should (the audit's report and JSON, and the other stages' described edits or checks).
2. Each stage left its own commit, so you can open the history and tie every change to one stage.
3. You read each stage's diff and could accept or reject its changes. The gates only mean something if you actually used them.
4. Nothing outside your document changed, and no stage touched literal commands or key names.
5. Knowledge files drove the result: a terminology or style change traces back to a rule you wrote, not one inherited from the Acme starters.

The README says it can vouch only for how the pipeline behaved on the author's docs, not yours. This trial is your evidence on that point.

