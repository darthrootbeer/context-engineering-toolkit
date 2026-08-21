# Pattern: rules-index architecture

A way to organize an AI agent's standing instructions so they scale past a handful of rules without becoming an unmaintainable wall of text — and so a new rule doesn't accidentally get buried inside an unrelated one.

## The problem

A single global instructions file (a system prompt, a `CLAUDE.md`, an `AGENTS.md`, whatever your tooling calls it) is the natural first place to put standing behavioral rules: how to write commits, how to handle a particular kind of ticket, what tone to use, what never to do without asking first. This works fine at a dozen rules. It stops working at fifty. Symptoms:

- Finding the rule that governs a specific situation means scanning a file that's grown to thousands of lines
- A new rule gets appended wherever there's room, not filed with related rules — so two rules about the same topic end up hundreds of lines apart
- Editing one rule risks context-bleeding into an unrelated instruction two paragraphs above it
- The whole file gets loaded into every session's context whether or not most of it is relevant to the task at hand

## The fix: one file per domain, one index

Split the monolithic instructions file into small, single-topic files — one per behavioral domain (git workflow, a specific tool's conventions, a communication-style rule, a safety rule). Keep a single top-level index file that lists every rule file with a one-line description of what it governs. The main instructions file becomes a short pointer, not a container:

```
Full rules for git behavior: rules/git-workflow.md
Full rules for how to handle X: rules/x-behavior.md
```

The index file (`rules/README.md` in this pattern) is the map — one row per file, kept genuinely current, so a rule can be found by scanning ~30 short lines instead of one long document.

## Why this actually scales

- **Editing is scoped.** Changing the git-workflow rule means opening one file, not searching a five-thousand-line document for the right paragraph.
- **New rules have an obvious home.** "Where does this go?" has an answer — either an existing domain file, or a new one that gets a new index row. No more "append to the bottom because there's room there."
- **Loading can be selective.** Depending on your tooling, some or all of these files might be loaded on demand rather than always-on — a rule about a tool you're not using in this session doesn't have to eat context budget.
- **The index itself becomes a design surface.** Reading just the index, top to bottom, answers "what does this agent's operator actually care about?" faster than reading the full rule bodies.

## A minimal generic example

```
rules/
  README.md              ← the index
  commit-conventions.md
  destructive-ops.md
  communication-style.md
  external-api-usage.md
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

Rules for anything that deletes, overwrites, or force-pushes.

## The rule

Never run a destructive operation without explicit confirmation in the
current turn, even if a similar operation was approved earlier in the
session. Approval for one instance is not standing approval for the class.

## What counts as destructive

- Force-push, hard reset, branch deletion with unmerged commits
- Any `rm -rf` or equivalent recursive delete
- Overwriting a file without first checking whether it has uncommitted or
  unbacked-up content
```

Each domain file is self-contained enough to be read on its own — you shouldn't need to also read three other files to understand what one rule means.

## When to split

There's no fixed threshold, but a good trigger is: the first time you catch yourself scrolling past unrelated content to find the rule you actually needed. That's the signal the monolith has stopped paying for itself.

## When not to

At a handful of rules, splitting adds indirection for no real benefit — a single short file is easier to scan than an index plus five one-paragraph files. This pattern earns its keep once the rule count is large enough that "just read the whole file" stops being a reasonable answer.

## Related pattern

The same idea applies one level up to long-term memory rather than standing rules — see how a memory-index file with linked topic files avoids the same monolith problem, described conceptually (not as real content) in this repo's other pattern docs.
