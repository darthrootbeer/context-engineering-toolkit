"""Tests for scripts/add_entry.py, the one checked door the intake writes through."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "scripts" / "add_entry.py"
GAPPY = ROOT / "fixtures" / "gappy-profile.yaml"
TEMPLATE = ROOT / "intake" / "templates" / "career-profile.template.yaml"
BANNER = "# FICTIONAL EXAMPLE DATA. Not a real person."


def add(profile: Path, section: str, entry: str, *extra):
    proc = subprocess.run([sys.executable, str(SCRIPT), str(profile), "--section", section, "--entry", "-", *extra],
                          input=entry, capture_output=True, text=True)
    return proc.returncode, proc.stdout, proc.stderr


@pytest.fixture
def profile(tmp_path) -> Path:
    path = tmp_path / "career-profile.yaml"
    path.write_text(GAPPY.read_text(encoding="utf-8"), encoding="utf-8")
    return path


GOOD_EVIDENCE = """\
id: ev-placeholder-search
employer_id: placeholder-labs
claim: Added search to the docs site.
dates: {start: 2024-01, end: 2024-02}
authorship: DIRECTED
proof: unchecked
source: {type: interview, ref: "interview:2026-10-01:s2.q7", captured_on: 2026-10-01}
"""


def test_good_entry_is_written_and_validated(profile):
    code, out, _ = add(profile, "evidence", GOOD_EVIDENCE)
    assert code == 0, out
    assert 'added evidence "ev-placeholder-search"' in out
    assert "validate_profile: clean, 0 warning(s)" in out
    data = yaml.safe_load(profile.read_text(encoding="utf-8"))
    assert data["evidence"][-1]["id"] == "ev-placeholder-search"
    assert len(data["evidence"]) == 4


def test_leading_banner_is_kept_on_rewrite(profile):
    assert add(profile, "evidence", GOOD_EVIDENCE)[0] == 0
    assert profile.read_text(encoding="utf-8").splitlines()[0] == BANNER


def test_duplicate_id_is_refused_and_file_untouched(profile):
    before = profile.read_bytes()
    entry = GOOD_EVIDENCE.replace("ev-placeholder-search", "ev-northwind-api-rebuild")
    code, out, err = add(profile, "evidence", entry)
    assert code == 1
    assert '"ev-northwind-api-rebuild" is already in evidence[0]' in out
    assert "not changed" in err
    assert profile.read_bytes() == before


def test_bad_enum_is_refused_and_file_untouched(profile):
    before = profile.read_bytes()
    code, out, _ = add(profile, "evidence", GOOD_EVIDENCE.replace("DIRECTED", "AUTHORED"))
    assert code == 1
    assert out.startswith('entry.authorship: "AUTHORED" is not an allowed value')
    assert profile.read_bytes() == before


@pytest.mark.parametrize("entry,expected", [
    (GOOD_EVIDENCE.replace("proof: unchecked", "proof: checked"),
     "entry.proof: source.type interview cannot carry proof: checked"),
    (GOOD_EVIDENCE.replace("Added search", "Added search, ask robin" + "@" + "example.com,"),
     "entry.claim: holds an email-shaped string"),
    (GOOD_EVIDENCE.replace("authorship: DIRECTED\n", ""),
     'entry: missing required field "authorship".'),
])
def test_entry_level_rules_refuse(profile, entry, expected):
    before = profile.read_bytes()
    code, out, _ = add(profile, "evidence", entry)
    assert code == 1
    assert out.startswith(expected), out
    assert profile.read_bytes() == before


def test_skill_contradiction_refused(profile):
    entry = "id: graphql\nlabel: GraphQL\nself_score: 5\nlast: never\n"
    code, out, _ = add(profile, "skills", entry)
    assert code == 1
    assert out.startswith("entry: self_score 5 with last: never is a contradiction.")


def test_replace_corrects_the_stored_entry_instead_of_keeping_both(profile):
    entry = GOOD_EVIDENCE.replace("ev-placeholder-search", "ev-placeholder-docs-ci")
    code, out, _ = add(profile, "evidence", entry, "--replace")
    assert code == 0, out
    assert 'replaced evidence "ev-placeholder-docs-ci"' in out
    data = yaml.safe_load(profile.read_text(encoding="utf-8"))
    ids = [e["id"] for e in data["evidence"]]
    assert ids.count("ev-placeholder-docs-ci") == 1
    assert data["evidence"][1]["claim"] == "Added search to the docs site."


def test_replace_of_unknown_id_is_refused(profile):
    before = profile.read_bytes()
    code, out, _ = add(profile, "evidence", GOOD_EVIDENCE, "--replace")
    assert code == 1 and "nothing to replace" in out
    assert profile.read_bytes() == before


def test_write_with_dangling_reference_is_written_and_reported(profile):
    entry = ("id: graphql\nlabel: GraphQL\nself_score: 3\nlast: 2y\n"
             "evidence_ids: [ev-not-written-yet]\n")
    code, out, _ = add(profile, "skills", entry)
    assert code == 0
    assert '"ev-not-written-yet" is not an evidence id in this file.' in out
    assert "validate_profile: 1 problem(s)" in out


def test_lane_names_are_the_key_for_lanes(profile):
    entry = "name: docs-platform\ndescription: Again.\nrequirements: []\n"
    code, out, _ = add(profile, "lanes", entry)
    assert code == 1 and '"docs-platform" is already in lanes[0]' in out


def test_mapping_section_merges_keys(profile):
    code, out, _ = add(profile, "meta", "intake: {stages_done: [1, 2], closing_answer: Mostly fair.}")
    assert code == 0, out
    data = yaml.safe_load(profile.read_text(encoding="utf-8"))
    assert data["meta"]["intake"] == {"stages_done": [1, 2], "closing_answer": "Mostly fair."}
    assert str(data["meta"]["updated"]) == "2026-10-01"


def test_mapping_section_bad_value_refused(profile):
    before = profile.read_bytes()
    code, out, _ = add(profile, "person", "working_style: lone_wolf")
    assert code == 1
    assert out.startswith('person.working_style: "lone_wolf" is not an allowed value')
    assert profile.read_bytes() == before


def test_unknown_section_refused(profile):
    code, out, _ = add(profile, "salary_history", "id: x")
    assert code == 1 and "not a section this tool writes" in out


@pytest.mark.parametrize("entry", ["", "- just\n- a list\n", "key: [unclosed\n"])
def test_empty_list_or_bad_yaml_entry_refused(profile, entry):
    before = profile.read_bytes()
    assert add(profile, "evidence", entry)[0] == 1
    assert profile.read_bytes() == before


def test_missing_profile_refused(tmp_path):
    code, out, _ = add(tmp_path / "missing.yaml", "evidence", GOOD_EVIDENCE)
    assert code == 1 and "does not exist" in out


def test_intake_can_build_a_valid_file_from_the_template(tmp_path):
    """Every write goes through add_entry.py, starting from the empty template."""
    path = tmp_path / "career-profile.yaml"
    path.write_text(TEMPLATE.read_text(encoding="utf-8"), encoding="utf-8")
    steps = [
        ("person", "display_name: Robin Sample\ntarget_roles: [Senior Technical Writer]\nyears_experience: 9\n"),
        ("employers", "id: northwind\nname: Northwind Example Co.\ntitle: Technical Writer\nstart: 2017-02\nend: 2021-12\n"),
        ("evidence", GOOD_EVIDENCE.replace("placeholder-labs", "northwind")),
        ("skills", "id: search\nlabel: Docs search\nself_score: 3\nlast: 2y\nevidence_ids: [ev-placeholder-search]\n"),
        ("hard_blocks", "id: gambling\nlabel: Gambling or betting\nwhy: Fictional reason.\n"),
        ("culture", "perks: [{id: offsites, label: Offsites, kind: nice}]\n"),
        ("lanes", "name: tech-writing\ndescription: Writing roles.\n"
                  "requirements: [{id: small_team, label: Small team, severity: soft}]\n"),
        ("meta", "updated: 2026-10-01\nintake: {stages_done: [1, 2, 3, 4, 5, 6]}\n"),
    ]
    out = ""
    for section, entry in steps:
        code, out, _ = add(path, section, entry)
        assert code == 0, (section, out)
    assert "validate_profile: clean, 0 warning(s)" in out
    header = path.read_text(encoding="utf-8").splitlines()[0]
    assert header.startswith("# career-profile.yaml")
