# Job assessment system

**Status: scaffold only. Nothing in this folder is runnable yet.** This folder holds the repo checks and test setup that the rest of the system will be built on. The scripts, schemas, sample data and skills listed below do not exist yet, and each one will be added in its own pull request.

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

- [ ] **Assessment skill.** The Claude Code skill that runs the assessment end to end.

- [ ] **Intake skill.** The interview skill that builds the central file one checked answer at a time.

- [ ] **Skills catalog and survey.** A generic skills list and an offline form for scoring yourself against it.

- [ ] **Integration and proof.** The whole chain run end to end from a clean clone, plus the removal of the earlier `tools/job-fit-screen`.

- [ ] **Docs and prompt blocks.** `ARCHITECTURE.md`, `SETUP.md`, and the tested prompts for each doc.

## What can be run today

Only the repo checks:

```text
python3 .github/scripts/safety_scan.py --tree
```

It prints `safety_scan: clean (tree)` and exits 0 when no email address, home path, private network address, tracker link, ticket id or secret-shaped string is in a tracked file.
