<!-- FICTIONAL EXAMPLE DATA. Not a real person. Saved by tests/prompt-runs/run_prompts.py -->
# Prompt run: Customize to my background (build my central file), on sonnet

- Prompt file: `prompts/02-customize.txt`
- Date: 2026-10-01. Model alias `sonnet`, which ran as `claude-sonnet-5-5` (Claude Code can add a small helper model call of its own).
- Turns: 25. Cost: $2.76 (the simulated user's calls are not included).
- Grade: see `GRADES.md`.

## Checks run by code on the reply

```text
$ python3 scripts/validate_profile.py <tmp>/career-profile.yaml
validate_profile: clean, 1 warning(s) in career-profile.yaml
warning: culture.perks: the perks list is empty, so no perk can raise Culture.
(exit code 0)
```

## Conversation

### User

[the prompt below, with attached files: intake/SKILL.md, intake/templates/career-profile.template.yaml]

I'm attaching intake/SKILL.md and intake/templates/career-profile.template.yaml. Interview me to build my own career-profile.yaml. Ask exactly one question at a time and wait for my answer. If a question has two parts, ask them separately. Never suggest an answer and never invent a fact, date, number or skill. After each answer, show the exact YAML entry you would add, put its source label on its own line under it (for example interview:<today's date>:s<stage>.q<question>), and ask me to confirm it. Anything I cannot point to a document, link or artifact for gets proof: unchecked. You cannot run commands or open files here, so never claim to have written anything: once I confirm an entry, show the scripts/add_entry.py command for me to run, then ask the next question. Start with stage 0, orientation. A good session ends with a file that passes scripts/validate_profile.py.

### Model

This is stage 0, orientation. Here is how the session will work:

- I ask one question at a time and wait for your answer.
- After each answer I show the exact YAML entry and its source label, and ask you to confirm it.
- Once you confirm, I give you the `scripts/add_entry.py` command to run. I can't run anything myself, so nothing is written until you run it and paste back the output.
- Anything you can't point to a document, link or artifact for stays `proof: unchecked`.
- If you'd rather not answer or don't know, I record a gap and never fill it in.

Before the first write I'll give you the one-time command that copies the template into place, so the file exists.

Question 1 of stage 0: what name should appear in the file as your `display_name`? A first name or nickname is fine.

### User

Robin Sample.

### Model

Here is the entry I would add:

```yaml
display_name: Robin Sample
```

Source label:

```
interview:2026-10-01:s0.q1
```

Is this right?

### User

Yes, that's right.

### Model

Run these from `pipelines/job-assessment/`. The first command copies the empty template into place. It only needs running once, and it's the one exception to the rule against touching the file directly. Adjust the template path if yours lives elsewhere.

```bash
cp intake/templates/career-profile.template.yaml career-profile.yaml
```

Then write the entry:

```bash
python3 scripts/add_entry.py career-profile.yaml --section person --entry - <<'YAML'
display_name: Robin Sample
YAML
```

Paste back what it prints. Validator problems are expected at this point, because the file is mostly empty. If it exits with a refusal, tell me and I'll fix the entry.

Question 2 of stage 0: how many whole years of experience do you have in your field?

### User

Done, it printed no errors. 9.

### Model

Here is the entry I would add:

```yaml
display_name: Robin Sample
years_experience: 9
```

Source label:

```
interview:2026-10-01:s0.q2
```

`person` is a mapping, so the whole entry is sent each time: the stored `display_name` plus the new key. Nothing already stored gets lost.

Is this right?

### User

Yes, that's right.

### Model

Run this:

```bash
python3 scripts/add_entry.py career-profile.yaml --section person --entry - <<'YAML'
display_name: Robin Sample
years_experience: 9
YAML
```

Paste back what it prints.

Question 3 of stage 0: what is the first role title you are targeting? If there are others, we'll add them one at a time afterwards.

### User

Done, it printed no errors. Senior Technical Writer and Docs Platform Engineer.

### Model

You gave two titles, so I've put both in the list. Here is the entry I would add:

