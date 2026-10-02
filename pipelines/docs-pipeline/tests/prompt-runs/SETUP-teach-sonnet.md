# SETUP-teach on sonnet

Prompt (inputs filled with made-up samples):

```text
I have attached the setup guide for "docs-pipeline". Teach it to me as if I am an engineer who has never used it.

1. Turn the guide into a numbered checklist in the order I should do things, with one sentence on why each step exists.
2. Say which steps I can skip for a first trial and which I cannot.
3. Then ask me three questions to check that I understood, one at a time. Wait for my answer before the next one, and correct me where I am wrong.

A good answer follows the guide's order, covers the prerequisites, the placeholders, the install loop, the smoke test, the knowledge sources, and running the pipeline, and does not add a step the guide does not contain.
```

Answer:

# docs-pipeline: checklist

The guide has nine sections. Sections 1-6 are the things you do, in order. Sections 7-9 are reference material (which skill reads which file, when to refresh knowledge, and what to do about errors), so they aren't steps.

## Checklist

1. **Check the prerequisites (section 1).** You need Claude Code (`claude`), `gh` authenticated for your org, Git, Node with `markdownlint-cli`, a docs repo, and a published or staging docs site. Skills fail partway through if a tool is missing.
2. **Replace the placeholders (section 2).** Find and replace the `{YOUR_...}` values in all the `.md` files in the folder, for the stages you plan to use. The install step copies the files, so a change made afterward means a re-install.
3. **Check what's left with the grep one-liner (section 2).** `grep -rl '{YOUR_' . --include='*.md'` shows any placeholder you missed. `{YOUR_PIPELINE_DIR}` will still appear in the source files, and that is expected.
4. **Run the install loop (section 3).** Claude Code only loads skills from `<skills folder>/<name>/SKILL.md`, and the repo's files are flat. The loop builds the folders, fills in `{YOUR_PIPELINE_DIR}`, and adds `docs-readability-check` from the repo's `skills/` folder, for 17 skills in total.
5. **Confirm they registered (section 3).** Start a new session and type `/docs-`, or run the `claude -p ... | wc -l` command. You should see 17. If the count is lower, check `SKILLS_DIR` and open a fresh session.
6. **Run the smoke test (section 4).**
   - Run `/docs-workspace-setup TICKET-1 smoke-test`, answer `y`, copy in the sample doc, then run `/docs-style-check-voice` and `/docs-sme-review`.
   - It proves the skills load their knowledge files and produce the expected findings, without publishing anything.
   - To undo it, delete `~/projects/workspace_doc-1_smoke-test/`.
7. **Build your knowledge sources (section 5).** Fill them in once, in the pipeline folder, before you create workspaces, because Stage 0 copies `_knowledge/` into each workspace and earlier workspaces keep the old copy.
   - 7a. Glossary (`glossary.yaml`) is used by grammar (3e).
   - 7b. Product knowledge base (`product-kb/`, seven files) is used by the SME review (4c). Refresh the `extracted:` date in `index.md`.
   - 7c. Style guide (`style-guide_general.md`) is used by voice (3b).
8. **Run the pipeline on real docs (section 6).** Run `/docs-pipeline TICKET-ID slug`. It pauses between stages, and at each pause you say `proceed`, `skip`, `stop`, or `redo` and do the job in the section 6 table. Individual skills can also be run on their own.

## What you can skip for a first trial

| Step | First trial | Why |
|---|---|---|
| 1. Prerequisites | **Partly skippable** | The guide says the docs repo placeholders are needed only for links (4b), the naming-collision part of 4c, publish, and the post-merge check. So `gh`, `markdownlint`, and the docs site matter only for those stages. This is my reading, since the guide lists them all as "before running any skill". You still need Claude Code and your clone of this repo. |
| 2. Placeholders | **Skip** | The guide says the smoke test needs none of them. The three optional ones can stay as they are. |
| 3. Grep check | **Skip** | There is nothing to check if you filled in nothing. |
| 4. Install loop | **Cannot skip** | Without it, the skills don't exist for Claude Code. |
| 5. Registration check | **Cannot skip** | It is the quickest way to catch a wrong `SKILLS_DIR`. |
| 6. Smoke test | **Skippable, but I'd keep it** | It is the only check in the guide that the knowledge files load and the findings come out as expected. |
| 7. Knowledge sources | **Skip, and don't do it yet** | The starters ship working. The smoke test's expected findings depend on the made-up Acme KB, so replacing it first would change the results. You must do this before any real docs. |
| 8. Full pipeline | **Skip for the trial** | The smoke test replaces it. It is the real goal afterward. |

**You cannot skip these before real docs:** the install loop, your own knowledge sources (the guide says to populate all three), and the placeholders for any stage you use. That includes the docs-repo ones for publish.

## Question 1 of 3

In step 2 you replace placeholders, and in step 4 you run the install loop. Suppose you run the install loop first, then notice you forgot to set `{YOUR_ORG}` and fix it in the files in the pipeline folder. Will Claude Code see the change in your next session? Why or why not?

