# typed-memory-system prompt 2 (Review it against your setup) on haiku

Prompt (the document's full text was pasted where it says [PASTE FILE]; other inputs filled with made-up samples):

```text
Here is a design pattern document: [PASTE FILE]

Below is a listing of my memory or notes folder with file sizes, plus the tool I use: Tool: Claude Code.
MEMORY.md 182 lines, 21,400 bytes
user_role.md 12 lines
feedback_testing.md 20 lines
feedback_commits.md 15 lines
project_billing_rewrite.md 40 lines
reference_dashboards.md 8 lines

Tell me which parts of the pattern my setup already has and which it lacks. Flag any number in the document (line limit, byte limit) that may be different for my tool and tell me how to find the real one. Name my biggest risk of hitting a size limit and one check I could automate.

A good answer says which parts of the pattern my listing already has and which it lacks, flags the line and byte limits as values that may differ for my tool and says how to find the real ones, and names one biggest size risk and one check I could automate.
```

Answer:

## What your setup already has

✓ **Four memory types** — user, feedback (2 files), project, reference — matching the pattern exactly  
✓ **Linked topic files** — individual files per topic instead of one growing dump  
✓ **A bounded index** (MEMORY.md as the table of contents)

## What you lack

✗ **Frontmatter in topic files** — The pattern specifies `---name: type---` metadata in each file so the system can validate them programmatically  
✗ **Organized index sections** — No visible grouping by type (## Feedback, ## Project, etc.) in MEMORY.md  
✗ **Topic index tier** — No INDEX-*.md files yet for when the main index grows too large  
✗ **Automated size checks** — No script running weekly to verify limits and warn before overflow

## Limits to verify for your version

The document cites **200 lines** and **25,000 bytes** for Claude Code 2.1.263. Those were not re-confirmed on version 2.1.287, so **test your own version**:

- Add 50 lines of test content to MEMORY.md, save, start a new Claude Code session, and check if the index still loads in full
- Repeat until the load truncates with a warning
- Check `wc -l` and `wc -c` to measure both limits precisely

## Your biggest risk: line limit imminent

**MEMORY.md is at 182/200 lines (91% full).** You have ~18 lines of headroom. Once you add a handful of new topics, the index will truncate at session start and hide everything past the cutoff. This is the highest-priority risk because a full index at session start is how the agent reads your memory—when it gets cut off, the session has no access to what was cut.

## One check to automate

A weekly script (or one you run before adding entries) that:

```bash
#!/bin/bash
lines=$(wc -l < MEMORY.md)
bytes=$(wc -c < MEMORY.md)
if [ $lines -gt 160 ] || [ $bytes -gt 20000 ]; then
  echo "⚠️  MEMORY.md is at $lines lines, $bytes bytes (80% threshold: 160 lines, 20000 bytes)"
  exit 1
fi
```

This gives you a warning at 80% instead of hitting the wall at 100%. Run it before adding entries, or set it to a weekly cron.

**Next step:** You're close enough to the limit that you should either test your exact limits now, or start compacting MEMORY.md into bundled format (combining short entries on one line) before you hit it.