```yaml
display_name: Robin Sample
years_experience: 9
target_roles: [Senior Technical Writer, Docs Platform Engineer]
```

Source label:

```
interview:2026-10-01:s0.q3
```

Is this right?

### User

Yes, that's right.

### Model

Run this:

```bash
python3 scripts/add_entry.py career-profile.yaml --section person --entry - <<'YAML'
display_name: Robin Sample
years_experience: 9
target_roles: [Senior Technical Writer, Docs Platform Engineer]
YAML
```

Paste back what it prints.

That covers everything stage 0 writes. The remaining `person` fields, `location_label` and `working_style`, are asked in stage 4. To save your place, here is the entry that records stage 0 as done:

```yaml
updated: "2026-10-01"
intake:
  stages_done: [0]
```

Source label:

```
interview:2026-10-01:s0 (bookkeeping, not an interview answer, so no question number)
```

Is this right?

### User

Yes, that's right.

### Model

Run this:

```bash
python3 scripts/add_entry.py career-profile.yaml --section meta --entry - <<'YAML'
updated: "2026-10-01"
intake:
  stages_done: [0]
YAML
```

Paste back what it prints. Stage 0 is then saved, and a later session would resume at stage 1.

Stage 1 is job history, which writes `employers[]`. You attached only SKILL.md and the template, not the `stages/` files, so I'm working from the rules in SKILL.md and the template's `employers` fields: name, title, start, end and summary.

Question 1 of stage 1: what is the name of your most recent employer?

### User

Done, it printed no errors. Placeholder Labs, an invented developer tool company.

### Model

Here is the entry so far. It isn't written yet, because the schema needs more fields first (title and dates), so I'll hold it until it's complete:

```yaml
id: placeholder-labs
name: Placeholder Labs
```

Source label:

```
interview:2026-10-01:s1.q1
```

I left out "an invented developer tool company", since it describes the company and not your role. The `summary` field is for what you were there to do, and I'll ask about that separately.

Is this right?

### User

Yes, that's right.

### Model

Question 2 of stage 1: what was your job title at Placeholder Labs?

### User

Senior Technical Writer.

### Model

Here is the entry so far, still held until the dates are in:

```yaml
id: placeholder-labs
name: Placeholder Labs
title: Senior Technical Writer
```

Source label:

```
interview:2026-10-01:s1.q2
```

Is this right?

### User

Yes, that's right.

### Model

Question 3 of stage 1: in what year and month did you start at Placeholder Labs?

### User

January 2022.

### Model

Here is the entry so far, still held until the end date is in:

```yaml
id: placeholder-labs
name: Placeholder Labs
title: Senior Technical Writer
start: 2022-01
```

Source label:

```
interview:2026-10-01:s1.q3
```

Is this right?

### User

Yes, that's right.

### Model

Question 4 of stage 1: in what year and month did you leave Placeholder Labs, or are you still there?

### User

Still there.

### Model

The template says `end` can be `present`, so here is the entry:

```yaml
id: placeholder-labs
name: Placeholder Labs
title: Senior Technical Writer
start: 2022-01
end: present
```

Source label:

```
interview:2026-10-01:s1.q4
```

This now has the id, name, title and both dates. If you confirm, I'll give you the command to write it. The `summary` comes after, and I'll add it with `--replace`.

Is this right?

### User

Yes, that's right.

### Model

Run this:

```bash
python3 scripts/add_entry.py career-profile.yaml --section employers --entry - <<'YAML'
id: placeholder-labs
name: Placeholder Labs
title: Senior Technical Writer
start: 2022-01
end: present
YAML
```

Paste back what it prints.

Question 5 of stage 1: in one or two sentences, what were you there to do at Placeholder Labs?

### User

Done, it printed no errors. I lead documentation and run the system that builds and checks the docs.

### Model

Here is the entry with your summary added. It replaces the stored one, so the command will use `--replace`:

```yaml
id: placeholder-labs
name: Placeholder Labs
title: Senior Technical Writer
start: 2022-01
end: present
summary: I lead documentation and run the system that builds and checks the docs.
```

