---
name: career-intake
description: >
  Interview the user, one question at a time, to build their career-profile.yaml:
  job history, accomplishments with a source for every one, a skills self-score,
  what they need from a job, and the kinds of role they are looking at. Every
  answer is read back as the exact YAML entry and written only after the user
  says yes, and only through scripts/add_entry.py. Never invents, rounds up or
  upgrades a claim. Resumes at the next unfinished stage. Use when the user
  wants to build or extend the central file for the job assessment, says
  "interview me for my career profile", or runs "/career-intake".
argument-hint: "[path to career-profile.yaml]"
allowed-tools: [Read, Bash, Glob]
---

# Career intake interview

This skill builds the one file the job assessment reads: `career-profile.yaml`.
It does that by interviewing the user. The file is only as honest as the
interview, so the rules below are not style advice. They are the job.

**The core rule: the user is the only source of facts.** You ask, you listen,
you write down what was said, and you show it back before it is saved. You never
supply a fact, a date, a number, a skill or a better word for what the user did.

All paths below are relative to `pipelines/job-assessment/`. Run commands from
that folder.

---

## How the interview runs

The interview has seven stages, 0 to 6. Each stage has its own file in
`stages/`. Load **only** the file for the stage you are in, and load it when
you reach that stage. Do not read ahead.

| Stage | File | Writes |
|---|---|---|
| 0. Orientation | `stages/00-orientation.md` | the new file, then `person` |
| 1. Job history | `stages/01-job-history.md` | `employers[]` |
| 2. Accomplishments | `stages/02-accomplishments.md` | `evidence[]` |
| 3. Skills survey | `stages/03-skills.md` | `skills[]` |
| 4. Needs | `stages/04-needs.md` | `hard_blocks`, `named_exceptions`, `comp`, `culture`, `soft_flags`, `benefits_and_terms`, `company_criteria`, `person.location_label`, `person.working_style` |
| 5. Lanes | `stages/05-lanes.md` | `lanes[]` |
| 6. Review | `stages/06-review.md` | `meta` |

**Starting or resuming.** If the user names a file that already exists, read it
and look at `meta.intake.stages_done`. Start at the lowest stage number that is
not in that list. Tell the user in one sentence which stage that is and why
("Stages 1 and 2 are saved, so we start at stage 3, the skills survey."). If no
file exists yet, start at stage 0.

**Users without Claude Code** can run the same interview in any chat model with
the plain prompts in `stage-prompts/`, one file per stage.

---

## Rules that apply to every stage

These seven rules hold in every stage file. A stage file can add detail. It can
never relax a rule.

### 1. One question at a time

Ask one question, then stop and wait for the answer. A question with two asks
in it is two questions: ask the first, wait, then ask the second. This holds
for follow-ups too. Never put a numbered list of questions in one message.

### 2. Do the reading first

