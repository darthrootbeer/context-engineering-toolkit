# FICTIONAL EXAMPLE DATA. Not a real person. Every company, role and URL below is invented.
"""Tests for parse_posting.py. All data is inline; no fixture files are needed."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest
import yaml

SCRIPTS = Path(__file__).resolve().parent.parent / "assessment" / "scripts"
sys.path.insert(0, str(SCRIPTS))

import parse_posting as pp  # noqa: E402

POSTING = """\
Docs Platform Lead

About the role
Examplon Co is hiring someone to run the tooling behind its documentation.

Responsibilities
- Own the docs build pipeline and keep it fast.
- Write the contributor guide for the docs repo.

Requirements
- 8+ years of technical writing experience
- Bachelor's degree or equivalent
- Hands-on experience with OpenAPI and Markdown

Benefits
- Generous time off
- Python or SQL experience is a plus in this benefits blurb
"""

URL = "https://boards.greenhouse.io/examplon/jobs/4455667788"


def run(tmp_path, *extra, text=POSTING, company="Examplon Co", role="Docs Platform Lead", lane="docs-platform"):
    src = tmp_path / "posting.txt"
    src.write_text(text, encoding="utf-8")
    archive = tmp_path / "archive"
    cmd = [
        sys.executable, str(SCRIPTS / "parse_posting.py"), str(src),
        "--company", company, "--role", role, "--lane", lane,
        "--archive-dir", str(archive), "--date", "2026-10-01", *extra,
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    return proc, archive


def frontmatter(path: Path) -> dict:
    parts = pp.split_frontmatter(path.read_text(encoding="utf-8"))
    assert parts is not None
    return yaml.safe_load(parts[0])


def test_requirement_split():
    reqs = {r.text: r for r in pp.parse_requirements(POSTING)}
    assert reqs["8+ years of technical writing experience"].read_as == "likely filter"
    assert reqs["8+ years of technical writing experience"].kind == "experience"
    assert reqs["Bachelor's degree or equivalent"].kind == "credential"
    assert reqs["Bachelor's degree or equivalent"].read_as == "likely filter"
    assert reqs["Own the docs build pipeline and keep it fast."].read_as == "likely real"
    assert reqs["Hands-on experience with OpenAPI and Markdown"].kind == "skill"


def test_benefits_section_is_not_lifted():
    texts = [r.text for r in pp.parse_requirements(POSTING)]
    assert not any("Generous time off" in t or "Python or SQL" in t for t in texts)


def test_wrapped_prose_is_not_a_requirement():
    text = "Requirements\nExamplon is looking for a writer to join our Docs\nteam. You will own the tooling\n- Own the build pipeline end to end\n"
    texts = [r.text for r in pp.parse_requirements(text)]
    assert texts == ["Own the build pipeline end to end"]


def test_archive_has_seven_state_fields_and_valid_yaml(tmp_path):
    proc, archive = run(tmp_path, "--url", URL, "--source", "board-a")
    assert proc.returncode == 0, proc.stderr
    notes = list(archive.glob("*.md"))
    assert len(notes) == 1
    fm = frontmatter(notes[0])
    for key in ("opportunity_id", "source_urls", "ats_id", "state",
                "state_updated", "next_action", "next_action_due"):
        assert key in fm, key
    assert fm["opportunity_id"] == "greenhouse-4455667788"
    assert fm["ats_id"] == "greenhouse-4455667788"
    assert fm["source_urls"] == [URL]
    assert fm["state"] == "needs_review"
    assert str(fm["state_updated"]) == "2026-10-01"
    assert fm["lane"] == "docs-platform"
    assert fm["source"] == "board-a"
    assert fm["company"] == "Examplon Co"


def test_seven_fields_are_in_order_at_the_end_of_frontmatter(tmp_path):
    _, archive = run(tmp_path, "--url", URL)
    note = next(archive.glob("*.md")).read_text(encoding="utf-8")
    front = pp.split_frontmatter(note)[0]
    keys = [ln.split(":")[0] for ln in front.splitlines() if ln and not ln.startswith((" ", "#"))]
    tail = keys[keys.index("opportunity_id"):]
    assert tail == ["opportunity_id", "source_urls", "ats_id", "state",
                    "state_updated", "next_action", "next_action_due"]


def test_company_role_and_job_url_are_in_frontmatter_for_the_email_card(tmp_path):
    _, archive = run(tmp_path, "--url", URL)
    fm = frontmatter(next(archive.glob("*.md")))
    assert fm["company"] == "Examplon Co"
    assert fm["role"] == "Docs Platform Lead"
    assert fm["url"] == URL
    assert fm["job_url"] == URL


def test_url_keys_exist_but_are_empty_for_pasted_text(tmp_path):
    _, archive = run(tmp_path)
    fm = frontmatter(next(archive.glob("*.md")))
    assert fm["url"] == "" and fm["job_url"] == ""


def test_next_action_with_colon_is_quoted(tmp_path):
    _, archive = run(tmp_path)
    fm = frontmatter(next(archive.glob("*.md")))
    assert isinstance(fm["next_action"], str)
    raw = next(archive.glob("*.md")).read_text(encoding="utf-8")
    assert 'next_action: "' in raw


def test_awkward_company_and_role_stay_valid_yaml(tmp_path):
    proc, archive = run(tmp_path, company='Examplon: "Labs" & Sons', role="Writer/Trainer: Level 2")
    assert proc.returncode == 0, proc.stderr
    note = next(archive.glob("*.md"))
    fm = frontmatter(note)
    assert fm["company"] == 'Examplon: "Labs" & Sons'
    assert fm["role"] == "Writer/Trainer: Level 2"
    assert "Writer-Trainer" in note.name


def test_no_url_gives_slug_id_and_empty_source_list(tmp_path):
    _, archive = run(tmp_path)
    fm = frontmatter(next(archive.glob("*.md")))
    assert fm["opportunity_id"] == "examplon-co-docs-platform-lead-2026-10-01"
    assert fm["ats_id"] == "none"
    assert fm["source_urls"] == []


def test_bare_domain_url_is_flagged_for_hand_fill(tmp_path):
    _, archive = run(tmp_path, "--url", "https://jobs.example.com")
    raw = next(archive.glob("*.md")).read_text(encoding="utf-8")
    assert "Fill ats_id in by hand" in raw
    assert frontmatter(next(archive.glob("*.md")))["ats_id"] == "none"


def test_duplicate_same_lane_exits_4_and_writes_nothing(tmp_path):
    first, archive = run(tmp_path)
    assert first.returncode == 0
    second, _ = run(tmp_path)
    assert second.returncode == 4
    assert "DUPLICATE" in second.stderr
    assert len(list(archive.glob("*.md"))) == 1


def test_duplicate_found_even_after_rename_and_case_change(tmp_path):
    _, archive = run(tmp_path)
    note = next(archive.glob("*.md"))
    note.rename(note.with_name("🟢 " + note.name))
    second, _ = run(tmp_path, company="EXAMPLON CO", role="docs platform lead")
    assert second.returncode == 4


def test_duplicate_found_by_same_ats_id_with_different_title(tmp_path):
    run(tmp_path, "--url", URL)
    second, _ = run(tmp_path, "--url", URL, role="Lead, Docs Platform")
    assert second.returncode == 4


def test_second_lane_is_not_a_duplicate(tmp_path):
    run(tmp_path)
    second, archive = run(tmp_path, lane="tech-writing")
    assert second.returncode == 0, second.stderr
    notes = sorted(archive.glob("*.md"))
    assert len(notes) == 2
    assert {frontmatter(n)["lane"] for n in notes} == {"docs-platform", "tech-writing"}
    assert "Also archived for another lane" in second.stdout


def test_force_archives_a_same_lane_duplicate(tmp_path):
    run(tmp_path)
    second, archive = run(tmp_path, "--force")
    assert second.returncode == 0, second.stderr


def test_no_archive_writes_nothing(tmp_path):
    proc, archive = run(tmp_path, "--no-archive")
    assert proc.returncode == 0
    assert not archive.exists()


def test_archive_dir_required_without_no_archive(tmp_path):
    src = tmp_path / "p.txt"
    src.write_text(POSTING, encoding="utf-8")
    proc = subprocess.run(
        [sys.executable, str(SCRIPTS / "parse_posting.py"), str(src),
         "--company", "A", "--role", "B", "--lane", "x"],
        capture_output=True, text=True,
    )
    assert proc.returncode == 1


def test_body_keeps_posting_text_and_status_line(tmp_path):
    _, archive = run(tmp_path)
    raw = next(archive.glob("*.md")).read_text(encoding="utf-8")
    assert "**Application status:**" in raw
    assert "## Full posting text" in raw
    assert "Own the docs build pipeline and keep it fast." in raw.split("## Full posting text")[1]


@pytest.mark.parametrize("url, expected", [
    ("https://boards.greenhouse.io/x/jobs/123", "greenhouse-123"),
    ("https://example.com/careers?gh_jid=987", "greenhouse-987"),
    ("https://jobs.lever.co/acme/abc-123-def", "lever-abc-123-def"),
    ("https://jobs.ashbyhq.com/acme/uuid-1", "ashby-uuid-1"),
    ("https://example.com/jobs/12", "none"),
    ("", "none"),
])
def test_ats_id_from_url(url, expected):
    assert pp.ats_id_from_url(url) == expected


def test_no_private_network_address_or_personal_path_in_script():
    src = (SCRIPTS / "parse_posting.py").read_text(encoding="utf-8")
    for needle in ("192." + "168", "/Us" + "ers/"):
        assert needle not in src
