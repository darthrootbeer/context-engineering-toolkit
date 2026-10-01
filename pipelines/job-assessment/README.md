# Job assessment system

**Status: the chain runs offline on fictional data; the architecture, setup and tested-prompt docs are still to come.** Everything listed as done below exists in this folder and is covered by tests. The last two bullets are the only work left.

The system is meant to score a job posting against a person's own written criteria and give a plain verdict: Apply, Apply with reservations, or Skip. Its docs will follow the style guides and prompt-block standard of [`pipelines/docs-pipeline`](../docs-pipeline/), which stays the first thing to look at in this repo.

Built by directing Claude Code. The author designed the rules, reviews the output, and verifies it with tests. It is not hand-typed. No production ML or RAG experience is claimed. All sample data will be fictional and labelled as such.

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

- [ ] **Docs and prompt blocks.** `ARCHITECTURE.md`, `SETUP.md`, and the tested prompts for each doc.

## What can be run today

From this folder, after `pip install -r requirements.txt`:

```text
python3 -m pytest -q
python3 scripts/assess_offline.py fixtures/postings/03-unlisted-pay-perks.md \
  --findings fixtures/findings/03-unlisted-pay-perks.findings.json \
  --profile fixtures/robin-sample/career-profile.yaml --out /tmp/ja-out
python3 ../../.github/scripts/safety_scan.py --tree
```

The second command runs the whole chain with no model and no network: it checks the findings, scores them, picks the verdict, writes the assessment into an archived note, renames the note and writes the email card as a local HTML file. The tests in `tests/test_e2e_offline.py` compare that output for all three fictional postings to `fixtures/expected.yaml` and `fixtures/golden/`.

The live runs in `tests/live/` need the `claude` CLI and `JA_LIVE=1`, are skipped otherwise, and never run in CI. Their saved records are `tests/intake-transcript.md`, `tests/e2e-output.md` and the first attempt, `tests/e2e-output-run1.md`.
