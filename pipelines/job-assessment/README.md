# Job assessment system

**What it is.** A small system that reads a job posting against your own written criteria and gives a plain verdict: **Apply**, **Apply with reservations**, or **Skip**. A model reads the posting and writes down what it found, quoting the posting for every claim. Ordinary scripts then check those quotes, do the scoring and apply the verdict rules, so the same findings always give the same answer.

It is the second example in this repo. The first, and the one to read first, is the documentation pipeline in [`../docs-pipeline/`](../docs-pipeline/). These docs follow that pipeline's style guides and its rule that every README and guide ends with a tested prompt. The skill files and stage files do not carry one.

**What you get.**

- **An intake interview** (`intake/`) that builds your `career-profile.yaml` one confirmed answer at a time: job history, accomplishments with a source for each, a 0 to 5 skills self-score, what you need from a job, and the kinds of role you want.
- **A checker** (`scripts/validate_profile.py`) that refuses a profile that contradicts itself, claims checked proof for an unchecked answer, or holds contact details.
- **An assessment skill** (`assessment/`) that turns one posting into four scores (Fit, Comp, Qualifications, Culture), a verdict, a note with the assessment written into it, a summary table, and an HTML summary card saved to a local file.
- **A fictional person and three fictional postings** (`fixtures/`), with the expected results written down, so you can see the whole thing work before you give it anything of yours.
- **Ten tested prompts** (`prompts/`) for using all of this in any chat model, without Claude Code.

## Quickstart: five minutes, from a clean clone

You need Python 3.10 or later and git. No API key, no model, no network after the install.

```text
git clone https://github.com/darthrootbeer/context-engineering-toolkit
cd context-engineering-toolkit/pipelines/job-assessment
python3 -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt
python3 -m pytest -q
python3 scripts/validate_profile.py --fixture fixtures/robin-sample/career-profile.yaml
python3 scripts/assess_offline.py fixtures/postings/03-unlisted-pay-perks.md \
  --findings fixtures/findings/03-unlisted-pay-perks.findings.json \
  --profile fixtures/robin-sample/career-profile.yaml --out /tmp/ja-out
```

The tests pass. The validator prints `clean`. The last command runs the whole chain on fictional posting 03 and prints its verdict, **Apply with reservations**, with four score bars and a table of what it checked. Open the HTML card it wrote under `/tmp/ja-out/email/` in a browser to see the summary card.

[`SETUP.md`](SETUP.md) has each step with what to expect, a fix for each common failure, and how to wire the skills into Claude Code.

## The lesson this repo exists to teach

**The model writes structured findings. Scripts check, score and decide.**

Ask a model "should I apply to this job?" and you get a confident answer that shifts from run to run. It fills silences with guesses, and it does the arithmetic and the verdict in its head, slightly differently each time. So this system never lets the model decide. The model's only output that counts is a findings file: one rating per criterion, each tied to words quoted from the posting, and each claimed qualification tied to an entry in your own evidence. Then code takes over:

1. `check_findings.py` refuses a quote that is not in the posting, an evidence entry that does not exist or is not yours, and a "you'd have no say" reading that rests only on generic phrases like "work closely with".
2. `score_helpers.py` does the arithmetic.
3. `verdict.py` applies the verdict rules in a fixed order. It has no input for the company's name, so a famous employer cannot talk its way past the rules.

**Why this matters, shown on a real run.** The live run with Claude Sonnet misjudged one of the fake postings on its first attempt. Posting 03 says "You can document our mobile SDK for iOS and Android", and Robin has no mobile SDK experience. The expected answer counts that as a skill gap. The model read "can" as optional and did not count it, so Qualifications came out 7 instead of 6, and the verdict came out Apply instead of Apply with reservations. That is a reading two careful people could disagree on. Every quote it gave was real, so the checks passed. A second attempt with no changes gave the expected answer. Both records are kept: [`tests/e2e-output-run1.md`](tests/e2e-output-run1.md) (the miss) and [`tests/e2e-output.md`](tests/e2e-output.md) (the pass).

The scripts did not catch that misreading, and no script can tell a real quote read too kindly from one read correctly. What the split buys is this: the disagreement sat in one visible field of one file, where a person can see it and fix it, and every number after it followed the written rules. Without the split, the same miss would be buried inside a paragraph of confident prose.

The checks do catch the mechanical misses. While the prompts below were being tested, one Claude Haiku run quoted a sentence that is not in the posting, and `check_findings.py` stopped the run before any score was computed ([`tests/prompt-runs/earlier-versions/p3-haiku-v3.md`](tests/prompt-runs/earlier-versions/p3-haiku-v3.md)).

[`ARCHITECTURE.md`](ARCHITECTURE.md) has every scoring and verdict rule in full, a worked example, and the places where a rule needed an interpretation.

## How it was built

Built by directing Claude Code. The author designed the rules, reviewed the output, and verified it with the tests shown here. It was not hand-typed.

