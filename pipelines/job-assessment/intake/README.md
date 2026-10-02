# Intake interview

**What it is.** A Claude Code skill that interviews you, one question at a time, and builds your `career-profile.yaml`: the one file the job assessment reads. It covers your job history, what you did at each job and where the proof of it lives, a 0 to 5 score on a list of skills, what you need from a job (pay, perks, hard limits), and the kinds of role you are looking at. The same interview also comes as plain prompts you can paste into any chat model.

**What problem it solves.** An assessment can only be as honest as the file behind it. If the file says you are strong at something you only watched others do, every verdict built on it is wrong in your favour. So the interview never writes a fact you did not say, labels where every accomplishment came from, and shows you each entry before it is saved. A skill score is kept as your own claim. It only counts as proven when it points at an accomplishment you described.

**How it was built.** Built by directing Claude Code. The author designed the interview rules and the question order, reviewed the output, and checked it against the file validator. It was not hand-typed. It is a set of instructions for a model plus the existing checked write script. There is no model training, no retrieval system, and no claim to production ML experience.

## How it works

- **`SKILL.md`** holds the rules for every stage and loads one stage file at a time.
- **`stages/00-orientation.md` to `stages/06-review.md`** hold the questions for each stage, in order, and how each answer becomes an entry.
- **`stage-prompts/00-orientation.txt` to `06-review.txt`** are the same seven stages as plain prompts, for people without Claude Code. Paste one per stage, with your current file attached.

| Stage | What it asks about | What it writes |
|---|---|---|
| 0. Orientation | where the file lives, documents to read first, your name, target roles, years in your field | the new file, `person` |
| 1. Job history | each employer, title and dates | `employers` |
| 2. Accomplishments | 2 to 5 things per employer, who did the work, what shows it happened | `evidence`, each with a source label |
| 3. Skills survey | a 0 to 5 score per skill, by offline form or in chat | `skills` |
| 4. Needs | hard limits, pay, perks, time off, wary phrases, work to avoid | `hard_blocks`, `comp`, `culture` and related lists |
| 5. Lanes | each kind of role and its own must-haves | `lanes` |
| 6. Review | the validator, a gap list, one question per gap, a closing question | `meta` |

**The rules it keeps.** One question at a time. Read any document you offer before asking what it already says. Never suggest an answer, round up a number or give you more credit than you claimed. Show the exact entry and its source label, and write it only after you say yes. Fix a contradicted entry instead of keeping two. Record each finished stage so a later session picks up where you stopped.

**One way to write.** Every answer is saved by `scripts/add_entry.py`. It checks the entry, refuses duplicates and dishonest labels (an interview answer marked as checked, for example), writes the file, and runs the full validator. The model never edits the file directly. Without shell access, the model shows the command and you run it. The two exceptions are copying the empty template at the start, and the skills form, whose saved file is merged by `intake/scripts/merge_survey.py`, a second checked script that refuses the whole merge if any answer is invalid.

## Requirements

- Python 3.10 or later with the packages in `../requirements.txt` (`pyyaml`, `jsonschema`, `pytest`).
- Claude Code for the skill, or any chat model for the plain prompts.
- Time for about 60 skill questions if you do the skills survey in chat. The offline form is quicker.

Run everything from `pipelines/job-assessment/`. To start, open Claude Code there and say "interview me for my career profile", or copy `intake/templates/career-profile.template.yaml` and paste `stage-prompts/00-orientation.txt` into your chat model.

## How it was verified

- The answers in `../fixtures/robin-sample/intake-answers.txt` (an invented person) were turned into entries the way the stage files describe and written one at a time through `scripts/add_entry.py`, starting from the empty template. `scripts/validate_profile.py` accepted the finished file with no problems. Its warnings were the gaps stage 6 is meant to ask about: accomplishments with no dates, and must-haves with no reason, because the scripted answers never gave them.
- The same run showed the write script refusing a duplicate entry, an interview answer marked as checked, and an authorship value outside the allowed list, each without changing the file.
- A model ran the intake skill with the `claude` CLI on Claude Sonnet, answering from the same scripted answers. The file it built passed the validator, with the same employers and lanes as the fictional person's file. The transcript is in `../tests/intake-transcript.md`.

What this does not prove: that the questions find everything worth saying about a career, or that a model will follow every rule on every run. The write script and the validator catch the mistakes that can be checked by code. The rest depends on the model and on you reading each entry before you say yes.

---

### Prompt for your AI model

Paste one of these into any AI model, together with the files it names.

**Build your own file**

<!-- prompt: prompts/02-customize.txt -->
```text
I'm attaching intake/SKILL.md and intake/templates/career-profile.template.yaml. Interview me to build my own career-profile.yaml. Ask exactly one question at a time and wait for my answer. If a question has two parts, ask them separately. Never suggest an answer and never invent a fact, date, number or skill. After each answer, show the exact YAML entry you would add, put its source label on its own line under it (for example interview:<today's date>:s<stage>.q<question>), and ask me to confirm it. Anything I cannot point to a document, link or artifact for gets proof: unchecked. You cannot run commands or open files here, so never claim to have written anything: once I confirm an entry, show the scripts/add_entry.py command for me to run, then ask the next question. Start with stage 0, orientation. A good session ends with a file that passes scripts/validate_profile.py.
```

**Find the gaps in your file**

<!-- prompt: prompts/05-find-gaps.txt -->
```text
I'm attaching the 'What the validator checks' section of ARCHITECTURE.md and my career-profile.yaml. Find the weak spots the validator cannot catch: skills scored 3 or higher that rest on thin evidence, unchecked evidence a posting would lean on, evidence with no dates, must-haves or hard blocks with no reason, and lanes whose requirements look copied from each other. For each, give the exact YAML path, why it matters for scoring, and one question you would ask me to fix it. Do not fill any gap yourself. A good answer on fixtures/gappy-profile.yaml finds all three planted gaps.
```

**Tested on:** Claude Sonnet and Claude Haiku, 2026-10-01. Results for every prompt are in `../tests/prompt-runs/GRADES.md`.
