# FICTIONAL EXAMPLE DATA. Not a real person. Minimal inline profile that follows the career-profile format.
"""Tests for match_skills.py."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import yaml

SCRIPTS = Path(__file__).resolve().parent.parent / "assessment" / "scripts"
sys.path.insert(0, str(SCRIPTS))

import match_skills as ms  # noqa: E402

PROFILE = {
    "schema_version": 1,
    "evidence": [
        {"id": "ev-good", "authorship": "WROTE", "proof": "checked"},
        {"id": "ev-own", "authorship": "DIRECTED", "proof": "unchecked"},
        {"id": "ev-banned", "authorship": "WROTE", "proof": "do_not_use"},
        {"id": "ev-other", "authorship": "OTHER-AUTHOR", "proof": "checked"},
    ],
    "skills": [
        {"id": "openapi", "label": "OpenAPI", "match": ["openapi|swagger"], "self_score": 5,
         "next": "more", "last": "2y", "how": ["self", "ai"], "evidence_ids": ["ev-good"]},
        {"id": "python", "label": "Python", "match": ["python"], "self_score": 3,
         "next": "neutral", "last": "5y", "how": ["self"], "evidence_ids": ["ev-own"]},
        {"id": "cv", "label": "Computer vision", "match": ["vision"], "self_score": 0,
         "next": "avoid", "last": "never", "how": [], "evidence_ids": []},
        {"id": "kafka", "label": "Kafka", "match": ["kafka"], "self_score": 2,
         "evidence_ids": ["ev-banned"]},
        {"id": "sql", "label": "SQL", "match": ["\\bsql\\b"], "self_score": 4,
         "evidence_ids": ["ev-other", "ev-missing"]},
        {"id": "figma", "label": "Figma", "match": ["figma"]},
        {"id": "nopattern", "label": "No pattern skill", "self_score": 4},
        {"id": "broken", "label": "Broken pattern", "match": ["(unclosed"], "self_score": 4},
    ],
}

POSTING = """\
---
title: "ignored frontmatter mentioning kafka"
---

# Heading that mentions SQL and is dropped

## Full posting text

## Responsibilities
You will keep the OpenAPI spec current and review Swagger output.
Python scripting helps. We also use Kafka and SQL daily. Figma is a plus.
We offer medical, dental and vision insurance after thirty days.
"""


def make(tmp_path):
    prof = tmp_path / "career-profile.yaml"
    prof.write_text(yaml.safe_dump(PROFILE, sort_keys=False), encoding="utf-8")
    post = tmp_path / "posting.md"
    post.write_text(POSTING, encoding="utf-8")
    return prof, post


def hits_by_id(tmp_path):
    prof, post = make(tmp_path)
    profile = ms.load_profile(prof)
    return {h["skill_id"]: h for h in ms.find_hits(ms.posting_text(str(post)), profile)}


def test_hits_are_bucketed_by_self_score(tmp_path):
    hits = hits_by_id(tmp_path)
    assert hits["openapi"]["bucket"] == "strength (4-5)"
    assert hits["python"]["bucket"] == "solid (3)"
    assert hits["kafka"]["bucket"] == "stretch (2)"
    assert hits["cv"]["bucket"] == "gap (0-1)"
    assert hits["figma"]["bucket"] == "unscored"


def test_evidence_backed_versus_unproven(tmp_path):
    hits = hits_by_id(tmp_path)
    assert hits["openapi"]["status"] == "backed" and not hits["openapi"]["only_unchecked"]
    assert hits["python"]["status"] == "backed" and hits["python"]["only_unchecked"]
    assert hits["cv"]["status"] == "unproven"        # no evidence ids at all
    assert hits["kafka"]["status"] == "unproven"     # only do_not_use evidence
    assert hits["sql"]["status"] == "unproven"       # other-author and unknown ids
    assert hits["figma"]["status"] == "unproven"


def test_false_positive_is_printed_with_its_sentence(tmp_path):
    hits = hits_by_id(tmp_path)
    assert "vision insurance" in hits["cv"]["snippet"]
    prof, post = make(tmp_path)
    out = subprocess.run(
        [sys.executable, str(SCRIPTS / "match_skills.py"), str(post), "--profile", str(prof)],
        capture_output=True, text=True,
    )
    assert out.returncode == 0, out.stderr
    assert "vision insurance" in out.stdout
    assert "Read every hit in its sentence" in out.stdout
    assert "RATHER AVOID hits: Computer vision" in out.stdout
    assert "WANT MORE hits: OpenAPI" in out.stdout
    assert "BACKED (own account, unchecked)" in out.stdout


def test_frontmatter_and_headings_are_not_searched(tmp_path):
    prof, post = make(tmp_path)
    text = ms.posting_text(str(post))
    assert "ignored frontmatter" not in text
    assert "Heading that mentions" not in text


def test_skill_without_pattern_or_with_bad_pattern_does_not_hit(tmp_path):
    hits = hits_by_id(tmp_path)
    assert "nopattern" not in hits and "broken" not in hits


def test_json_output(tmp_path):
    prof, post = make(tmp_path)
    out = subprocess.run(
        [sys.executable, str(SCRIPTS / "match_skills.py"), str(post), "--profile", str(prof), "--json"],
        capture_output=True, text=True,
    )
    assert out.returncode == 0
    data = json.loads(out.stdout)
    ids = {h["skill_id"] for h in data["hits"]}
    assert {"openapi", "python", "cv", "kafka", "sql", "figma"} == ids


def test_missing_profile_exits_1(tmp_path):
    _, post = make(tmp_path)
    out = subprocess.run(
        [sys.executable, str(SCRIPTS / "match_skills.py"), str(post), "--profile", str(tmp_path / "x.yaml")],
        capture_output=True, text=True,
    )
    assert out.returncode == 1
