# rules-index-architecture prompt 3 (Adapt and test it) on haiku

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

I'll propose a split for your small ruleset. Even though you only have five domains, splitting makes sense here because each is distinct—a reader won't have to scan past deploy rules to find the style guide.

## Proposed structure

```
rules/
  README.md                    <- index
  git-workflow.md
  testing-requirements.md
  deploy-process.md
  code-style.md
  reference/
    billing-migration-2023.md  <- excluded from startup
```

**`rules/README.md`** (index table)

```markdown
# Rules Index

| File | What it governs |
|---|---|
| git-workflow.md | Commit messages, branch protection, push safety |
| testing-requirements.md | Test coverage for bugs, pre-merge testing |
| deploy-process.md | Deployment workflow, timing restrictions |
| code-style.md | Type hints, function length limits |
```

**Exclude from startup:** `rules/reference/**` in your `settings.json`:
```json
{
  "claudeMdExcludes": ["rules/reference/**"]
}
```

The billing migration note is reference material you'll only need when working with that specific code, so it goes in `reference/` and stays out of every startup.

## How to test it worked

**Before/after measurement:**
```bash
# Before (current state)
wc -c CLAUDE.md

# After (new state)
cat CLAUDE.md rules/*.md | wc -c
```

Both should be the same total—splitting doesn't shrink what loads. Then verify the exclude works:
```bash
cat CLAUDE.md rules/*.md | wc -c    # with reference/
cat CLAUDE.md rules/[^r]*.md | wc -c  # without reference/ folder
```

The gap is what you saved by excluding.

**Testing question:** Ask "What must I include when I fix a bug?" The answer should come only from `testing-requirements.md` and mention adding a test. If the agent answers correctly, the rule file was loaded and understood in isolation.
