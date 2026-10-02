# typed-memory-system prompt 3 (Adapt and test it) on haiku

Prompt (the document's full text was pasted where it says [PASTE FILE]; other inputs filled with made-up samples):

```text
Here is a design pattern document: [PASTE FILE]

My tool is: Claude Code. Here are five things I want it to remember: 1. I am a backend engineer who knows Go but not React. 2. Do not mock the database in integration tests; we got burned when mocks passed and the real migration failed. 3. Yes, the single bundled PR was the right call for the refactor. 4. The billing rewrite must finish before 2026-12-01 because of an audit. 5. Pipeline bugs are tracked in the Ops board in the issue tracker.

Sort each into a memory type, write the topic files and the index for them, and then write a short script that checks the index against a size limit in bytes. Finish with a test: how I check the next session actually loaded the index, and how I confirm the size check fails when I add too much.

A good answer sorts each of my five items into a memory type, writes topic files and an index for them, gives a script that measures the index in bytes, and finishes with a test that the next session loaded the index and a test that the size check fails when the index grows too large.
```

Answer:

# Sorting your five items into memory types

1. **Backend engineer, knows Go not React** → `user`
2. **Don't mock the database in integration tests** → `feedback` (a correction/lesson learned)
3. **Single bundled PR was right for the refactor** → `feedback` (a confirmation)
4. **Billing rewrite deadline: 2026-12-01, audit-driven** → `project`
5. **Pipeline bugs tracked in Ops board** → `reference`

---

# Topic files

I'll create these four files for you:

**feedback_no_db_mocks.md**
```markdown
---
name: feedback-no-db-mocks
description: don't mock the database in integration tests
metadata:
  type: feedback
---
Do not mock the database in integration tests.

**Why:** mocks passed but the real migration failed, catching the bug only after deploy.

**How to apply:** write integration tests against a real (test) database. Let the migration run. Mocks hide real database issues.
```

**feedback_bundled_pr_refactor.md**
```markdown
---
name: feedback-bundled-pr-refactor
description: single bundled PR was the right call for the refactor
metadata:
  type: feedback
---
The single bundled PR approach for the refactor was correct.

**Why:** it kept related changes visible together and made the review simpler than breaking it into many small PRs.

**How to apply:** use this pattern again for similar refactors where the changes are interdependent.
```

**user_backend_engineer.md**
```markdown
---
name: user-backend-engineer
description: backend engineer, Go expertise, no React
metadata:
  type: user
---
Backend engineer. Expertise in Go. Does not know React; steer away from frontend tasks or pair on them.
```

**project_billing_rewrite.md**
```markdown
---
name: project-billing-rewrite
description: deadline 2026-12-01, audit-driven
metadata:
  type: project
---
Billing rewrite must finish by **2026-12-01** (audit deadline). Blocks other work. No slip room.
```

**reference_pipeline_bugs.md**
```markdown
---
name: reference-pipeline-bugs
description: pipeline bugs tracked in Ops board
metadata:
  type: reference
---
Pipeline bugs are tracked in the Ops board in the issue tracker. Not in a separate system. Check there first.
```

---

# Memory index

Create a file called `MEMORY.md` in a `.claude-memory` folder (or wherever you keep your memory):

```markdown
# Memory Index

## User
- [Backend engineer](user_backend_engineer.md) Go expertise, no React

## Feedback
- [No DB mocks](feedback_no_db_mocks.md) mocks passed, real migration failed
- [Bundled PR refactor](feedback_bundled_pr_refactor.md) single PR was correct approach

## Project
- [Billing rewrite](project_billing_rewrite.md) deadline 2026-12-01, audit-driven

## Reference
- [Pipeline bugs location](reference_pipeline_bugs.md) Ops board in issue tracker
```

---

# Size check script

Create `memory-size-check.sh`:

```bash
#!/bin/bash
set -e

MEMORY_FILE=".claude-memory/MEMORY.md"
BYTE_LIMIT=25000
WARNING_THRESHOLD=20000  # 80% of limit

if [[ ! -f "$MEMORY_FILE" ]]; then
  echo "Error: $MEMORY_FILE not found"
  exit 1
fi

BYTES=$(wc -c < "$MEMORY_FILE")
LINES=$(wc -l < "$MEMORY_FILE")

echo "Memory index: $BYTES bytes, $LINES lines"

if [[ $BYTES -gt $LIMIT ]]; then
  echo "⚠️  WARNING: $MEMORY_FILE exceeds $BYTE_LIMIT byte limit by $((BYTES - BYTE_LIMIT)) bytes"
  exit 1
elif [[ $BYTES -gt $WARNING_THRESHOLD ]]; then
  echo "⚠️  CAUTION: $MEMORY_FILE is at $((BYTES * 100 / BYTE_LIMIT))% of limit"
  exit 0
else
  echo "✓ Memory index is healthy"
  exit 0
fi
```

Make it executable: `chmod +x memory-size-check.sh`

---

# Tests

**Test 1: Verify the index loads in the next session**

At the start of the next Claude Code session:
1. Ask me: "What do I know about your backend stack?"
2. I should reference Go, React avoidance, and the database mocking lesson without you restating it.
3. If I mention these facts without you re-explaining them, the index loaded.

Alternatively, check the session logs: if the `.claude-memory/MEMORY.md` file was read, it appears in the context window summary.

**Test 2: Confirm the size check fails when you exceed the limit**

1. Add 5,000+ bytes of dummy content to `MEMORY.md` (push it past 20,000 bytes).
2. Run `./memory-size-check.sh`
3. It should print a WARNING and exit with code 1.

Restore the file and run again—it should pass.

---

**Current state:** Your index is ~700 bytes. You have plenty of room. Run the script weekly (add to cron: `0 22 * * 0 /path/to/memory-size-check.sh`) to catch drift early.
