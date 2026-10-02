# rules-index-architecture prompt 2 (Review it against your setup) on haiku

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

Your setup is close to the pattern but not quite there yet. You're at ~980 lines spread across five files—the threshold where an index becomes useful, and where that 300-line rarely-needed file is dragging down startup load.

**Does your setup need this pattern?** Yes, but just barely. You've already felt the pain enough to split into domains (good instinct), but you're missing the index and the exclusion mechanism to complete it. The payoff is immediate: removing old-notes.md from startup load could save ~15–20% of your instruction context at session start.

**Verify this claim about Claude Code:** The document states that Claude Code loads CLAUDE.md plus *every* markdown file under `rules/` recursively at startup, with no default lazy loading. Before you reorganize, test this: ask the agent a specific detail from `old-notes.md` (something it shouldn't know unless it was loaded). If it answers correctly, the claim holds for your version.

**What to do with each file:**

| File | Action | Why |
|---|---|---|
| CLAUDE.md | Stay, but trim to ~150 lines | Keep only rules that apply every session. Move domain-specific stuff to the rules files where it belongs. |
| rules/git.md | Stay as-is | 90 lines is lean and focused. |
| rules/testing.md | Stay as-is | 60 lines is already minimal. |
| rules/deploy.md | Stay as-is | 120 lines is on the edge but specific enough to stay. |
| rules/old-notes.md | Move to rules/reference/old-notes.md, exclude from startup | 300 rarely-used lines is exactly what `claudeMdExcludes` is for. You can still consult it during a session if needed. |
| (new) rules/README.md | Add | One table: file name, one-line description. Five rows, takes 30 seconds. |

**Settings:** Add to your `settings.json`:
```json
{
  "claudeMdExcludes": ["rules/reference/**"]
}
```

Then test: before excluding, count characters in your rule files. After the exclude, ask the agent a question only something in old-notes.md can answer—it shouldn't know it anymore.
