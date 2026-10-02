# typed-memory-system prompt 2 (Review it against your setup) on sonnet

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

## Already in place

- **Types:** the filename prefixes (`user_`, `feedback_`, `project_`, `reference_`) match the four types. I can't confirm the `metadata: type:` frontmatter from a listing.
- **One small file per topic:** the largest is 40 lines, so topic files aren't a concern.
- **Separated reference and project state:** `reference_dashboards.md` and `project_billing_rewrite.md` are their own files.

## Missing or unverifiable

- **The index is far larger than its files.** `MEMORY.md` has 182 lines but only 5 topic files are listed. An index should be about one line per file, so either the listing is partial or `MEMORY.md` holds content directly. That is the "ever-growing dump" failure the pattern describes. At about 118 bytes per line, the entries look like content rather than pointers.
- **No second tier:** no `INDEX-*.md` files, so overflow has nowhere to go except deletion.
- **No automated check:** nothing in the listing suggests a weekly size check, a wrapper that logs every run, or an orphan-file check.
- **No compaction contract:** I see no written rules for what is safe to drop or merge.
- **Few feedback files:** I see only `feedback_testing` and `feedback_commits`. I can't tell whether confirmations ("that approach was right") are captured alongside corrections.

## Numbers to verify

The document's **200 lines** and **25,000 bytes** were observed in Claude Code 2.1.263 only. The author could not re-confirm them on 2.1.287, so treat them as unverified for your version. Two ways to find the real values:

1. **Empirical (more reliable):** in a scratch project, make a `MEMORY.md` of 300 short lines, then another that is over 30,000 bytes in fewer than 200 lines. Start a session in each. The harness should show a truncation warning naming the file and the limit that was hit.
2. **Static:** run `claude --version`, then search the installed program for `25000` and `200` near memory-loading code. That check failed for the document's author on 2.1.287, so don't rely on it alone.

Also, the topic-file limit is untested in the document.

## Biggest risk

**Line count.** You're at 182 of 200 lines (91%), with 18 lines of headroom. Bytes are at 21,400 of 25,000 (86%). Both are past the document's 80% warning thresholds (160 lines, 20,000 bytes), so you're already in the "compact on purpose" zone. Lines will break first, and any entries past the cutoff won't load in that session.

## One check to automate

A weekly size check, measuring bytes with `wc -c`, not characters:

```sh
#!/bin/sh
f="$HOME/.claude/projects/<your-project>/memory/MEMORY.md"   # adjust path
lines=$(wc -l < "$f"); bytes=$(wc -c < "$f")
echo "$(date -u +%FT%TZ) lines=$lines bytes=$bytes" >> "$HOME/memory-check.log"
[ "$lines" -ge 160 ] || [ "$bytes" -ge 20000 ] && echo "MEMORY.md near limit: $lines lines, $bytes bytes"
```

Run it from cron through a wrapper that logs on every run and complains if the script is missing, so a job that never ran can't look like a clean result.

The next step is to compact `MEMORY.md` into pointer lines and bundled entries, moving any inline content into topic files. Then add an `INDEX-*.md` tier, and don't delete anything.
