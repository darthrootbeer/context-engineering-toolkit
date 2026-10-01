"""Tests for the skills catalog, the offline survey page and merge_survey.py.

Everything here uses inline data and temporary files. No network, no browser.
"""
import json
import os
import re
import subprocess
import sys

import pytest
import yaml

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SCRIPT = os.path.join(ROOT, "intake", "scripts", "merge_survey.py")
CATALOG = os.path.join(ROOT, "intake", "templates", "skills-catalog.yaml")
PAGE = os.path.join(ROOT, "intake", "templates", "skills-survey.html")

sys.path.insert(0, os.path.join(ROOT, "intake", "scripts"))
import merge_survey as ms  # noqa: E402


@pytest.fixture(scope="module")
def cat():
    return ms.load_catalog(CATALOG)


def run(*args):
    return subprocess.run([sys.executable, SCRIPT] + [str(a) for a in args], capture_output=True, text=True)


PROFILE = """\
# FICTIONAL EXAMPLE DATA. Not a real person.
schema_version: 1
person:
  display_name: Robin Sample   # keep this comment
employers:
  - {id: northwind, name: Northwind Example Co.}

# Skills come from the survey. Evidence links are added by hand.
skills:
  # one line of guidance that must survive
  - id: python
    label: Python
    group: code
    match: ['\\bpython\\b']
    self_score: 2
    next: neutral
    last: 5y
    how: [self]
    evidence_ids: [ev-one]
    custom_field: keep me
  - id: homegrown-skill
    label: A skill that is not in the catalog
    self_score: 3
    evidence_ids: []

# Everything below must be untouched.
meta:
  updated: 2026-10-01
"""


def write_profile(tmp_path, text=PROFILE):
    p = tmp_path / "career-profile.yaml"
    p.write_text(text, encoding="utf-8")
    return p


def write_survey(tmp_path, items, **extra):
    data = {"format": "skills-survey", "survey_version": 1, "catalog_version": 1, "items": items}
    data.update(extra)
    p = tmp_path / "survey.json"
    p.write_text(json.dumps(data), encoding="utf-8")
    return p


# --------------------------------------------------------------- catalog


def test_catalog_is_about_sixty_items(cat):
    n = sum(len(g["items"]) for g in cat["groups"])
    assert 55 <= n <= 65


def test_catalog_has_no_problems(cat):
    assert ms.catalog_problems(cat) == []


def test_every_group_has_both_anchors(cat):
    for g in cat["groups"]:
        assert g["zero"].strip(), g["id"]
        assert g["five"].strip(), g["id"]
        assert g["zero"] != g["five"], g["id"]


def test_item_ids_are_unique_and_patterns_compile(cat):
    ids = [i["id"] for g in cat["groups"] for i in g["items"]]
    assert len(ids) == len(set(ids))
    for g in cat["groups"]:
        for i in g["items"]:
            assert i["match"], i["id"]
            for pattern in i["match"]:
                re.compile(pattern, re.IGNORECASE)


def test_catalog_problems_catches_the_basics(cat):
    broken = json.loads(json.dumps(cat))
    broken["groups"][0]["zero"] = ""
    broken["groups"][1]["items"][0]["id"] = broken["groups"][0]["items"][0]["id"]
    broken["groups"][2]["items"][0]["match"] = ["(unclosed"]
    problems = "\n".join(ms.catalog_problems(broken))
    assert "zero is missing" in problems
    assert "duplicate item id" in problems
    assert "does not compile" in problems


# ----------------------------------------------------------- survey page


def test_page_matches_catalog(cat):
    assert run("--check-html").returncode == 0


def test_page_embeds_the_same_items_as_the_catalog(cat):
    html = open(PAGE, encoding="utf-8").read()
    start = html.index(ms.MARK_BEGIN) + len(ms.MARK_BEGIN)
    end = html.index(ms.MARK_END)
    embedded = json.loads(html[start:end])
    assert embedded == ms.catalog_for_page(cat)


def test_check_html_fails_on_a_stale_page(tmp_path):
    html = open(PAGE, encoding="utf-8").read()
    stale = tmp_path / "stale.html"
    stale.write_text(html.replace('"Python"', '"Pythons"', 1), encoding="utf-8")
    r = run("--check-html", "--html", stale)
    assert r.returncode == 1
    assert "out of date" in r.stdout
    assert run("--build-html", "--html", stale).returncode == 0
    assert run("--check-html", "--html", stale).returncode == 0


def test_page_needs_no_server_and_no_outside_files():
    html = open(PAGE, encoding="utf-8").read()
    assert "fetch(" not in html
    assert "XMLHttpRequest" not in html
    assert not re.search(r"""(src|href)\s*=\s*["']?(https?:)?//""", html)
    assert not re.search(r"@import|url\(\s*[\"']?https?:", html)
    assert "<script src" not in html
    assert "localStorage" in html and "try" in html  # storage is best effort


