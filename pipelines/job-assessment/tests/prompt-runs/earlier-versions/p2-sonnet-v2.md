<!-- FICTIONAL EXAMPLE DATA. Not a real person. Saved by tests/prompt-runs/run_prompts.py -->
# Prompt run: Customize to my background (build my central file), on sonnet

- Prompt file: `prompts/02-customize.txt`
- Date: 2026-10-01. Model alias `sonnet`, which ran as `claude-sonnet-5-5` (Claude Code can add a small helper model call of its own).
- Turns: 25. Cost: $2.89 (the simulated user's calls are not included).
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

I'm attaching intake/SKILL.md and intake/templates/career-profile.template.yaml. Interview me to build my own career-profile.yaml. Ask exactly one question at a time and wait for my answer. If a question has two parts, ask them separately. Never suggest an answer and never invent a fact, date, number or skill. After each answer, show the exact YAML entry you would add, with its source label, and ask me to confirm it. Anything I cannot point to a document, link or artifact for gets proof: unchecked. You cannot run commands or open files here, so never claim to have written anything: once I confirm an entry, show the scripts/add_entry.py command for me to run, then ask the next question. Start with stage 0, orientation. A good session ends with a file that passes scripts/validate_profile.py.

### Model

We're at stage 0, orientation. I only have `SKILL.md` and the template, not `stages/00-orientation.md`, so I'm working from the rules in `SKILL.md`.

Here's how it will go:
- I ask one question at a time and never suggest an answer.
- After each answer I show the exact YAML entry with its source label and ask "Is this right?"
- Once you say yes, I show the `scripts/add_entry.py` command for you to run. I can't run it or open files here, so I won't claim anything is written.
- Anything you can't point to a document, link or artifact for stays `proof: unchecked`.
- "I don't know" or "I'd rather not say" is stored as a gap, not a guess.

First, create the empty file. From `pipelines/job-assessment/`, run this (adjust the template path if yours differs):

```bash
cp intake/templates/career-profile.template.yaml career-profile.yaml
```

Do you have a résumé or any other document you'd like me to read before we start? If so, paste its text here. If not, say so and we'll go straight to questions.

### User

Done, it printed no errors. No resume or portfolio to read. Start from scratch.

### Model

What name should the file use for you? A first name or nickname is fine.

### User

Robin Sample.

### Model

Here is the entry I would add, with its source label.

```yaml
display_name: "Robin Sample"
```

Section: `person`
Source: interview, `interview:2026-10-01:s0.q2`. The `person` section has no `source` field, so this label lives only in the transcript and not in the file.

Is this right?

### User

Yes, that's right.

### Model

Run this from `pipelines/job-assessment/`:

```bash
python3 scripts/add_entry.py career-profile.yaml --section person --entry - <<'YAML'
display_name: "Robin Sample"
YAML
```

Paste the output back here. If it exits with 1, tell me what it refused and I'll fix the entry.

Next question: what job title or titles are you looking for?

### User

Done, it printed no errors. Senior Technical Writer and Docs Platform Engineer.

### Model

Here is the entry I would add.

```yaml
target_roles: ["Senior Technical Writer", "Docs Platform Engineer"]
```

Section: `person`
Source: interview, `interview:2026-10-01:s0.q3`. As before, `person` has no `source` field, so the label stays in the transcript.

Is this right?

### User

Yes, that's right.

### Model

Run this from `pipelines/job-assessment/`:

```bash
python3 scripts/add_entry.py career-profile.yaml --section person --entry - <<'YAML'
target_roles: ["Senior Technical Writer", "Docs Platform Engineer"]
YAML
```

The `person` section merges top-level keys, so `display_name` stays as stored. Paste the output back here.

Next question: how many whole years of experience do you have in your field?

### User

Done, it printed no errors. 9.

### Model

Here is the entry I would add.

```yaml
years_experience: 9
```

Section: `person`
Source: interview, `interview:2026-10-01:s0.q4`. As before, the label stays in the transcript because `person` has no `source` field.

I have stored this as your own figure of 9 whole years, with no document behind it.

Is this right?

### User

Yes, that's right.

### Model

Run this from `pipelines/job-assessment/`:

```bash
python3 scripts/add_entry.py career-profile.yaml --section person --entry - <<'YAML'
years_experience: 9
YAML
```

Paste the output back here. That finishes everything stage 0 asks for. Per the save-after-every-stage rule, I would then record the stage in `meta`:

```yaml
updated: "2026-10-01"
intake:
  stages_done: [0]
```

Section: `meta`
Source: none. This is bookkeeping and not a claim from you, so it has no interview label.

Is this meta entry right?

### User

Done, it printed no errors. Yes, that's right.

### Model

Run this from `pipelines/job-assessment/`:

```bash
python3 scripts/add_entry.py career-profile.yaml --section meta --entry - <<'YAML'
updated: "2026-10-01"
intake:
  stages_done: [0]
YAML
```

Paste the output back here. If it saves, stage 0 is done. Your name, target roles and years of experience will be stored, and a later session will resume at stage 1, job history.

Stage 1 starts with this question: what is the name of the most recent employer you want in this file?

### User

Done, it printed no errors. Placeholder Labs, an invented developer tool company.

### Model

Here is what I have so far for this employer, read back before anything is saved.

```yaml
id: placeholder-labs
name: Placeholder Labs
```

Section: `employers`
Source: interview, `interview:2026-10-01:s1.q1`. `employers` entries have no `source` field, so the label stays in the transcript.

- **Not written yet:** the entry will be written once it also has your title and start date. I'll ask for those next, one at a time.
- **The id:** `placeholder-labs` is only a label I made from the name so other entries can point at it. It is not a fact about you.
- **What I left out:** I haven't stored that it is an invented developer tool company, because you gave that as an aside and not as a field answer. If you want it in the entry's `summary`, say so when we get there.

Is this right?

### User

Yes, that's right.

### Model

Next question: what was your job title at Placeholder Labs?

### User

Senior Technical Writer.

### Model

Here is the entry so far, with the title added.

```yaml
id: placeholder-labs
name: Placeholder Labs
title: Senior Technical Writer
```

Section: `employers`
Source: interview, `interview:2026-10-01:s1.q2`. As before, the label stays in the transcript.

Still not written. It needs a start date first, and I'll ask for that after you confirm.

Is this right?

### User

Yes, that's right.

### Model

Next question: in what year and month did you start at Placeholder Labs?

### User

January 2022.

### Model

Here is the entry so far, with the start date added.

```yaml
id: placeholder-labs
name: Placeholder Labs
title: Senior Technical Writer
start: 2022-01
```

Section: `employers`
Source: interview, `interview:2026-10-01:s1.q3`. As before, the label stays in the transcript.

Dates in this file use the `YYYY-MM` format, so "January 2022" is written as `2022-01`.

I haven't given you a command yet. I'd like to ask for the end date first, so the entry is written once and not replaced afterwards.

Is this right?

### User

Yes, that's right.

### Model

Next question: do you still work at Placeholder Labs, or did you leave? If you left, tell me the year and month.

### User

Still there.

### Model

Here is the entry with the end date added.

```yaml
id: placeholder-labs
name: Placeholder Labs
title: Senior Technical Writer
start: 2022-01
end: present
```

Section: `employers`
Source: interview, `interview:2026-10-01:s1.q4`. As before, the label stays in the transcript.

The template says `end` can be `present`, so "still there" is stored that way.

Is this right?

### User

Yes, that's right.

### Model

Run this from `pipelines/job-assessment/`:

```bash
python3 scripts/add_entry.py career-profile.yaml --section employers --entry - <<'YAML'
id: placeholder-labs
name: Placeholder Labs
title: Senior Technical Writer
start: 2022-01
end: present
YAML
```

Paste the output back here.

Next question: in one or two sentences, what were you there to do at Placeholder Labs?

### User

Done, it printed no errors. I lead documentation and run the system that builds and checks the docs.

### Model

Here is the entry with your summary added. It replaces the stored one, so the full entry is shown.

```yaml
id: placeholder-labs
name: Placeholder Labs
title: Senior Technical Writer
start: 2022-01
end: present
summary: I lead documentation and run the system that builds and checks the docs.
```

Section: `employers`
Source: interview, `interview:2026-10-01:s1.q5`. As before, the label stays in the transcript.

The summary is your sentence as you said it, with nothing added.

Is this right?

### User

Yes, that's right.

### Model

Run this from `pipelines/job-assessment/`:

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

Paste the output back here.

Next question: before Placeholder Labs, what was the name of the employer you worked for?

### User

Done, it printed no errors. Northwind Example Co., an invented software company.

### Model

Here is what I have so far for this employer. It is read back before anything is saved.

```yaml
id: northwind-example-co
name: Northwind Example Co.
```

Section: `employers`
Source: interview, `interview:2026-10-01:s1.q6`. As before, the label stays in the transcript.

- **Not written yet:** I'll ask for your title and dates next, then write the entry once.
- **The id:** `northwind-example-co` is only a label I made from the name so other entries can point at it. It is not a fact about you.
- **What I left out:** I haven't stored that it is an invented software company, same as before.

Is this right?

### User

Yes, that's right.

### Model

Next question: what was your job title at Northwind Example Co.?

### User

Technical Writer.

### Model

Here is the entry so far, with the title added.

```yaml
id: northwind-example-co
name: Northwind Example Co.
title: Technical Writer
```

Section: `employers`
Source: interview, `interview:2026-10-01:s1.q7`. As before, the label stays in the transcript.

Still not written. I'll ask for the start date after you confirm.

Is this right?

### User

Yes, that's right.

### Model

Next question: in what year and month did you start at Northwind Example Co.?

### User

February 2017.

### Model

Here is the entry so far, with the start date added.

```yaml
id: northwind-example-co
name: Northwind Example Co.
title: Technical Writer
start: 2017-02
```

Section: `employers`
Source: interview, `interview:2026-10-01:s1.q8`. As before, the label stays in the transcript.

"February 2017" is written as `2017-02`. I'll ask for the end date after you confirm, then write the entry once.

Is this right?

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
  display_name: "Robin Sample"
  target_roles: ["Senior Technical Writer", "Docs Platform Engineer"]
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

# Northwind Example Co. is not here yet: its read-back was never confirmed with an
# end date and no add_entry.py command was run for it.
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
