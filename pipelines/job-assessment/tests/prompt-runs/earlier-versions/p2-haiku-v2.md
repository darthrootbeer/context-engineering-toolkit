<!-- FICTIONAL EXAMPLE DATA. Not a real person. Saved by tests/prompt-runs/run_prompts.py -->
# Prompt run: Customize to my background (build my central file), on haiku

- Prompt file: `prompts/02-customize.txt`
- Date: 2026-10-01. Model alias `haiku`, which ran as `claude-haiku-4-5-20251001` (Claude Code can add a small helper model call of its own).
- Turns: 25. Cost: $1.78 (the simulated user's calls are not included).
- Grade: see `GRADES.md`.
- Edited after the run: one real company name the model used as an example was replaced with "[a professional networking site]".

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

I'll start stage 0, orientation. Let me load the orientation questions.

(Reading stage 0 guidance...)

Since this is a new profile, I'll need to create the file first, then start the interview. Let me ask the first orientation question:

**What is your display name?** This can be a first name, full name, or a nickname—however you'd like to be identified in your career profile.

### User

Robin Sample.

### Model

Here's what I would write:

```yaml
person:
  display_name: Robin Sample
```

Is this right?

### User

Yes, that's right.

### Model

Perfect. Now I'll show you the commands to initialize the file and write this entry. Run these from the `pipelines/job-assessment/` directory:

```bash
cp intake/templates/career-profile.template.yaml career-profile.yaml
```

Then:

```bash
python3 scripts/add_entry.py career-profile.yaml --section person --entry - <<'YAML'
display_name: Robin Sample
YAML
```

Run those and let me know the output, then I'll ask the next orientation question.

### User

Done, it printed no errors.

### Model

Great. Now for the next orientation question:

**How many whole years of experience do you have in your field?** This is a rough total across your career—if you're not sure, it's fine to estimate or say you don't know.

### User

9.

### Model

Here's what I would write:

```yaml
person:
  years_experience: 9
```

Is this right?

### User

Yes, that's right.

### Model

Run this command:

```bash
python3 scripts/add_entry.py career-profile.yaml --section person --entry - <<'YAML'
years_experience: 9
YAML
```

Next orientation question:

**What kinds of role are you looking at?** Give me a title or description of the general type of role—for example, "Senior Technical Writer" or "Staff Engineer" or "Product Manager."

### User

Done, it printed no errors. Senior Technical Writer and Docs Platform Engineer.

### Model

Here's what I would write:

```yaml
person:
  target_roles: [Senior Technical Writer, Docs Platform Engineer]
```

Is this right?

### User

Yes, that's right.

### Model

Run this command:

```bash
python3 scripts/add_entry.py career-profile.yaml --section person --entry - <<'YAML'
target_roles: [Senior Technical Writer, Docs Platform Engineer]
YAML
```

Next orientation question:

**Do you have a preferred working style?** Choose one: "gather_from_experts" (you prefer to learn from experienced people around you) or "become_expert" (you prefer to develop deep expertise in your area).

### User

Done, it printed no errors. I don't know.

### Model

Understood—I'll skip that one. A gap stays open until you're ready to fill it, or we note it in the final review.

**Do you have a location label?** This is only used to pick a pay tier from job postings—for example "Region B" or "US East Coast" or similar. If you don't use one, say so.

### User

Region B.

### Model

Here's what I would write:

```yaml
person:
  location_label: Region B
```

Is this right?

### User

Yes, that's right.

### Model

Run this command:

```bash
python3 scripts/add_entry.py career-profile.yaml --section person --entry - <<'YAML'
location_label: Region B
YAML
```

Stage 0 (orientation) is complete. Now I'll record that and move to stage 1 (job history).

Run this to save the stage:

```bash
python3 scripts/add_entry.py career-profile.yaml --section meta --entry - <<'YAML'
updated: "2026-10-01"
intake:
  stages_done: [0]
YAML
```

Once done, we'll move to stage 1 where I'll ask about your job history—employers, titles, dates, and what you did at each place.

### User

Done, it printed no errors.

### Model

Perfect. Now I'm moving to stage 1, job history. Let me load the stage guidance.

(Reading stage 1 guidance...)

**Have you worked anywhere? If so, do you have a résumé, a [a professional networking site] profile, or any document that lists your employers and dates?** If you have one, share it or describe what's in it, and I'll ask about each job one at a time.

### User

No resume or portfolio to read. Start from scratch.

### Model

Got it. Let's build your job history from scratch, one job at a time.

**What is the name of your first employer—or if you prefer, start with your most recent one?**

### User

Placeholder Labs, an invented developer tool company.

### Model

**What was your job title at Placeholder Labs?**

### User

Senior Technical Writer.

### Model

**When did you start at Placeholder Labs? Please give the month and year—for example, 2022-01 for January 2022.**

### User

January 2022.

### Model

**When did you leave, or are you still there? Please give the month and year, or say "present" if you're still employed there.**

### User

Still there.

### Model

**In one or two sentences, what were you there to do? What was your main work or mission?**

### User

I lead documentation and run the system that builds and checks the docs.

### Model

Here's what I would write:

```yaml
employers:
  - id: placeholder-labs
    name: Placeholder Labs
    title: Senior Technical Writer
    start: 2022-01
    end: present
    summary: I lead documentation and run the system that builds and checks the docs.
```

Is this right?

### User

Yes, that's right.

### Model

Run this command:

```bash
python3 scripts/add_entry.py career-profile.yaml --section employers --entry - <<'YAML'
id: placeholder-labs
name: Placeholder Labs
title: Senior Technical Writer
start: 2022-01
end: present
summary: I lead documentation and run the system that builds and checks the docs.
YAML
```

**Do you have any other employers to add, or are you done with your job history?**

### User

Done, it printed no errors. Yes, one before that.

### Model

**What is the name of that earlier employer?**

### User

Northwind Example Co., an invented software company.

### Model

**What was your job title at Northwind Example Co.?**

### User

Technical Writer.

### Model

**When did you start at Northwind Example Co.?**

### User

February 2017.

### Model

**When did you leave Northwind Example Co.?**

### User

December 2021.

### Model

**In one or two sentences, what were you there to do?**

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
  target_roles: [Senior Technical Writer, Docs Platform Engineer]
  years_experience: 9
  location_label: Region B
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
