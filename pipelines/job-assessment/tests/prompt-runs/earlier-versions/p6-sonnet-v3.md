<!-- FICTIONAL EXAMPLE DATA. Not a real person. Saved by tests/prompt-runs/run_prompts.py -->
# Prompt run: Fix errors, on sonnet

Note: the pay figures in this record were changed after the run to fictional ones. Nothing else was edited; the scores and verdicts are as recorded.

- Prompt file: `prompts/06-fix-errors.txt`
- Date: 2026-10-01. Model alias `sonnet`, which ran as `claude-sonnet-5-5` (Claude Code can add a small helper model call of its own).
- Turns: 1. Cost: $0.03 (the simulated user's calls are not included).
- Grade: see `GRADES.md`.

## Conversation

### User

[the prompt below, with attached files: output of the failed command, fixtures/broken-profile.yaml]

I'm attaching the output of a failed command from this tool (the validator, the tests, check_findings.py or assess_offline.py) and the file it names. For each problem in the output, explain the cause in one or two plain sentences, point to the exact line or YAML path, and propose the smallest change that fixes it, shown as before and after. Change nothing else. Never invent a value I did not give you: where the right value is my call, such as a date, a number or which entry to keep, say so, offer the choices, and write the after with a placeholder such as <your value> instead of a guess. Any value you do suggest must be one the file or the output shows is allowed. If the output is not enough to know the cause, name the single command I should run next. A good answer on the validator output for fixtures/broken-profile.yaml covers all five problems and names the missing evidence id that one skill points to.

### Model

All five problems are in `fixtures/broken-profile.yaml`. Nothing was changed.

## 1. `evidence[2].authorship` (line with `authorship: AUTHORED`)

**Cause:** `AUTHORED` isn't in the allowed list (WROTE, DIRECTED, CO-WROTE, DESIGNED, REVIEWED, OTHER-AUTHOR).

**Which value is right is your call.** The claim is "Rewrote the release notes template", so `WROTE` fits the wording. If someone else did it with you, `CO-WROTE` is the alternative.

```yaml
# before
    authorship: AUTHORED
# after
    authorship: WROTE        # or CO-WROTE, <your choice>
```

## 2. `skills[1].evidence_ids` (style_guides)

**Cause:** The skill points to `ev-placeholder-style-guide`, and no evidence entry has that id. The ids in the file are `ev-northwind-api-rebuild`, `ev-placeholder-docs-ci` and `ev-placeholder-release-notes`.

**The missing id is `ev-placeholder-style-guide`.** Which fix to use is your call:
- Point the skill at an existing entry. `ev-placeholder-release-notes` is the closest match, but only you know whether it backs "Style guides".
- Or add a new evidence entry with that id. That needs facts only you have, so I won't invent them.

```yaml
# before
    evidence_ids: [ev-placeholder-style-guide]
# after (option A)
    evidence_ids: [<your choice: ev-placeholder-release-notes or another existing id>]
```

## 3. `comp` (`min` / `open_ask`)

**Cause:** The order must be `floor <= min <= open_ask <= target <= stretch_ceiling`, but `min` (98000) is above `open_ask` (85000).

**Which number is wrong is your call.** Either value fits between `floor` (75000) and `target` (100000), so keep one and change the other.

```yaml
# before
  min: 98000
  open_ask: 85000
# after (option A: lower min)
  min: <your value, between 75000 and 85000>
  open_ask: 85000
# after (option B: raise open_ask)
  min: 98000
  open_ask: <your value, between 98000 and 100000>
```

## 4. `evidence[1].proof` (ev-placeholder-docs-ci)

**Cause:** The source type is `interview`, and an interview can't carry `proof: checked` because nothing was read to back it.

**Smallest fix:** use `unchecked`, which the message names as allowed. The alternative is to change `source` to a document, link or artifact you actually have, which needs a value from you.

```yaml
# before
    proof: checked
# after
    proof: unchecked
```

## 5. `skills[2]` (graphql: `self_score` / `last`)

**Cause:** A score of 5 with `last: never` is a contradiction, because a 4 or 5 needs some real use.

**Which one is wrong is your call.**
- If you have never used GraphQL, lower the score. The output only says a 4 or 5 is not allowed here, so choose a lower value yourself.
- If you have used it, fix `last`. The only format this file shows is values like `2y`, so use your real figure.

```yaml
# before
    self_score: 5
    last: never
# after (option A: lower the score)
    self_score: <your value, below 4>
    last: never
# after (option B: fix last)
    self_score: 5
    last: <your value, e.g. in the same format as 2y>
```

Note that `skills[2]` also cites `ev-northwind-api-rebuild`, which is an OpenAPI rebuild rather than GraphQL. The validator doesn't flag this, so I'm leaving it alone, but it may be relevant to option A or B.
