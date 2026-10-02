# SETUP-adapt on sonnet

Prompt (inputs filled with made-up samples):

```text
I have attached the setup guide for "docs-pipeline". Section 4 is a smoke test on a sample doc. I want to run the same test on one of my own short docs instead.

reset-api-key.md. It explains how to reset an API key from the dashboard.

Rewrite the smoke test in section 4 for my doc. Change only what has to change for my file. Keep every command the guide gives, in the guide's order. In the copy command, write my doc's location as `<path to my doc>`. Say which placeholders in section 2 I still do not need to fill in for this test. Do not invent a command or a file path. Do not predict what any stage will find in my doc. If my doc cannot be checked the way section 4 describes (for example because it is not about a product the knowledge files describe), say so plainly.

A good answer keeps the guide's commands and order, changes only the file name and where the guide's expected results depend on the sample doc, stops before the publish stage, repeats the guide's undo step, and says that Stage 4c checks my doc against the knowledge files, which describe a made-up product until I replace them.
```

Answer:

## Smoke test for `reset-api-key.md`

Run these in Claude Code, in this order:

1. `/docs-workspace-setup TICKET-1 smoke-test` and answer `y`. This creates `~/projects/workspace_doc-1_smoke-test/` with a copy of `_knowledge/`.
2. In that folder, copy your doc in: `cp "<path to my doc>" docs/output/docs/`
3. `/docs-style-check-voice docs/output/docs/` (Stage 3b). It edits `reset-api-key.md` in place and writes a report to `docs/output/_process/style-audit/`.
4. `/docs-sme-review docs/output/docs/` (Stage 4c). It writes `_process/sme-review/reset-api-key-sme-review.md`.

The test stops after Stage 4c. Nothing is published.

**What proves it worked.** Stage 3b does not stop with "Style guide not found". Stage 4c does not stop with "Product KB not found". Both stages finish and write their reports to the paths above. The guide's other expected results (a tone fix from a casual opener, and the three HIGH findings about cancellations, webhooks and the rate limit) apply only to the sample doc, so I have left them out. They say nothing about what your doc will produce.

**Undo.** Delete the folder `~/projects/workspace_doc-1_smoke-test/`. Nothing else was changed.

## Placeholders in section 2

You do not need to fill in any of them for this test. That covers all eight `{YOUR_...}` placeholders (`{YOUR_ORG}`, `{YOUR_DOCS_REPO}`, `{YOUR_DOCS_SITE}`, `{YOUR_DOCS_REPO_PATH}`, `{YOUR_ISSUE_TRACKER}`, `{YOUR_TICKET_URL}`, `{YOUR_USERNAME}`, `{YOUR_DEFAULT_OG_IMAGE_URL}`). The three optional ones (`{SHARED_CONFIG_DIR}`, `{NOTES_DIR}`, `{YOUR_PIPELINE_DIR}`) can stay as they are. The install loop in section 3 fills in `{YOUR_PIPELINE_DIR}` itself, so the skills must be installed before you start.

## Limit of this test

Stage 4c cannot meaningfully check your doc yet. It compares your doc against `_knowledge/product-kb/`, which describes a made-up product (the "Acme Orders API"). Unless `reset-api-key.md` is about that product, the review will only show that the stage runs, not whether your doc is accurate. To get a real accuracy check, replace the knowledge files with your own, as described in section 5.2, before you create the workspace. A workspace keeps the copy of `_knowledge/` it was created with.

Stage 3b is less affected. It uses the generic style guide, so it can run on your doc as it is.

