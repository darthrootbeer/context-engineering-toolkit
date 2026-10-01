# FICTIONAL EXAMPLE DATA. Not a real person. Minimal inline profile that follows the career-profile format.
"""Tests for load_criteria.py."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import yaml

SCRIPTS = Path(__file__).resolve().parent.parent / "assessment" / "scripts"

PROFILE = {
    "schema_version": 1,
    "person": {
        "display_name": "Robin Sample",
        "target_roles": ["Docs Lead"],
        "years_experience": 9,
        "location_label": "Region B",
        "working_style": "gather_from_experts",
    },
    "hard_blocks": [
        {"id": "gambling", "label": "Gambling or betting", "why": "Not for me.",
         "match_hints": ["sports betting", "casino"]},
        {"id": "non_remote", "label": "On-site only", "why": "Remote only.",
         "match_hints": ["on-site five days"]},
    ],
    "named_exceptions": [
        {"company": "Placeholder Labs", "block_id": "non_remote", "why": "One-off.", "added": "2026-10-01"},
    ],
    "comp": {"currency": "USD", "floor": 90000, "min": 110000, "open_ask": 125000,
             "target": 140000, "stretch_ceiling": 170000},
    "culture": {
        "perks": [{"id": "unlimited_pto", "label": "Unlimited PTO", "kind": "big"},
                  {"id": "offsites", "label": "Regular offsites", "kind": "nice"}],
        "low_time_off_days": 15,
        "hustle_phrases": ["rockstar"],
        "free_phrases": ["fast-paced"],
    },
    "soft_flags": [{"id": "agency", "label": "Agency work", "why": "Many clients."}],
    "benefits_and_terms": [{"id": "equity_only", "label": "Equity-heavy pay", "why": "Cash matters."}],
    "company_criteria": {
        "high_interest": [{"name": "Northwind Example Co.", "why": "Good docs culture."}],
        "good_not_dream": [{"name": "Placeholder Labs", "why": "Fine job."}],
    },
    "lanes": [
        {
            "name": "docs-platform",
            "emoji": "🔧",
            "description": "Roles building the systems that produce docs.",
            "requirements": [
                {"id": "ai_forward", "label": "AI-forward team", "severity": "strong", "why": "Wants it."},
                {"id": "solo_ownership", "label": "Owns the docs", "severity": "soft", "bonus": True},
            ],
            "autonomy": {"positive_signals": ["owns the roadmap"], "negative_signals": ["approval for every change"]},
            "keyword_signals": {"strong_positive": [{"phrase": "docs as code", "why": "Matches the work."}]},
            "known_gaps": [{"id": "gap_video", "label": "Video production", "skill_id": "video"}],
        },
        {
            "name": "tech-writing",
            "emoji": "✍️",
            "description": "Senior writing roles.",
            "requirements": [{"id": "only_writing", "label": "Mostly writing", "severity": "strong"}],
        },
    ],
    "skills": [{"id": "video", "label": "Video editing", "next": "avoid", "self_score": 1}],
}


def make_profile(tmp_path) -> Path:
    path = tmp_path / "career-profile.yaml"
    path.write_text(yaml.safe_dump(PROFILE, allow_unicode=True, sort_keys=False), encoding="utf-8")
    return path


def make_posting(tmp_path, lane: str | None) -> Path:
    front = "---\ntitle: \"Job Posting - X\"\n" + (f"lane: {lane}\n" if lane else "") + "---\n\n# X\n"
    path = tmp_path / "posting.md"
    path.write_text(front, encoding="utf-8")
    return path


def run(*args):
    return subprocess.run(
        [sys.executable, str(SCRIPTS / "load_criteria.py"), *map(str, args)],
        capture_output=True, text=True,
    )


def test_prints_every_hard_block_and_requirement(tmp_path):
    proc = run("--profile", make_profile(tmp_path), "--lane", "docs-platform")
    assert proc.returncode == 0, proc.stderr
    out = proc.stdout
    for needle in ("[gambling]", "[non_remote]", "[ai_forward]", "[solo_ownership]",
                   "AI-forward team", "Owns the docs", "bonus"):
        assert needle in out
    assert "Placeholder Labs" in out  # named exception is listed
    assert "docs as code" in out
    assert "Video production (skill: video)" in out
    assert "[unlimited_pto]" in out and "(big)" in out
    assert "RATHER AVOID" in out and "Video editing" in out


def test_only_the_requested_lane_is_printed(tmp_path):
    out = run("--profile", make_profile(tmp_path), "--lane", "docs-platform").stdout
    assert "only_writing" not in out
    out2 = run("--profile", make_profile(tmp_path), "--lane", "tech-writing").stdout
    assert "only_writing" in out2 and "ai_forward" not in out2


def test_unknown_lane_exits_2_and_lists_lanes(tmp_path):
    proc = run("--profile", make_profile(tmp_path), "--lane", "nonsense")
    assert proc.returncode == 2
    assert "docs-platform" in proc.stderr and "tech-writing" in proc.stderr
    assert proc.stdout == ""


def test_posting_lane_mismatch_exits_3_and_prints_no_rubric(tmp_path):
    posting = make_posting(tmp_path, "tech-writing")
    proc = run("--profile", make_profile(tmp_path), "--lane", "docs-platform", "--posting", posting)
    assert proc.returncode == 3
    assert "LANE MISMATCH" in proc.stderr
    assert proc.stdout == ""


def test_posting_without_lane_exits_3(tmp_path):
    posting = make_posting(tmp_path, None)
    proc = run("--profile", make_profile(tmp_path), "--lane", "docs-platform", "--posting", posting)
    assert proc.returncode == 3


def test_matching_posting_lane_passes(tmp_path):
    posting = make_posting(tmp_path, "docs-platform")
    proc = run("--profile", make_profile(tmp_path), "--lane", "docs-platform", "--posting", posting)
    assert proc.returncode == 0, proc.stderr
    assert "posting and profile agree" in proc.stdout


def test_missing_profile_exits_1(tmp_path):
    proc = run("--profile", tmp_path / "nope.yaml", "--lane", "docs-platform")
    assert proc.returncode == 1
