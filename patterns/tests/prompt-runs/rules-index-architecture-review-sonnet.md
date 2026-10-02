# rules-index-architecture prompt 2 (Review it against your setup) on sonnet

Prompt (the document's full text was pasted where it says [PASTE FILE]; other inputs filled with made-up samples):

```text
Here is a design pattern document: [PASTE FILE]

Below is the folder listing and approximate line counts of my own instruction files, plus the agent tool I use: Tool: Claude Code.
CLAUDE.md 410 lines
rules/git.md 90 lines
rules/testing.md 60 lines
rules/deploy.md 120 lines
rules/old-notes.md 300 lines (rarely needed)

Tell me whether my setup needs this pattern yet. Flag any claim in the document that may not be true for my tool, especially about what gets loaded at startup. Suggest which of my files should be split out, which should stay, and which belong in a reference folder, and give a reason for each.

A good answer judges from my listing whether the pattern is needed yet, says which startup-loading claims should be checked for my tool and does not assume them, and sorts my files into split out, stay, and reference folder with a reason for each.
```

Answer:

**Short answer:** yes, but mainly for `CLAUDE.md`. Your `rules/` folder is already split by domain. The 410-line `CLAUDE.md` and the 300-line `old-notes.md` are the real problems.

## Does your setup need it?

- **`CLAUDE.md` (410 lines):** This is past the point where the document says to split, since you're scrolling past unrelated rules to find one. It's likely a mix of domains.
- **`rules/` (four files):** These are already single-topic. An index for four files is more indirection than it's worth. Add `rules/README.md` once the `CLAUDE.md` split brings you to around 8 or more files.
- **Context cost:** Total is about 980 lines. If everything loads at startup, `old-notes.md` is 300 lines of mostly dead weight every session.

## Claims to check for your setup

I haven't inspected your install, so verify these rather than assuming them:

1. **Where `rules/` lives.** The document's exclude example uses `.claude/rules/`. If your folder is a plain `rules/` at the project root, it may not auto-load at all. Check whether it's under `.claude/`.
2. **"Loads every `.md` under `rules/` recursively."** The document says this was confirmed in one installed version. Confirm it in yours by asking the agent a question only `old-notes.md` can answer, in a fresh session.
3. **Pointers in `CLAUDE.md`.** A line like `Full rules: rules/git.md` is plain text, not an import. The agent reads the file only if it decides to. If you want guaranteed loading, check whether your version supports `@path` imports.
4. **`paths:` frontmatter and `claudeMdExcludes`.** Check that your version supports both and what glob syntax it expects. Test each on one file and compare loaded size.
5. **The character counts (150k to 177k).** These are from the author's setup and don't transfer. Measure your own with `wc -c CLAUDE.md rules/*.md` before and after.

## File sorting

| File | Verdict | Reason |
|---|---|---|
| `CLAUDE.md` (410) | **Split out, keep a core** | Keep only what's needed every session, plus pointers. Move each domain section into its own `rules/*.md`. Merge into `git.md`, `testing.md`, or `deploy.md` where the topic matches, so you don't duplicate rules. |
| `rules/git.md` (90) | **Stay** | Already one topic and a reasonable size. |
| `rules/testing.md` (60) | **Stay**, maybe add `paths:` | Add `paths:` for your test globs if it only matters when editing tests. |
| `rules/deploy.md` (120) | **Stay, trim**, maybe add `paths:` | Keep the rules here. Move long command listings and incident history to `reference/`. Consider `paths:` if it only applies to deploy or CI files. |
| `rules/old-notes.md` (300) | **Reference folder** | Move it to `rules/reference/`, split by topic if you can, and add `**/rules/reference/**` to `claudeMdExcludes`. If it's truly stale, archive or delete it instead (look at it first). |

## Suggested order

1. Measure the current load.
2. Move `old-notes.md` to `reference/` and add the exclude. This is the cheapest win.
3. Split `CLAUDE.md` by domain.
4. Add the index once you have 8 or more files, and add its row in the same change as each new file.
5. Re-measure.

If you paste `CLAUDE.md`, I can propose the actual split and index table.
