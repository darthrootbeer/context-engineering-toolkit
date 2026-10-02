# rules-index-architecture prompt 3 (Adapt and test it) on sonnet

Prompt (the document's full text was pasted where it says [PASTE FILE]; other inputs filled with made-up samples):

```text
Here is a design pattern document: [PASTE FILE]

My instructions file is pasted below. My tool is: Claude Code.

# Project rules

## Git
Use short commit messages. Never push to main.

## Testing
Run pytest before every merge. Add a test for every bug fix.

## Deploys
Deploys go through make deploy. Check the changelog first. Never deploy on Fridays.

## Style
Use type hints. Keep functions under 40 lines.

## Old migration notes
The 2023 migration moved the billing tables. See docs/billing-2023.md for the details.

Propose a split into domain files with an index table, and tell me which files should be excluded from startup loading. Then give me a way to test that the split worked: how to measure total loaded size before and after, and one question to ask the agent that only a specific rule file can answer.

A good answer proposes domain files and an index table built from my file's own contents, names which files to exclude from startup loading, and gives a before-and-after way to measure loaded size plus one question that only a specific rule file can answer.
```

Answer:

## Proposed layout

Your file is about 15 lines, so the pattern's "when not to" section applies: five one-line files plus an index is more indirection than you need today. If you want the split anyway (for example because you expect these sections to grow), here is how I'd do it.

```
CLAUDE.md                  <- keeps only the pointers, plus the one rule you want every session
.claude/rules/
  README.md                <- the index
  git-workflow.md
  testing.md
  deploys.md
  code-style.md            <- has paths: frontmatter
  reference/               <- excluded from startup loading
    billing-2023-migration.md
```

**`rules/README.md`**

```markdown
# Rules Index

| File | What it governs |
|---|---|
| git-workflow.md | Commit message length, never pushing to main |
| testing.md | pytest before merge, a test for every bug fix |
| deploys.md | make deploy, changelog check, no Friday deploys |
| code-style.md | Type hints, 40-line function limit (Python files only) |
| reference/billing-2023-migration.md | Pointer to the 2023 billing-table migration notes (docs/billing-2023.md) |
```

**`rules/git-workflow.md`**
```markdown
# Git Workflow
- Use short commit messages.
- Never push to main.
```

**`rules/testing.md`**
```markdown
# Testing
- Run pytest before every merge.
- Add a test for every bug fix.
```

**`rules/deploys.md`**
```markdown
# Deploys
- Deploy only through `make deploy`.
- Check the changelog first.
- Never deploy on Fridays.
```

**`rules/code-style.md`**
```markdown
---
paths:
  - "**/*.py"
---
# Code Style
- Use type hints.
- Keep functions under 40 lines.
```

**`rules/reference/billing-2023-migration.md`**
```markdown
# 2023 billing migration
The 2023 migration moved the billing tables. Details: docs/billing-2023.md
```

**`CLAUDE.md`**
```markdown
# Project rules
Index of all rules: .claude/rules/README.md
```

## What to exclude from startup loading

1. **`reference/`**: the migration notes are history, not instructions. Exclude them in `settings.json`:
   ```json
   { "claudeMdExcludes": ["**/.claude/rules/reference/**"] }
   ```
   The index row stays visible, so the agent knows the notes exist and can read them on demand.
2. **`code-style.md`**: it is scoped with `paths:` to `**/*.py`, so it loads only when Python files are in play.

I would leave `git-workflow.md`, `testing.md`, and `deploys.md` always loaded. They aren't tied to file patterns and are tiny.

`docs/billing-2023.md` is outside `rules/`, so it is not loaded at startup either way. The stub exists only so the index can point to it.

The Friday deploy ban and the no-push-to-main rule are good candidates for a hook, since a prose rule is only a request. If you add one, note "hook-enforced" in the rule file.

## How to test the split

**Measure loaded size.** The document's claim that every file under `rules/` loads at startup is worth checking on your install rather than trusting.

- Before the split, save your original file and run `wc -c CLAUDE.md`.
- After the split, run:
  ```bash
  cat CLAUDE.md .claude/rules/*.md | wc -c
  ```
  This counts only top-level rule files. Add `.claude/rules/reference/*.md` to the command to see what the exclude is saving.
- To see what Claude Code actually loaded, start a fresh session and run `/memory` (lists loaded instruction files) or `/context` (shows memory-file token usage). The reference file should be absent from the list. Compare the numbers with and without the `claudeMdExcludes` entry.

Expect the total to stay about the same or grow slightly from the index and frontmatter. At this size the split gives you findability, not savings.

**One question only a specific file can answer.** In a fresh session, ask:

> What day are deploys forbidden, and what must I check before running `make deploy`?

The answer (Fridays, check the changelog) lives only in `deploys.md`. If the agent gets it right, the rule file loaded and the pointer chain works. Then check the opt-outs:

- In a fresh session where you haven't touched any `.py` file, ask "What's the maximum function length?" It should not know, because `code-style.md` is path-scoped. Open a Python file and ask again, and it should say 40 lines.
- Ask "What did the 2023 migration move?" The agent should have to open the reference stub and `docs/billing-2023.md` to answer, which confirms the exclude kept it out of startup context.
