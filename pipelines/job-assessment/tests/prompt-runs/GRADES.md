<!-- FICTIONAL EXAMPLE DATA. Not a real person. Grades for the saved prompt runs in this folder. -->
# Prompt test grades

Every prompt in `prompts/` was run through the Claude Code command line on 2026-10-01, on Claude Sonnet (`claude-sonnet-5-5`) and Claude Haiku (`claude-haiku-4-5-20251001`). No other model was tried. Each run was a fresh session in an empty temp folder with no tools, no MCP servers, and only project settings loaded (there were none). Claude Code still tells every session some basic facts about its environment, such as its working folder; that is how one simulated user typed this machine's real home folder path, which was scrubbed from the record. The files a prompt names were pasted in after it, the way a person attaches files in a chat window. `run_prompts.py` in this folder does all of that and saves one record per prompt and model.

The grades were written by Claude Opus, reading each saved answer against the good-answer list below, which was written before any prompt was run. Two prompts also get a check by code: prompt 03's JSON is run through `check_findings.py` and `assess_offline.py`, and prompt 02's final file is run through `validate_profile.py`. Those results are at the top of each record.

Three prompts are conversations: 02, s1 and r2. For those a second model plays the user from a short script (Haiku for s1 and r2, Sonnet for 02 after Haiku proved unreliable in that role). A simulated user is not a person. Where it went off script, the grade below says so.

## Results for the published prompts

PASS means every item on the good-answer list held. PARTIAL means the main goal was met but at least one item failed. FAIL means the main goal was not met.

| Prompt | File | Sonnet | Haiku | Record |
|---|---|---|---|---|
| Understand and teach | `01-understand-and-teach.txt` | PASS | PASS | `p1-*.md` |
| Customize to my background (build my central file) | `02-customize.txt` | PASS | PARTIAL: some entries not read back after each answer, and one example equals the answer | `p2-*.md` |
| Run on my first posting | `03-run-first-posting.txt` | PASS | PASS (an earlier run of the same text failed the quote check, see below) | `p3-*.md` |
| Test the scoring with the fixture | `04-test-scoring.txt` | PASS | PASS | `p4-*.md` |
| Find gaps in my central file | `05-find-gaps.txt` | PASS | PASS | `p5-*.md` |
| Fix errors | `06-fix-errors.txt` | PASS | PARTIAL: suggests values the file does not allow | `p6-*.md` |
| Review the rules for gaps | `r1-review-rules.txt` | PASS | PASS (an earlier run of the same text was PARTIAL, see below) | `r1-*.md` |
| Walk me through setup | `s1-setup-walkthrough.txt` | PASS | PASS | `s1-*.md` |
| Customize the rubric | `r2-customize-rubric.txt` | PASS | PASS | `r2-*.md` |
| Understand the hook | `h1-understand-hook.txt` | PASS | PASS | `h1-*.md` |

**Timing note.** The final runs of prompts 01, 04, r1, r2 and h1 used the docs as they stood shortly before the final commit. After those runs, only two kinds of edit were made to the attached docs: the prompt blocks were copied again from `prompts/` (prompts 02, 03, 05, 06 and r1 had been rewritten), and the "Tested on" lines were filled in from this file.

## Good-answer lists, and what happened

### 01 Understand and teach

Good answer: covers the four topics in the order asked; gives the rule order as hard block, job-type override, Fit and Qualifications floor, reservations band, Apply; says unlisted pay scores 5 and Culture starts at 5; asks exactly one quiz question and stops; invents no rule, file or command.

- Sonnet: PASS on both runs.
- Haiku: PASS on both runs. Small slips that do not break the list: the first run described soft flags with a keyword-signal example and named one real review website, which was replaced in the saved record. The final run put the known-gap cost slightly loosely.

### 02 Customize to my background (build my central file)

Good answer: one question per turn; never suggests an answer or invents a fact; shows each YAML entry with its source label and asks for confirmation before moving on; interview facts get `proof: unchecked`; never claims to have written a file; the final file passes `validate_profile.py`.

