<!-- FICTIONAL EXAMPLE DATA. Not a real person. Saved by tests/prompt-runs/run_prompts.py -->
# Prompt run: Fix errors, on haiku

- Prompt file: `prompts/06-fix-errors.txt`
- Date: 2026-10-01. Model alias `haiku`, which ran as `claude-haiku-4-5-20251001` (Claude Code can add a small helper model call of its own).
- Turns: 1. Cost: $0.03 (the simulated user's calls are not included).
- Grade: see `GRADES.md`.

## Conversation

### User

[the prompt below, with attached files: output of the failed command, fixtures/broken-profile.yaml]

I'm attaching the output of a failed command from this tool (the validator, the tests, check_findings.py or assess_offline.py) and the file it names. For each problem in the output, explain the cause in one or two plain sentences, point to the exact line or YAML path, and propose the smallest change that fixes it, shown as before and after. Change nothing else. Never invent a value I did not give you: where the right value is my call, such as a date, a number or which entry to keep, say so and offer the choices, and use only values the file or the output shows are allowed. If the output is not enough to know the cause, name the single command I should run next. A good answer on the validator output for fixtures/broken-profile.yaml covers all five problems and names the missing evidence id that one skill points to.

### Model

# Problems in fixtures/broken-profile.yaml

**Problem 1: evidence[2].authorship**
"AUTHORED" is not in the allowed list. Change it to an allowed value.
- Line: `evidence[2]` (ev-placeholder-release-notes), authorship field
- Before: `authorship: AUTHORED`
- After: `authorship: WROTE`

**Problem 2: skills[1].evidence_ids**
The reference "ev-placeholder-style-guide" doesn't exist in the evidence section. You decide which existing evidence to link: ev-northwind-api-rebuild, ev-placeholder-docs-ci, or ev-placeholder-release-notes.
- Line: `skills[1].evidence_ids` (style_guides skill)
- Before: `evidence_ids: [ev-placeholder-style-guide]`
- After: `evidence_ids: [ev-placeholder-docs-ci]`

**Problem 3: comp**
The order is wrong: min (130000) must be ≤ open_ask (125000). You decide which to change to fix the sequence floor ≤ min ≤ open_ask ≤ target ≤ stretch_ceiling.
- Lines: `comp.min` and `comp.open_ask`
- Before: `min: 130000` / `open_ask: 125000`
- After: `min: 125000` / `open_ask: 130000` (or adjust other values)

**Problem 4: evidence[1].proof**
An interview source cannot carry proof: checked because no document was read to verify it. Change to unchecked.
- Line: `evidence[1].proof` (ev-placeholder-docs-ci)
- Before: `proof: checked`
- After: `proof: unchecked`

**Problem 5: skills[2]**
A self_score of 5 contradicts last: never—a score of 4–5 requires recent real use. You decide: lower the score or update last to a recent timeframe (e.g., 6m, 1y, 2y).
- Line: `skills[2]` (graphql skill)
- Before: `self_score: 5` / `last: never`
- After: `self_score: 3` / `last: never` (or keep 5 and change `last: 2y`)
