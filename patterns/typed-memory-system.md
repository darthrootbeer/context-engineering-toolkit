# Pattern: a typed, size-bounded memory system

A way to give an AI coding agent memory that lasts across sessions and stays readable, instead of an ever-growing dump nobody can load in one pass.

Written for Claude Code's file-based memory, where the limits below are real. Other tools will have different limits. Find yours before copying the numbers.

## The problem

Long-lived agent memory has an obvious failure mode: everything goes into one growing file with no structure. Early on that works. Months in:

- The index crosses the size the harness will load, and everything past that point is cut off from the session.
- A standing rule and a one-time fact look the same, so stale facts never get pruned.
- Corrections and confirmations get written the same way, so the agent cannot tell "keep doing this" from "never do this again."
- Nobody prunes, because there is no rule for what is safe to remove.

## The fix: typed memories, a bounded index, a maintenance contract

### 1. Types, not one pile

Give each memory a type that says why it is kept:

| Type | What it holds | Written when |
|---|---|---|
| `user` | Who the operator is: role, expertise, how they like to work | Learned in passing, or stated |
| `feedback` | A correction or a confirmation of an approach | The operator corrects a mistake, or validates a non-obvious choice |
| `project` | Ongoing state: decisions, deadlines, who is doing what | Learned during work, with absolute dates |
| `reference` | A pointer to where information lives elsewhere | Learned once, rarely changes |

The type goes in each file's frontmatter. In a real memory folder of several hundred files these four types cover everything, and `feedback` is by far the largest, because every correction becomes one.

Capture confirmations as well as corrections. A memory system that only records "don't do X" teaches the agent to avoid things without ever saying what to keep doing. "Yes, that approach was right" stops the agent from second-guessing a good call in a later session.

### 2. A bounded index, content in linked files

The index is a table of contents, not the memory. Each entry is one line: a short title, a link, a few words of gist. The full content lives in one small file per topic.

```markdown
# Memory Index

## Feedback
- [Terse commits](feedback_terse_commits.md) imperative mood, no body unless asked
- [Test before merge](feedback_test_before_merge.md) skipped tests once, broke prod

## Project
- [Q3 migration](project_q3_migration.md) deadline 2026-09-01, blocks two repos

## Reference
- [Error tracking lives in Sentry](reference_error_tracking.md) project slug: example-api
```

A topic file looks like this:

```markdown
---
name: feedback-test-before-merge
description: one-line summary used to decide relevance
metadata:
  type: feedback
---
Run the test suite before merging.
**Why:** a skipped test run once shipped a broken build.
**How to apply:** before any merge command, run tests and read the result.
```

### 3. Know the real limits

In Claude Code, the memory index is read in full at session start. In the version I use, I observed two limits on it that apply separately: **200 lines** and **25,000 bytes**. Whichever you hit first is the cutoff. I found the two numbers by reading them out of the installed Claude Code program, version 2.1.263. I have not re-confirmed them on later versions: on 2026-10-01, with version 2.1.287 installed, my check script could not find them in the program and fell back to these same values. So read them as numbers that were true for one version, and test your own.

Three details that are easy to miss:

- **Topic files may be limited too, but I have not tested that.** Topic files may be read on demand rather than at session start, in which case a limit on them would only matter when one is opened, and it may not apply at all. I have not tested what your version does. Keeping topic files short is cheap, so I do it anyway.
- **Going over is loud, not silent.** The harness cuts at a line boundary and adds a visible warning naming the file and the limit. Everything past the cut is still missing from that session, so treat the warning as a fault to fix, not noise.
- **Measure bytes, not characters.** The limit is in bytes. Emoji and accented letters are several bytes each, so a character count undercounts. Use `wc -c file`, never a script that counts decoded characters.

Treat the numbers as working values that can change with the tool version. Re-check them when you update, and keep your warning threshold well under them: 80 percent (160 lines or 20,000 bytes) leaves room to compact on purpose instead of in a panic.

### 4. A second tier: topic index files

When the main index is capped, memories that no longer fit do not get deleted. They go into topic index files, such as `INDEX-todoist.md` or `INDEX-writing.md`, each listing the memories for one area. The main index links to each topic index with a short count and a line saying "read the relevant one before working in that area."

```markdown
## More memories: topic indexes
- [Git and PRs](INDEX-git.md) (example: 8 entries)
- [Todoist](INDEX-todoist.md) (example: 3 entries)
- [Writing and output](INDEX-writing.md) (example: 6 entries)
```

The agent reads the one that matches the task. The cost is that these are not auto-loaded, so the main index must say they exist and when to open them. In my own setup this tier grew to several files, and it was the most important change that came after the first version of this pattern.

### 5. A weekly automatic check

A size limit nobody checks gets crossed. Run a small script on a schedule that checks the index against both limits (and keeps topic files short, since their limit is untested), flags any topic file the index does not link to, and sends a message only when something needs a human. A weekly cron entry is enough:

```
0 22 * * 0  /path/to/memory-size-check.sh     # Sundays, 10pm
```

