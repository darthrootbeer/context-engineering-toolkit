#!/usr/bin/env python3
"""Run the whole assessment chain on one posting with no model and no network.

    assess_offline.py POSTING --findings F.json --profile P.yaml --out DIR
                      [--date YYYY-MM-DD] [--company C] [--role R] [--lane L]
                      [--url U] [--source KEY] [--force]

The findings file stands in for the model's reading of the posting. Everything
after that is the same code the assessment skill calls, in the same order:

    validate profile -> check findings against the schema -> archive the posting
    -> load the lane -> check quotes -> score -> verdict -> render the block
    -> write it into the note -> rename the note -> terminal summary -> email card

The terminal summary goes to stdout. Progress lines and file paths go to stderr.
Files written under DIR: archive/<renamed note>.md, work/*.json, work/block.md,
work/terminal.txt, email/<slug>.html.

A fixture posting may start with a few `key: value` lines (company, role, lane,
url, source) before a `---` line. Those fill in any option you leave out.

Exit codes: 0 done, 1 a step refused (the step and its message are printed),
2 an input could not be read.
"""
import argparse
import json
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
SCRIPTS = ROOT / "assessment" / "scripts"
sys.path.insert(0, str(SCRIPTS))
import verdict as verdict_mod  # noqa: E402

PY = sys.executable
WORD = {"Apply": "apply", "Apply with reservations": "reservations", "Skip": "skip"}


class StepFailed(Exception):
    def __init__(self, step, message, code=1):
        super().__init__(message)
        self.step, self.message, self.code = step, message, code


def run(step, cmd, ok=(0,)):
    """Run one script. Return its stdout. Raise StepFailed on a bad exit code."""
    p = subprocess.run([PY, *[str(c) for c in cmd]], capture_output=True, text=True)
    if p.returncode not in ok:
        text = (p.stdout + p.stderr).strip() or f"exit {p.returncode}"
        raise StepFailed(step, text, 1)
    return p.stdout


def preamble(text):
    """Read the `key: value` lines that may sit above the first `---` line."""
    found = {}
    for line in text.splitlines():
        if line.strip() == "---":
            break
        m = re.match(r"^([a-z_]+):\s*(.+)$", line)
        if m:
            found[m.group(1)] = m.group(2).strip()
    return found


def check_schema(findings, step="findings schema"):
    try:
        import jsonschema
    except ImportError:
        return
    schema = json.loads((ROOT / "schema" / "findings.schema.json").read_text(encoding="utf-8"))
    errors = sorted(jsonschema.Draft202012Validator(schema).iter_errors(findings), key=lambda e: list(e.path))
    if errors:
        lines = [f"{'/'.join(str(p) for p in e.path) or 'top level'}: {e.message}" for e in errors[:5]]
        raise StepFailed(step, "\n".join(lines))


