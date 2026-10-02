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

I'm attaching the output of a failed command from this tool (the validator, the tests, check_findings.py or assess_offline.py) and the file it names. For each problem in the output, explain the cause in one or two plain sentences, point to the exact line or YAML path, and propose the smallest change that fixes it, shown as before and after. Change nothing else. Never invent a value I did not give you: where the right value is my call, such as a date, a number or which entry to keep, say so, offer the choices, and write the after with a placeholder such as <your value> instead of a guess. Any value you do suggest must be one the file or the output shows is allowed. If the output is not enough to know the cause, name the single command I should run next. A good answer on the validator output for fixtures/broken-profile.yaml covers all five problems and names the missing evidence id that one skill points to.

### Model

## Problem 1: Invalid authorship value
**Cause:** `evidence[2]` (ev-placeholder-release-notes, line 63) has `authorship: AUTHORED`, but the validator only accepts WROTE, DIRECTED, CO-WROTE, DESIGNED, REVIEWED, or OTHER-AUTHOR.

**Fix:**
- Before: `authorship: AUTHORED`
- After: `authorship: <your value>` (choose from: WROTE, DIRECTED, CO-WROTE, DESIGNED, REVIEWED, OTHER-AUTHOR)

---

## Problem 2: Nonexistent evidence reference
**Cause:** `skills[1]` (style_guides, line 95) references `ev-placeholder-style-guide`, which doesn't exist in the evidence section—only ev-northwind-api-rebuild, ev-placeholder-docs-ci, and ev-placeholder-release-notes are defined.

**Fix:**
- Before: `evidence_ids: [ev-placeholder-style-guide]`
- After: `evidence_ids: [<your value>]` (must be one of the three evidence ids that exist)

---

## Problem 3: Compensation order violation
**Cause:** Lines 28–30 have `min: 98000` and `open_ask: 85000`, violating the required order of floor ≤ min ≤ open_ask ≤ target ≤ stretch_ceiling.

**Fix (choose one):**
- Before: `min: 98000` / `open_ask: 85000`
- After: `min: <your value>` / `open_ask: <your value>` (ensure min ≤ open_ask)

---

## Problem 4: Invalid proof type for interview source
**Cause:** `evidence[1]` (ev-placeholder-docs-ci, lines 51–56) sets `proof: checked` with `source.type: interview`, but interviews cannot validate proof—only documents, links, or artifacts can.

**Fix (choose one):**
- Before: `proof: checked` / `source: {type: interview, ...}`
- After: `proof: unchecked` (keep interview source), **OR** change `type: interview` to `type: document` or `type: link`

---

## Problem 5: Contradictory self-score and recency
**Cause:** `skills[2]` (graphql, lines 103–105) has `self_score: 5` with `last: never`—a 4 or 5 score requires recent real use, not "never."

**Fix (choose one):**
- Before: `self_score: 5` / `last: never`
- After: `self_score: <your value>` (lower to 3 or below), **OR** change `last: never` to a recent timeframe like `last: 2y` or `last: 1y`