It is a public rebuild of a private tool the author has had in daily use since late August 2026. The earliest public trace is this repo's first job-screening commit, dated 2026-08-25 (`git log --reverse --format='%ad %s' --date=short | grep job-fit-screen`). That earlier tool has since been removed; git history keeps it. Everything personal was left out: no real postings, no real person's data, no real employers. The rules were rewritten from a written list of the private tool's behaviors, and the scoring and verdict were rebuilt as scripts so they can be tested from a clean clone.

**Timeline, so the dates make sense.** The public version was assembled and reviewed on 2026-10-01, from a private system in daily use since late August. The pull requests that built it (listed in `git log`) were built by Claude Code agents under the author's direction. They merged between 16:38 and 22:02 that day, several a minute apart, because they were prepared in parallel and merged after CI passed on each. The author's check on that work is the tests and saved run records in this folder. No claim is made here about how much of each diff a person read line by line.

No production machine-learning or retrieval (RAG) work is claimed. This is prompts, a schema, and ordinary scripts with tests.

## What it proves, and what it does not

**It shows:**

- The rules are written down and applied by code the same way every time. The tests pin every scoring rule, every verdict rule and its order, and the full output for three fictional postings, byte for byte.
- The intake produces a file the validator accepts. A live run of the intake skill on the fictional person's scripted answers is saved in [`tests/intake-transcript.md`](tests/intake-transcript.md).
- What the model claims is checked against the posting text and the person's own evidence before any score is computed.

**It does not show:**

- That a verdict predicts getting hired, or that it beats any other way of choosing jobs.
- That the model's reading of tone or emphasis is right. The run above shows it can vary.
- That it works on models other than the two it was tested on: Claude Sonnet and Claude Haiku.
- Anything about real postings or a real person. Only fictional data is included.

## Verified

Run on 2026-10-01 from a fresh `git clone` of this repo at commit `17a49ce`, in a new virtual environment with Python 3.11, on macOS:

```text
$ python3 -m pytest -q -p no:cacheprovider
SKIPPED [1] tests/live/test_live_assessment.py:97: live tests are off: set JA_LIVE=1 to run them (they call a model and cost money)
SKIPPED [1] tests/live/test_live_intake.py:38: live tests are off: set JA_LIVE=1 to run them (they call a model and cost money)
461 passed, 2 skipped in 24.85s
$ python3 scripts/validate_profile.py --fixture fixtures/robin-sample/career-profile.yaml
validate_profile: clean, 0 warning(s) in career-profile.yaml
$ python3 scripts/validate_profile.py fixtures/broken-profile.yaml; echo "exit=$?"
exit=1
$ python3 scripts/assess_offline.py fixtures/postings/03-unlisted-pay-perks.md ... | head -3
ASSESSMENT: fixtures/postings/03-unlisted-pay-perks.md

🚦 VERDICT: Apply with reservations
```

