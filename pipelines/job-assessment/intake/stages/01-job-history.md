# Stage 1: Job history

**Writes:** `employers[]`
**Rules:** every rule in `../SKILL.md` applies. One question at a time.

## Questions, in order

Ask one, wait for the answer, then ask the next. Start with the most recent
job and work backwards.

1. "What is the most recent place you worked?"
2. "What was your title there?"
3. "What month and year did you start?"
4. "What month and year did you leave, or are you still there?"
5. "In one or two sentences, what were you there to do?"
6. "Was there a job before that?"

If the answer to question 6 is yes, loop back to question 1 for that job
(ask "What was the place you worked before that?"). Stop when the answer is no.

If stage 0 read a résumé, confirm each employer from it instead of asking
questions 1 to 4 cold: "Your résumé lists Technical Writer at Northwind
Example Co., 2017-02 to 2021-12. Is that right?" Ask only what the résumé
does not say.

## Follow-ups, only when an answer leaves a gap

- A vague date ("a while ago", "after the pandemic"): "Roughly which year?"
- A year with no month: "Do you remember the month?" If not, store January of
  that year and write "(start month not known, stored as January)" into the
  read-back so the user sees it. Do the same for an end date.

No other follow-ups in this stage.

## Turning answers into an entry

| Field | From | Notes |
|---|---|---|
| `id` | the place's name | lowercase, words joined with `_` (`northwind`, `placeholder_labs`). Show it in the read-back. |
| `name` | question 1 | the name only. Drop descriptions like "a small software company". |
| `title` | question 2 | exactly as said |
| `start` | question 3 | `YYYY-MM`, quoted |
| `end` | question 4 | `YYYY-MM`, quoted, or `present` |
| `summary` | question 5 | the user's sentence, trimmed of filler only |

Write as soon as `id`, `name`, `title` and `start` are confirmed (after
question 3). Questions 4 and 5 then update the stored entry with `--replace`,
each after its own read-back:

```bash
python3 scripts/add_entry.py PROFILE --section employers --entry - <<'YAML'
id: northwind
name: Northwind Example Co.
title: Technical Writer
start: "2017-02"
YAML
```

```bash
python3 scripts/add_entry.py PROFILE --section employers --entry - --replace <<'YAML'
id: northwind
name: Northwind Example Co.
title: Technical Writer
start: "2017-02"
end: "2021-12"
YAML
```

A personal project, freelance work or a career break is not an employer.
Accomplishments from them are stored in stage 2 with `employer_id: null`.

## End of stage

Read back the list of employers (name, title, dates) in one short block and ask
whether anything is missing. Then record stage 1 in `meta.intake.stages_done`
and move to stage 2.