Source label:

```
interview:2026-10-01:s1.q5
```

I kept your sentence word for word and added nothing.

Is this right?

### User

Yes, that's right.

### Model

Run this:

```bash
python3 scripts/add_entry.py career-profile.yaml --section employers --entry - --replace <<'YAML'
id: placeholder-labs
name: Placeholder Labs
title: Senior Technical Writer
start: 2022-01
end: present
summary: I lead documentation and run the system that builds and checks the docs.
YAML
```

Paste back what it prints.

Question 6 of stage 1: what is the name of the employer you had before Placeholder Labs? If there wasn't one, tell me and we'll close the stage.

### User

Done, it printed no errors. Northwind Example Co., an invented software company.

### Model

Here is the entry so far, held until the title and dates are in:

```yaml
id: northwind-example-co
name: Northwind Example Co.
```

Source label:

```
interview:2026-10-01:s1.q6
```

As before, I left out "an invented software company", since it describes the company and not your role.

Is this right?

### User

Yes, that's right.

### Model

Question 7 of stage 1: what was your job title at Northwind Example Co.?

### User

Technical Writer.

### Model

Here is the entry so far, still held until the dates are in:

```yaml
id: northwind-example-co
name: Northwind Example Co.
title: Technical Writer
```

Source label:

```
interview:2026-10-01:s1.q7
```

Is this right?

### User

Yes, that's right.

### Model

Question 8 of stage 1: in what year and month did you start at Northwind Example Co.?

### User

February 2017.

### Model

Here is the entry so far, still held until the end date is in:

```yaml
id: northwind-example-co
name: Northwind Example Co.
title: Technical Writer
start: 2017-02
```

Source label:

```
interview:2026-10-01:s1.q8
```

Is this right?

### User

Yes, that's right.

### Model

Question 9 of stage 1: in what year and month did you leave Northwind Example Co.?

### User

Let's stop here for today. Print the whole career-profile.yaml as it would stand after I ran your commands: the template with every entry I confirmed written in, as one yaml code block and nothing else.

### Model

```yaml
# career-profile.yaml: your job history, your evidence, your skills and what you need
# from a job, in one file. The intake interview fills it in one checked answer at a
# time. Copy this file, then let the interview write to it through
# scripts/add_entry.py. Check it any time with:
#
#     python3 scripts/validate_profile.py career-profile.yaml
#
# Rules that keep the file honest:
#   - Every accomplishment is an evidence entry with a source. Where did the fact
#     come from: the interview, a document, a public link, an artifact, or a
#     reference? Interview and reference facts stay proof: unchecked.
#   - A skill score is your own claim. It is never proof on its own. An
#     assessment only counts a skill as proven when the skill points at evidence.
#   - There are no contact fields. Do not put an email address or phone number
#     anywhere; the validator rejects them.
#   - Ids use lowercase letters, digits, hyphens and underscores.
#
# Note: add_entry.py rewrites the file, so the comments below are dropped after the
# first write. This header block is kept. The commented examples show one entry of
# each kind; they are fictional.

schema_version: 1

person:
  display_name: Robin Sample
  target_roles:
    - Senior Technical Writer
    - Docs Platform Engineer
  years_experience: 9
  location_label: null
  working_style: null

sources: []

hard_blocks: []

named_exceptions: []

comp:
  currency: USD
  floor: null
  min: null
  open_ask: null
  target: null
  stretch_ceiling: null

culture:
  perks: []
  low_time_off_days: null
  hustle_phrases: []
  free_phrases: []

soft_flags: []

benefits_and_terms: []

company_criteria:
  high_interest: []
  good_not_dream: []

lanes: []

employers:
  - id: placeholder-labs
    name: Placeholder Labs
    title: Senior Technical Writer
    start: 2022-01
    end: present
    summary: I lead documentation and run the system that builds and checks the docs.

evidence: []

skills: []

writing_samples: []

meta:
  updated: "2026-10-01"
  intake:
    stages_done: [0]
```
