"""The whole chain, offline, on the three fictional postings.

Runs scripts/assess_offline.py as a user would (a subprocess, no model, no
network) and compares the result to fixtures/expected.yaml and to the files in
fixtures/golden/. Golden files carry one extra first line, the FICTIONAL
banner the safety scan requires; the test drops that line before comparing, so
the rest matches byte for byte.

To refresh the golden files after a deliberate change to a renderer:
    JA_UPDATE_GOLDEN=1 python3 -m pytest tests/test_e2e_offline.py -q
then read the diff before committing.
"""
import json
import os
import re
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parent.parent
FIX = ROOT / "fixtures"
GOLDEN = FIX / "golden"
SCRIPT = ROOT / "scripts" / "assess_offline.py"
PROFILE = FIX / "robin-sample" / "career-profile.yaml"
EXPECTED = yaml.safe_load((FIX / "expected.yaml").read_text(encoding="utf-8"))["postings"]
IDS = sorted(EXPECTED)
DATE = "2026-10-01"
BANNER = "FICTIONAL EXAMPLE DATA. Not a real person."
DOT = {"Apply": "\U0001F7E2", "Apply with reservations": "\U0001F7E1", "Skip": "\U0001F534"}


def banner_line(name):
    return f"<!-- {BANNER} -->\n" if name.endswith(".html") else f"{BANNER}\n"


def assess(posting_id, out, *extra):
    cmd = [sys.executable, str(SCRIPT), str(FIX / "postings" / f"{posting_id}.md"),
           "--findings", str(FIX / "findings" / f"{posting_id}.findings.json"),
           "--profile", str(PROFILE), "--out", str(out), "--date", DATE, *extra]
    # Run from the pipeline folder so the posting path in the output is the same for everyone.
    return subprocess.run(cmd, capture_output=True, text=True, cwd=ROOT)


def outputs(out):
    note = next((out / "archive").glob("*.md"))
    card = next((out / "email").glob("*.html"))
    return {
        "note.md": note.read_text(encoding="utf-8"),
        "terminal.txt": (out / "work" / "terminal.txt").read_text(encoding="utf-8"),
        "email.html": card.read_text(encoding="utf-8"),
        "note-name.txt": note.name + "\n",
    }


@pytest.fixture(scope="module")
def runs(tmp_path_factory):
    """Run the chain once per posting and keep the results."""
    results = {}
    for pid in IDS:
        out = tmp_path_factory.mktemp(pid)
        proc = assess(pid, out)
        results[pid] = (proc, out)
    return results


@pytest.mark.parametrize("pid", IDS)
def test_chain_exits_clean(runs, pid):
    proc, _ = runs[pid]
    assert proc.returncode == 0, proc.stderr


@pytest.mark.parametrize("pid", IDS)
def test_scores_and_verdict_match_expected_yaml(runs, pid):
    _, out = runs[pid]
    want = EXPECTED[pid]
    scores = json.loads((out / "work" / "scores.json").read_text(encoding="utf-8"))
    verdict = json.loads((out / "work" / "verdict.json").read_text(encoding="utf-8"))
    got = {k: scores[k] for k in ("fit", "comp", "qualifications", "culture")}
    assert got == {k: want[k] for k in got}
    assert verdict["label"] == want["verdict"]
    assert verdict["trigger"].replace(" ", "-") == want["trigger"]


@pytest.mark.parametrize("pid", IDS)
def test_note_is_renamed_and_carries_the_assessment(runs, pid):
    _, out = runs[pid]
    note = next((out / "archive").glob("*.md"))
    want = EXPECTED[pid]
    assert note.name.startswith(DOT[want["verdict"]])
    text = note.read_text(encoding="utf-8")
    assert "<!-- assessment:start -->" in text
    assert want["verdict"] in text
    assert "Full posting text" in text
    state = re.search(r"^state: (\S+)$", text, re.M).group(1)
    assert state == ("closed" if want["verdict"] == "Skip" else "apply_ready")
    assert len(list((out / "archive").glob("*.md"))) == 1


@pytest.mark.parametrize("pid", IDS)
def test_email_card_is_written_and_passes_its_own_check(runs, pid):
    _, out = runs[pid]
    card = next((out / "email").glob("*.html"))
    check = subprocess.run([sys.executable, str(ROOT / "assessment" / "scripts" / "check_email.py"), str(card)],
                           capture_output=True, text=True)
    assert check.returncode == 0, check.stdout + check.stderr


@pytest.mark.parametrize("pid", IDS)
def test_stdout_is_the_terminal_summary(runs, pid):
    proc, out = runs[pid]
    assert proc.stdout == (out / "work" / "terminal.txt").read_text(encoding="utf-8")
    assert EXPECTED[pid]["verdict"] in proc.stdout


@pytest.mark.parametrize("pid", IDS)
def test_outputs_match_golden_files_byte_for_byte(runs, pid):
    _, out = runs[pid]
    got = outputs(out)
    gdir = GOLDEN / pid
    if os.environ.get("JA_UPDATE_GOLDEN") == "1":
        gdir.mkdir(parents=True, exist_ok=True)
        for name, text in got.items():
            (gdir / name).write_text(banner_line(name) + text, encoding="utf-8")
    for name, text in got.items():
        golden = (gdir / name).read_text(encoding="utf-8")
        first, rest = golden.split("\n", 1)
        assert BANNER in first, f"{gdir / name} lost its banner line"
        assert rest == text, f"{pid}/{name} differs from the golden file"


