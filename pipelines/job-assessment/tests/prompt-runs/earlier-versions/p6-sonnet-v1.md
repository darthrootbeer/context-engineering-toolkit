<!-- FICTIONAL EXAMPLE DATA. Not a real person. Saved by tests/prompt-runs/run_prompts.py -->
# Prompt run: Fix errors, on sonnet

- Prompt file: `prompts/06-fix-errors.txt`
- Date: 2026-10-01. Model alias `sonnet`, which ran as `claude-sonnet-5-5` (Claude Code can add a small helper model call of its own).
- Turns: 1. Cost: $0.04 (the simulated user's calls are not included).
- Grade: see `GRADES.md`.

## Conversation

### User

[the prompt below, with attached files: output of the failed command, fixtures/broken-profile.yaml]

I'm attaching the output of a failed command from this tool (the validator, the tests, check_findings.py or assess_offline.py) and the file it names. For each problem in the output, explain the cause in one or two plain sentences, point to the exact line or YAML path, and propose the smallest change that fixes it, shown as before and after. Change nothing else. Never invent a value I did not give you: where the right value is my call, such as a date, a number or which entry to keep, say so and offer the choices. If the output is not enough to know the cause, name the single command I should run next. A good answer on the validator output for fixtures/broken-profile.yaml covers all five problems and names the missing evidence id that one skill points to.

### Model

All five problems are fixable with one-line edits. Three need a choice from you, because the right value is your call.

## 1. `evidence[2].authorship` (the `ev-placeholder-release-notes` entry)

**Cause:** `AUTHORED` isn't in the allowed list. The validator only accepts WROTE, DIRECTED, CO-WROTE, DESIGNED, REVIEWED or OTHER-AUTHOR.

**Your call:** the claim says "Rewrote the release notes template", so `WROTE` is the likely match. If someone else shared the work, `CO-WROTE` fits better.

```yaml
# before
    authorship: AUTHORED
# after
    authorship: WROTE
```

## 2. `skills[1].evidence_ids` (the `style_guides` skill)

**Cause:** the skill points to `ev-placeholder-style-guide`, and no evidence entry has that id. The ids in the file are `ev-northwind-api-rebuild`, `ev-placeholder-docs-ci` and `ev-placeholder-release-notes`.

**Your call**, pick one:
- **A.** Point to an existing entry, if one really backs this skill (maybe `ev-placeholder-release-notes`).
- **B.** Add a new `ev-placeholder-style-guide` entry under `evidence:`. That needs real facts from you (claim, dates, authorship, source), so I won't make them up.
- **C.** Use an empty list, `evidence_ids: []`, if the skill has no backing yet.

```yaml
# before
    evidence_ids: [ev-placeholder-style-guide]
# after (option A, only if you confirm it fits)
    evidence_ids: [ev-placeholder-release-notes]
```

## 3. `comp.min` and `comp.open_ask`

**Cause:** `min` is 130000 but `open_ask` is 125000. The order must be `floor <= min <= open_ask <= target <= stretch_ceiling`.

**Your call:** which number is wrong?
- **A.** If `min` is wrong, lower it to a value between 90000 (`floor`) and 125000.
- **B.** If `open_ask` is wrong, raise it to a value between 130000 and 140000 (`target`).

```yaml
# before
  min: 130000
  open_ask: 125000
# after (option A; <N> is yours to choose, 90000 to 125000)
  min: <N>
  open_ask: 125000
# after (option B; <N> is yours to choose, 130000 to 140000)
  min: 130000
  open_ask: <N>
```

## 4. `evidence[1].proof` (the `ev-placeholder-docs-ci` entry)

**Cause:** `source.type` is `interview`, meaning nothing was read to back the claim, so `proof: checked` isn't allowed.

**Fix:** the smallest change is to set `proof` to `unchecked`. Only change `source` to a document, link or artifact if you have a real one to point at.

```yaml
# before
    proof: checked
# after
    proof: unchecked
```

## 5. `skills[2]` (the `graphql` skill)

**Cause:** `self_score: 5` with `last: never` is a contradiction, because a score of 4 or 5 needs some real use.

**Your call**, pick one:
- **A.** Lower the score to 3 or less, which fits if you've never used it.
- **B.** Fix `last` to when you actually used it. The other skills use the form `2y`.

```yaml
# before
    self_score: 5
    last: never
# after (option A; <N> is yours to choose, 3 or less)
    self_score: <N>
    last: never
# after (option B; <period> is yours to choose, in the same form as "2y")
    self_score: 5
    last: <period>
```

After you choose, rerun `python3 scripts/validate_profile.py fixtures/broken-profile.yaml`.

**One thing to check before you edit:** this file is a test fixture, and the header says its five mistakes are planted on purpose. Fixing them will make the validator and `tests/test_validate_profile.py` stop matching, so you probably only want these edits if you're repairing a real profile, not this fixture.
