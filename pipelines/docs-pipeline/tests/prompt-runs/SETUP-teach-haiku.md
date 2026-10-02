# SETUP-teach on haiku

Prompt (inputs filled with made-up samples):

```text
I have attached the setup guide for "docs-pipeline". Teach it to me as if I am an engineer who has never used it.

1. Turn the guide into a numbered checklist in the order I should do things, with one sentence on why each step exists.
2. Say which steps I can skip for a first trial and which I cannot.
3. Then ask me three questions to check that I understood, one at a time. Wait for my answer before the next one, and correct me where I am wrong.

A good answer follows the guide's order, covers the prerequisites, the placeholders, the install loop, the smoke test, the knowledge sources, and running the pipeline, and does not add a step the guide does not contain.
```

Answer:

# The docs-pipeline Checklist

Here's what to do in order:

1. **Verify Claude Code is installed** — This is the tool that runs every stage of the pipeline
2. **Verify GitHub CLI is installed and authenticated to your org** — Needed to clone your docs repo and create PRs
3. **Verify Git is installed** — Required for version control throughout the pipeline
4. **Verify Node.js is installed with `markdownlint-cli` globally** — The publish stage needs this to validate markdown
5. **Ensure you have a docs repository with markdown files** — This is what the pipeline will improve
6. **Ensure you have a published docs site** — This is where improved docs are synced to
7. **Find and replace all `{YOUR_*}` placeholders in the guide's markdown files** — Each skill file references your org's specific values (repo name, domain, username) and won't work with placeholders
8. **Run the install loop from inside the pipeline folder** — This copies the 16 markdown skill files to Claude Code's skills directory and fills in your pipeline path on each copy
9. **Start a new Claude Code session and verify all 17 skills registered** — Type `/docs-` and confirm you see all 17 skill names listed; if you don't, the loop wrote to the wrong folder
10. **Run the smoke test on the included sample doc** — This validates that your setup works end-to-end without needing your real configuration
11. **Populate `_knowledge/glossary.yaml` with your product's 10–20 key terms** — Stage 3e (grammar) won't flag errors unless terms are in the glossary
12. **Populate all 7 files in `_knowledge/product-kb/`** — Stage 4c (SME review) fact-checks against these files and will stop if the KB is missing
13. **Customize `_knowledge/style-guides/general/style-guide_general.md` to match your team's conventions** — Stage 3b loads this; a baseline is already there, but you can add your own rules
14. **Run the full pipeline** — Once everything is set up, run `/docs-pipeline TICKET-ID slug` on your real docs

---

## What you can skip for a first trial

**Cannot skip:** Steps 1–9 (prerequisites and install)  
You need all of these before anything will work.

**Can skip:** Steps 11–12 (knowledge source population)  
The smoke test (step 10) works with *sample* data that ships with the pipeline. You must populate these before running the pipeline on *real* docs, but for a first trial, you can run the smoke test and see the pipeline work without building the glossary and knowledge base.

**Can skip:** Step 13 (customizing the style guide)  
The baseline is already there and sufficient to run Stage 3b. Customize it only if your team has specific conventions beyond the defaults.

**Can skip:** Step 14 (running on real docs)  
The smoke test (step 10) is the trial; the full pipeline is the real work.

---

Now I'll ask you three questions to check you understand. **Answer the first one before I ask the second.**

**Question 1:** You're about to run the install loop in step 8. What does that loop do, and why can't you just copy the `.md` files manually?

