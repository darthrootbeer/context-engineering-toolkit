# Roadmap

What's here now is a first batch. This is what's planned next, so it's clear what's deliberately not done yet versus what's missing by accident.

## Planned — batch 2

**More utility scripts, genericized.** A handful of scripts proved useful enough to keep using but need their hardcoded IDs, team names, and paths pulled out into config before they're safe to publish:
- A backlog-hygiene script that sweeps a ticket tracker for stale or malformed tickets
- A triage helper for routing incoming work items
- A link-integrity checker for a linked-notes knowledge base
- A project-state bootstrap script for standing up a new tracked project consistently
- An export-cleanup script for migrating notes out of a legacy note-taking tool

**A fourth pattern doc: always-read-first / write-back state files.** A convention for keeping a piece of live state (a machine's current status, a project's current phase) trustworthy across many separate agent sessions touching it — read the state file before acting, write back immediately after any change, and enforce both halves with hooks rather than hoping the instruction gets followed every time.

**Further development on the documentation pipeline.** The version in `pipelines/docs-pipeline/` is a first cleaned pass, not the finished shape. Ongoing work on it will land here as it develops.

**A handful of additional skills**, pending a lighter genericization pass:
- An AI-writing-tell detector — scans prose for patterns that read as machine-written and proposes rewrites, backed by a pattern registry with a cited source per rule, dated retirements for tells that stopped working, a documented false-positive case per rule, and a scheduled refresh step that diffs several outside source authorities to keep the pattern list current. Two small genericization items: a hardcoded personal file path and a house-style config tuned to one person's preferences.
- A structured multi-perspective review skill (runs a draft or decision past several distinct reviewer lenses and synthesizes the results)
- A session close-out skill (makes sure external systems reflect the current state of work before a session ends)
- A context hand-off skill (writes a compact, resumable summary of in-progress work so a fresh session can pick it up without the original conversation)
- A "has this already been solved" research skill (fans out across public sources before committing to build something from scratch)
- A source-to-structured-output research prep skill
- A "verify the claimed work is actually done" skill (checks a tracked task's actual state against what was reported, before it gets marked complete)
- A systematic codebase cleanup skill (dedup, dead code, inconsistent types, in one pass)

## Explicitly out of scope for this repo

- Anything narratively specific to one product's fictional world or brand voice — general technique only, not product content
- Anything still under an employer's confidentiality terms without explicit permission to publish
- Scratch/throwaway scripts that were never meant to be reused

## Not yet decided

Whether to link this repo from a resume, portfolio site, or LinkedIn — that's a deliberate later decision, not part of standing this repo up.