Make silence mean "clean" and nothing else. In the real setup a cron entry once pointed at a script that had never been written. Cron does not report a missing target, so a check that never ran looked like a check that found nothing, and the index drifted toward its limit unwarned. The fix was a wrapper that logs on every run, and tells you if it cannot find the checker. A job that has never run and a job that found nothing must not look the same.

### 6. Compaction that never deletes content

When the index nears its limit, reorganize the pointers. Never delete memory content.

1. Never delete a topic file.
2. Drop an index line whose file is empty or missing.
3. Merge verbose entries into a denser bundled format: several short entries on one line, explanatory clauses cut to a few words, every link kept.
4. Drop an index line only for a resolved one-time event that a live status document now covers. Never for a standing rule or preference that is still true.
5. Before moving a note to an archive folder, search your rules, skills and scripts for its name. If something still cites it, keep it live.
6. Check the size again in bytes and leave real headroom.
7. Confirm every link in the index still resolves to a file.

Bundled format, before and after:

```markdown
- [Terse commits](feedback_terse_commits.md) imperative mood, no body unless asked
- [Test before merge](feedback_test_before_merge.md) skipped tests once, broke prod

**Git:** [Terse commits](feedback_terse_commits.md) imperative, no body · [Test before merge](feedback_test_before_merge.md) tests first
```

## Why this is information architecture

The interesting part is not the file format. It is that this is information architecture for a reader that consumes information differently from a person. A person can skim a wiki and backtrack. An agent reading an index at the start of a session gets the whole picture in one pass or does not have it. That constraint, a bounded read with no backtracking, is what forces the types, the size limits, the second-tier indexes and the habit of compacting without deleting.

## When to use this pattern

Any agent workflow that has to remember things beyond one conversation, where you do not want to repeat the same context, correction or preference twice.

## When not to

A single-session tool with no saved state. It is solving index growth over months, which a stateless workflow does not have.

## Related

- [Rules-index architecture](rules-index-architecture.md) uses the same one-index-many-files idea for standing rules.
- The [docs pipeline](../pipelines/docs-pipeline/) keeps a small bounded reference set of its own: a glossary and per-concern style guides in `_knowledge/`, read by each stage instead of re-explained each time.

## How this was checked

Every claim was compared against a working Claude Code memory folder: the four types (counted from file frontmatter), the index size against both limits, the topic index files, the weekly cron entry and its wrapper, and the written compaction steps. The limit numbers are the values I observed in Claude Code 2.1.263. They are not read from the program at run time, and I could not re-confirm them on version 2.1.287, so re-check them for your version. The claim that topic files are limited is not checked here at all. The example files were written for this page.

## Prompt for your AI model

Give any AI model this file plus one of the prompts below. Paste the file text where the prompt says `[PASTE FILE]`.

**1. Understand and teach it**

```
Here is a design pattern document: [PASTE FILE]

Explain it to me as if I have never given an AI tool long-term memory. Use a different everyday analogy than the one in the document. Then ask me three questions, one at a time, that check I understand the difference between a correction and a confirmation, why the index has a size limit, and why compaction never deletes topic files. Wait for my answer before each next question.

A good answer uses an analogy that is not the document's, explains the difference between a correction and a confirmation, why the index has a size limit, and why compaction never deletes topic files. It asks exactly three questions, one at a time, and waits for my answer before the next.
```

**2. Review it against your setup**

```
Here is a design pattern document: [PASTE FILE]

Below is a listing of my memory or notes folder with file sizes, plus the tool I use: [PASTE LISTING AND TOOL NAME]

Tell me which parts of the pattern my setup already has and which it lacks. Flag any number in the document (line limit, byte limit) that may be different for my tool and tell me how to find the real one. Name my biggest risk of hitting a size limit and one check I could automate.

A good answer says which parts of the pattern my listing already has and which it lacks, flags the line and byte limits as values that may differ for my tool and says how to find the real ones, and names one biggest size risk and one check I could automate.
```

**3. Adapt and test it**

```
Here is a design pattern document: [PASTE FILE]

My tool is: [YOUR AGENT TOOL]. Here are five things I want it to remember: [LIST FIVE FACTS, PREFERENCES AND CORRECTIONS]

Sort each into a memory type, write the topic files and the index for them, and then write a short script that checks the index against a size limit in bytes. Finish with a test: how I check the next session actually loaded the index, and how I confirm the size check fails when I add too much.

A good answer sorts each of my five items into a memory type, writes topic files and an index for them, gives a script that measures the index in bytes, and finishes with a test that the next session loaded the index and a test that the size check fails when the index grows too large.
```

**How these prompts were checked.** On 2026-10-01 each of the three prompts was run once on Claude Sonnet and once on Claude Haiku, with this file pasted in and sample details filled in. A Claude model (Sonnet 5.5) graded each answer against the "A good answer ..." sentence under the prompt. I have not re-read every answer. Sonnet met all three. Haiku met none of them in full: its explanation left out why compaction keeps topic files, it listed gaps it could not see from a file listing, and the size-check script it wrote uses a variable it never sets. The answers are in [`tests/prompt-runs/`](tests/prompt-runs/).
