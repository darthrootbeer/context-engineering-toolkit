# Job assessment: setup

This page takes you from nothing to a working install: the tests passing, the whole chain run on a fictional posting, and, if you use Claude Code, the two skills wired in. It takes about five minutes. Nothing here needs an API key or a network connection after the install.

Every command below runs from `pipelines/job-assessment/` unless the step says otherwise.

## What you need

- **Python 3.10 or later.** Check with `python3 --version`. CI tests 3.10 and 3.12 on Ubuntu and macOS.
- **git**, to clone the repo.
- **Three Python packages**, installed in step 2: `pyyaml`, `jsonschema` and `pytest`. Nothing else.
- **Optional: Claude Code**, to run the intake and assessment as skills. Without it, every step has a plain prompt you can paste into any chat model.
- **Optional: the `requests` package**, only if you want `parse_posting.py` to fetch a posting from a link. Pasted text needs nothing extra.

## Install and check

**Step 1. Clone the repo and go to this folder.**

```text
git clone https://github.com/darthrootbeer/context-engineering-toolkit
cd context-engineering-toolkit/pipelines/job-assessment
```

**Step 2. Make a virtual environment and install the packages.**

```text
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
```

On Windows, activate with `.venv\Scripts\activate` instead.

**Step 3. Run the tests.**

```text
python3 -m pytest -q
```

