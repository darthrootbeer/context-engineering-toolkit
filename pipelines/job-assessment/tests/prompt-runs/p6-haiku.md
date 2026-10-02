<!-- FICTIONAL EXAMPLE DATA. Not a real person. Saved by tests/prompt-runs/run_prompts.py -->
# Prompt run: Fix errors, on haiku

- Prompt file: `prompts/06-fix-errors.txt`
- Date: 2026-10-01. Model alias `haiku`, which ran as `claude-haiku-4-5-20251001` (Claude Code can add a small helper model call of its own).
- Turns: 1. Cost: $0.02 (the simulated user's calls are not included).
- Grade: see `GRADES.md`.

## Conversation

### User

[the prompt below, with attached files: output of the failed command, fixtures/broken-profile.yaml]

I'm attaching the output of a failed command from this tool (the validator, the tests, check_findings.py or assess_offline.py) and the file it names. For each problem in the output, explain the cause in one or two plain sentences, name the YAML path or file the output points to (do not guess line numbers), and propose the smallest change that fixes it, shown as before and after. Change nothing else. Never invent a value I did not give you: where the right value is my call, such as a date, a number or which entry to keep, say so, offer the choices, and write the after with a placeholder such as <your value> instead of a guess. Suggest only values the file or the output shows are allowed; if the allowed values are not shown, say they are listed in schema/career-profile.schema.json instead of guessing. If the output is not enough to know the cause, name the single command I should run next. A good answer on the validator output for fixtures/broken-profile.yaml covers all five problems and names the missing evidence id that one skill points to.

### Model

## Problem 1: evidence[2].authorship
**Cause:** The value `AUTHORED` is not in the allowed list for the authorship field.

**Path:** `evidence[2].authorship`

**Fix:**
```yaml
# Before
authorship: AUTHORED

# After
authorship: WROTE
```

---

## Problem 2: skills[1].evidence_ids
**Cause:** The skill "Style guides" references `ev-placeholder-style-guide`, but that evidence id doesn't exist in the file (only three evidence items are defined).

**Path:** `skills[1].evidence_ids`

**Fix:** Either remove the reference or create the missing evidence. If removing:
```yaml
# Before
evidence_ids: [ev-placeholder-style-guide]

# After
evidence_ids: []
```

---

## Problem 3: comp pay order
**Cause:** The `min` value (98000) exceeds `open_ask` (85000), violating the required ordering: floor ≤ min ≤ open_ask ≤ target ≤ stretch_ceiling.

**Path:** `comp.min` and `comp.open_ask`

**Fix:** You need to decide the correct values. Choose one:
```yaml
# Before
floor: 75000
min: 98000
open_ask: 85000
target: 100000
stretch_ceiling: 175000

# After (choose your value)
floor: 75000
min: <your value>
open_ask: <your value>
target: 100000
stretch_ceiling: 175000
```

---

## Problem 4: evidence[1].proof
**Cause:** Interview sources cannot be marked as `checked` proof since there's no document to verify; they must use `unchecked`.

**Path:** `evidence[1].proof`

**Fix:**
```yaml
# Before
proof: checked

# After
proof: unchecked
```

---

## Problem 5: skills[2] score/last mismatch
**Cause:** A `self_score` of 5 requires recent real-world use, but `last: never` indicates no recent experience.

**Path:** `skills[2]`

**Fix:** Either lower the score or update the last-used date:
```yaml
# Before
self_score: 5
last: never

# After (choose one)
# Option A: lower the score
self_score: 3
last: never

# Option B: add recent use
self_score: 5
last: <your value>  # e.g., 1y, 2y, 6m
```
