# Stage 0: Orientation

**Writes:** a new `career-profile.yaml` copied from the template, then `person`.
**Rules:** every rule in `../SKILL.md` applies. One question at a time.

## Questions, in order

Ask one, wait for the answer, then ask the next.

1. "Where should the file live?"
2. "Do you have a résumé, portfolio or old job descriptions I should read first?"
3. "What name should the file use for you? A first name or a nickname is fine."
4. "Which job titles are you aiming for?"
5. "How many years have you worked in your field?"

Questions 1 and 2 are the stage 0 questions from the design. Questions 3 to 5
exist because the file's `person` section requires a name, at least one target
role and a years figure, and later stages cannot write to `person` until those
three are stored.

## What to do with each answer

**Question 1.** Copy the empty template to the place the user named. This is
the only write in the whole interview that does not go through `add_entry.py`,
because there is no file yet for it to check:

```bash
cp intake/templates/career-profile.template.yaml PATH/career-profile.yaml
```

If a file already exists there, do not overwrite it. Read it, check
`meta.intake.stages_done`, and resume at the right stage (see `../SKILL.md`).

**Question 2.** If the user offers documents, read every one of them now, before
question 3. Make a short list of candidate facts the documents state (names,
titles, dates, accomplishments). Keep the list in the conversation; nothing is
written yet. In stages 1 and 2, confirm each candidate one at a time instead of
asking the user to retype it. Every candidate from a résumé is stored as
`source.type: document`, `proof: unchecked` (see "Do the reading first").

If the user says no, move on. Do not ask again.

**Questions 3 to 5.** Read back each answer as you get it. Because the schema
needs all three fields together, write `person` once, after the third is
confirmed:

```yaml
display_name: Robin Sample
target_roles: [Senior Technical Writer, Docs Platform Engineer]
years_experience: 9
```

```bash
python3 scripts/add_entry.py PATH/career-profile.yaml --section person --entry - <<'YAML'
display_name: Robin Sample
target_roles: [Senior Technical Writer, Docs Platform Engineer]
years_experience: 9
YAML
```

- Use the titles exactly as the user said them.
- If the years answer is a range ("eight or nine"), ask once: "Which whole
  number should the file use?" If the user cannot pick, use the lower number
  and say so in the read-back. Never round up.

## End of stage

Record stage 0 in `meta.intake.stages_done`, tell the user the file exists and
where, and move to stage 1.
