# Context Engineering Toolkit

Skills, pipelines, and technique write-ups for building AI-agent systems that stay correct as they scale — built by using Claude Code every day, not by reading about it.

## Start here: the best things to look at

**1. [`pipelines/docs-pipeline`](pipelines/docs-pipeline/)** is the strongest piece in this repo. It is a chain of Claude Code skills that takes a documentation change from the first request through structure review, voice, grammar, links, visuals, expert review, and publishing, with a real gate between every stage. I used a version of it every working day on real documentation. If you only open one thing, open this, and start with its [README](pipelines/docs-pipeline/README.md) and [ARCHITECTURE](pipelines/docs-pipeline/ARCHITECTURE.md).

**2. [`pipelines/job-assessment`](pipelines/job-assessment/)** scores a job posting against your own written criteria and gives a plain verdict: Apply, Apply with reservations, or Skip. A model reads the posting and writes down findings, quoting the posting for every claim. Ordinary code then checks those quotes, does the scoring and picks the verdict, so the same findings always give the same answer. It was built by directing Claude Code, not hand-typed. What is shown: the whole chain runs offline on three invented postings with no model, no network and no API key, and the tests in that folder (run again in a fresh clone by CI) compare its scores, verdicts and saved output files to written-down expected values. A separate run with the `claude` CLI on Claude Sonnet is saved in [`tests/`](pipelines/job-assessment/tests/): the interview built a file that passed the checker, and the assessment gave the expected verdicts on 2 of 2 postings in its second attempt, after the first attempt got one verdict wrong ([both records are kept](pipelines/job-assessment/tests/e2e-output-run1.md)). What is not shown: that a verdict predicts getting hired, or that it beats any other method. No real postings or real person's data are in it. Its README starts with a five-minute quickstart from a clean clone, and every doc in the folder ends with prompts tested on Claude Sonnet and Claude Haiku.

**3. [`patterns/block-and-tell-hooks.md`](patterns/block-and-tell-hooks.md)** explains how to make an AI agent follow a rule every time instead of hoping it remembers. It is the idea behind most of the guards in my own setup.

**4. [`patterns/typed-memory-system.md`](patterns/typed-memory-system.md) and [`patterns/rules-index-architecture.md`](patterns/rules-index-architecture.md)** cover how to keep an agent's memory and standing rules organized as they grow.

## Why this exists

Every piece in here started as a real problem: a rule that kept getting skipped, an instruction file that got too big to scan, an agent's memory that would eventually stop fitting in one read. None of it was written as a demo. It's the actual tooling built to solve those problems while working, then cleaned up and made generic enough to be useful outside the project it came from.

**What this is not:** a claim to production ML engineering or RAG-pipeline experience. What it actually shows is direction and evaluation — designing a system, prompting and iterating with an AI coding agent to build it, then rigorously checking that the output does what it's supposed to. That's the real skill on display here, and it's stated plainly rather than dressed up as something else.

## What's inside

**`skills/`** — self-contained Claude Code skills. Each one is a single markdown file (plus a README) that defines a repeatable, well-scoped task for an AI agent to carry out — a readability pass on documentation, a way to capture an in-progress plan so it survives a context reset, an audit that checks whether an agent's own guardrails are actually strong enough to trust.

**`pipelines/`** — multi-stage systems, not single tasks. The anchor piece here is a documentation-engineering pipeline: a chain of skills that takes a raw content change through structure review, voice/style checks, grammar, link and visual verification, and a subject-matter-expert review gate before anything publishes. This is a first pass, still being developed further — see `pipelines/docs-pipeline/` for its own README and current state.

**`patterns/`** — written technique docs for ideas that are more valuable described in prose than shipped as literal runnable code, either because the real implementation is too specific to one project to be useful as-is, or because the idea itself is the point. Covers: how to make an "always do X first" instruction actually reliable instead of hoped-for (block-and-tell hooks), how to keep an agent's standing instructions from becoming an unmaintainable single file as they grow (rules-index architecture), and how to give an agent memory that survives months of use without turning into an unreadable dump (typed, size-bounded memory).

## How the pieces relate

A skill is one task. A pipeline is several skills chained with real gates between them (nothing moves to the next stage until the current one passes). A pattern is the idea behind a mechanism, written down so it can be rebuilt in a different codebase without copying code that won't fit.

## A note on how this was built

Everything here was built using Claude Code, directed and reviewed by a human, not hand-typed line by line. That's not a caveat — it's the actual differentiator this repo is trying to demonstrate: designing the system, prompting and iterating to get it right, and evaluating the output rigorously enough to trust it. The skills and patterns in here are, among other things, examples of exactly that evaluation discipline applied to itself.

## What's next

See `ROADMAP.md` for what's planned for the next batch — genericized versions of a few more utility scripts, further development on the documentation pipeline, and a handful of additional skills that need a lighter cleanup pass before they're ready to publish.
