"""Tests for render_email.py and the card check. Inline data only, no network, no mail."""
import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "assessment" / "scripts"
TEMPLATE = ROOT / "assessment" / "templates" / "assessment-email.html"
sys.path.insert(0, str(SCRIPTS))

import check_email  # noqa: E402
import render_email  # noqa: E402

NOTE = """---
company: Example Co
role: Docs Writer
url: https://jobs.example.com/postings/1234
---
Saved posting text.
"""
FINDINGS = {
    "lane": "tech-writing",
    "verdict_reason": "A good match on the work, with pay left unsaid.",
    "requirements": [
        {"id": "ai_forward", "rating": "strong", "quote": "uses AI", "read": "The team uses AI tools daily."},
        {"id": "owns_docs", "rating": "weak", "quote": "supports", "read": "Mostly a support role."},
    ],
    "autonomy": {"net": "positive", "quotes": ["own your work"], "read": "You own the docs."},
    "pay": {"stated": False},
}
SCORES = {"fit": 9, "comp": 5, "qualifications": 6.5, "culture": 10}


@pytest.fixture
def inputs(tmp_path):
    (tmp_path / "note.md").write_text(NOTE, encoding="utf-8")
    (tmp_path / "findings.json").write_text(json.dumps(FINDINGS), encoding="utf-8")
    (tmp_path / "scores.json").write_text(json.dumps(SCORES), encoding="utf-8")
    return tmp_path


def run_render(inputs, verdict="apply", extra=()):
    return subprocess.run(
        [sys.executable, str(SCRIPTS / "render_email.py"),
         "--note", str(inputs / "note.md"), "--findings", str(inputs / "findings.json"),
         "--scores", str(inputs / "scores.json"), "--verdict", verdict,
         "--out", str(inputs / "out"), "--date", "2026-10-01", *extra],
        capture_output=True, text=True,
    )


def test_render_writes_a_card_that_passes(inputs):
    res = run_render(inputs)
    assert res.returncode == 0, res.stderr
    card = inputs / "out" / "example-co-docs-writer.html"
    assert card.is_file()
    html = card.read_text(encoding="utf-8")
    assert check_email.card_problems(html) == []
    assert "{{" not in html
    assert 'href="https://jobs.example.com/postings/1234"' in html
    assert "\U0001F7E2 Job Assessment: Example Co - Docs Writer - 2026-10-01" in res.stdout


def test_job_button_is_above_the_verdict(inputs):
    run_render(inputs)
    html = (inputs / "out" / "example-co-docs-writer.html").read_text(encoding="utf-8")
    assert html.index("View the job posting") < html.index('data-card="verdict"')
    assert html.index("View the job posting") < html.index("Apply</div>")


def test_scores_in_order_with_bars(inputs):
    run_render(inputs)
    html = (inputs / "out" / "example-co-docs-writer.html").read_text(encoding="utf-8")
    order = [html.index(">%s<" % n) for n in ("Fit", "Comp", "Qualifications", "Culture")]
    assert order == sorted(order)
    assert "width:100%" in html  # culture 10
    assert "#7c3aed" in html     # purple tier for 10
    assert ">7<" in html         # 6.5 rounds half up to 7


def test_check_rows_use_ratings(inputs):
    run_render(inputs)
    html = (inputs / "out" / "example-co-docs-writer.html").read_text(encoding="utf-8")
    assert "Ai forward" in html and "&#9679; Strong" in html and "&#9679; Weak" in html
    assert "The posting does not list pay." in html


@pytest.mark.parametrize("verdict,label,dot", [
    ("apply", "Apply", "\U0001F7E2"),
    ("reservations", "Apply with reservations", "\U0001F7E1"),
    ("skip", "Skip", "\U0001F534"),
])
def test_each_verdict(inputs, verdict, label, dot):
    res = run_render(inputs, verdict)
    assert res.returncode == 0, res.stderr
    html = (inputs / "out" / "example-co-docs-writer.html").read_text(encoding="utf-8")
    assert ">%s</div>" % label in html
    assert res.stdout.count(dot) == 1


def test_verdict_from_json_file(inputs):
    (inputs / "verdict.json").write_text(json.dumps({"label": "Skip", "trigger": "4a"}), encoding="utf-8")
    assert run_render(inputs, str(inputs / "verdict.json")).returncode == 0


def test_note_link_button_only_when_given(inputs):
    run_render(inputs)
    html = (inputs / "out" / "example-co-docs-writer.html").read_text(encoding="utf-8")
    assert "Open the saved note" not in html
    run_render(inputs, extra=["--note-link", "https://notes.example.com/n/1"])
    html = (inputs / "out" / "example-co-docs-writer.html").read_text(encoding="utf-8")
    assert "Open the saved note" in html and "https://notes.example.com/n/1" in html


def test_no_job_url_stops_and_writes_nothing(inputs):
    (inputs / "note.md").write_text(NOTE.replace("url: https://jobs.example.com/postings/1234\n", ""), encoding="utf-8")
    res = run_render(inputs)
    assert res.returncode == 1
    assert "job posting URL" in res.stderr
    assert not (inputs / "out").exists()


def test_placeholder_url_stops(inputs):
    res = run_render(inputs, extra=["--job-url", "#"])
    assert res.returncode == 1


def test_values_are_escaped(inputs):
    (inputs / "note.md").write_text(NOTE.replace("Example Co", "Fish & <b>Chips</b> Co"), encoding="utf-8")
    run_render(inputs)
    html = next((inputs / "out").glob("*.html")).read_text(encoding="utf-8")
    assert "<b>Chips</b>" not in html and "Fish &amp; &lt;b&gt;Chips" in html


def test_bad_verdict_word(inputs):
    assert run_render(inputs, "maybe").returncode == 1


def test_no_mail_sending_code_in_the_package():
    banned = ("smtplib", "sendmail", "msmtp", "send-email", "send_message", "mailto:")
    for path in list((ROOT / "assessment").rglob("*")):
        if path.is_file() and path.suffix in {".py", ".sh", ".html"}:
            text = path.read_text(encoding="utf-8").lower()
            for word in banned:
                assert word not in text, "%s mentions %s" % (path.name, word)


def test_template_has_the_job_button_first():
    html = TEMPLATE.read_text(encoding="utf-8")
    assert html.index("View the job posting") < html.index('data-card="verdict"')
