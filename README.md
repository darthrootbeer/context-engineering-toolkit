# Context Engineering Toolkit

[![ci](https://github.com/darthrootbeer/context-engineering-toolkit/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/darthrootbeer/context-engineering-toolkit/actions/workflows/ci.yml)

Skills, pipelines, and technique write-ups for building AI-agent systems that stay correct as they scale — built by using Claude Code every day, not by reading about it.

**The 60-second tour.**

- **What this is:** working examples of directing an AI coding agent and then checking what it built, with tests and written grades. Not a claim to machine-learning engineering.
- **See it work:** the job assessment system runs from a clean clone with no model and no API key. The quickstart is in [`pipelines/job-assessment/README.md`](pipelines/job-assessment/README.md).
- **The one file to read first:** [`pipelines/docs-pipeline/README.md`](pipelines/docs-pipeline/README.md), the documentation pipeline.

## Start here: the best things to look at

**1. [`pipelines/docs-pipeline`](pipelines/docs-pipeline/)** is the strongest piece in this repo, and a generic export of the version I used. It is a chain of Claude Code skills that takes a documentation change from the first request through structure review, voice, grammar, links, visuals, expert review, and publishing, with a real gate between every stage. I used a version of it every working day on real documentation. If you only open one thing, open this, and start with its [README](pipelines/docs-pipeline/README.md) and [ARCHITECTURE](pipelines/docs-pipeline/ARCHITECTURE.md).

**2. [`pipelines/job-assessment`](pipelines/job-assessment/)** scores a job posting against your own written criteria and gives a plain verdict: Apply, Apply with reservations, or Skip. A model reads the posting and quotes it for every finding, then ordinary code checks the quotes, does the scoring and picks the verdict, so the same findings always give the same answer. It runs offline from a clean clone with no model and no API key, over 500 tests pin its scores, verdicts and output files, and CI re-runs them in a fresh clone on every change; its README has the five-minute quickstart, the saved live runs (including one that got a verdict wrong), and what it does not show.

**3. [`patterns/block-and-tell-hooks.md`](patterns/block-and-tell-hooks.md)** explains how to make an AI agent follow a rule every time instead of hoping it remembers. It is the idea behind most of the guards in my own setup.

**4. [`patterns/typed-memory-system.md`](patterns/typed-memory-system.md) and [`patterns/rules-index-architecture.md`](patterns/rules-index-architecture.md)** cover how to keep an agent's memory and standing rules organized as they grow.

## Why this exists

Every piece in here started as a real problem: a rule that kept getting skipped, an instruction file that got too big to scan, an agent's memory that would eventually stop fitting in one read. None of it was written as a demo. It's the actual tooling built to solve those problems while working, then cleaned up and made generic enough to be useful outside the project it came from.

**What this is not:** a claim to production ML engineering or RAG-pipeline experience. What it actually shows is direction and evaluation — designing a system, prompting and iterating with an AI coding agent to build it, then rigorously checking that the output does what it's supposed to. That's the real skill on display here, and it's stated plainly rather than dressed up as something else.

## What's inside

**`skills/`** — two self-contained Claude Code skills, each in its own folder with a `SKILL.md` that defines one repeatable, well-scoped task for an AI agent: `docs-readability-check` (a readability pass on documentation) and `plan-this` (capture an in-progress plan so it survives a context reset). Each has a README.

**`pipelines/`** — multi-stage systems, not single tasks. The anchor piece here is a documentation-engineering pipeline: a chain of skills that takes a raw content change through structure review, voice/style checks, grammar, link and visual verification, and a subject-matter-expert review gate before anything publishes. See `pipelines/docs-pipeline/` for its own README and current state. The second pipeline is [`pipelines/job-assessment/`](pipelines/job-assessment/), which scores a job posting against written criteria.

**`patterns/`** — written technique docs for ideas that are more valuable described in prose than shipped as literal runnable code, either because the real implementation is too specific to one project to be useful as-is, or because the idea itself is the point. Covers: how to make an "always do X first" instruction actually reliable instead of hoped-for (block-and-tell hooks), how to keep an agent's standing instructions from becoming an unmaintainable single file as they grow (rules-index architecture), and how to give an agent memory that survives months of use without turning into an unreadable dump (typed, size-bounded memory).

**Prompt blocks.** The READMEs and guides of the two pipelines, the `docs-readability-check` README and the three pattern docs end with a "Prompt for your AI model" block. Each of those prompts has a written "A good answer ..." sentence. Records of runs on Claude Sonnet and Claude Haiku are saved in `pipelines/job-assessment/tests/prompt-runs/`, `pipelines/docs-pipeline/tests/prompt-runs/` (which also covers the readability README) and `patterns/tests/prompt-runs/`. A Claude model graded each answer against its sentence, and I have not re-read every answer. The prompts in the docs-pipeline ARCHITECTURE guide and style guides were checked without keeping the answers. This README, `ROADMAP.md` and `plan-this` have no prompt block.

## How the pieces relate

A skill is one task. A pipeline is several skills chained with real gates between them (nothing moves to the next stage until the current one passes). A pattern is the idea behind a mechanism, written down so it can be rebuilt in a different codebase without copying code that won't fit.

## A note on how this was built

Everything here was built using Claude Code, directed by a human and checked with tests, not hand-typed line by line. That's not a caveat — it's the actual differentiator this repo is trying to demonstrate: designing the system, prompting and iterating to get it right, and evaluating the output rigorously enough to trust it. The skills and patterns in here are, among other things, examples of exactly that evaluation discipline applied to itself.

## What's next

See `ROADMAP.md` for what is done and what is planned next: more genericized utility scripts, a fourth pattern doc, and a handful of additional skills that need a lighter cleanup pass before they are ready to publish.