Clone, install and all of the above took 31 seconds, and left the clone with no changed files. CI repeats the same steps in a fresh clone on every pull request (the `clean-clone` job) and runs the tests on Ubuntu and macOS with Python 3.10 and 3.12. The test count grows over time; the [CI runs](https://github.com/darthrootbeer/context-engineering-toolkit/actions) show the current one.

The ten prompts in `prompts/` were each run on Claude Sonnet and Claude Haiku, once per prompt per model, and graded by a Claude model (Claude Opus for the first round, Claude Sonnet 5.5 for the re-runs of prompts 03, 04, 05 and 06) against a written good-answer list that was written before each run. No claim is made that a person re-graded the answers, and one run is not a pass rate. Sonnet passed all ten. Haiku passed seven and partly passed three: "Fix errors", where it still suggests values the file does not allow, "Customize to my background", where it sometimes skipped reading an entry back and once offered an example that was the answer itself, and "Find gaps", where it missed some planted gaps. Prompt 05 was tested on a second, held-out profile whose gaps the prompt does not name: Sonnet found 6 of 6 and Haiku 5 of 6. Five prompts were rewritten after a failed or partial run (prompt 05 twice), and every earlier run is kept in [`tests/prompt-runs/earlier-versions/`](tests/prompt-runs/earlier-versions/), with the grades in [`tests/prompt-runs/GRADES.md`](tests/prompt-runs/GRADES.md).

## Where things are

| Path | What it is |
|---|---|
| [`ARCHITECTURE.md`](ARCHITECTURE.md) | How the parts fit, every rule, the interpretations |
| [`SETUP.md`](SETUP.md) | Install, check, wire into Claude Code, troubleshooting |
| [`intake/`](intake/README.md) | The interview that builds your central file |
| [`assessment/`](assessment/README.md) | The skill and scripts that judge one posting |
| [`fixtures/`](fixtures/README.md) | Robin Sample, three postings, expected results |
| `schema/` | The contracts for the central file and the findings file |
| `scripts/` | The validator, the checked write door, and the offline runner |
| `prompts/` | The tested prompts, one file each. The blocks in these docs are copied from them, and a test keeps them identical. |
| `tests/` | The offline suite, the live runs, and the prompt test records in `tests/prompt-runs/` |

## Status

Each bullet flips from planned to done in the pull request that delivers it.

- [x] **Scaffold and safety.** CI workflow, the safety scan that blocks personal data from the repo, the pull request template, this README, `requirements.txt`, `pytest.ini` and an empty `tests/conftest.py`.

- [x] **Central file schema and validator.** The file format that holds a person's job history, evidence and skills, and the checker that rejects a bad one.

- [x] **Fictional sample data.** An invented person and three invented postings, with the expected results written down.

- [x] **Scoring core.** The four scores (Fit, Comp, Qualifications, Culture), the verdict rules, and the checks that every claim quotes the posting.

- [x] **Posting pipeline.** Parsing a posting, archiving it, matching skills, and writing the result back into the saved note.

- [x] **Email card and guard.** A formatted summary card written to a local HTML file, and an optional hook that blocks a plain-text version.

- [x] **Assessment skill.** The Claude Code skill that runs the assessment end to end.

- [x] **Intake skill.** The interview skill that builds the central file one checked answer at a time.

- [x] **Skills catalog and survey.** A generic skills list and an offline form for scoring yourself against it.

- [x] **Integration and proof.** The whole chain run end to end offline, a separate live run with the `claude` CLI, a clean-clone check in CI, and the removal of the earlier `tools/job-fit-screen` (git history keeps it).

- [x] **Docs and prompt blocks.** `ARCHITECTURE.md`, `SETUP.md`, and the tested prompts for each doc.

---

### Prompt for your AI model

Paste one of these into any AI model, together with the files it names. Each one says what a good answer looks like, so you can tell whether it worked.

**Understand and teach**

<!-- prompt: prompts/01-understand-and-teach.txt -->
```text
I'm attaching README.md, ARCHITECTURE.md and fixtures/robin-sample/career-profile.yaml from a job assessment tool. Teach me how it works as if I have never seen it. Cover, in this order: what the career-profile file holds and why every claim in it needs a source; how one job posting becomes four scores called Fit, Comp, Qualifications and Culture; the exact order the verdict rules are checked in; and what the tool refuses to do. Use plain words and short sentences. Then ask me three quiz questions, one at a time, and wait for my answer before asking the next. A good answer gives the rule order as hard block, job-type override, Fit and Qualifications floor, reservations band, then Apply, and says unlisted pay scores a neutral 5.
```

**Customize it to my background and requirements**

<!-- prompt: prompts/02-customize.txt -->
```text
I'm attaching intake/SKILL.md and intake/templates/career-profile.template.yaml. Interview me to build my own career-profile.yaml. Ask exactly one question at a time and wait for my answer. If a question has two parts, ask them separately. Never suggest an answer and never invent a fact, date, number or skill. After each answer, show the exact YAML entry you would add, put its source label on its own line under it (for example interview:<today's date>:s<stage>.q<question>), and ask me to confirm it. Anything I cannot point to a document, link or artifact for gets proof: unchecked. You cannot run commands or open files here, so never claim to have written anything: once I confirm an entry, show the scripts/add_entry.py command for me to run, then ask the next question. Start with stage 0, orientation. A good session ends with a file that passes scripts/validate_profile.py.
```

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

**Find gaps in my central file**

<!-- prompt: prompts/05-find-gaps.txt -->
```text
I'm attaching the 'What the validator checks' section of ARCHITECTURE.md and my career-profile.yaml. The validator checks shape and consistency, not truth, so find what it cannot catch. Read my whole file the way a skeptical hiring manager and a careful editor would: look for places where the file claims more than its own evidence shows, says something that conflicts with another part of the file, or would make a posting score in a misleading way. Check every section, not only skills. For each weak spot, give the exact YAML path, quote the part that worries you, say why it matters for scoring, and give one question you would ask me to fix it. Do not fill any gap yourself, and do not report a problem you cannot point to in the file. A good answer names only things that are really in the file and gives a YAML path for each one.
```

**Fix errors**

<!-- prompt: prompts/06-fix-errors.txt -->
```text
I'm attaching the output of a failed command from this tool (the validator, the tests, check_findings.py or assess_offline.py) and the file it names. For each problem in the output, explain the cause in one or two plain sentences, name the YAML path or file the output points to (do not guess line numbers), and propose the smallest change that fixes it, shown as before and after. Change nothing else. Never invent a value I did not give you: where the right value is my call, such as a date, a number or which entry to keep, say so, offer the choices, and write the after with a placeholder such as <your value> instead of a guess. Suggest only values the file or the output shows are allowed; if the allowed values are not shown, say they are listed in schema/career-profile.schema.json instead of guessing. If the output is not enough to know the cause, name the single command I should run next. A good answer on the validator output for fixtures/broken-profile.yaml covers all five problems and names the missing evidence id that one skill points to.
```

**Tested on:** Claude Sonnet and Claude Haiku through the Claude Code command line, 2026-10-01. Sonnet passed all 6 prompts here. Haiku passed 3 and partly passed three: "Customize" (it skipped some read-backs and offered an example that was the answer), "Find gaps" (it missed a planted gap on each of two profiles) and "Fix errors" (it still suggests values the file does not allow). One run per prompt per model, graded by a Claude model, not a person. Every run, every rewrite and every grade is in `tests/prompt-runs/GRADES.md`.
