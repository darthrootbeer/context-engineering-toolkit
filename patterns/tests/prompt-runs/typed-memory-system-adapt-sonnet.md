# typed-memory-system prompt 3 (Adapt and test it) on sonnet

Prompt (the document's full text was pasted where it says [PASTE FILE]; other inputs filled with made-up samples):

```text
Here is a design pattern document: [PASTE FILE]

My tool is: Claude Code. Here are five things I want it to remember: 1. I am a backend engineer who knows Go but not React. 2. Do not mock the database in integration tests; we got burned when mocks passed and the real migration failed. 3. Yes, the single bundled PR was the right call for the refactor. 4. The billing rewrite must finish before 2026-12-01 because of an audit. 5. Pipeline bugs are tracked in the Ops board in the issue tracker.

Sort each into a memory type, write the topic files and the index for them, and then write a short script that checks the index against a size limit in bytes. Finish with a test: how I check the next session actually loaded the index, and how I confirm the size check fails when I add too much.

A good answer sorts each of my five items into a memory type, writes topic files and an index for them, gives a script that measures the index in bytes, and finishes with a test that the next session loaded the index and a test that the size check fails when the index grows too large.
```

Answer:

I sorted the five items, then wrote the files, the script and the tests. Nothing has been written to disk yet.

## Sorting

| # | Item | Type | Why |
|---|---|---|---|
| 1 | Backend engineer, knows Go, not React | `user` | Who you are and what you know |
| 2 | Don't mock the DB in integration tests | `feedback` | A correction, with the reason it hurt |
| 3 | Single bundled PR was right for the refactor | `feedback` | A confirmation of a non-obvious call |
| 4 | Billing rewrite due before 2026-12-01 (audit) | `project` | Ongoing state with an absolute date |
| 5 | Pipeline bugs live on the Ops board | `reference` | A pointer to where information lives |

## Files

Put these in your memory folder. For Claude Code that is usually `~/.claude/projects/<project>/memory/`, but check yours.

`MEMORY.md`
```markdown
# Memory Index

## User
- [Backend engineer, Go not React](user_background.md) strong Go, new to React: explain frontend concepts, skip backend basics

## Feedback
- [No DB mocks in integration tests](feedback_no_db_mocks_integration.md) mocks passed, real migration failed
- [Bundled PR for refactors](feedback_bundled_refactor_pr.md) confirmed: one PR was right for the refactor

## Project
- [Billing rewrite](project_billing_rewrite.md) must finish before 2026-12-01, audit

## Reference
- [Pipeline bugs: Ops board](reference_pipeline_bugs.md) tracked on the Ops board in the issue tracker
```

`user_background.md`
```markdown
---
name: user-background
description: user's role and expertise, for tuning explanations
metadata:
  type: user
---
Backend engineer. Fluent in Go; does not know React.
**How to apply:** don't explain Go or backend basics. When touching frontend code, explain React concepts (hooks, state, rendering) briefly and relate them to backend ideas where possible.
```

`feedback_no_db_mocks_integration.md`
```markdown
---
name: feedback-no-db-mocks-integration
description: integration tests must hit a real database, not mocks
metadata:
  type: feedback
---
Do not mock the database in integration tests.
**Why:** mocked tests passed but the real migration failed.
**How to apply:** when writing or editing integration tests, use a real database and run real migrations. Mocks are fine only in unit tests.
```

`feedback_bundled_refactor_pr.md`
```markdown
---
name: feedback-bundled-refactor-pr
description: confirmed that one bundled PR was the right shape for the refactor
metadata:
  type: feedback
---
A single bundled PR was the right call for the refactor.
**Why:** confirmed by the user after the fact. Splitting would have been the default instinct, so this is a validated non-obvious choice.
**How to apply:** for similar refactors where the pieces only make sense together, bundle them without asking again. This is specific to tightly coupled refactors, not all changes.
```

`project_billing_rewrite.md`
```markdown
---
name: project-billing-rewrite
description: billing rewrite deadline driven by an audit
metadata:
  type: project
---
The billing rewrite must finish before 2026-12-01.
**Why:** an audit depends on it.
**How to apply:** prioritize billing-rewrite work, and flag anything that risks the date. Update this file as scope or status changes.
```

`reference_pipeline_bugs.md`
```markdown
---
name: reference-pipeline-bugs
description: where pipeline bugs are tracked
metadata:
  type: reference
---
Pipeline bugs are tracked on the Ops board in the issue tracker.
**How to apply:** look there for existing bugs before investigating, and point to it when a pipeline bug needs filing.
```

## Size check script

`memory-size-check.sh`
```bash
#!/usr/bin/env bash
# Usage: memory-size-check.sh [memory_dir]
# Limits are the values observed in Claude Code 2.1.263; re-check for your version.
set -u

DIR="${1:-$HOME/.claude/projects/PROJECT/memory}"
INDEX="$DIR/MEMORY.md"
MAX_LINES="${MAX_LINES:-200}"
MAX_BYTES="${MAX_BYTES:-25000}"
WARN_LINES=$((MAX_LINES * 80 / 100))
WARN_BYTES=$((MAX_BYTES * 80 / 100))

if [ ! -f "$INDEX" ]; then
  echo "FAIL: index not found: $INDEX"
  exit 2
fi

lines=$(wc -l < "$INDEX" | tr -d ' ')
bytes=$(wc -c < "$INDEX" | tr -d ' ')   # bytes, not characters
status=0

echo "index: $lines lines (limit $MAX_LINES), $bytes bytes (limit $MAX_BYTES)"

if [ "$lines" -ge "$MAX_LINES" ] || [ "$bytes" -ge "$MAX_BYTES" ]; then
  echo "FAIL: index is at or over a limit; content past the cut is not loaded"
  status=1
elif [ "$lines" -ge "$WARN_LINES" ] || [ "$bytes" -ge "$WARN_BYTES" ]; then
  echo "WARN: index is over 80% of a limit; compact now"
  status=1
fi

# Every link in the index must resolve
while IFS= read -r f; do
  [ -f "$DIR/$f" ] || { echo "FAIL: broken link: $f"; status=1; }
done < <(grep -o '](\([^)]*\.md\))' "$INDEX" | sed 's/^](//; s/)$//')

# Every topic file should be linked from the index
for f in "$DIR"/*.md; do
  b=$(basename "$f")
  [ "$b" = "MEMORY.md" ] && continue
  grep -q "]($b)" "$INDEX" || { echo "WARN: not in index: $b"; status=1; }
done

[ "$status" -eq 0 ] && echo "OK"
exit "$status"
```

Run `chmod +x memory-size-check.sh` first. The weekly cron entry should go through a wrapper that logs every run, as the document describes.

## Tests

**1. Did the next session load the index?** Add a canary as the last line of `MEMORY.md`, because the end is what gets cut first:

```markdown
- [Canary](reference_canary.md) the canary word is "heron-4471"
```

Create `reference_canary.md` with any content so the link resolves. Start a fresh session and ask:

> Without opening any files, what is my background, what is the billing deadline, and what is the canary word?

- **Pass:** you get Go but not React, 2026-12-01, and "heron-4471". Those come from the index gists alone, and the canary proves the tail was read.
- **Fail:** the canary is missing or a truncation warning appears. Check the size script's output.

Delete the canary line and file afterwards.

**2. Does the size check fail when the index grows too large?** Run this on a copy so your real memory stays untouched:

```bash
T=$(mktemp -d) && cp ~/.claude/projects/PROJECT/memory/*.md "$T/"

# Baseline: should print OK, exit 0
./memory-size-check.sh "$T"; echo "exit=$?"

# Line limit: pad past 160 lines (80% of 200) -> expect WARN, exit 1
for i in $(seq 1 170); do echo "- [Pad $i](reference_pipeline_bugs.md) filler" >> "$T/MEMORY.md"; done
./memory-size-check.sh "$T"; echo "exit=$?"

# Byte limit with few lines: multibyte padding -> expect WARN/FAIL, exit 1
cp ~/.claude/projects/PROJECT/memory/MEMORY.md "$T/MEMORY.md"
for i in $(seq 1 40); do printf -- '- [Pad](reference_pipeline_bugs.md) %s\n' "$(printf 'é%.0s' $(seq 1 450))" >> "$T/MEMORY.md"; done
./memory-size-check.sh "$T"; echo "exit=$?"

# Broken link: expect FAIL, exit 1
echo "- [Ghost](missing.md) nope" >> "$T/MEMORY.md"
./memory-size-check.sh "$T"; echo "exit=$?"
```

- **Pass:** the baseline exits 0, and each of the other three exits 1 with the matching message.
- **Third case:** it stays well under 200 lines, so only the byte count can trip it. If it doesn't fire, the script is counting characters instead of bytes.

One caveat: the 200-line and 25,000-byte limits come from your document's observations on Claude Code 2.1.263, and they weren't confirmed on later versions. The script reads them from `MAX_LINES` and `MAX_BYTES`, so you can change them without editing the script.
