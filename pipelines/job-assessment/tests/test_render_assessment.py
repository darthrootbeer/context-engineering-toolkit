"""Bars, tiers, order, legend and the rendered block. Inline data only.

FICTIONAL EXAMPLE DATA. Nothing here is a real person or posting.
"""
import json
import sys
from pathlib import Path

import pytest
import yaml

SCRIPTS = Path(__file__).resolve().parents[1] / "assessment" / "scripts"
sys.path.insert(0, str(SCRIPTS))

import render_assessment as ra  # noqa: E402

PROFILE = {
    "lanes": [{"name": "lane-a", "requirements": [
        {"id": "ai_forward", "label": "✨ AI-forward team", "severity": "strong"},
    ]}],
    "evidence": [
        {"id": "ev-1", "claim": "Rebuilt the API reference.", "proof": "checked"},
        {"id": "ev-2", "claim": "Ran a docs migration.", "proof": "unchecked"},
    ],
}
FINDINGS = {
    "posting_file": "postings/example.md",
    "lane": "lane-a",
    "hard_block": {"tripped": False},
    "requirements": [{"id": "ai_forward", "rating": "fair", "quote": "uses AI tools", "read": "Some use of AI."}],
    "autonomy": {"net": "negative", "read": "Reviews are tight."},
    "pay": {"stated": False},
    "culture": {"soft_flags_tripped": []},
    "qualifications": {
        "years_required": 5,
        "matches": [{"requirement_quote": "API docs", "evidence_ids": ["ev-1", "ev-2"]}],
        "unproven": [{"skill_id": "openapi", "requirement_quote": "OpenAPI"}],
    },
    "company_read": {"status": "none"},
    "verdict_reason": "A solid match with one thing to confirm.",
    "keyword_signals_found": [{"phrase": "we hire on a work sample", "read": "Fair hiring."}],
    "new_signals_to_consider": [],
}
SCORES = {"fit": 9, "comp": 5, "qualifications": 10, "culture": 0, "why": {}}
VERDICT = {"label": "Apply with reservations", "trigger": "4c culture"}


# ------------------------------------------------------------------ bars

def test_zero_is_all_empty():
    assert ra.bar(0) == "⬛" * 10


def test_ten_is_all_stars():
    assert ra.bar(10) == "🌟" * 10


@pytest.mark.parametrize("score,segment", [
    (1, "🔴"), (2, "🔴"), (3, "🟠"), (4, "🟠"), (5, "🟡"), (6, "🟡"),
    (7, "🟢"), (8, "🟢"), (9, "🟢"),
])
def test_tier_colors(score, segment):
    expected = segment * score + "⬛" * (10 - score)
    assert ra.bar(score) == expected
    assert len(expected) == 10  # 10 single-codepoint segments


def test_a_nine_is_nine_green_and_one_empty_not_a_star():
    assert ra.bar(9) == "🟢" * 9 + "⬛"
    assert "🌟" not in ra.bar(9)


def test_every_bar_has_ten_segments():
    for n in range(11):
        assert len(ra.bar(n)) == 10


def test_scores_print_in_fit_comp_qualifications_culture_order():
    lines = ra.score_lines({"culture": 1, "qualifications": 2, "comp": 3, "fit": 4})
    assert [l.split()[0] for l in lines] == ["Fit", "Comp", "Qualifications", "Culture"]
    assert lines[0] == "Fit 4 🟠🟠🟠🟠⬛⬛⬛⬛⬛⬛"


def test_no_slash_ten_suffix():
    assert "/10" not in "\n".join(ra.score_lines(SCORES))


# --------------------------------------------------------------- terminal

def terminal():
    return ra.render_terminal(FINDINGS, SCORES, VERDICT, PROFILE)


def test_terminal_has_the_legend_line_last():
    last = terminal().rstrip().splitlines()[-1]
    assert last == "🟢 Strong · 🟡 Fair · 🟠 Weak · 🔴 Poor · ❓ Unknown"


def test_terminal_verdict_comes_before_the_scores_and_table():
    out = terminal()
    assert out.index("VERDICT: Apply with reservations") < out.index("Fit 9") < out.index("| Check |")


def test_terminal_scores_in_order():
    out = terminal()
    assert out.index("Fit 9") < out.index("Comp 5") < out.index("Qualifications 10") < out.index("Culture 0")


def test_terminal_uses_criterion_labels_not_ids():
    out = terminal()
    assert "✨ AI-forward team" in out
    assert "ai_forward" not in out


