<!-- FICTIONAL EXAMPLE DATA. Not a real person. Saved by tests/prompt-runs/run_prompts.py -->
# Prompt run: Fix errors, on sonnet

- Prompt file: `prompts/06-fix-errors.txt`
- Date: 2026-10-01. Model alias `sonnet`, which ran as `claude-sonnet-5-5` (Claude Code can add a small helper model call of its own).
- Turns: 1. Cost: $0.03 (the simulated user's calls are not included).
- Grade: see `GRADES.md`.

## Conversation

### User

[the prompt below, with attached files: output of the failed command, fixtures/broken-profile.yaml]

I'm attaching the output of a failed command from this tool (the validator, the tests, check_findings.py or assess_offline.py) and the file it names. For each problem in the output, explain the cause in one or two plain sentences, name the YAML path or file the output points to (do not guess line numbers), and propose the smallest change that fixes it, shown as before and after. Change nothing else. Never invent a value I did not give you: where the right value is my call, such as a date, a number or which entry to keep, say so, offer the choices, and write the after with a placeholder such as <your value> instead of a guess. Suggest only values the file or the output shows are allowed; if the allowed values are not shown, say they are listed in schema/career-profile.schema.json instead of guessing. If the output is not enough to know the cause, name the single command I should run next. A good answer on the validator output for fixtures/broken-profile.yaml covers all five problems and names the missing evidence id that one skill points to.

### Model

All five problems in `fixtures/broken-profile.yaml` are covered below. No line numbers are given, only YAML paths.

## 1. `evidence[2].authorship`: "AUTHORED" is not allowed

**Cause:** The evidence entry `ev-placeholder-release-notes` uses `AUTHORED`, which is not in the allowed list (WROTE, DIRECTED, CO-WROTE, DESIGNED, REVIEWED, OTHER-AUTHOR).

**Which value is right is your call.** The claim says you "rewrote" the template, so `WROTE` fits, but `CO-WROTE` applies if someone else shared the work.

```yaml
# before
    authorship: AUTHORED
# after
    authorship: <WROTE or CO-WROTE>
```

## 2. `skills[1].evidence_ids`: unknown evidence id

**Cause:** The Style guides skill points to `ev-placeholder-style-guide`, and no evidence entry has that id. The missing id is **`ev-placeholder-style-guide`**. The file has only three ids: `ev-northwind-api-rebuild`, `ev-placeholder-docs-ci` and `ev-placeholder-release-notes`.

**Your call, with two choices:**
- Point the skill at an existing entry. The release-notes entry is the closest topical match, but only you know whether it backs this skill.
- Add a new evidence entry with the id `ev-placeholder-style-guide`. That needs a claim, dates and a source from you, which I can't supply.

```yaml
# before (path: skills[1].evidence_ids)
    evidence_ids: [ev-placeholder-style-guide]
# after
    evidence_ids: [<an existing evidence id, or the id of the entry you add>]
```

## 3. `comp`: pay numbers out of order

**Cause:** The required order is `floor <= min <= open_ask <= target <= stretch_ceiling`, but `min` (98000) is above `open_ask` (85000). The other values (floor 75000, target 100000, stretch_ceiling 175000) already fit the order.

**Your call, with two choices:**
- Lower `min` to somewhere between 75000 and 85000.
- Raise `open_ask` to somewhere between 98000 and 100000.

```yaml
# before
  min: 98000
  open_ask: 85000
# after (change one of the two)
  min: <your value, 75000 to 85000>
  open_ask: 85000
# or
  min: 98000
  open_ask: <your value, 98000 to 100000>
```

## 4. `evidence[1].proof`: interview source cannot be "checked"

**Cause:** The entry `ev-placeholder-docs-ci` has `source.type: interview`, and nothing was read to back it, so `proof: checked` is not allowed. The output gives two fixes.

**Your call, with two choices:**
- Set `proof` to `unchecked`. This is the smaller change and matches the facts as they stand.
- Keep `checked` and point `source` at a document, link or artifact you can actually supply.

```yaml
# before
    proof: checked
# after
    proof: unchecked
```

## 5. `skills[2]`: `self_score` 5 with `last: never`

**Cause:** The GraphQL skill claims a score of 5 but says it was never used, and a score of 4 or 5 needs some real use.

**Your call, with two choices:**
- Lower `self_score`. The output says only that it must be below 4, so I can't pick the number for you.
- Fix `last` if you have used GraphQL. The allowed values for `last` aren't shown in the output; they are listed in `schema/career-profile.schema.json`.

```yaml
# before
    self_score: 5
    last: never
# after (change one of the two)
    self_score: <your value, below 4>
    last: never
# or
    self_score: 5
    last: <your value, from schema/career-profile.schema.json>
```

Nothing else in the file needs to change. After you pick the values, rerun `python3 scripts/validate_profile.py fixtures/broken-profile.yaml` to confirm the result.

One note: this file is a test fixture. Its header says it must keep exactly five planted mistakes so the validator exits 1, and `tests/test_validate_profile.py` lists them. If you're fixing it rather than just reading the output, check whether the tests expect it to stay broken.
