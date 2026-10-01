# FICTIONAL EXAMPLE DATA. Not a real person. Every company and posting below is invented.
"""Tests for write_assessment.py. The note is built by parse_posting.py, so the
two scripts are tested against each other."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import yaml

SCRIPTS = Path(__file__).resolve().parent.parent / "assessment" / "scripts"
sys.path.insert(0, str(SCRIPTS))

import parse_posting as pp  # noqa: E402
import write_assessment as wa  # noqa: E402

POSTING = "Requirements\n- Experience with Markdown and Git\n\nResponsibilities\n- Own the docs build pipeline\n"


def make_note(tmp_path) -> Path:
    note = pp.build_archive_note(
        "Examplon Co", "Docs Lead", ["https://example.com/jobs/1"], "2026-10-01",
        POSTING, pp.parse_requirements(POSTING), "docs-platform", "board-a",
    )
    path = tmp_path / "Examplon Co - Docs Lead - 2026-10-01.md"
    path.write_text(note, encoding="utf-8")
    return path


def make_block(tmp_path, text="## Assessment\n\nVerdict: Apply.\n") -> Path:
    path = tmp_path / "block.md"
    path.write_text(text, encoding="utf-8")
    return path


def run(note, block, verdict, date="2026-10-02"):
    return subprocess.run(
        [sys.executable, str(SCRIPTS / "write_assessment.py"), str(note),
         "--block", str(block), "--verdict", verdict, "--date", date],
        capture_output=True, text=True,
    )


def fm(path: Path) -> dict:
    return yaml.safe_load(pp.split_frontmatter(path.read_text(encoding="utf-8"))[0])


def below_divider(text: str) -> str:
    return text.split("\n---\n\n## Requirements read", 1)[1]


def test_block_goes_under_status_line_and_body_is_untouched(tmp_path):
    note = make_note(tmp_path)
    before = note.read_text(encoding="utf-8")
    proc = run(note, make_block(tmp_path), "apply")
    assert proc.returncode == 0, proc.stderr
    after = note.read_text(encoding="utf-8")
    status_at = after.index("**Application status:**")
    block_at = after.index("Verdict: Apply.")
    divider_at = after.index("\n---\n\n## Requirements read")
    assert status_at < block_at < divider_at
    assert below_divider(after) == below_divider(before)


def test_skip_sets_closed(tmp_path):
    note = make_note(tmp_path)
    assert run(note, make_block(tmp_path), "skip").returncode == 0
    data = fm(note)
    assert data["state"] == "closed"
    assert data["next_action"] == "none"
    assert str(data["state_updated"]) == "2026-10-02"


def test_apply_and_reservations_set_apply_ready(tmp_path):
    for verdict in ("apply", "reservations"):
        note = make_note(tmp_path)
        assert run(note, make_block(tmp_path), verdict).returncode == 0
        data = fm(note)
        assert data["state"] == "apply_ready"
        assert data["next_action"] == "Decide: apply, hold, or skip"


def test_pending_leaves_state_alone(tmp_path):
    note = make_note(tmp_path)
    assert run(note, make_block(tmp_path), "pending").returncode == 0
    assert fm(note)["state"] == "needs_review"


def test_never_advances_or_pulls_back_a_note_already_past_apply_ready(tmp_path):
    note = make_note(tmp_path)
    text = note.read_text(encoding="utf-8").replace("state: needs_review", "state: applied", 1)
    note.write_text(text, encoding="utf-8")
    assert run(note, make_block(tmp_path), "apply").returncode == 0
    assert fm(note)["state"] == "applied"


def test_rerun_replaces_the_block_and_notes_the_date(tmp_path):
    note = make_note(tmp_path)
    run(note, make_block(tmp_path, "FIRST BLOCK\n"), "apply")
    proc = run(note, make_block(tmp_path, "SECOND BLOCK\n"), "skip", date="2026-10-09")
    assert proc.returncode == 0, proc.stderr
    text = note.read_text(encoding="utf-8")
    assert "FIRST BLOCK" not in text and "SECOND BLOCK" in text
    assert text.count(wa.START) == 1 and text.count(wa.END) == 1
    assert "Re-assessed 2026-10-09" in text
    assert fm(note)["state"] == "closed"


def test_how_to_use_sentence_is_updated_and_frontmatter_stays_valid(tmp_path):
    note = make_note(tmp_path)
    run(note, make_block(tmp_path), "apply")
    data = fm(note)
    assert "assessment block at the top" in data["how_to_use_this_file"]
    assert wa.OLD_HOW_TO not in note.read_text(encoding="utf-8")
    assert str(data["updated"]) == "2026-10-02"


def test_refuses_and_leaves_note_untouched_when_status_line_is_missing(tmp_path):
    note = make_note(tmp_path)
    broken = note.read_text(encoding="utf-8").replace("**Application status:**", "**Something else:**")
    note.write_text(broken, encoding="utf-8")
    proc = run(note, make_block(tmp_path), "apply")
    assert proc.returncode == 1
    assert note.read_text(encoding="utf-8") == broken


def test_refuses_empty_block_and_bad_date(tmp_path):
    note = make_note(tmp_path)
    before = note.read_text(encoding="utf-8")
    assert run(note, make_block(tmp_path, "  \n"), "apply").returncode == 1
    assert run(note, make_block(tmp_path), "apply", date="Oct 2").returncode == 1
    assert note.read_text(encoding="utf-8") == before
