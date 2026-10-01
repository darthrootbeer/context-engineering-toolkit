# Stage 3: Skills survey

**Writes:** `skills[]`
**Rules:** every rule in `../SKILL.md` applies. One question at a time.

A skill score is the user's own claim. It is never proof. The assessment
counts a skill as proven only when it points at an evidence entry, and reports
the rest as "unproven". That is not a failure; it is the file being honest.

The list of skills comes from `intake/templates/skills-catalog.yaml`: about 60
items in ten groups. Each group has a 0 anchor and a 5 anchor in plain words.

## Choose a way to do it

Ask: "There are about 60 skills to score. Do you want to fill in a form on your
own (option A), or go through them here with me, one at a time (option B)?"

### Option A: the offline form

1. The user opens `intake/templates/skills-survey.html` in a browser, straight
   from disk. No server, nothing is sent anywhere.
2. They score the items, then click Download, which saves a JSON file.
3. They run, or you run with their go-ahead:

   ```bash
   python3 intake/scripts/merge_survey.py PROFILE path/to/skills-survey-DATE.json --dry-run
   python3 intake/scripts/merge_survey.py PROFILE path/to/skills-survey-DATE.json
   python3 scripts/validate_profile.py PROFILE
   ```

   `merge_survey.py` is a second checked door, used only for the survey file:
   it refuses the whole merge if any answer is invalid, writes only the
   `skills:` block, and never touches evidence links. You do not edit its
   output. Show the user the dry-run report before the real merge, and treat
   it as the read-back.
4. Then go to "Linking skills to evidence" below.

### Option B: in the chat

Go through the catalog group by group, item by item. For each item ask, one at
a time:

1. "From 0 to 5, where 0 is [group's 0 anchor] and 5 is [group's 5 anchor],
   where are you on [item label]?"

For items scored 2 or higher, then ask, one at a time:

2. "Do you want more of it in your next job, don't mind it, or would you rather
   avoid it?"
3. "When did you last use it: within the last 2 years, 2 to 5 years ago, longer
   ago, or never?"
4. "Did you do it yourself, by directing AI, or by teaching others?" (more than
   one can be true)

If the user says a whole group does not apply ("skip the design group"), write
nothing for it. A skipped item is left out of the file, never stored as 0.

If the user names a skill that is not in the catalog, it can be added. Use the
user's words as the `label`, make an id from it, ask question 1 for it, and
show any `match` pattern you propose in the read-back so the user can check it.

**Turning answers into an entry**

| Field | From |
|---|---|
| `id`, `label`, `group`, `match` | the catalog item (or the user's words for an added skill) |
| `self_score` | question 1, a whole number 0 to 5 |
| `next` | question 2: `more`, `neutral` (don't mind) or `avoid` |
| `last` | question 3: `2y`, `5y`, `5plus` or `never` |
| `how` | question 4: any of `self`, `ai`, `team` |
| `evidence_ids` | "Linking skills to evidence" below |

Write each item once its questions are answered:

```bash
python3 scripts/add_entry.py PROFILE --section skills --entry - <<'YAML'
id: api-specs
label: API specifications (OpenAPI)
group: web
self_score: 4
next: more
last: 2y
how: [self, ai]
YAML
```

A score of 4 or 5 with `last: never` is refused by the door. If that happens,
read the contradiction back to the user and ask which part is right.

## Linking skills to evidence

For each skill scored 3 or higher, ask, one at a time:

- "Which of your accomplishments shows [skill]?"

Read back the user's own list of accomplishments (the `claim` lines from stage
2, and their "Skills used" notes) so they can pick. Do not pick for them.

- If they name one or more, write the ids with `--replace` on that skill.
- If they say "none of them", leave `evidence_ids` empty. The skill is marked
  unproven, never failed, and stage 6 will ask about it once.

Never link evidence the user did not name, and never link an entry marked
`proof: do_not_use` or `authorship: OTHER-AUTHOR`.

## End of stage

Tell the user how many skills were scored, and how many at 3 or higher have no
evidence yet. Record stage 3 in `meta.intake.stages_done` and move to stage 4.
