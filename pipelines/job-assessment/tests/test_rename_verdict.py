# FICTIONAL EXAMPLE DATA. Not a real person. Every company and role below is invented.
"""Tests for verdict, source and lane emoji naming.

The naming rule lives in code because a prose instruction is followed most of
the time and not every time. Emoji for sources and lanes come from the career
profile, so these tests build a minimal inline profile.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import yaml

SCRIPTS = Path(__file__).resolve().parent.parent / "assessment" / "scripts"
sys.path.insert(0, str(SCRIPTS))

import rename_verdict as rv  # noqa: E402

PROFILE = {
    "schema_version": 1,
    "sources": [
        {"key": "board-a", "emoji": "📋", "label": "Job board A"},
        {"key": "board-b", "emoji": "🚀", "label": "Job board B"},
    ],
    "lanes": [
        {"name": "docs-platform", "emoji": "🔧"},
        {"name": "tech-writing", "emoji": "✍️"},
    ],
}

FRONTMATTER = 'title: "Job Posting - Acme: Senior Technical Writer"\n'


def make(tmp_path, name="Acme - Senior Technical Writer - 2026-09-07.md", lane=None, source=None):
    extra = (f'lane: "{lane}"\n' if lane else "") + (f'source: "{source}"\n' if source else "")
    p = tmp_path / name
    p.write_text("---\n" + FRONTMATTER + extra + "---\n", encoding="utf-8")
    return p


def profile_path(tmp_path) -> Path:
    p = tmp_path / "career-profile.yaml"
    p.write_text(yaml.safe_dump(PROFILE, allow_unicode=True), encoding="utf-8")
    return p


def cli(note, profile, *args):
    return subprocess.run(
        [sys.executable, str(SCRIPTS / "rename_verdict.py"), str(note),
         "--profile", str(profile), *args],
        capture_output=True, text=True,
    )


def test_verdict_emoji_is_the_first_character(tmp_path):
    """The verdict must survive truncation in a file list."""
    out = rv.rename_file(make(tmp_path), "🟢")
    assert out.name.startswith("🟢 ")


def test_source_emoji_sits_second(tmp_path):
    out = rv.rename_file(make(tmp_path), "🟢", "📋")
    assert out.name.startswith("🟢 📋 ")
    assert out.name.endswith("Acme - Senior Technical Writer - 2026-09-07.md")


def test_title_matches_the_filename(tmp_path):
    out = rv.rename_file(make(tmp_path), "🔴", "🚀")
    rv.update_title(out, "🔴", "🚀")
    assert 'title: "🔴 🚀 Job Posting - Acme' in out.read_text(encoding="utf-8")


def test_rerunning_does_not_stack_emoji(tmp_path):
    out = rv.rename_file(make(tmp_path), "🟢", "📋")
    out = rv.rename_file(out, "🔴", "📋")
    assert out.name.count("🟢") == 0
    assert out.name.count("🔴") == 1
    assert out.name.count("📋") == 1


def test_source_can_be_added_to_an_untagged_note(tmp_path):
    out = rv.rename_file(make(tmp_path), "🟢")
    out = rv.rename_file(out, "🟢", "📋")
    assert out.name.startswith("🟢 📋 ")


def test_omitting_source_still_works(tmp_path):
    out = rv.rename_file(make(tmp_path), "🟡")
    assert out.name.startswith("🟡 ")
    assert "📋" not in out.name and "🚀" not in out.name


def test_emoji_stranded_in_an_old_position_is_cleaned_up(tmp_path):
    p = make(tmp_path, "Acme - Writer - 2026-09-07 🔴.md")
    out = rv.rename_file(p, "🟢", "🚀")
    assert out.name.startswith("🟢 🚀 ")
    assert "🔴" not in out.name


def test_non_markdown_file_is_rejected(tmp_path):
    p = tmp_path / "notes.txt"
    p.write_text("x")
    try:
        rv.rename_file(p, "🟢")
    except ValueError:
        return
    raise AssertionError("expected a ValueError for a non-.md file")


def test_lane_emoji_sits_third(tmp_path):
    p = make(tmp_path, "Acme - Senior Technical Writer - 2026-09-16.md")
    new = rv.rename_file(p, "🟡", "📋", "✍️")
    assert new.name == "🟡 📋 ✍️ Acme - Senior Technical Writer - 2026-09-16.md"


def test_lane_without_source(tmp_path):
    p = make(tmp_path, "Beta - Docs Engineer - 2026-09-16.md")
    new = rv.rename_file(p, "🟢", None, "🔧")
    assert new.name == "🟢 🔧 Beta - Docs Engineer - 2026-09-16.md"


def test_lane_rerun_does_not_stack(tmp_path):
    p = make(tmp_path, "Acme - Writer - 2026-09-16.md")
    first = rv.rename_file(p, "🟡", "📋", "✍️")
    second = rv.rename_file(first, "🔴", "📋", "✍️")
    assert second.name == "🔴 📋 ✍️ Acme - Writer - 2026-09-16.md"
    assert second.name.count("✍️") == 1
    assert "🟡" not in second.name


def test_changing_source_removes_the_old_marker_when_profile_emoji_are_known(tmp_path):
    p = make(tmp_path, "Acme - Writer - 2026-09-16.md")
    first = rv.rename_file(p, "🟢", "📋", "🔧", known=["📋", "🚀", "🔧", "✍️"])
    second = rv.rename_file(first, "🟢", "🚀", "🔧", known=["📋", "🚀", "🔧", "✍️"])
    assert second.name == "🟢 🚀 🔧 Acme - Writer - 2026-09-16.md"


def test_lane_title_updated(tmp_path):
    p = make(tmp_path, "Acme - Writer - 2026-09-16.md")
    new = rv.rename_file(p, "🟡", "📋", "✍️")
    rv.update_title(new, "🟡", "📋", "✍️")
    assert 'title: "🟡 📋 ✍️ Job Posting' in new.read_text(encoding="utf-8")


def test_no_lane_still_works(tmp_path):
    p = make(tmp_path, "Gamma - Writer - 2026-09-16.md")
    new = rv.rename_file(p, "🟢", "🚀")
    assert new.name == "🟢 🚀 Gamma - Writer - 2026-09-16.md"


def test_cli_reads_lane_and_source_from_frontmatter_and_profile(tmp_path):
    note = make(tmp_path, "Acme - Writer - 2026-09-16.md", lane="tech-writing", source="board-b")
    proc = cli(note, profile_path(tmp_path), "--verdict", "reservations")
    assert proc.returncode == 0, proc.stderr
    renamed = tmp_path / "🟡 🚀 ✍️ Acme - Writer - 2026-09-16.md"
    assert renamed.exists()
    assert 'title: "🟡 🚀 ✍️ Job Posting' in renamed.read_text(encoding="utf-8")


def test_cli_flags_override_frontmatter_and_rerun_is_idempotent(tmp_path):
    note = make(tmp_path, "Acme - Writer - 2026-09-16.md", lane="tech-writing", source="board-b")
    prof = profile_path(tmp_path)
    assert cli(note, prof, "--verdict", "apply").returncode == 0
    first = next(tmp_path.glob("🟢*"))
    proc = cli(first, prof, "--verdict", "skip", "--source", "board-a", "--lane", "docs-platform")
    assert proc.returncode == 0, proc.stderr
    names = [p.name for p in tmp_path.glob("*.md")]
    assert names == ["🔴 📋 🔧 Acme - Writer - 2026-09-16.md"]


def test_cli_pending_verdict(tmp_path):
    note = make(tmp_path, "Acme - Writer - 2026-09-16.md", lane="docs-platform")
    assert cli(note, profile_path(tmp_path), "--verdict", "pending").returncode == 0
    assert (tmp_path / "⚪ 🔧 Acme - Writer - 2026-09-16.md").exists()


def test_cli_unknown_source_or_lane_is_refused_and_nothing_renamed(tmp_path):
    note = make(tmp_path, "Acme - Writer - 2026-09-16.md", lane="docs-platform")
    prof = profile_path(tmp_path)
    assert cli(note, prof, "--verdict", "apply", "--source", "nope").returncode == 1
    assert cli(note, prof, "--verdict", "apply", "--lane", "nope").returncode == 1
    assert note.exists()


def test_cli_without_lane_warns_and_still_renames(tmp_path):
    note = make(tmp_path, "Acme - Writer - 2026-09-16.md")
    proc = cli(note, profile_path(tmp_path), "--verdict", "apply")
    assert proc.returncode == 0
    assert "no lane found" in proc.stderr
    assert (tmp_path / "🟢 Acme - Writer - 2026-09-16.md").exists()
