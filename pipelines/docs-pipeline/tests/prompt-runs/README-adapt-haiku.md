# README-adapt on haiku

Prompt (inputs filled with made-up samples):

```text
I have attached the README for "docs-pipeline". I want to try it on one short document before I trust it on a real doc set.

It is a 60-line markdown file about resetting an API key. It lives in docs/guides/reset-api-key.md.

Write me a trial plan that uses only the stages that do not need a docs platform: the audit, the style passes, the readability check, and the grammar check. For each stage give the exact slash command from the README, what the README says that stage produces, and one sign that the stage went wrong. Finish with the knowledge files I must fill in before I run it, and how I will know the trial worked.

A good answer uses the real command names from the README, leaves out the publish and verify stages, describes each stage's output only as the README does, and does not predict what the stage will find in my document.
```

Answer:

# Trial Plan: docs-pipeline on reset-api-key.md

## Stage 1 — Audit

**Command:** `/docs-diataxis-audit docs/guides/reset-api-key.md`

**What it produces:** Classifies doc content by Diataxis type, produces audit report + JSON mapping

**Sign it went wrong:** The stage returns an error message instead of producing the audit report

## Stage 3a — Structure

**Command:** `/docs-style-check-structure docs/guides/reset-api-key.md`

**What it produces:** Checks required sections, headings, and Diataxis structural rules

**Sign it went wrong:** The stage exits with an error or cannot read the file

## Stage 3b — Voice

**Command:** `/docs-style-check-voice docs/guides/reset-api-key.md`

**What it produces:** Applies general style guide voice, tone, list formatting, and terminology rules

**Sign it went wrong:** The stage fails to load the style guide or returns an error

## Stage 3c — Human

**Command:** `/docs-style-check-human docs/guides/reset-api-key.md`

**What it produces:** Removes AI writing patterns (em dashes, filler phrases, uniform sentences)

**Sign it went wrong:** The stage cannot process the input file or returns no output

## Stage 3d — Readability

**Command:** `/docs-readability-check docs/guides/reset-api-key.md`

**What it produces:** Estimates reading grade level, finds dense sentence patterns, and rewrites them to the target level for the doc type

**Sign it went wrong:** The stage returns an error or cannot estimate the grade level

## Stage 3e — Grammar

**Command:** `/docs-grammar-spelling docs/guides/reset-api-key.md`

**What it produces:** Grammar, spelling, and domain terminology check

**Sign it went wrong:** The stage exits with an error before completing the check

## Knowledge Files to Fill In

Before running the trial:

- `_knowledge/glossary.yaml` — Fill with domain terminology, canonical forms, and common mistakes for your product
- `_knowledge/product-kb/` — Fill with your product model (integration types, API endpoints, domain objects, webhooks, error codes)
- `_knowledge/style-guides/general/style-guide_general.md` — Fill with your voice, tone, and formatting rules

## How to Know the Trial Worked

The trial worked if all six stages complete without errors and each stage produces output (audit report, style findings, readability findings, grammar/spelling findings). All output files should be created without tool errors or missing data.

