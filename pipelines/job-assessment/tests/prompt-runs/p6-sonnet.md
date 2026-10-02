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

All five problems, in the order the validator printed them.

## 1. `evidence[2].authorship`

**Cause:** `AUTHORED` is not one of the allowed values. The output lists them: WROTE, DIRECTED, CO-WROTE, DESIGNED, REVIEWED, OTHER-AUTHOR.

**Path:** `evidence[2].authorship`, the entry with id `ev-placeholder-release-notes`.

Which value is right depends on what you actually did, so that's your call. The claim says "Rewrote the release notes template", which points to WROTE, but you know the situation better.

```yaml
# before
    authorship: AUTHORED
# after
    authorship: <your value: WROTE, DIRECTED, CO-WROTE, DESIGNED, REVIEWED or OTHER-AUTHOR>
```

## 2. `skills[1].evidence_ids`

**Cause:** The skill `style_guides` points to `ev-placeholder-style-guide`, and no evidence entry in the file has that id. The missing evidence id is **`ev-placeholder-style-guide`**.

**Path:** `skills[1].evidence_ids`.

Your options:
- Point it at an evidence id that already exists: `ev-northwind-api-rebuild`, `ev-placeholder-docs-ci` or `ev-placeholder-release-notes`. The release notes entry is the closest topical match, but you should confirm.
- Add a new evidence entry with the id `ev-placeholder-style-guide`.
- Use an empty list if there's no evidence for this skill.

```yaml
# before
    evidence_ids: [ev-placeholder-style-guide]
# after
    evidence_ids: [<an existing evidence id, or your new entry's id>]
```

## 3. `comp`

**Cause:** The pay numbers must satisfy `floor <= min <= open_ask <= target <= stretch_ceiling`. Here `min` (130000) is above `open_ask` (125000).

**Path:** `comp.min` and `comp.open_ask`.

Which number is wrong is your call. Either lower `min` to 125000 or less (and keep it at or above the floor of 90000), or raise `open_ask` to at least 130000 (and keep it at or below the target of 140000).

```yaml
# before
  min: 130000
  open_ask: 125000
# after (fix one of the two)
  min: <your value, between 90000 and open_ask>
  open_ask: 125000
# or
  min: 130000
  open_ask: <your value, between 130000 and 140000>
```

## 4. `evidence[1].proof`

**Cause:** The source type is `interview`, which can't carry `proof: checked` because nothing was read to back it. The validator offers two ways out: use `unchecked`, or point `source` at a document, link or artifact.

**Path:** `evidence[1].proof`, the entry with id `ev-placeholder-docs-ci`.

The smallest change is the first option:

```yaml
# before
    proof: checked
# after
    proof: unchecked
```

If you do have a document, link or artifact for this claim, change `source.type` and `source.ref` to it instead and keep `checked`. I won't make up that reference.

## 5. `skills[2]`

**Cause:** `self_score: 5` with `last: never` is a contradiction, because a score of 4 or 5 needs some real use.

**Path:** `skills[2]`, the skill `graphql`.

Either lower the score or correct `last`. Only you know which. The output doesn't show the allowed values for either field, so they are listed in `schema/career-profile.schema.json`.

```yaml
# before
    self_score: 5
    last: never
# after (fix one of the two)
    self_score: <your value, 3 or lower>
    last: never
# or
    self_score: 5
    last: <your value, from the allowed values in schema/career-profile.schema.json>
```

I haven't edited the file. After you pick the values, rerun `python3 scripts/validate_profile.py fixtures/broken-profile.yaml`.

One note: this file is a deliberate fixture with five planted mistakes, and `tests/test_validate_profile.py` expects the validator to fail on exactly these. If you fix them in place, that test will break. Make the changes in a copy, or only if you meant to repair the fixture.
