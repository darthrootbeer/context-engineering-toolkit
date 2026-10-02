<!-- FICTIONAL EXAMPLE DATA. Not a real person. Saved by tests/prompt-runs/run_prompts.py -->
# Prompt run: Fix errors, on sonnet

Note: the pay figures in this record were changed after the run to fictional ones. Nothing else was edited; the scores and verdicts are as recorded.

- Prompt file: `prompts/06-fix-errors.txt`
- Date: 2026-10-01. Model alias `sonnet`, which ran as `claude-sonnet-5-5` (Claude Code can add a small helper model call of its own).
- Turns: 1. Cost: $0.04 (the simulated user's calls are not included).
- Grade: see `GRADES.md`.

## Conversation

### User

[the prompt below, with attached files: output of the failed command, fixtures/broken-profile.yaml]

I'm attaching the output of a failed command from this tool (the validator, the tests, check_findings.py or assess_offline.py) and the file it names. For each problem in the output, explain the cause in one or two plain sentences, point to the exact line or YAML path, and propose the smallest change that fixes it, shown as before and after. Change nothing else. Never invent a value I did not give you: where the right value is my call, such as a date, a number or which entry to keep, say so and offer the choices, and use only values the file or the output shows are allowed. If the output is not enough to know the cause, name the single command I should run next. A good answer on the validator output for fixtures/broken-profile.yaml covers all five problems and names the missing evidence id that one skill points to.

### Model

All five problems are below. I haven't changed any files.

## 1. `evidence[2].authorship`: "AUTHORED" is not allowed
**Cause:** The entry `ev-placeholder-release-notes` uses a value the schema doesn't have.
**Choices:** WROTE, DIRECTED, CO-WROTE, DESIGNED, REVIEWED, OTHER-AUTHOR. Which one is true is your call. The claim says "Rewrote the release notes template", so WROTE looks closest.

```yaml
# before
authorship: AUTHORED
# after (if you wrote it)
authorship: WROTE
```

## 2. `skills[1].evidence_ids`: unknown evidence id
**Cause:** The skill `style_guides` points to **`ev-placeholder-style-guide`**, and no evidence entry has that id. The ids in the file are `ev-northwind-api-rebuild`, `ev-placeholder-docs-ci` and `ev-placeholder-release-notes`.
**Choices:** Which is right depends on what you can back the skill with.
- Point it at an existing entry, if one really supports "Style guides". The release-notes template entry is the likeliest.
- Add a new evidence entry with the id `ev-placeholder-style-guide`. I'd need its claim, dates, authorship and source from you.

```yaml
# before
evidence_ids: [ev-placeholder-style-guide]
# after (option A)
evidence_ids: [ev-placeholder-release-notes]
```

## 3. `comp`: `min` is above `open_ask`
**Cause:** The order must be `floor <= min <= open_ask <= target <= stretch_ceiling`, but `min` is 98000 and `open_ask` is 85000.
**Choices:** The number is your decision. Change one of the two:
- Lower `min` to a value from 75000 (`floor`) to 85000.
- Raise `open_ask` to a value from 98000 to 100000 (`target`).

```yaml
# before
min: 98000
open_ask: 85000
# after (option A: you pick min, 75000–85000)
min: <your value>
open_ask: 85000
# after (option B: you pick open_ask, 98000–100000)
min: 98000
open_ask: <your value>
```

## 4. `evidence[1].proof`: interview source can't be "checked"
**Cause:** `ev-placeholder-docs-ci` has `source.type: interview` and `proof: checked`. An interview means nothing was read to verify the claim.
**Smallest fix:** set `proof` to `unchecked`. Only switch the source to a document, link or artifact if you have a real one. That would also need a new `ref` from you.

```yaml
# before
proof: checked
# after
proof: unchecked
```

## 5. `skills[2]`: `self_score: 5` with `last: never`
**Cause:** The `graphql` skill claims top proficiency but says you've never used it. A score of 4 or 5 needs some real use.
**Choices:** Pick whichever is true.
- Lower `self_score` below 4.
- Change `last` to when you actually used it. The file only shows `2y` and `never`, and the output doesn't list the allowed values, so I can't suggest others.

```yaml
# before
self_score: 5
last: never
# after (option A: you pick a score below 4)
self_score: <your value>
last: never
```

If you choose to fix `last` instead, run this first to see the allowed values:
`grep -n "last" scripts/validate_profile.py`

After the edits, re-run `python3 scripts/validate_profile.py fixtures/broken-profile.yaml`. Note that this file is a fixture meant to fail with exactly these five problems, so fixing them will break the test in `tests/test_validate_profile.py` unless you're working on a copy.
