"""Live run 1: the intake skill, answered from Robin's scripted answers.

A model plays the interviewer by following intake/SKILL.md. There is no human, so the
scripted answers stand in for one. The produced file must pass the validator and match
Robin's structure: same employer ids, same lanes, evidence count within 2.
Skill ids in the answers are Robin's own words, not catalog ids, so none are expected.

The record is saved to tests/intake-transcript.md.
"""
import shutil
import subprocess
import sys
from datetime import date
from pathlib import Path

import yaml

from driver import (MODEL, ROOT, TESTS, assert_ran, make_scrub, make_workdir, render_record, run_claude)

FIX = ROOT / "fixtures"

PROMPT = """You are running the career-intake skill from this folder. Read intake/SKILL.md and the stage files
it points to, then follow them exactly.

This is a scripted test, so there is no human. The user's answers are in ./intake-answers.txt, one per
question, keyed like s2.q3 (stage 2, question 3). When the skill says to ask a question, print it on a line
starting with ASK:, then take the next matching answer from the file and print it on a line starting with
USER:. Keys repeat when a stage loops (two employers, several accomplishments), so take repeated keys in file
order. Stage 3 answers are keyed by skill id and use option B, in chat. Stages 4 and 5 use their own key
names, so match them by topic. Never invent an answer the file does not hold: print "USER: (no scripted
answer)" and treat it as an I-don't-know. After each answer do exactly what the skill says: read it back,
write it only through scripts/add_entry.py, and save after each stage.

Save the profile as ./career-profile.yaml. Use `python3` for every script. When every stage is done, run
`python3 scripts/validate_profile.py career-profile.yaml` and print its output. Everything is fictional."""


def test_intake_builds_a_valid_profile_from_scripted_answers(tmp_path):
    work = make_workdir(tmp_path)
    shutil.copy(FIX / "robin-sample" / "intake-answers.txt", work / "intake-answers.txt")
    proc, events, final = run_claude(PROMPT, work, tmp_path / "bin")
    scrub = make_scrub(work)
    tool_calls = assert_ran(proc, events, final)

    profile_path = work / "career-profile.yaml"
    record = [
        "<!-- FICTIONAL EXAMPLE DATA. Not a real person. Saved by tests/live/test_live_intake.py -->",
        "# Live run: intake transcript", "",
        f"Date: {date.today().isoformat()}. Model: `{MODEL}`. Commands run by the model: {tool_calls}. "
        f"Turns: {final.get('num_turns')}. Cost: ${float(final.get('total_cost_usd') or 0):.2f}.", "",
        "A model followed `intake/SKILL.md` and answered from `fixtures/robin-sample/intake-answers.txt`. "
        "Tool output is cut to the first 700 characters. Folder names are replaced with `<work>` and `<tmp>`.", "",
        "## Transcript", "", render_record(events, scrub), "",
    ]

    checks = ["## Checks", ""]
    ok = True
    if not profile_path.is_file():
        checks.append("- FAIL: no career-profile.yaml was produced.")
        ok = False
    else:
        v = subprocess.run([sys.executable, str(ROOT / "scripts" / "validate_profile.py"), str(profile_path)],
                           capture_output=True, text=True, cwd=work)
        checks.append(f"- Validator exit code: {v.returncode} ({'pass' if v.returncode == 0 else 'FAIL'})")
        checks.append("```text\n" + scrub((v.stdout + v.stderr).strip())[:1500] + "\n```")
        ok = ok and v.returncode == 0
        got = yaml.safe_load(profile_path.read_text(encoding="utf-8")) or {}
        want = yaml.safe_load((FIX / "robin-sample" / "career-profile.yaml").read_text(encoding="utf-8"))
        got_emp = sorted(e["id"] for e in got.get("employers", []))
        want_emp = sorted(e["id"] for e in want["employers"])
        got_lanes = sorted(l["name"] for l in got.get("lanes", []))
        want_lanes = sorted(l["name"] for l in want["lanes"])
        ev_got, ev_want = len(got.get("evidence", [])), len(want["evidence"])
        rows = [("employer ids", got_emp == want_emp, f"{got_emp} vs {want_emp}"),
                ("lane names", got_lanes == want_lanes, f"{got_lanes} vs {want_lanes}"),
                ("evidence count within 2", abs(ev_got - ev_want) <= 2, f"{ev_got} vs {ev_want}"),
                ("skills count", len(got.get("skills", [])) == len(want["skills"]),
                 f"{len(got.get('skills', []))} vs {len(want['skills'])}")]
        for name, passed, detail in rows:
            checks.append(f"- {name}: {'pass' if passed else 'FAIL'} ({detail})")
        ok = ok and all(p for n, p, _ in rows if n != "skills count")
        if got.get("person"):
            checks.append(f"- person: {got['person'].get('display_name')}, {got['person'].get('years_experience')} years")
        checks.append("- Skill ids are Robin's own words, not catalog ids: "
                      + ", ".join(sorted(s["id"] for s in got.get("skills", []))[:8]) + ", ...")
    record += checks + ["", f"Result: {'PASS' if ok else 'FAIL'}", ""]
    (TESTS / "intake-transcript.md").write_text("\n".join(record), encoding="utf-8")
    assert ok, "see tests/intake-transcript.md"
