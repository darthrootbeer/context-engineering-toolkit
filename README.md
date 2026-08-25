# Context Engineering Toolkit

Skills, pipelines, and technique write-ups for building AI-agent systems that stay correct as they scale — built by using Claude Code every day, not by reading about it.

## Why this exists

Every piece in here started as a real problem: a rule that kept getting skipped, an instruction file that got too big to scan, an agent's memory that would eventually stop fitting in one read. None of it was written as a demo. It's the actual tooling built to solve those problems while working, then cleaned up and made generic enough to be useful outside the project it came from.

**What this is not:** a claim to production ML engineering or RAG-pipeline experience. What it actually shows is direction and evaluation — designing a system, prompting and iterating with an AI coding agent to build it, then rigorously checking that the output does what it's supposed to. That's the real skill on display here, and it's stated plainly rather than dressed up as something else.

## What's inside

**`skills/`** — self-contained Claude Code skills. Each one is a single markdown file (plus a README) that defines a repeatable, well-scoped task for an AI agent to carry out — a readability pass on documentation, a way to capture an in-progress plan so it survives a context reset, an audit that checks whether an agent's own guardrails are actually strong enough to trust.

**`pipelines/`** — multi-stage systems, not single tasks. The anchor piece here is a documentation-engineering pipeline: a chain of skills that takes a raw content change through structure review, voice/style checks, grammar, link and visual verification, and a subject-matter-expert review gate before anything publishes. This is a first pass, still being developed further — see `pipelines/docs-pipeline/` for its own README and current state.

**`patterns/`** — written technique docs for ideas that are more valuable described in prose than shipped as literal runnable code, either because the real implementation is too specific to one project to be useful as-is, or because the idea itself is the point. Covers: how to make an "always do X first" instruction actually reliable instead of hoped-for (block-and-tell hooks), how to keep an agent's standing instructions from becoming an unmaintainable single file as they grow (rules-index architecture), and how to give an agent memory that survives months of use without turning into an unreadable dump (typed, size-bounded memory).

**`tools/`** — small standalone utilities. A Word-to-Markdown converter with line-by-line content verification, so a batch document conversion can be trusted without manually diffing every file afterward. A job-fit screener that scores a real job posting against your own personal fit criteria — culture, autonomy, and actual eligibility, not just keyword matching — using Claude to make the judgment calls a plain keyword scan can't.

## How the pieces relate

A skill is one task. A pipeline is several skills chained with real gates between them (nothing moves to the next stage until the current one passes). A pattern is the idea behind a mechanism, written down so it can be rebuilt in a different codebase without copying code that won't fit. The tools are the smaller, single-purpose things that don't need any of that structure.

## A note on how this was built

Everything here was built using Claude Code, directed and reviewed by a human, not hand-typed line by line. That's not a caveat — it's the actual differentiator this repo is trying to demonstrate: designing the system, prompting and iterating to get it right, and evaluating the output rigorously enough to trust it. The skills and patterns in here are, among other things, examples of exactly that evaluation discipline applied to itself.

## What's next

See `ROADMAP.md` for what's planned for the next batch — genericized versions of a few more utility scripts, further development on the documentation pipeline, and a handful of additional skills that need a lighter cleanup pass before they're ready to publish.