def test_page_scale_and_answers_match_the_merge_script():
    html = open(PAGE, encoding="utf-8").read()
    for value in ms.NEXT_VALUES + ms.LAST_VALUES + ms.HOW_VALUES:
        assert '"%s"' % value in html, value
    assert 'format: "skills-survey"' in html


# ----------------------------------------------------------------- merge


def test_merge_adds_new_skills_with_catalog_fields(tmp_path, cat):
    profile = write_profile(tmp_path)
    survey = write_survey(tmp_path, {"sql": {"score": 3, "next": "more", "last": "2y", "how": ["ai", "self"]}})
    r = run(profile, survey)
    assert r.returncode == 0, r.stdout + r.stderr
    data = yaml.safe_load(profile.read_text())
    sql = next(s for s in data["skills"] if s["id"] == "sql")
    item, group = ms.catalog_index(cat)["sql"]
    assert sql == {
        "id": "sql",
        "label": item["label"],
        "group": group,
        "match": item["match"],
        "self_score": 3,
        "next": "more",
        "last": "2y",
        "how": ["self", "ai"],
        "evidence_ids": [],
    }
    assert "1 skills added, 0 updated" in r.stdout


def test_merge_keeps_evidence_links_and_extra_fields(tmp_path):
    profile = write_profile(tmp_path)
    survey = write_survey(tmp_path, {"python": {"score": 4, "next": "more", "last": "2y", "how": ["self", "ai"]}})
    assert run(profile, survey).returncode == 0
    data = yaml.safe_load(profile.read_text())
    py = next(s for s in data["skills"] if s["id"] == "python")
    assert py["evidence_ids"] == ["ev-one"]
    assert py["custom_field"] == "keep me"
    assert py["self_score"] == 4 and py["last"] == "2y" and py["how"] == ["self", "ai"]


def test_merge_never_touches_evidence_or_other_sections(tmp_path):
    profile = write_profile(tmp_path)
    before = yaml.safe_load(profile.read_text())
    survey = write_survey(tmp_path, {"git": {"score": 1}, "python": {"score": 5, "last": "2y"}})
    assert run(profile, survey).returncode == 0
    after = yaml.safe_load(profile.read_text())
    for key in before:
        if key != "skills":
            assert after[key] == before[key]
    assert "evidence" not in after


def test_merge_leaves_skills_not_in_the_survey_alone(tmp_path):
    profile = write_profile(tmp_path)
    survey = write_survey(tmp_path, {"git": {"score": 2}})
    assert run(profile, survey).returncode == 0
    data = yaml.safe_load(profile.read_text())
    home = next(s for s in data["skills"] if s["id"] == "homegrown-skill")
    assert home == {"id": "homegrown-skill", "label": "A skill that is not in the catalog", "self_score": 3, "evidence_ids": []}


def test_blank_items_are_skipped_not_zero(tmp_path):
    profile = write_profile(tmp_path)
    survey = write_survey(tmp_path, {"sql": {"note": "no score given"}, "git": {"score": 0}})
    r = run(profile, survey)
    assert r.returncode == 0
    data = yaml.safe_load(profile.read_text())
    ids = [s["id"] for s in data["skills"]]
    assert "sql" not in ids
    git = next(s for s in data["skills"] if s["id"] == "git")
    assert git["self_score"] == 0
    assert "1 answered, 1 skipped as blank" in r.stdout


def test_comments_and_other_lines_survive_byte_for_byte(tmp_path):
    profile = write_profile(tmp_path)
    survey = write_survey(tmp_path, {"sql": {"score": 2}})
    assert run(profile, survey).returncode == 0
    new = profile.read_text()
    old_lines = PROFILE.splitlines()
    skills_at = old_lines.index("skills:")
    meta_at = old_lines.index("# Everything below must be untouched.")
    assert new.splitlines()[:skills_at] == old_lines[:skills_at]
    assert new.splitlines()[-(len(old_lines) - meta_at):] == old_lines[meta_at:]
    assert "# one line of guidance that must survive" in new
    assert "# keep this comment" in new


def test_merge_is_idempotent(tmp_path):
    profile = write_profile(tmp_path)
    survey = write_survey(tmp_path, {"sql": {"score": 3, "last": "5y"}, "git": {"score": 4, "last": "2y", "how": ["team"]}})
    assert run(profile, survey).returncode == 0
    first = profile.read_text()
    r = run(profile, survey)
    assert r.returncode == 0
    assert profile.read_text() == first
    assert "0 skills added, 2 updated" in r.stdout


def test_rerun_with_changed_answer_updates_in_place(tmp_path):
    profile = write_profile(tmp_path)
    assert run(profile, write_survey(tmp_path, {"sql": {"score": 3, "last": "5y"}})).returncode == 0
    assert run(profile, write_survey(tmp_path, {"sql": {"score": 1}})).returncode == 0
    data = yaml.safe_load(profile.read_text())
    sql = [s for s in data["skills"] if s["id"] == "sql"]
    assert len(sql) == 1
    assert sql[0]["self_score"] == 1 and "last" not in sql[0]