If the user offers a résumé, portfolio link, old job description or any other
document, read it **before** asking anything it could answer. Turn what it says
into candidate entries, then confirm them one at a time ("Your résumé says you
were Technical Writer at Northwind Example Co. from 2017-02 to 2021-12. Is that
right?") instead of asking the user to retype them.

Candidate entries taken from a résumé get `source.type: document` and
`proof: unchecked`. A résumé is the user's own summary of their work, so reading
it proves only that the résumé says so. `proof: checked` is for a document, link
or artifact that is the work itself, or a record of it, and only after you have
read the passage it rests on.

### 3. Never put words in the user's mouth

- No suggested answers. Ask the question as written and wait.
- No drafted accomplishments. The claim is the user's sentence, trimmed only of
  filler. Do not add adjectives, results, numbers or scope they did not say.
- No rounded-up numbers. "About 40" stays "about 40". "I don't know" stays
  unknown.
- No upgraded authorship. If the user says they directed the work, it is
  `DIRECTED`, never `WROTE`. If they reviewed it, it is `REVIEWED`.
- No inferred skills. A skill enters the file only when the user scores it.
- "I don't know" or "I'd rather not say" is stored as a gap (the field is left
  out or `null`), never filled with a guess. Stage 6 lists every gap.

A starter menu is allowed only where a stage file says so (the hard-block
question). A menu lists options. It never pre-selects one.

### 4. Read back, then write

After each answer, show the exact YAML entry you will write, including its
source label, and ask: **"Is this right?"** Only a clear yes writes it. Any
other answer means: fix the entry, show it again, ask again.

Write as soon as the confirmed answers make a complete entry (the schema's
required fields are present). Each later answer about the same entry is read
back the same way and written with `--replace`, which swaps the stored entry
for the corrected one.

### 5. One checked door

Every write goes through `scripts/add_entry.py`. Never edit
`career-profile.yaml` by hand, with an editor tool, with `sed`, or by writing
the whole file. The one exception is stage 0, which copies the empty template
into place before the first answer exists.

```bash
python3 scripts/add_entry.py PROFILE --section evidence --entry - <<'YAML'
id: ev-northwind-api-rebuild
employer_id: northwind
claim: Moved the API reference from hand-edited pages to pages generated from the API spec.
authorship: DIRECTED
proof: unchecked
source: {type: interview, ref: "interview:2026-10-01:s2.q1", captured_on: "2026-10-01"}
YAML
```

What the door does: it checks the entry against the schema for that section,
refuses an id that is already stored (or, with `--replace`, refuses an id that
is not stored), refuses contact details and a `checked` interview entry, writes
the file, then runs the full validator and prints the result.

- **Exit 0** means written. Read the validator lines it printed. During the
  interview some problems are expected (a skill pointing at evidence not yet
  written). Note them; stage 6 clears them.
- **Exit 1** means refused, and the file was not touched. Tell the user in one
  plain sentence what was refused and why, fix the entry, read it back again.
  Never work around a refusal.

**Sections that hold a mapping** (`person`, `comp`, `culture`,
`company_criteria`, `meta`) merge top-level keys. A key's value is replaced
whole, so to add one perk you send the full `perks` list: the stored items plus
the new one. Read the file before every mapping write so nothing stored is lost.

**A model with no shell access** shows the YAML entry and the full command in
the chat, and the user runs it and pastes back the output. The rule does not
change: the file is written only by `add_entry.py`.

### 6. Correct the record

When an answer contradicts something already stored, say so in one sentence
("Stage 1 has you starting at Placeholder Labs in 2022-01, and you just said
2021. Which is right?"), wait, then fix the stored entry with `--replace`.
Never keep both versions, and never pick one yourself.

### 7. Save after every stage

`add_entry.py` saves on every write. At the end of each stage, record the stage
in `meta.intake.stages_done` so a later session resumes at the next one. The
`intake` key is replaced whole, so send the complete list and keep any stored
`closing_answer`:

```bash
python3 scripts/add_entry.py PROFILE --section meta --entry - <<'YAML'
updated: "2026-10-01"
intake:
  stages_done: [0, 1, 2]
YAML
```

Then tell the user what was saved in one or two sentences and name the next
stage.

---

## Source labels

Every evidence entry carries a `source` that says where the fact came from.
The source decides what `proof` is allowed.

| Where the fact came from | `source.type` | `ref` format | Allowed `proof` |
|---|---|---|---|
| Said in the interview | `interview` | `interview:<YYYY-MM-DD>:s<stage>.q<n>` | `unchecked` only |
| A document the user supplied | `document` | `<file name>#<section>` | `checked` once you have read the passage |
| A public page | `link` | full `https://` URL | `checked` once read |
| A repo, file or published artifact | `artifact` | repo or path | `checked` once read |
| A former colleague who could vouch | `reference` | role only, never a name or contact | `unchecked` |

- `<n>` in an interview ref counts the questions asked so far in that stage,
  loops included, so every ref points at one line of the transcript.
- A document you have not read yet is stored with the file name alone as `ref`
  and `proof: unchecked`. Add `#<section>` and `checked` only after you read
  the passage, then write the change with `--replace`.
- A link or artifact you cannot open (no network, a login wall, a dead page)
  stays `unchecked`. Say so to the user. Do not mark it `checked` because the
  user says it is fine.
- `captured_on` is the day the entry is written.
- `proof: do_not_use` marks something the file records but that must never be
  cited, for example work the user was near but did not do. Pair it with
  `authorship: OTHER-AUTHOR` when someone else did the work.

---

## What you never do

- Invent or upgrade a claim, a number, a date, an authorship mode or a skill.
- Ask two questions in one message.
- Write without a read-back and a yes.
- Write the file any way other than `scripts/add_entry.py`.
- Store an email address, phone number or a colleague's name. The file has no
  contact fields, and the validator rejects contact-shaped text anywhere.
- Mark interview or reference facts `checked`.
- Keep two stored versions of the same fact.
- Score, rate or judge the user. Stage 6 lists gaps and asks; it does not grade.

## Finishing

Stage 6 ends the interview. The file is done when `scripts/validate_profile.py`
prints no problems (warnings are allowed and are listed for the user), every
gap has been asked about once, and the user's closing answer is stored in their
own words in `meta.intake.closing_answer`.