def test_golden_folder_has_exactly_the_expected_files():
    for pid in IDS:
        names = sorted(p.name for p in (GOLDEN / pid).iterdir())
        assert names == ["email.html", "note-name.txt", "note.md", "terminal.txt"]
    assert sorted(p.name for p in GOLDEN.iterdir()) == IDS


def test_no_personal_path_in_any_output(runs):
    for pid in IDS:
        _, out = runs[pid]
        for name, text in outputs(out).items():
            for bad in ("/Users/", "/tmp/", "/private/", str(out)):
                assert bad not in text, f"{pid}/{name} contains {bad}"


def test_a_second_run_into_the_same_folder_is_refused_as_a_duplicate(runs):
    _, out = runs[IDS[0]]
    proc = assess(IDS[0], out)
    assert proc.returncode == 1
    assert "parse posting" in proc.stderr
    assert "already archived" in proc.stderr.lower() or "duplicate" in proc.stderr.lower()


def test_force_archives_a_second_copy(tmp_path):
    assert assess(IDS[0], tmp_path).returncode == 0
    assert assess(IDS[0], tmp_path, "--force").returncode == 0


def test_invented_quote_stops_the_chain_at_the_quote_check(tmp_path):
    findings = json.loads((FIX / "findings" / f"{IDS[0]}.findings.json").read_text(encoding="utf-8"))
    findings["requirements"][0]["quote"] = "This sentence is nowhere in the posting."
    bad = tmp_path / "bad.findings.json"
    bad.write_text(json.dumps(findings), encoding="utf-8")
    out = tmp_path / "out"
    cmd = [sys.executable, str(SCRIPT), str(FIX / "postings" / f"{IDS[0]}.md"), "--findings", str(bad),
           "--profile", str(PROFILE), "--out", str(out), "--date", DATE]
    proc = subprocess.run(cmd, capture_output=True, text=True, cwd=ROOT)
    assert proc.returncode == 1
    assert "check findings" in proc.stderr
    assert not list((out / "email").glob("*.html")), "no card may be written after a failed check"


def test_findings_that_break_the_schema_stop_the_chain_first(tmp_path):
    findings = json.loads((FIX / "findings" / f"{IDS[0]}.findings.json").read_text(encoding="utf-8"))
    findings["requirements"][0]["rating"] = "great"
    bad = tmp_path / "bad.findings.json"
    bad.write_text(json.dumps(findings), encoding="utf-8")
    cmd = [sys.executable, str(SCRIPT), str(FIX / "postings" / f"{IDS[0]}.md"), "--findings", str(bad),
           "--profile", str(PROFILE), "--out", str(tmp_path / "out"), "--date", DATE]
    proc = subprocess.run(cmd, capture_output=True, text=True, cwd=ROOT)
    assert proc.returncode == 1
    assert "findings schema" in proc.stderr
    assert not list((tmp_path / "out" / "archive").glob("*"))


def test_missing_input_exits_2(tmp_path):
    cmd = [sys.executable, str(SCRIPT), str(tmp_path / "nope.md"), "--findings", str(tmp_path / "nope.json"),
           "--profile", str(PROFILE), "--out", str(tmp_path / "out")]
    proc = subprocess.run(cmd, capture_output=True, text=True, cwd=ROOT)
    assert proc.returncode == 2


def test_wrong_lane_stops_at_the_lane_gate(tmp_path):
    cmd = [sys.executable, str(SCRIPT), str(FIX / "postings" / f"{IDS[0]}.md"),
           "--findings", str(FIX / "findings" / f"{IDS[0]}.findings.json"),
           "--profile", str(PROFILE), "--out", str(tmp_path / "out"), "--date", DATE, "--lane", "no-such-lane"]
    proc = subprocess.run(cmd, capture_output=True, text=True, cwd=ROOT)
    assert proc.returncode == 1
    assert "load criteria" in proc.stderr


def test_the_documented_clean_clone_commands_behave(tmp_path):
    """The two validator lines from the README's Verified block."""
    ok = subprocess.run([sys.executable, str(ROOT / "scripts" / "validate_profile.py"), "--fixture", str(PROFILE)],
                        capture_output=True, text=True, cwd=ROOT)
    assert ok.returncode == 0
    broken = subprocess.run([sys.executable, str(ROOT / "scripts" / "validate_profile.py"), "--fixture",
                             str(FIX / "broken-profile.yaml")], capture_output=True, text=True, cwd=ROOT)
    assert broken.returncode == 1
    assert len(broken.stdout.strip().splitlines()) == 5


def test_the_script_never_needs_the_claude_cli():
    text = SCRIPT.read_text(encoding="utf-8")
    for word in ("claude", "anthropic", "requests", "urllib"):
        assert word not in text.lower().replace("claude code", "")
