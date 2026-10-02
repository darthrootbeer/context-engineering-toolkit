# Saved prompt runs

These are the answers behind the "How these prompts were checked" paragraphs in the docs-pipeline README, the SETUP guide, and the readability skill README.

**How they were produced.** On 2026-10-01 each prompt was run through the Claude Code command line (`claude -p`, version 2.1.287) with no tools and no other instructions, once on `sonnet` and once on `haiku`. The document the prompt names (plus `_knowledge/glossary.yaml` for the glossary prompt) was pasted after the prompt, and each bracketed input was replaced with a made-up sample. Each saved file shows the exact prompt that was sent, then the answer.

**How they were graded.** The agent that ran them (Claude Sonnet 5.5, working under my direction) read each answer against that prompt's own "good answer" list. One run per prompt per model, so a Pass here says "this run met the list", not "this prompt always does". The maintainer has not re-read every answer.

File names: `README-*` is the docs-pipeline README, `SETUP-*` is `SETUP.md`, `RC-*` is the README of `skills/docs-readability-check`. The ARCHITECTURE prompts and the prompts at the end of the style guides were checked on 2026-10-01 before this folder existed, and no records of those runs were kept.

| Prompt | Sonnet | Haiku |
|---|---|---|
| README, understand and teach | Pass | Pass. It said the pipeline "works through seven stages", which counts the numbered stage groups and is not a figure the README states. |
| README, review against your own setup | Pass | Pass. It did not list the three optional placeholders, which the README describes in prose and not in the table. |
| README, adapt and test | Pass | Pass |
| SETUP, glossary | Pass (8 entries, because the sample text supports no more) | Pass |
| SETUP, understand and teach | Pass | Pass. It told me to replace every placeholder before the smoke test, although section 4 says the smoke test needs none. |
| SETUP, review against your own setup | Pass | Pass |
| SETUP, adapt and test | Pass | Pass on the third version of the prompt (see below) |
| Readability README, understand and teach | Pass | Pass on the second version of the prompt (see below) |
| Readability README, review against your own setup | Pass | Pass. It said all three of the sample's doc types match, where "conceptual pages" only loosely matches the README's "explanation". |
| Readability README, adapt and test | Pass | Pass. It suggested `webhook-retries-trial.md` as a name for the copy, which is an example and not a path from the README. |

## Prompts that failed first and were changed

The earlier versions that were kept are in `earlier-versions/`.

- **Readability README, understand and teach, Haiku (v1).** The prompt asked for what the skill checks and changes. Haiku never stated the target grade for any doc type, then asked a quiz question that said the answer was in what it had just told me, which it was not. The prompt now asks for the target grade for each doc type.
- **SETUP, adapt and test, Haiku (v1, kept).** Haiku predicted what Stage 4c would report for the reader's own doc, which the guide does not say. The prompt now says "Do not predict what any stage will find in my doc".
- **SETUP, adapt and test, Haiku (v2, not kept).** The answer to the second version of the prompt kept `sample/` in the copy command, so the command pointed at a folder that does not exist for the reader's own doc. That file was overwritten by the next run and I did not keep it. The prompt now asks for the doc's location to be written as `<path to my doc>`. The third version passed on Haiku and Sonnet.

The first version of the SETUP "adapt and test" prompt (before the guide had a smoke test) failed on Haiku in an earlier check. That is why this prompt now adapts the guide's own smoke test instead of asking the model to write one from nothing.
