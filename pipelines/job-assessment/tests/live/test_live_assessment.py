"""Live run 2: the assessment skill on fixture postings 01 and 03.

A model follows assessment/SKILL.md and writes findings.json itself. The test then does
not trust the model's own numbers: it runs check_findings.py on the findings, recomputes the
scores and verdict with the scripts, and compares the verdict to fixtures/expected.yaml.
The answer key (fixtures/findings, expected.yaml, golden) is not in the model's folder.

The record is saved to tests/e2e-output.md.
"""
import json
import shutil
import subprocess
import sys
from datetime import date

import pytest
import yaml

from driver import (MODEL, ROOT, TESTS, assert_ran, make_scrub, make_workdir, render_record, run_claude)

FIX = ROOT / "fixtures"
EXPECTED = yaml.safe_load((FIX / "expected.yaml").read_text(encoding="utf-8"))["postings"]
SCRIPTS = ROOT / "assessment" / "scripts"
sys.path.insert(0, str(SCRIPTS))
import verdict as verdict_mod  # noqa: E402

PROMPT = """Follow assessment/SKILL.md from this folder to assess ONE posting. Nobody is here to answer
questions, and the skill says never to ask, so finish every step.

- Profile: ./career-profile.yaml
- Posting text: ./posting.md (the text is already here, nothing needs fetching). Its first lines give the
  company, role, lane, url and source.
- Folders: ARCHIVE=./archive, WORK=./work, OUT=./out. Create them. Assessment date: 2026-10-01.
- Write your findings to ./work/findings.json.
- Run every command in the skill in order, including the email card. Use `python3` for every script.
- Do not look for answer files outside what is in this folder. Read the posting and judge it yourself.
- End by printing the terminal summary.

Everything here is fictional."""

CASES = [("01-strong-fit", "Apply"), ("03-unlisted-pay-perks", "Apply with reservations")]


def run_one(pid, tmp_path):
    work = make_workdir(tmp_path)
    shutil.copy(FIX / "robin-sample" / "career-profile.yaml", work / "career-profile.yaml")
    shutil.copy(FIX / "postings" / f"{pid}.md", work / "posting.md")
    proc, events, final = run_claude(PROMPT, work, tmp_path / "bin")
    scrub = make_scrub(work)
    calls = assert_ran(proc, events, final)

    notes = []
    ok = True

    def check(label, passed, detail=""):
        nonlocal ok
        ok = ok and passed
        notes.append(f"- {label}: {'pass' if passed else 'FAIL'}{(' (' + detail + ')') if detail else ''}")

    findings = work / "work" / "findings.json"
    check("findings.json written", findings.is_file())
    archive_notes = sorted((work / "archive").glob("*.md"))
    check("exactly one archived note", len(archive_notes) == 1, str([scrub(n.name) for n in archive_notes]))
    cards = sorted((work / "out").glob("*.html"))
    check("email card written", len(cards) == 1)
    if findings.is_file() and archive_notes:
        note = archive_notes[0]
        profile = work / "career-profile.yaml"
        c = subprocess.run([sys.executable, str(SCRIPTS / "check_findings.py"), str(findings), "--posting", str(note),
                            "--profile", str(profile)], capture_output=True, text=True)
        check("check_findings.py passes on the model's findings", c.returncode == 0, scrub((c.stdout + c.stderr).strip())[:300])
        s = subprocess.run([sys.executable, str(SCRIPTS / "score_helpers.py"), str(findings), "--profile", str(profile), "--json"],
                           capture_output=True, text=True)
        if s.returncode == 0:
            scores = json.loads(s.stdout)
            data = json.loads(findings.read_text(encoding="utf-8"))
            decision = verdict_mod.decide(scores["fit"], scores["qualifications"], scores["comp"], scores["culture"],
                                          override=verdict_mod.override_skill(data), hard_block=verdict_mod.hard_block_id(data))
            want = EXPECTED[pid]
            got = {k: scores[k] for k in ("fit", "comp", "qualifications", "culture")}
            check("verdict matches expected.yaml", decision["label"] == want["verdict"],
                  f"got {decision['label']} ({decision['trigger']}), expected {want['verdict']}")
            same = got == {k: want[k] for k in got}
            notes.append(f"- Scores from the model's findings: {got}. Expected: {{'fit': {want['fit']}, 'comp': {want['comp']}, "
                         f"'qualifications': {want['qualifications']}, 'culture': {want['culture']}}}. "
                         f"{'Identical.' if same else 'They differ: the model read the posting a little differently. The test requires the verdict, not identical scores.'}")
            check("note name starts with the verdict dot", note.name[0] == {"Apply": "\U0001F7E2",
                  "Apply with reservations": "\U0001F7E1", "Skip": "\U0001F534"}[decision["label"]], scrub(note.name))
        else:
            check("score_helpers.py ran on the model's findings", False, scrub(s.stdout + s.stderr)[:300])
    section = [f"## Posting {pid}", "", f"Commands run by the model: {calls}. Turns: {final.get('num_turns')}. "
               f"Cost: ${float(final.get('total_cost_usd') or 0):.2f}.", "", "### Checks", "", *notes, "",
               f"Result: {'PASS' if ok else 'FAIL'}", "", "### Transcript", "", render_record(events, scrub, clip=500), ""]
    return ok, "\n".join(section)


def test_assessment_skill_gives_the_expected_verdicts(tmp_path_factory):
    parts, results = [], []
    for pid, _ in CASES:
        ok, text = run_one(pid, tmp_path_factory.mktemp(pid))
        results.append(ok)
        parts.append(text)
        head = ["<!-- FICTIONAL EXAMPLE DATA. Not a real person. Saved by tests/live/test_live_assessment.py -->",
                "# Live run: assessment on the fictional postings", "",
                f"Date: {date.today().isoformat()}. Model: `{MODEL}`. A model followed `assessment/SKILL.md` and wrote its own "
                "findings. The test recomputes scores and the verdict with the scripts and does not trust the model's numbers. "
                "Tool output is cut to 500 characters. Folder names are replaced with `<work>` and `<tmp>`.", ""]
        (TESTS / "e2e-output.md").write_text("\n".join(head + parts), encoding="utf-8")
    assert all(results), "see tests/e2e-output.md"
