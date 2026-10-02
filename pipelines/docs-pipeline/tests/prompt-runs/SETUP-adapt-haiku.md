# SETUP-adapt on haiku

Prompt (inputs filled with made-up samples):

```text
I have attached the setup guide for "docs-pipeline". Section 4 is a smoke test on a sample doc. I want to run the same test on one of my own short docs instead.

reset-api-key.md. It explains how to reset an API key from the dashboard.

Rewrite the smoke test in section 4 for my doc. Change only what has to change for my file. Keep every command the guide gives, in the guide's order. In the copy command, write my doc's location as `<path to my doc>`. Say which placeholders in section 2 I still do not need to fill in for this test. Do not invent a command or a file path. Do not predict what any stage will find in my doc. If my doc cannot be checked the way section 4 describes (for example because it is not about a product the knowledge files describe), say so plainly.

A good answer keeps the guide's commands and order, changes only the file name and where the guide's expected results depend on the sample doc, stops before the publish stage, repeats the guide's undo step, and says that Stage 4c checks my doc against the knowledge files, which describe a made-up product until I replace them.
```

Answer:

## Smoke test for reset-api-key.md

This runs the pipeline on your doc (`reset-api-key.md`, explaining how to reset an API key from the dashboard). It stops before anything is published and needs no placeholders. Run these in Claude Code:

1. `/docs-workspace-setup TICKET-1 smoke-test` and answer `y`. This creates `~/projects/workspace_doc-1_smoke-test/` with a copy of `_knowledge/`.
2. In that folder, copy your doc in: `cp "<path to my doc>/reset-api-key.md" docs/output/docs/`
3. `/docs-style-check-voice docs/output/docs/` (Stage 3b). It edits your doc in place and writes a report to `docs/output/_process/style-audit/`.
4. `/docs-sme-review docs/output/docs/` (Stage 4c). It writes `_process/sme-review/reset-api-key-sme-review.md`.

**What proves it worked.** Stage 3b does not stop with "Style guide not found". Stage 4c does not stop with "Product KB not found".

**About the Stage 4c findings.** Stage 4c checks your doc against the knowledge files in `_knowledge/product-kb/`, which currently describe a made-up product (the Acme Orders API). Until you replace them with your actual product's specifications, the SME review will compare your doc against that fictional product model.

**Placeholders you do not need.** None. The smoke test needs zero placeholders from section 2.

**Undo.** Delete the folder `~/projects/workspace_doc-1_smoke-test/`. Nothing else was changed.

