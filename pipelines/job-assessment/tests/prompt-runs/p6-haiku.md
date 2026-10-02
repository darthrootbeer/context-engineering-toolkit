<!-- FICTIONAL EXAMPLE DATA. Not a real person. Saved by tests/prompt-runs/run_prompts.py -->
# Prompt run: Fix errors, on haiku

Note: the pay figures in this record were changed after the run to fictional ones. Nothing else was edited; the scores and verdicts are as recorded.

- Prompt file: `prompts/06-fix-errors.txt`
- Date: 2026-10-01. Model alias `haiku`, which ran as `claude-haiku-4-5-20251001` (Claude Code can add a small helper model call of its own).
- Turns: 1. Cost: $0.03 (the simulated user's calls are not included).
- Grade: see `GRADES.md`.

## Conversation

### User

[the prompt below, with attached files: output of the failed command, fixtures/broken-profile.yaml]

I'm attaching the output of a failed command from this tool (the validator, the tests, check_findings.py or assess_offline.py) and the file it names. For each problem in the output, explain the cause in one or two plain sentences, name the YAML path or file the output points to (do not guess line numbers), and propose the smallest change that fixes it, shown as before and after. Change nothing else. Never invent a value I did not give you: where the right value is my call, such as a date, a number or which entry to keep, say so, offer the choices, and write the after with a placeholder such as <your value> instead of a guess. Suggest only values the file or the output shows are allowed; if the allowed values are not shown, say they are listed in schema/career-profile.schema.json instead of guessing. If the output is not enough to know the cause, name the single command I should run next. A good answer on the validator output for fixtures/broken-profile.yaml covers all five problems and names the missing evidence id that one skill points to.

### Model

# Problem 1: evidence[2].authorship
**Cause:** The authorship value "AUTHORED" is not in the allowed list. Based on the claim "Rewrote the release notes template," WROTE is the appropriate value.

**Location:** `evidence[2].authorship`

**Fix:**
```yaml
# Before
authorship: AUTHORED

# After
authorship: WROTE
```

---

# Problem 2: skills[1].evidence_ids
**Cause:** The skill references `ev-placeholder-style-guide`, but no evidence entry with that id exists in the file. The evidence section only contains `ev-northwind-api-rebuild`, `ev-placeholder-docs-ci`, and `ev-placeholder-release-notes`.

**Location:** `skills[1].evidence_ids`

**Fix:** You must either create a matching evidence entry or change the reference to an existing evidence id. If this skill should reference an existing entry, replace the reference:
```yaml
# Before
evidence_ids: [ev-placeholder-style-guide]

# After
evidence_ids: [<existing-evidence-id>]  # e.g., ev-placeholder-docs-ci
```

---

# Problem 3: comp
**Cause:** The compensation values are not in ascending order—min (98000) exceeds open_ask (85000). The correct order must be: floor ≤ min ≤ open_ask ≤ target ≤ stretch_ceiling.

**Location:** `comp.min` and `comp.open_ask`

**Fix:** Reorder the pay values:
```yaml
# Before
floor: 75000
min: 98000
open_ask: 85000
target: 100000
stretch_ceiling: 175000

# After
floor: 75000
min: <your value>
open_ask: <your value>
target: 100000
stretch_ceiling: 175000
```

---

# Problem 4: evidence[1].proof
**Cause:** Interview sources cannot have `proof: checked` because interviews cannot be independently verified like documents or links. Either change the proof to `unchecked` or change the source type to document/link.

**Location:** `evidence[1].proof` and `evidence[1].source.type`

**Fix:**
```yaml
# Before
proof: checked
source: {type: interview, ref: "interview:2026-10-01:s2.q3", captured_on: 2026-10-01}

# After (option 1: mark proof as unchecked)
proof: unchecked
source: {type: interview, ref: "interview:2026-10-01:s2.q3", captured_on: 2026-10-01}

# After (option 2: change source to document/link and keep checked)
proof: checked
source: {type: document, ref: "<document-path>", captured_on: 2026-10-01}
```

---

# Problem 5: skills[2]
**Cause:** A self_score of 5 requires recent use, but `last: never` indicates no recent use. Either lower the score or update the last field to a recent timeframe.

**Location:** `skills[2]` (graphql skill)

**Fix:**
```yaml
# Before
self_score: 5
last: never

# After (option 1: lower the score)
self_score: <your value>  # 3 or lower
last: never

# After (option 2: update last to recent use)
self_score: 5
last: <your value>  # e.g., 1y, 6m, 1m
```