def assess(args):
    posting = Path(args.posting)
    findings_path = Path(args.findings)
    profile = Path(args.profile)
    for label, path in (("posting", posting), ("findings", findings_path), ("profile", profile)):
        if not path.is_file():
            raise StepFailed("read inputs", f"Cannot read {label}: {path}", 2)
    try:
        findings = json.loads(findings_path.read_text(encoding="utf-8"))
    except ValueError as exc:
        raise StepFailed("read inputs", f"{findings_path} is not valid JSON: {exc}", 2)

    pre = preamble(posting.read_text(encoding="utf-8"))
    company = args.company or pre.get("company")
    role = args.role or pre.get("role")
    lane = args.lane or pre.get("lane") or findings.get("lane")
    url = args.url or pre.get("url")
    source = args.source or pre.get("source")
    missing = [n for n, v in (("company", company), ("role", role), ("lane", lane)) if not v]
    if missing:
        raise StepFailed("read inputs", f"No {', '.join(missing)}: pass it as an option or put it at the top of the posting.", 2)

    out = Path(args.out)
    archive, work, mail = out / "archive", out / "work", out / "email"
    for d in (archive, work, mail):
        d.mkdir(parents=True, exist_ok=True)
    day = args.date or date.today().isoformat()
    log = lambda msg: print(msg, file=sys.stderr)  # noqa: E731

    log("1/10 validate the profile")
    run("validate profile", [ROOT / "scripts" / "validate_profile.py", profile, "--fixture"])
    log("2/10 check the findings against the schema")
    check_schema(findings)

    log("3/10 parse and archive the posting")
    cmd = [SCRIPTS / "parse_posting.py", posting, "--company", company, "--role", role, "--lane", lane,
           "--archive-dir", archive, "--date", day]
    if url:
        cmd += ["--url", url]
    if source:
        cmd += ["--source", source]
    if args.force:
        cmd.append("--force")
    parsed = subprocess.run([PY, *[str(c) for c in cmd]], capture_output=True, text=True)
    if parsed.returncode == 4:
        raise StepFailed("parse posting", (parsed.stdout + parsed.stderr).strip() + "\nUse a new --out folder, or pass --force.")
    if parsed.returncode != 0:
        raise StepFailed("parse posting", (parsed.stdout + parsed.stderr).strip())
    m = re.search(r"^Archived: (.+)$", parsed.stdout, re.M)
    if not m:
        raise StepFailed("parse posting", "parse_posting did not say where it saved the note.")
    note = Path(m.group(1).strip())

    log("4/10 load the lane and check the posting's lane matches")
    run("load criteria", [SCRIPTS / "load_criteria.py", "--profile", profile, "--lane", lane, "--posting", note])

    log("5/10 check every quote and id in the findings")
    run("check findings", [SCRIPTS / "check_findings.py", findings_path, "--posting", note, "--profile", profile])

    log("6/10 score and decide")
    scores_text = run("score", [SCRIPTS / "score_helpers.py", findings_path, "--profile", profile, "--json"])
    (work / "scores.json").write_text(scores_text, encoding="utf-8")
    scores = json.loads(scores_text)
    decision = verdict_mod.decide(
        scores["fit"], scores["qualifications"], scores["comp"], scores["culture"],
        override=verdict_mod.override_skill(findings), hard_block=verdict_mod.hard_block_id(findings))
    (work / "verdict.json").write_text(json.dumps(decision, indent=2) + "\n", encoding="utf-8")
    word = WORD[decision["label"]]

    log("7/10 render the assessment block and write it into the note")
    render = [SCRIPTS / "render_assessment.py", findings_path, "--scores", work / "scores.json",
              "--verdict", work / "verdict.json", "--profile", profile, "--date", day]
    (work / "block.md").write_text(run("render block", render), encoding="utf-8")
    run("write assessment", [SCRIPTS / "write_assessment.py", note, "--block", work / "block.md",
                             "--verdict", word, "--date", day])

    log("8/10 rename the note with its verdict emoji")
    renamed = run("rename", [SCRIPTS / "rename_verdict.py", note, "--verdict", word, "--profile", profile])
    m = re.search(r"^Renamed: (.+)$", renamed, re.M)
    final = Path(m.group(1).strip()) if m else note

    log("9/10 render the terminal summary")
    terminal = run("terminal summary", render + ["--terminal"])
    (work / "terminal.txt").write_text(terminal, encoding="utf-8")

    log("10/10 render the email card")
    card = [SCRIPTS / "render_email.py", "--note", final, "--findings", findings_path, "--scores", work / "scores.json",
            "--verdict", work / "verdict.json", "--profile", profile, "--out", mail, "--date", day]
    emailed = run("email card", card)

    print(terminal, end="" if terminal.endswith("\n") else "\n")
    log(f"Verdict: {decision['label']} (trigger {decision['trigger']})")
    log(f"Saved note: {final}")
    log(emailed.strip())
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description="Run the assessment chain offline from a findings file.")
    ap.add_argument("posting", help="posting text file")
    ap.add_argument("--findings", required=True, help="findings JSON that stands in for the model's reading")
    ap.add_argument("--profile", required=True, help="career-profile.yaml")
    ap.add_argument("--out", required=True, help="folder for the note, work files and email card")
    ap.add_argument("--date", help="assessment date YYYY-MM-DD (default today; pass it for repeatable output)")
    ap.add_argument("--company")
    ap.add_argument("--role")
    ap.add_argument("--lane")
    ap.add_argument("--url")
    ap.add_argument("--source", help="job source key from the profile")
    ap.add_argument("--force", action="store_true", help="archive even if the posting is already in DIR/archive")
    args = ap.parse_args(argv)
    try:
        return assess(args)
    except StepFailed as exc:
        print(f"assess_offline: step '{exc.step}' stopped the run.\n{exc.message}", file=sys.stderr)
        return exc.code


if __name__ == "__main__":
    sys.exit(main())