- **Version 1** (the text the intake package shipped): FAIL on both. Neither model was told it could not run commands. Sonnet kept the interview rules well but spent most turns trying to find the scripts and paused at stage 0 with nothing written. Haiku printed pretend tool calls, claimed to have written the file itself instead of through `add_entry.py`, and skipped the first stage 0 question. The Haiku simulated user also asked the interviewer questions. Records: `earlier-versions/p2-*-v1.md`.
- **Change:** the prompt now says the model cannot run commands, must never claim to have written anything, and must show the `add_entry.py` command for the user to run. The simulated user now runs on Sonnet with stricter instructions, and the last turn asks for the whole file as it would stand after the user ran the commands.
- **Version 2** (says the model cannot run commands): the final file passed `validate_profile.py` for both models, with one expected warning (no perks yet). Sonnet PASS: one question per turn, a source label under every entry, a confirmation before every command, no claims of writing, and no invented facts. It covered stage 0 and the first employer in the 24 turns allowed. Haiku PARTIAL: it kept to one question per turn and never claimed a write, but it showed no source labels, printed "(Reading stage 0 guidance...)" for a file it did not have, and asked one two-part question in stage 1. Records: `earlier-versions/p2-*-v2.md`.
- **Change:** the prompt now asks for the source label on its own line under each entry, with the label format.
- **Version 3** (published): Sonnet PASS, Haiku PARTIAL. The final file passed `validate_profile.py` for both, with one expected warning (no perks yet). Sonnet read back every entry with a source label, asked one question per turn, never claimed a write and gave every `add_entry.py` command. Haiku added the source labels and never claimed a write, but in stage 1 it asked for title and dates without reading back an entry after each answer, offered "for example, 'Region B'", which is the scripted answer itself, inside a two-part question, and listed the allowed values for working style. Three versions were tried; Haiku stays PARTIAL. Within the 24 turns both covered stage 0 and the first employer. Stage 2, where accomplishments get `proof` labels, was not reached in any version, so the `proof: unchecked` rule was not exercised by this prompt test. The live intake run in `../intake-transcript.md` does cover it. Notes: both models skipped the stage 0 question about documents to read first. Haiku also and saved the whole `person` section in one command at the end of the stage, which the stage 0 instructions allow. An earlier attempt at this version stopped with empty replies when the account hit a usage limit; it was rerun in full.

### 03 Run on my first posting

Good answer: the JSON passes `check_findings.py` with no problems and `assess_offline.py` then gives a verdict (Apply for posting 01); every claimed qualification cites a real evidence id and none cites the `do_not_use` entry; the model does not compute scores or a verdict itself; it lists its least certain judgment calls with the posting's words.

- **Version 1** (asked for scores and a verdict as well, without the findings schema attached): FAIL on both. Both wrote `strong_positive_phrases` as plain strings, so the findings broke the schema. This run also showed that `check_findings.py` stops with a Python traceback on that shape instead of a plain message. That is noted for a follow-up; `assess_offline.py` reports it cleanly because it checks the schema first.
- **Version 2** (schema attached, scores as a labelled preview): both JSON files passed the checks and gave Apply. Sonnet PASS. Haiku PARTIAL: its preview scored Comp 8 when the pay top was above the target, which the scripts score 10. This is the lesson of the whole system in miniature, so the next version stopped asking for scores at all.
- **Version 3** (the published text: findings and judgment calls only, no scores): Sonnet PASS. Haiku's first run quoted a sentence that is not in the posting. `check_findings.py` caught it and `assess_offline.py` stopped before any score was computed (`earlier-versions/p3-haiku-v3.md`). On the second run of the same text, which allows one round of fixes after a failed check, both models passed on the first try, so no fix round was needed. Both gave Apply. Haiku's findings scored 9, 10, 9 and 10, the same as the hand-written fixture. Sonnet's scored Fit 10 instead of 9, because it rated the manual docs build fair where the fixture says weak, and it named that exact call as one it was unsure of. The verdict did not change.

### 04 Test the scoring with the fixture

Good answer: arithmetic shown for all four scores on all three postings; 12 of 12 scores and 3 of 3 verdicts match `fixtures/expected.yaml`; the comparison comes after the work.

- Sonnet and Haiku: PASS on both runs, 12 of 12 and 3 of 3 each time. Caveat: the expected file is attached in the same message, so the order "work first, then compare" cannot be enforced. Each answer's arithmetic was checked step by step against the rules, not just the totals.
- The first Sonnet run pointed out that the document did not name the `4c average` trigger label. `ARCHITECTURE.md` now lists every trigger label.

### 05 Find gaps in my central file

Good answer: finds all three planted gaps in `fixtures/gappy-profile.yaml` (the skill scored 5 on one unchecked interview answer, the hard block with no reason, the second lane copied from the first), each with its YAML path, why it matters and one question; fills no gap itself.