Expect a line like `542 passed, 2 skipped`. The two skipped tests are the live runs, which call a model and only run when you ask for them (see [Live runs](#live-runs-optional)). The exact count grows as tests are added. What matters is that nothing fails.

**Step 4. Check the fictional person's file, and watch a broken one fail.**

```text
python3 scripts/validate_profile.py --fixture fixtures/robin-sample/career-profile.yaml
python3 scripts/validate_profile.py fixtures/broken-profile.yaml
```

The first prints `validate_profile: clean, 0 warning(s)` and exits 0. The second lists five problems, one per line, and exits 1. That is correct: the file has five planted mistakes.

**Step 5. Run the whole chain on one posting.**

```text
python3 scripts/assess_offline.py fixtures/postings/03-unlisted-pay-perks.md \
  --findings fixtures/findings/03-unlisted-pay-perks.findings.json \
  --profile fixtures/robin-sample/career-profile.yaml --out /tmp/ja-out
```

It prints ten progress lines, then a summary that starts:

```text
ASSESSMENT: fixtures/postings/03-unlisted-pay-perks.md

🚦 VERDICT: Apply with reservations
```

followed by four score bars (Fit 7, Comp 5, Qualifications 6, Culture 9) and a table of checks. In `/tmp/ja-out` you will find the archived note with the verdict emoji at the front of its name, the working files, and an email card in `email/` that you can open in a browser. Nothing is sent anywhere.

On Windows, use any folder you like in place of `/tmp/ja-out`.

## Use your own file

1. **Build your file.** Either run the intake skill in Claude Code (see the next section) or follow `intake/README.md` with the plain prompts in `intake/stage-prompts/`. Copy `intake/templates/career-profile.template.yaml` to wherever you want to keep your file first. Keep your file outside this repo, so it never ends up in a commit.
2. **Check it.** `python3 scripts/validate_profile.py PATH/career-profile.yaml`. Fix every line it prints. Warnings are worth reading too.
3. **Assess a posting.** Run the assessment skill in Claude Code, or paste the "Run on my first posting" prompt from `README.md` into a chat model with your file and the posting. Save the JSON it gives you as `findings.json`, then run:

```text
python3 scripts/assess_offline.py PATH/posting.md --findings findings.json \
  --profile PATH/career-profile.yaml --out PATH/out \
  --company "Company name" --role "Role title" --lane LANE --url https://the-job-link
```

If the findings break a rule, the run stops at the step that refused and prints why. Fix the findings, not the script.

## Wire the skills into Claude Code

The skills' commands use paths relative to this folder, so open Claude Code here and link the two skill folders into this folder's `.claude/skills/`:

```text
mkdir -p .claude/skills
ln -s ../../intake .claude/skills/career-intake
ln -s ../../assessment .claude/skills/job-assessment
```

On Windows, copy the two folders instead of linking them. Then start Claude Code in this folder:

- Say "interview me for my career profile", or run `/career-intake`, to build your file.
- Paste a posting and say "should I apply to this", or run `/job-assessment`, to assess it.

The links are not tracked by git, so `git status` will list `.claude/` as new. That is expected.

**Optional: the email card guard.** `assessment/hooks/README.md` shows how to add a hook that blocks a plain-text assessment email if you later send cards with your own mail tool.

## Live runs (optional)

`tests/live/` holds two tests that call a real model through the `claude` CLI: one runs the intake with the fictional person's scripted answers, the other runs the assessment on postings 01 and 03. They are skipped unless you set `JA_LIVE=1`, they cost money, and they never run in CI.

```text
JA_LIVE=1 python3 -m pytest tests/live -q
```

They rewrite the saved records in `tests/` (`intake-transcript.md`, `e2e-output.md`), so only run them when you mean to refresh those files. `JA_LIVE_MODEL` picks the model (default `sonnet`).

## When something fails

| What you see | Cause | Fix |
|---|---|---|
| `missing dependency (yaml)` or `(jsonschema)`, exit 2 | The packages are not installed in the Python you are running. | Activate the virtual environment from step 2, or run `pip install -r requirements.txt` again. |
| `SyntaxError` or a type error on import | Python is older than 3.10. | Install Python 3.10 or later and make the virtual environment again. |
| `assess_offline.py` stops at "parse and archive the posting" with a duplicate message | You ran the same posting into the same `--out` folder twice, and the archive refuses a duplicate on purpose. | Use a new `--out` folder, or add `--force`. |
| `assess_offline.py` stops at "check every quote and id in the findings" | A quote in the findings is not in the posting, or an id is not in the profile. The printed line names the field. | Fix that entry in the findings file. |
| `validate_profile.py` exits 1 on your own file | The file breaks one of the rules in `ARCHITECTURE.md`, "What the validator checks". | Each line names the YAML path. Use the "Fix errors" prompt below. |
| Tests fail after you edited a fixture | The fixtures are pinned to expected values and golden files. | Undo the fixture edit, or use your own files outside `fixtures/`. |

---

### Prompt for your AI model

Paste one of these into any AI model, together with this document and any files it names.

**Walk me through setup**

<!-- prompt: prompts/s1-setup-walkthrough.txt -->
```text
I'm attaching SETUP.md. Walk me through installing and testing this on my computer, one step at a time, waiting for me to paste each command's output. Stop at the first error and help me fix it. A good session ends with pytest passing and assess_offline.py printing the posting 03 summary.
```

**Fix errors**

<!-- prompt: prompts/06-fix-errors.txt -->
```text
I'm attaching the output of a failed command from this tool (the validator, the tests, check_findings.py or assess_offline.py) and the file it names. For each problem in the output, explain the cause in one or two plain sentences, name the YAML path or file the output points to (do not guess line numbers), and propose the smallest change that fixes it, shown as before and after. Change nothing else. Never invent a value I did not give you: where the right value is my call, such as a date, a number or which entry to keep, say so, offer the choices, and write the after with a placeholder such as <your value> instead of a guess. Suggest only values the file or the output shows are allowed; if the allowed values are not shown, say they are listed in schema/career-profile.schema.json instead of guessing. If the output is not enough to know the cause, name the single command I should run next. A good answer on the validator output for fixtures/broken-profile.yaml covers all five problems and names the missing evidence id that one skill points to.
```

**Tested on:** Claude Sonnet and Claude Haiku through the Claude Code command line, 2026-10-01. Sonnet passed both prompts here. Haiku passed one and partly passed "Fix errors" (it still suggests values the file does not allow). Every run, every rewrite and every grade is in `tests/prompt-runs/GRADES.md`.