@pytest.mark.parametrize(
    "items, message",
    [
        ({"not-a-real-item": {"score": 3}}, "not an item in the catalog"),
        ({"sql": {"score": 6}}, "0 to 5"),
        ({"sql": {"score": "3"}}, "0 to 5"),
        ({"sql": {"score": True}}, "0 to 5"),
        ({"sql": {"score": 3, "next": "maybe"}}, "items.sql.next"),
        ({"sql": {"score": 3, "last": "yesterday"}}, "items.sql.last"),
        ({"sql": {"score": 3, "how": ["magic"]}}, "items.sql.how"),
        ({"sql": {"score": 5, "last": "never"}}, "does not fit"),
        ({"sql": {"score": 4, "last": "never"}}, "does not fit"),
    ],
)
def test_bad_answers_are_refused_and_nothing_is_written(tmp_path, items, message):
    profile = write_profile(tmp_path)
    survey = write_survey(tmp_path, dict(items, git={"score": 2}))
    r = run(profile, survey)
    assert r.returncode == 1
    assert message in r.stdout
    assert "nothing written" in r.stdout
    assert profile.read_text() == PROFILE


def test_low_score_with_never_is_allowed(tmp_path):
    profile = write_profile(tmp_path)
    survey = write_survey(tmp_path, {"sql": {"score": 1, "last": "never"}})
    assert run(profile, survey).returncode == 0


def test_notes_are_counted_but_not_stored(tmp_path):
    profile = write_profile(tmp_path)
    survey = write_survey(tmp_path, {"sql": {"score": 3, "note": "used it at my last job"}})
    r = run(profile, survey)
    assert r.returncode == 0
    assert "1 survey note(s) not stored" in r.stdout
    assert "last job" not in profile.read_text()


def test_dry_run_and_out(tmp_path):
    profile = write_profile(tmp_path)
    survey = write_survey(tmp_path, {"sql": {"score": 3}})
    r = run(profile, survey, "--dry-run")
    assert r.returncode == 0 and "dry run" in r.stdout
    assert profile.read_text() == PROFILE
    out = tmp_path / "merged.yaml"
    assert run(profile, survey, "--out", out).returncode == 0
    assert profile.read_text() == PROFILE
    assert any(s["id"] == "sql" for s in yaml.safe_load(out.read_text())["skills"])


def test_profile_with_empty_inline_skills_and_with_no_skills_key(tmp_path):
    survey = write_survey(tmp_path, {"sql": {"score": 2}})
    for text in ("person:\n  display_name: Robin Sample\nskills: []\nmeta:\n  updated: 2026-10-01\n",
                 "person:\n  display_name: Robin Sample\n"):
        profile = write_profile(tmp_path, text)
        assert run(profile, survey).returncode == 0
        data = yaml.safe_load(profile.read_text())
        assert [s["id"] for s in data["skills"]] == ["sql"]
        assert data["person"] == {"display_name": "Robin Sample"}


def test_exit_2_when_files_cannot_be_read(tmp_path):
    survey = write_survey(tmp_path, {"sql": {"score": 2}})
    assert run(tmp_path / "missing.yaml", survey).returncode == 2
    profile = write_profile(tmp_path)
    assert run(profile, tmp_path / "missing.json").returncode == 2
    other = tmp_path / "other.json"
    other.write_text(json.dumps({"format": "something-else", "items": {}}))
    r = run(profile, other)
    assert r.returncode == 2 and "not a skills-survey file" in r.stderr


def test_page_export_shape_is_accepted_by_the_merge(tmp_path):
    """The shape the page writes (see exportData in the page) merges cleanly."""
    profile = write_profile(tmp_path)
    survey = write_survey(
        tmp_path,
        {"api-specs": {"score": 3, "next": "more", "last": "2y", "how": ["self"], "note": ""}},
        saved="2026-10-01T12:00:00.000Z",
        group_notes={"web": "a group note"},
    )
    assert run(profile, survey).returncode == 0


def test_special_characters_round_trip(tmp_path, cat):
    """Patterns with quotes, colons and backslashes survive the hand-written YAML."""
    awkward = json.loads(json.dumps(cat))
    awkward["groups"][0]["items"][0]["match"] = ["it's: here", "\\bword\\b", "# not a comment", "yes", "123"]
    item_id = awkward["groups"][0]["items"][0]["id"]
    merged, added, _ = ms.merge_skills([], awkward, {item_id: {"self_score": 2}})
    text = ms.replace_skills_block("a: 1\n", merged)
    assert yaml.safe_load(text)["skills"] == merged
    assert added == [item_id]
