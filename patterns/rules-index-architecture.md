# Pattern: rules-index architecture

A way to organize an AI agent's standing instructions so they scale past a handful of rules without becoming a wall of text, and so a new rule does not get buried inside an unrelated one.

Written for Claude Code, where the loading behavior described below is real. Check your own tool before assuming it works the same way.

## The problem

A single global instructions file (`CLAUDE.md`, `AGENTS.md`, a system prompt) is the natural first home for standing rules: how to write commits, how to handle a kind of ticket, what tone to use, what never to do without asking. It works at a dozen rules. At fifty it breaks:

- Finding the rule for a situation means scanning thousands of lines.
- New rules get appended wherever there is room, so two rules on one topic end up hundreds of lines apart.
- Editing one rule risks bleeding into the unrelated rule above it.

## The fix: one file per domain, one index

Split the big file into small single-topic files, one per domain (git workflow, one tool's conventions, a communication style, a safety rule). Keep one index file that lists every rule file with a one-line description. The main instructions file keeps the few things needed in every session and points at the rest:

```
Full rules for git behavior: rules/git-workflow.md
Full rules for how to handle X: rules/x-behavior.md
```

The index (`rules/README.md` here) is the map: one row per file, so a rule can be found by scanning a short table.

In a real setup of this shape, the main file stays a hybrid: pointers to the rule files, plus a small amount of content that really is needed every session. It does not have to be pure pointers. Rarely needed material gets split out.

## What splitting does NOT do: it does not save context

This is the most common wrong assumption. In Claude Code, splitting rules into files does **not** by itself shrink what gets loaded. At startup Claude Code reads `CLAUDE.md` plus every markdown file under `rules/`, including subfolders. There is no default lazy loading. Moving text from one big file into thirty small ones leaves the total load the same, and adding a subfolder can make it grow.

What splitting gives you is editing and findability. If you also want it to cut context, there are two real opt-outs:

1. **`paths:` frontmatter in a rule file.** A rule that starts with a `paths:` list of file globs is loaded only when the agent works on matching files. Use it for rules that only matter in one corner of a project.
2. **`claudeMdExcludes` in `settings.json`.** A list of globs for instruction files to skip. Pointing it at a subfolder such as `rules/reference/**` keeps that whole folder out of startup loading.

```markdown
---
paths:
  - "**/release/VERSION"
  - "**/release/**/*.yaml"
---
# Release versioning
...
```

```json
{
  "claudeMdExcludes": ["**/.claude/rules/reference/**"]
}
```

In the real setup this came from, most rule files load every session, and only a few use `paths:`. A subfolder of long detail files once pushed total startup load from about 150k to about 177k characters before the exclude was added. Measure your own load before and after you split.

## A third layer: a reference folder

Rule files stay short and say what to do. The history of why (the incident that created the rule, worked examples, long command listings) goes into a `rules/reference/` folder that the exclude keeps out of startup loading. The rule file links to it. The agent reads a reference file only when it needs the detail.

Where a hook enforces a rule, say so in the rule file ("hook-enforced, see the guard script"). Then the prose and the enforcement stay linked, and a reader knows which rules are only requests. See [block-and-tell hooks](block-and-tell-hooks.md).

## A minimal generic example

```
rules/
  README.md              <- the index
  commit-conventions.md
  destructive-ops.md
  communication-style.md
  external-api-usage.md
  reference/             <- excluded from startup loading
    destructive-ops-history.md
```

**`rules/README.md`**

```markdown
# Rules Index

| File | What it governs |
|---|---|
| commit-conventions.md | Commit message format, branch naming, PR structure |
| destructive-ops.md | What requires explicit confirmation before running |
| communication-style.md | Tone, banned phrases, response length |
| external-api-usage.md | Rate limits, retry behavior, credential handling |
```

**`rules/destructive-ops.md`** (one topic, self-contained)

```markdown
# Destructive Operations

## The rule

Never run a destructive operation without explicit confirmation in the
current turn. Approval for one instance is not standing approval for the class.

## What counts as destructive

- Force-push, hard reset, deleting a branch with unmerged commits
- Any recursive delete
- Overwriting a file that may hold uncommitted work

Why this rule exists, and the incident behind it: reference/destructive-ops-history.md
```

Each domain file should make sense on its own. You should not need three other files to understand one rule.

## The index drifts

An index is only useful while it is complete, and indexes go stale. In the real setup, the index table had fewer rows than there were rule files after a few months of additions. Add a row in the same change that adds a file, and re-check the table against the folder now and then:

```bash
ls rules/*.md | wc -l          # files on disk
grep -c '^|' rules/README.md   # table rows, minus 2 for the header
```

## When to split

When you catch yourself scrolling past unrelated rules to find the one you need.

## When not to

At a handful of rules, an index plus five one-paragraph files is more indirection than one short file.

## Related

- [Typed, size-bounded memory](typed-memory-system.md) applies the same idea to long-term memory instead of standing rules.
- The [docs pipeline](../pipelines/docs-pipeline/) is a small instance of this layout: one style guide per concern in its `_knowledge/` folder, one README as the index.

## How this was checked

Each claim was compared against a working Claude Code setup: the count and layout of rule files, the index table and its drift, the `claudeMdExcludes` entry in `settings.json`, a rule file that uses `paths:`, and a note recording that startup loading includes every file under `rules/` recursively (confirmed by inspecting the installed program). The generic example files were written for this page.

## Prompt for your AI model

Give any AI model this file plus one of the prompts below. Paste the file text where the prompt says `[PASTE FILE]`.

**1. Understand and teach it**

```
Here is a design pattern document: [PASTE FILE]

Explain it to me as if I have one long instructions file and have never split it. Use a different everyday analogy than the one in the document. Then ask me three questions, one at a time, that check I understand why splitting files does not shrink what is loaded, and what the two opt-outs are. Wait for my answer before each next question.
```

**2. Review it against your setup**

```
Here is a design pattern document: [PASTE FILE]

Below is the folder listing and approximate line counts of my own instruction files, plus the agent tool I use: [PASTE LISTING AND TOOL NAME]

Tell me whether my setup needs this pattern yet. Flag any claim in the document that may not be true for my tool, especially about what gets loaded at startup. Suggest which of my files should be split out, which should stay, and which belong in a reference folder, and give a reason for each.
```

**3. Adapt and test it**

```
Here is a design pattern document: [PASTE FILE]

My instructions file is pasted below. My tool is: [YOUR AGENT TOOL].

[PASTE YOUR INSTRUCTIONS FILE]

Propose a split into domain files with an index table, and tell me which files should be excluded from startup loading. Then give me a way to test that the split worked: how to measure total loaded size before and after, and one question to ask the agent that only a specific rule file can answer.
```

**How these prompts were checked.** Each of the three prompts was run once with a small model (Claude Haiku) through the `claude` command line, with the full text of this file pasted in and sample details filled in. All three gave an on-topic answer that matched what this file says. In two runs a placeholder was left unfilled by my test setup, and the model noticed and said so or asked for the missing text instead of making something up. That is the behavior you want. One run per prompt is a light check, not a benchmark, so read the answers critically. I did not save those answers, so there is no record to read here, unlike the saved runs in `pipelines/job-assessment/tests/`.
