# Assessment: judge one job posting

This folder is the second half of the job assessment system. It takes one job posting and the person's own `career-profile.yaml` and gives a plain verdict: **Apply**, **Apply with reservations**, or **Skip**. The first half, `intake/`, builds the profile.

The docs in this folder follow the style guides and prompt-block standard of [`pipelines/docs-pipeline`](../../docs-pipeline/).

## What it is

- `SKILL.md` is a Claude Code skill. It walks the model through one posting: archive it, load the one lane's checklist, read the posting, write a findings file, then call the scripts for everything that counts or decides.
- `scripts/` holds the scripts the skill calls. Each one is a plain command-line tool with tests in `../tests/`.
- `templates/assessment-email.html` is the summary card. Its first element is a **View the job posting** button that opens the live job page.
- `hooks/` holds an optional Claude Code hook that blocks a plain-text assessment email.

The flow for one posting:

| Step | Who | What happens |
|---|---|---|
| Archive | `parse_posting.py` | Saves the posting as a note, splits likely-real lines from likely-filter lines, and refuses a duplicate (same company, role and lane). |
| Checklist | `load_criteria.py` | Prints the one lane's rules. Refuses an unknown lane or a lane that disagrees with the note. |
| Read | the model | Reads the posting and writes `findings.json`. Every rating quotes the posting. Every claimed qualification cites an evidence id. |
| Check | `check_findings.py` | Rejects a quote that is not in the posting, an evidence id that does not exist or cannot be used, and a "bad autonomy" read that rests only on generic phrases. |
| Score | `score_helpers.py` | Computes Fit, Comp, Qualifications and Culture, 0 to 10 each. |
| Decide | `verdict.py` | Applies the verdict rules in a fixed order. It takes no company input. |
| Write | `render_assessment.py`, `write_assessment.py`, `rename_verdict.py` | Writes the assessment into the note, sets its state, and puts the verdict emoji at the front of the file name. |
| Show | `render_assessment.py --terminal`, `render_email.py` | Prints the summary table and writes the email card to a local HTML file. Nothing is sent. |

## What problem it solved

A model asked "should I apply to this?" gives a confident answer that changes from run to run. Two habits cause most of that drift. It invents a reading when the posting says nothing, and it does the arithmetic and the verdict in its head, a little differently each time.

This design splits the work. The model does only the reading, which is the part that needs judgment. Code checks that what the model claims is really in the posting and the person's own evidence, then does the arithmetic and applies the verdict rules the same way every time. A score or verdict the scripts did not produce does not count.

## How it was built

Built by directing Claude Code. The author designed the rules, reviewed the output and checked it with the tests in `../tests/`. It was not hand-typed.

The skill was written fresh from a written list of behaviors taken from the author's private version of this tool, then stripped of everything personal. The scoring, the verdict rules and the card were rebuilt as scripts, so the rules can be tested from a clean copy of this repo. The full rules, and the places where a rule needed an interpretation, are in `../ARCHITECTURE.md`.

## How it was verified

- Every script the skill calls has tests in `../tests/`, run in CI on Ubuntu and macOS with Python 3.10 and 3.12. Run them with `python3 -m pytest -q` from `pipelines/job-assessment/`.
- The commands in `SKILL.md` were run in order, by hand, on an invented posting and an invented profile: archive, a second archive refused as a duplicate (exit 4), checklist, skill match, findings check, scores, verdict, note write, rename and email card. The findings example in `SKILL.md` passes `check_findings.py` and validates against `../schema/findings.schema.json`.
- The step 5 and step 6 commands from `SKILL.md`, run on the three hand-written findings files in `../fixtures/findings/`, pass the check and give all twelve scores and all three verdicts listed in `../fixtures/expected.yaml`.
- A model ran the whole skill on fictional postings 01 and 03 with the `claude` CLI on Claude Sonnet, and the scripts recomputed the verdict from the model's own findings. The first attempt got posting 03 wrong (it read one duty as optional and gave Apply instead of Apply with reservations). The second attempt, with no changes, gave both expected verdicts. Both records are in `../tests/e2e-output-run1.md` and `../tests/e2e-output.md`.

## Requirements

- Python 3.10 or later, with `pip install -r requirements.txt` run from `pipelines/job-assessment/`.
- A `career-profile.yaml` that passes `python3 scripts/validate_profile.py`.
- Claude Code to run `SKILL.md` as a skill. Without it, use the "Run on my first posting" prompt below in any chat model, then run the scripts yourself.
- The `requests` package only if you want `parse_posting.py` to fetch a posting from a link. Pasted text needs nothing extra.

---

### Prompt for your AI model

Paste this into any AI model, together with this document and the files it describes.

**Run on my first posting**

<!-- prompt: prompts/03-run-first-posting.txt -->
```text
I'm attaching assessment/SKILL.md, schema/findings.schema.json, my career-profile.yaml and one job posting. Assess the posting for the lane named in its lane field, following SKILL.md. Check hard blocks first and stop if one trips. Quote the posting's own words for every rating; if the posting says nothing on a point, rate it Unknown. Only claim a qualification when my file has an evidence entry for it, and name that entry's id. Give the findings as one JSON block that matches schema/findings.schema.json exactly, including the shape of every list item, so I can run assessment/scripts/check_findings.py and scripts/assess_offline.py on it. Do not work out scores or a verdict yourself: the scripts do that, the same way every time. After the JSON, list the two or three judgment calls you were least sure of, each with the posting's words and the other way it could be read. A good answer's JSON passes check_findings.py with no problems, and assess_offline.py then gives the verdict.
```

**Test the scoring with the fixture**

<!-- prompt: prompts/04-test-scoring.txt -->
```text
I'm attaching ARCHITECTURE.md, fixtures/robin-sample/career-profile.yaml, the three postings in fixtures/postings/ and their files in fixtures/findings/. For each posting, apply the scoring rules by hand to its findings file. Show the arithmetic for Fit, Comp, Qualifications and Culture, round each the way ARCHITECTURE.md says, then apply the verdict rules in order and name the rule that decided it. Only after all three answers are written, open fixtures/expected.yaml, compare, and list every mismatch with the step where your arithmetic and the file disagree. A good answer matches all three verdicts and all twelve scores.
```

**Fix errors**

<!-- prompt: prompts/06-fix-errors.txt -->
```text
I'm attaching the output of a failed command from this tool (the validator, the tests, check_findings.py or assess_offline.py) and the file it names. For each problem in the output, explain the cause in one or two plain sentences, name the YAML path or file the output points to (do not guess line numbers), and propose the smallest change that fixes it, shown as before and after. Change nothing else. Never invent a value I did not give you: where the right value is my call, such as a date, a number or which entry to keep, say so, offer the choices, and write the after with a placeholder such as <your value> instead of a guess. Suggest only values the file or the output shows are allowed; if the allowed values are not shown, say they are listed in schema/career-profile.schema.json instead of guessing. If the output is not enough to know the cause, name the single command I should run next. A good answer on the validator output for fixtures/broken-profile.yaml covers all five problems and names the missing evidence id that one skill points to.
```

**Customize the rubric**

<!-- prompt: prompts/r2-customize-rubric.txt -->
```text
I'm attaching assessment/README.md, ARCHITECTURE.md and my career-profile.yaml. Help me change which perks count as big or nice and which phrases count as hustle, one question at a time, and show the YAML change for each. Do not change the verdict rules.
```

**Tested on:** Claude Sonnet and Claude Haiku, 2026-10-01. Results for every prompt are in `../tests/prompt-runs/GRADES.md`.