def test_terminal_maps_ratings_to_dots_and_autonomy_net():
    out = terminal()
    assert "🟡 Fair" in out
    assert "🟠 Weak" in out  # autonomy net negative


def test_terminal_company_line_only_when_there_is_a_stored_reaction():
    assert "🏢" not in terminal()
    f = dict(FINDINGS, company_read={"status": "high_interest", "name": "Example Co.",
                                     "stored_reason": "I use their product daily."})
    out = ra.render_terminal(f, SCORES, VERDICT, PROFILE)
    assert "🏢 Example Co. is one you have said you want to work for." in out
    assert "did not change the scores or the verdict" in out


def test_terminal_shows_a_tripped_hard_block_row():
    f = dict(FINDINGS, hard_block={"tripped": True, "id": "gambling", "quote": "q"})
    assert "| Hard block | 🔴 Poor | gambling |" in ra.render_terminal(f, SCORES, VERDICT, PROFILE)


def test_a_pipe_in_a_read_cannot_break_the_table():
    f = dict(FINDINGS, requirements=[{"id": "ai_forward", "rating": "fair", "read": "a | b"}])
    row = [l for l in ra.render_terminal(f, SCORES, VERDICT, PROFILE).splitlines() if "AI-forward" in l][0]
    assert row.count("|") == 4


# ------------------------------------------------------------------ block

def block():
    return ra.render_block(FINDINGS, SCORES, VERDICT, PROFILE, "2026-10-01")


def test_block_opens_with_the_verdict_and_reason():
    lines = block().splitlines()
    assert lines[0] == "## Assessment"
    assert lines[2] == "**🚦 Verdict:** Apply with reservations"
    assert lines[3] == "A solid match with one thing to confirm."


def test_block_has_scores_in_order_and_the_date():
    out = block()
    assert out.index("Fit 9") < out.index("Comp 5") < out.index("Qualifications 10") < out.index("Culture 0")
    assert "**Assessed:** 2026-10-01" in out


def test_block_sections_come_in_the_live_order():
    out = block()
    heads = ["### ⛔ Hard blocks", "### 🏢 The company itself", "### ✅ / ⚠️ Requirements",
             "### 🎯 How much say you'd actually have", "### 🔑 Language worth noticing",
             "### 🧩 How well the skills line up", "### 🚩 Other things worth knowing"]
    positions = [out.index(h) for h in heads]
    assert positions == sorted(positions)


def test_block_says_the_company_read_did_not_change_the_verdict():
    assert "did not change the scores or the verdict" in block()


def test_block_marks_unchecked_evidence_and_unproven_skills():
    out = block()
    assert "Rebuilt the API reference." in out
    assert "Ran a docs migration. (your own account, not yet backed by a document)" in out
    assert "nothing in your file proves it (openapi)" in out


def test_block_says_unlisted_pay_is_unknown_not_bad():
    assert "Not listed. Scored as unknown, not as bad." in block()


def test_block_ends_with_a_single_newline_and_has_no_em_dash():
    out = block()
    assert out.endswith("\n") and not out.endswith("\n\n")
    assert "—" not in out


def test_block_hard_block_text():
    f = dict(FINDINGS, hard_block={"tripped": True, "id": "gambling", "quote": "casino"})
    assert 'gambling was tripped: "casino"' in ra.render_block(f, SCORES, VERDICT, PROFILE, "2026-10-01")


# -------------------------------------------------------------------- cli

def test_cli_block_and_terminal(tmp_path, capsys):
    (tmp_path / "f.json").write_text(json.dumps(FINDINGS))
    (tmp_path / "s.json").write_text(json.dumps(SCORES))
    (tmp_path / "v.json").write_text(json.dumps(VERDICT))
    (tmp_path / "p.yaml").write_text(yaml.safe_dump(PROFILE))
    base = [str(tmp_path / "f.json"), "--scores", str(tmp_path / "s.json"),
            "--verdict", str(tmp_path / "v.json"), "--profile", str(tmp_path / "p.yaml")]
    assert ra.main(base + ["--date", "2026-10-01"]) == 0
    assert capsys.readouterr().out == block()
    assert ra.main(base + ["--terminal"]) == 0
    assert capsys.readouterr().out == terminal()


def test_cli_exit_two_when_a_file_is_missing(tmp_path):
    assert ra.main([str(tmp_path / "x.json"), "--scores", "a", "--verdict", "b", "--profile", "c"]) == 2