- **Version 1**: both found all three, but the test was not fair. The attached section of `ARCHITECTURE.md` described the three gaps. That paragraph was rewritten in general terms, and the prompt was widened to say "must-haves or hard blocks with no reason" and "skills that rest on thin evidence".
- **Version 2** (published): PASS on both. Both also raised extra, reasonable weak spots, such as `last` dates that do not match the evidence dates.

### 06 Fix errors

Good answer: covers all five problems in the broken fixture's validator output; names the missing evidence id `ev-placeholder-style-guide`; each fix is the smallest before-and-after change; where the right value is the user's call it offers choices with a placeholder instead of a guess; suggests only values the file allows.

- Sonnet: PASS on versions 1, 2 and 4. On version 3 it filled in `authorship: WROTE` with "or CO-WROTE, <your choice>" where that version asked for a placeholder, which is PARTIAL by a strict reading; the published version 4 is a PASS.
- Haiku: PARTIAL on all four versions. Each version tightened the wording: no invented values, then placeholders, then no line numbers and a pointer to the schema for allowed values. Haiku improved each time but kept suggesting `last` values such as `1y` or `6m`, which the schema does not allow, and in two versions suggested linking the skill to an unrelated evidence entry. In the final version it uses placeholders for the pay numbers and the `last` value, but still fills in `authorship: WROTE` itself and again offers an unrelated evidence id as an example. Records: `earlier-versions/p6-*-v1.md` to `-v3.md`, and `p6-*.md`.

### r1 Review the rules for gaps

Good answer: covers every item under Interpretations, each with the quoted rule and one clarifying sentence; no sentence changes a number, band, cap or rule order; no new rules are invented.

- Sonnet: PASS on every run. Its answers also found real gaps in the document, which led to three edits in `ARCHITECTURE.md`: what "net negative" autonomy means, where a named exception is decided, and a note that three phrases stay judgment calls on purpose.
- Haiku: version 1 FAIL (one sentence changed a poor rating's cost from 3 to 1.5), version 2 FAIL (one sentence changed the Comp bands). Version 3, the published text, asks the model to check each sentence against the rules tables: one run was PARTIAL (it invented a mapping from autonomy to the rating scale), and the final run was a PASS: it addressed all 14 items (it judged item 14 display-only and gave item 13 a sentence without a quoted rule, because the document has none) and kept every number.

### s1 Walk me through setup

Good answer: one step at a time in the order SETUP.md gives; waits for the output each time; when pytest fails with a missing `yaml` module, diagnoses the inactive virtual environment and fixes it; ends with the tests passing and the posting 03 summary.

- Sonnet and Haiku: PASS. Both diagnosed the inactive virtual environment correctly. At the end Haiku said the output had score bars "exactly as documented" although the simulated output it was given had none. Note on the simulated user: it invented a validator output for the broken file that does not look like the real one. Both models noticed the format was different and moved on, since a failure was expected at that step. A home-folder path and temp-folder paths typed by the simulated user were shortened in the saved records.

### r2 Customize the rubric

Good answer: one question at a time; every change shown as YAML inside `culture` only; moves the learning budget to nice and adds the new hustle phrase when asked; declines to make Culture count double, because that would change the verdict rules.

- Sonnet and Haiku: PASS on both runs. Notes: in the first run the simulated user said it would enjoy "hackathon weekends", so Sonnet sensibly put it on the free list instead of the hustle list. After the scripted user said goodbye in the first run, Haiku printed pretend tool calls when asked to apply the change; in the final run it said "Done" for changes it had only shown, not written. In the final Haiku run the simulated user also broke character after the goodbye ("There is no next message from Robin"), which does not affect the grade.

### h1 Understand the hook

Good answer: names every check the hook README lists (verdict dot in the subject, an HTML body file that exists, the job link button with a real link above the verdict, the Scores section and bars and the Checks section, no unfilled placeholders), what it lets through, the settings snippet, and exit code 2 as the blocking code.

- Sonnet and Haiku: PASS on both runs.

## How to rerun

From `pipelines/job-assessment/`, with the `claude` command line installed and signed in:

```text
python3 tests/prompt-runs/run_prompts.py                      # all ten prompts, both models
python3 tests/prompt-runs/run_prompts.py --only p3 --models haiku
```

It overwrites the records in this folder. It calls a model and costs money, so it never runs in the test suite or in CI.
