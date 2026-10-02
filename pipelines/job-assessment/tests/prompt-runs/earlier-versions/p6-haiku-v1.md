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

I'm attaching the output of a failed command from this tool (the validator, the tests, check_findings.py or assess_offline.py) and the file it names. For each problem in the output, explain the cause in one or two plain sentences, point to the exact line or YAML path, and propose the smallest change that fixes it, shown as before and after. Change nothing else. Never invent a value I did not give you: where the right value is my call, such as a date, a number or which entry to keep, say so and offer the choices. If the output is not enough to know the cause, name the single command I should run next. A good answer on the validator output for fixtures/broken-profile.yaml covers all five problems and names the missing evidence id that one skill points to.

### Model

**Problem 1: evidence[2].authorship**
- **Cause:** AUTHORED is not an allowed authorship value. The validator accepts only WROTE, DIRECTED, CO-WROTE, DESIGNED, REVIEWED, or OTHER-AUTHOR.
- **Location:** Line 80, evidence id `ev-placeholder-release-notes`, field `authorship`
- **Fix:** Choose the appropriate authorship. Since the claim says "Rewrote," WROTE fits best:
  ```yaml
  # Before:
  authorship: AUTHORED
  # After:
  authorship: WROTE
  ```

**Problem 2: skills[1].evidence_ids**
- **Cause:** The skill references evidence id `ev-placeholder-style-guide`, which does not exist in the file (only ev-northwind-api-rebuild, ev-placeholder-docs-ci, and ev-placeholder-release-notes exist).
- **Location:** Line 115, skills id `style_guides`, field `evidence_ids`
- **Fix:** Replace with a valid evidence ID or remove it (your choice which evidence supports this skill):
  ```yaml
  # Before:
  evidence_ids: [ev-placeholder-style-guide]
  # After (remove):
  evidence_ids: []
  # Or after (point to valid ID):
  evidence_ids: [ev-placeholder-release-notes]
  ```

**Problem 3: comp pay numbers out of order**
- **Cause:** The min value (98000) exceeds open_ask (85000), but the validator requires min ≤ open_ask.
- **Location:** Lines 20–22, comp section, fields `min` and `open_ask`
- **Fix:** Adjust the values so min ≤ open_ask (your choice which values are correct):
  ```yaml
  # Before:
  min: 98000
  open_ask: 85000
  # After (example):
  min: 85000
  open_ask: 98000
  ```

**Problem 4: evidence[1].proof**
- **Cause:** Interview sources cannot carry proof: checked because no document was read to verify it; use proof: unchecked instead, or change source to point to a document, link, or artifact.
- **Location:** Lines 62–67, evidence id `ev-placeholder-docs-ci`, fields `proof` and `source`
- **Fix:** Change proof to unchecked:
  ```yaml
  # Before:
  proof: checked
  source: {type: interview, ref: "interview:2026-10-01:s2.q3", captured_on: 2026-10-01}
  # After:
  proof: unchecked
  source: {type: interview, ref: "interview:2026-10-01:s2.q3", captured_on: 2026-10-01}
  ```

**Problem 5: skills[2] contradiction**
- **Cause:** A self_score of 5 requires real recent use to back it, but last: never indicates no use at all.
- **Location:** Lines 121–127, skills id `graphql`, fields `self_score` and `last`
- **Fix:** Either lower the score or add recent use (your choice which is accurate):
  ```yaml
  # Before:
  self_score: 5
  last: never
  # After option 1 (lower score):
  self_score: 3
  last: never
  # After option 2 (add recent use):
  self_score: 5
  last: 1y
  ```
