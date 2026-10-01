"""Tests for the card check and the optional hook wrapper."""
import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "assessment" / "scripts"
HOOK = ROOT / "assessment" / "hooks" / "assessment-email-template-guard.sh"
TEMPLATE = ROOT / "assessment" / "templates" / "assessment-email.html"
sys.path.insert(0, str(SCRIPTS))

import check_email  # noqa: E402

GREEN = "\U0001F7E2"


@pytest.fixture
def card(tmp_path):
    """A real rendered card."""
    (tmp_path / "note.md").write_text(
        "---\ncompany: Example Co\nrole: Docs Writer\nurl: https://jobs.example.com/p/1\n---\n", encoding="utf-8")
    (tmp_path / "f.json").write_text(json.dumps({"lane": "x", "verdict_reason": "ok", "requirements": []}), encoding="utf-8")
    (tmp_path / "s.json").write_text(json.dumps({"fit": 8, "comp": 8, "qualifications": 8, "culture": 8}), encoding="utf-8")
    res = subprocess.run(
        [sys.executable, str(SCRIPTS / "render_email.py"), "--note", str(tmp_path / "note.md"),
         "--findings", str(tmp_path / "f.json"), "--scores", str(tmp_path / "s.json"),
         "--verdict", "apply", "--out", str(tmp_path)], capture_output=True, text=True)
    assert res.returncode == 0, res.stderr
    return tmp_path / "example-co-docs-writer.html"


def run_check(path, *extra):
    return subprocess.run([sys.executable, str(SCRIPTS / "check_email.py"), str(path), *extra],
                          capture_output=True, text=True)


def test_card_with_job_link_passes(card):
    res = run_check(card, "--subject", GREEN + " Job Assessment: Example Co - Docs Writer - 2026-10-01")
    assert res.returncode == 0, res.stderr


def test_plain_body_is_blocked_with_exit_2(tmp_path):
    plain = tmp_path / "plain.html"
    plain.write_text("<html><body><p>Apply. Fit 9, Comp 8.</p></body></html>", encoding="utf-8")
    res = run_check(plain)
    assert res.returncode == 2
    assert "View the job posting" in res.stderr


def test_missing_file_is_blocked(tmp_path):
    assert run_check(tmp_path / "nope.html").returncode == 2


def test_raw_template_with_leftover_placeholders_is_blocked():
    res = run_check(TEMPLATE)
    assert res.returncode == 2
    assert "unfilled placeholders" in res.stderr and "{{JOB_URL}}" in res.stderr


def test_one_leftover_placeholder_is_blocked(card):
    card.write_text(card.read_text(encoding="utf-8").replace("Docs Writer", "{{ROLE}}", 1), encoding="utf-8")
    res = run_check(card)
    assert res.returncode == 2 and "{{ROLE}}" in res.stderr


@pytest.mark.parametrize("bad", ["#", "", "notes://saved/1", "https://", "javascript:alert(1)", "/relative"])
def test_job_link_must_be_a_real_http_url(card, bad):
    html = card.read_text(encoding="utf-8").replace("https://jobs.example.com/p/1", bad)
    card.write_text(html, encoding="utf-8")
    res = run_check(card)
    assert res.returncode == 2


def test_missing_job_button_is_blocked(card):
    html = card.read_text(encoding="utf-8").replace("View the job posting", "Open")
    card.write_text(html, encoding="utf-8")
    assert run_check(card).returncode == 2


def test_job_button_below_verdict_is_blocked(card):
    html = card.read_text(encoding="utf-8")
    start = html.index('<tr><td style="padding:18px')
    end = html.index("</td></tr>", start) + len("</td></tr>")
    button_row = html[start:end]
    html = html[:start] + html[end:]
    marker = '<tr><td style="padding:20px 24px 4px'
    html = html.replace(marker, button_row + marker, 1)
    card.write_text(html, encoding="utf-8")
    res = run_check(card)
    assert res.returncode == 2 and "above the verdict" in res.stderr


def test_missing_scores_bars_checks_each_blocked(card):
    base = card.read_text(encoding="utf-8")
    for old, new in ((">Scores<", ">Totals<"), ("border-radius:5px 0 0 5px", "border-radius:0"), (">Checks<", ">Notes<")):
        card.write_text(base.replace(old, new), encoding="utf-8")
        assert run_check(card).returncode == 2, old


@pytest.mark.parametrize("subject", ["Job Assessment: Example Co", "Job Assessment: " + GREEN, " " + GREEN + " Job Assessment"])
def test_subject_without_leading_dot_is_blocked(card, subject):
    assert run_check(card, "--subject", subject).returncode == 2


# --- hook wrapper ---------------------------------------------------------

def run_hook(command):
    payload = json.dumps({"tool_input": {"command": command}})
    return subprocess.run(["bash", str(HOOK)], input=payload, capture_output=True, text=True)


def test_hook_ignores_unrelated_commands():
    assert run_hook("ls -la").returncode == 0
    assert run_hook("mailer -s 'Weekly notes' -H /tmp/x.html").returncode == 0


def test_hook_blocks_plain_body_payload(tmp_path):
    plain = tmp_path / "plain.html"
    plain.write_text("<p>Apply.</p>", encoding="utf-8")
    res = run_hook("mailer -t me -s '%s Job Assessment: Example Co - Docs Writer' -H %s" % (GREEN, plain))
    assert res.returncode == 2
    assert "BLOCK" in res.stderr


def test_hook_blocks_assessment_email_with_no_html_body():
    res = run_hook("mailer -s '%s Job Assessment: Example Co' -b 'plain text'" % GREEN)
    assert res.returncode == 2


def test_hook_blocks_bad_subject_even_with_a_good_card(card):
    res = run_hook("mailer -s 'Job Assessment: Example Co' -H %s" % card)
    assert res.returncode == 2


def test_hook_allows_good_card(card):
    res = run_hook("mailer -s '%s Job Assessment: Example Co - Docs Writer' --html %s" % (GREEN, card))
    assert res.returncode == 0, res.stderr


def test_hook_finds_the_command_in_a_chained_line(tmp_path):
    plain = tmp_path / "plain.html"
    plain.write_text("<p>x</p>", encoding="utf-8")
    res = run_hook("cd /tmp && mailer -s '%s Job Assessment: A - B' -H %s; echo done" % (GREEN, plain))
    assert res.returncode == 2


def test_hook_survives_garbage_payload():
    res = subprocess.run(["bash", str(HOOK)], input="job assessment {not json", capture_output=True, text=True)
    assert res.returncode == 0
