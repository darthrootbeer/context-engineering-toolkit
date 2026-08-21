# Pattern: a typed, size-bounded memory system

A way to give an AI coding agent persistent memory across sessions that stays useful instead of turning into an unstructured, ever-growing dump that eventually can't be read in one pass.

## The problem

Long-lived agent memory — facts, preferences, and context that should persist between separate conversations — has an obvious failure mode: everything gets written to one growing file or one growing collection with no structure. Early on this works fine. Months in, it doesn't:

- The index (or the memory itself, if there's no index) crosses whatever size limit the harness can load in one read, and content past that point becomes invisible
- There's no way to tell a standing behavioral rule from a one-time fact that's now stale
- Corrections and confirmations both get written the same way, so the agent can't distinguish "this was validated, keep doing it" from "this was a mistake, don't repeat it"
- Nobody prunes, because there's no criterion for what's safe to prune

## The fix: typed memories, a size-bounded index, and a maintenance contract

Three separate design decisions, each solving one part of the problem.

### 1. Memory types, not one undifferentiated pile

Give every memory a type that describes *why* it's being kept, not just what it says. A working set of types that covers most of what an agent needs to remember:

| Type | What it holds | Written when |
|---|---|---|
| `user` | Facts about who the operator is — role, expertise, how they like to work | Learned incidentally, or stated directly |
| `feedback` | A correction *or* a confirmation of an approach — both matter | The operator corrects a mistake, or explicitly validates a non-obvious choice |
| `project` | Ongoing state — decisions, deadlines, who's doing what | Learned during work, converted to absolute dates |
| `reference` | A pointer to where information lives in an external system | Learned once, rarely changes |

The `feedback` type matters more than it looks — most memory systems only capture corrections ("don't do X"), which silently teaches the agent to avoid things without ever confirming what to keep doing. Capturing confirmations too ("yes, that approach was right, keep doing it") prevents an agent from second-guessing a validated judgment call in a later session.

### 2. A hard-bounded index, with content living in linked files

The index is not the memory — it's a table of contents. Each entry is a single line: a short title, a link to the full content, and a compressed hint of what it's about. The full content lives in a separate small file per topic, linked from the index by name.

```markdown
# Memory Index

## Feedback
- [Terse commits](feedback_terse_commits.md) — imperative mood, no body unless asked
- [Test before merge](feedback_test_before_merge.md) — corrected 2026-03: skipped tests once, broke prod

## Project
- [Q3 migration](project_q3_migration.md) — deadline 2026-09-01, blocks two other repos

## Reference
- [Error tracking lives in Sentry](reference_error_tracking.md) — project slug: example-api
```

Because the index is deliberately kept small — a hard line-count or byte ceiling that the harness can always load in one pass — it can never silently exceed what gets read at session start. New memories add one line to the index and one new linked file; they never make the index itself unreadable.

### 3. A documented, non-destructive compaction process

Once the index approaches its size ceiling, it needs a maintenance pass — but the fix must never delete memory content, only reorganize the pointers to it:

1. Check for dead links — an index entry pointing at a file that's empty or missing gets dropped (nothing there to point to).
2. Merge verbose entries into a denser bundled-link format — several short entries on one line instead of one line each, cutting explanatory clauses to a few words while keeping every link intact.
3. Drop an index line only for a genuinely resolved one-time event that's now superseded by a live status document elsewhere — never for a standing rule or preference that's still true.
4. Re-check the size after compacting, and aim for real headroom, not just barely under the ceiling.

This is a content-editing pass, not a data-loss event — every topic file survives; only how densely the index points to it changes.

## Why this is genuinely information architecture, not just "note-taking for AI"

The interesting part of this pattern isn't the file format — it's that it's IA applied to a reader that consumes information differently than a person does. A human skimming a wiki tolerates loose structure because they can visually scan and backtrack. An agent reading a memory index at the start of every session either gets the whole picture in one read or effectively doesn't have it — there's no skimming, no "I'll come back to that section later." That constraint (bounded read, no backtracking) is what forces the type system, the size ceiling, and the non-destructive compaction discipline. Designing for that constraint, deliberately, is the actual skill — not the specific file layout above, which is one implementation of it.

## When to use this pattern

Any agent workflow that needs to remember things across sessions longer than a single conversation, where the operator doesn't want to repeat the same context, correction, or preference more than once.

## When not to

A single-session tool with no persistent state doesn't need this — it's solving a problem (index growth over months of accumulated memory) that doesn't exist yet for a short-lived or stateless workflow.
