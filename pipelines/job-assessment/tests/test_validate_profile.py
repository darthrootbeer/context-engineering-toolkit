"""Tests for scripts/validate_profile.py and the two schema files.

All data here is fictional. Email and phone shapes are built at run time so this
file itself never holds one (the repo safety scan would rightly flag it).
"""
from __future__ import annotations

import copy
import json
import subprocess
import sys
from pathlib import Path

import pytest
import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"
FIXTURES = ROOT / "fixtures"
SCHEMA_DIR = ROOT / "schema"
TEMPLATE = ROOT / "intake" / "templates" / "career-profile.template.yaml"
ROBIN = FIXTURES / "robin-sample" / "career-profile.yaml"
BANNER = "# FICTIONAL EXAMPLE DATA. Not a real person."

sys.path.insert(0, str(SCRIPTS))
import validate_profile as vp  # noqa: E402

# The five planted mistakes in fixtures/broken-profile.yaml, one per rule family.
BROKEN_EXPECTED = [
    # rule 1, schema: an authorship value that is not in the enum
    'evidence[2].authorship: "AUTHORED" is not an allowed value '
    "(allowed: WROTE, DIRECTED, CO-WROTE, DESIGNED, REVIEWED, OTHER-AUTHOR).",
    # rule 2, references: a skill points at an evidence id that does not exist
    'skills[1].evidence_ids: "ev-placeholder-style-guide" is not an evidence id in this file.',
    # rule 4, pay order: min is above open_ask
    "comp: pay numbers out of order: min (98000) is above open_ask (85000). "
    "Expected floor <= min <= open_ask <= target <= stretch_ceiling.",
    # rule 5, proof: an interview answer marked as checked
    "evidence[1].proof: source.type interview cannot carry proof: checked. Nothing was read to back it; "
    "use unchecked, or point source at a document, link or artifact.",
    # rule 7, contradiction: self_score 5 with last: never
    "skills[2]: self_score 5 with last: never is a contradiction. "
    "A score of 4 or 5 needs some real use; lower the score or fix last.",
]

# The three planted judgment gaps in fixtures/gappy-profile.yaml. The validator
# cannot see them; a careful reader (or prompt P5) has to.
GAPPY_PLANTED_GAPS = {
    "unchecked_evidence_carries_top_skill":
        "skills[1] (docs_ci) is scored 5 and rests only on evidence[1], an unchecked interview answer.",
    "copied_lane":
        "lanes[1] (tech-writing) has the same requirements, autonomy and keyword signals as lanes[0] "
        "(docs-platform), including a build-ownership must-have that does not fit a writing lane.",
    "hard_block_without_reason":
        "hard_blocks[1] (weapons) has no why.",
}


def run_cli(*args):
    proc = subprocess.run([sys.executable, str(SCRIPTS / "validate_profile.py"), *map(str, args)],
                          capture_output=True, text=True)
    return proc.returncode, proc.stdout, proc.stderr


def load(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


@pytest.fixture
def base() -> dict:
    """A known-good profile (the gappy fixture is valid with no warnings)."""
    return load(FIXTURES / "gappy-profile.yaml")


def errors_of(data, **kw):
    errors, _ = vp.validate(data, **kw)
    return [str(e) for e in errors]


def warnings_of(data):
    _, warnings = vp.validate(data)
    return [str(w) for w in warnings]


# ---------------------------------------------------------------- the fixtures


def test_broken_fixture_prints_exactly_the_five_planted_problems():
    code, out, err = run_cli(FIXTURES / "broken-profile.yaml")
    assert code == 1
    lines = out.splitlines()
    assert len(lines) == 5, out
    assert sorted(lines) == sorted(BROKEN_EXPECTED)
    assert "5 problem(s), 0 warning(s)" in err


def test_broken_fixture_same_five_with_fixture_flag():
    code, out, _ = run_cli("--fixture", FIXTURES / "broken-profile.yaml")
    assert code == 1
    assert sorted(out.splitlines()) == sorted(BROKEN_EXPECTED)


def test_gappy_fixture_passes_clean_with_no_warnings():
    code, out, err = run_cli("--fixture", FIXTURES / "gappy-profile.yaml")
    assert code == 0
    assert out == ""
    assert "clean, 0 warning(s)" in err


def test_gappy_fixture_really_holds_the_planted_gaps():
    data = load(FIXTURES / "gappy-profile.yaml")
    skill = data["skills"][1]
    assert skill["id"] == "docs_ci" and skill["self_score"] == 5
    backing = [e for e in data["evidence"] if e["id"] in skill["evidence_ids"]]
    assert backing and all(e["proof"] == "unchecked" and e["source"]["type"] == "interview" for e in backing)

    a, b = data["lanes"]
    for key in ("requirements", "autonomy", "keyword_signals"):
        assert a[key] == b[key]

    assert data["hard_blocks"][1]["id"] == "weapons" and "why" not in data["hard_blocks"][1]
    assert len(GAPPY_PLANTED_GAPS) == 3


@pytest.mark.skipif(not ROBIN.exists(), reason="Robin's fixture arrives in a separate package")
def test_robin_sample_passes_with_fixture_flag():
    code, out, _ = run_cli("--fixture", ROBIN)
    assert code == 0, out


# ---------------------------------------------------------------- the template


def fill_template_with_robins_ids(data: dict) -> dict:
    data = copy.deepcopy(data)
    data["person"].update(display_name="Robin Sample", target_roles=["Senior Technical Writer"],
                          years_experience=9, location_label="Region B",
                          working_style="gather_from_experts")
    data["comp"].update(floor=75000, min=80000, open_ask=85000, target=100000, stretch_ceiling=175000)
    data["culture"]["perks"] = [{"id": "unlimited_pto", "label": "Unlimited PTO", "kind": "big"}]
    data["culture"]["low_time_off_days"] = 15
    data["hard_blocks"] = [{"id": "gambling", "label": "Gambling or betting", "why": "Fictional reason."}]
    data["lanes"] = [
        {"name": "docs-platform", "emoji": "🔧", "description": "Roles building docs systems.",
         "requirements": [{"id": "ai_forward", "label": "AI-forward team", "severity": "strong",
                           "why": "Fictional reason."}]},
        {"name": "tech-writing", "emoji": "✍️", "description": "Roles writing technical content.",
         "requirements": [{"id": "small_team", "label": "Small team", "severity": "soft"}]},
    ]
    data["employers"] = [
        {"id": "northwind", "name": "Northwind Example Co.", "title": "Technical Writer",
         "start": "2017-02", "end": "2021-12"},
        {"id": "placeholder-labs", "name": "Placeholder Labs", "title": "Senior Technical Writer",
         "start": "2022-01", "end": "present"},
    ]
    data["evidence"] = [{
        "id": "ev-northwind-api-rebuild", "employer_id": "northwind",
        "claim": "Moved the API reference to pages generated from the API spec.",
        "dates": {"start": "2021-03", "end": "2021-09"},
        "authorship": "DIRECTED", "proof": "checked",
        "source": {"type": "link", "ref": "https://example.com/fictional/api-rebuild",
                   "captured_on": "2026-10-01"},
    }]
    data["skills"] = [{"id": "openapi", "label": "OpenAPI / Swagger", "group": "api",
                       "match": ["openapi|swagger"], "self_score": 4, "next": "more", "last": "2y",
                       "how": ["self", "ai"], "evidence_ids": ["ev-northwind-api-rebuild"]}]
    data["meta"]["updated"] = "2026-10-01"
    data["meta"]["intake"]["stages_done"] = [1, 2, 3, 4, 5, 6]
    return data


def test_template_parses_and_lists_every_schema_section():
    data = load(TEMPLATE)
    schema = vp.load_schema()
    assert set(data) == set(schema["properties"])


def test_empty_template_needs_filling_but_runs():
    errors = errors_of(load(TEMPLATE))
    assert errors, "an empty template should not pass"
    assert all(e.startswith("person.") for e in errors), errors


def test_template_validates_once_filled_with_robins_ids(tmp_path):
    filled = fill_template_with_robins_ids(load(TEMPLATE))
    path = tmp_path / "career-profile.yaml"
    path.write_text(yaml.safe_dump(filled, sort_keys=False, allow_unicode=True), encoding="utf-8")
    code, out, _ = run_cli(path)
    assert code == 0, out
    assert out == ""


# ---------------------------------------------------------------- rule by rule


def test_unknown_field_is_a_schema_error(base):
    base["person"]["contact"] = "anything"
    assert errors_of(base) == ['person: unknown field "contact". The schema has no such field.']


def test_missing_required_field(base):
    del base["evidence"][0]["source"]
    assert errors_of(base) == ['evidence[0]: missing required field "source".']


def test_self_score_range_and_type(base):
    base["skills"][0]["self_score"] = 6
    assert errors_of(base) == ["skills[0].self_score: 6 should be at most 5."]


@pytest.mark.parametrize("section,index,field,value,expected", [
    ("evidence", 0, "employer_id", "nowhere",
     'evidence[0].employer_id: "nowhere" is not an employer id in this file.'),
    ("writing_samples", 0, "evidence_id", "ev-nothing",
     'writing_samples[0].evidence_id: "ev-nothing" is not an evidence id in this file.'),
    ("named_exceptions", 0, "block_id", "no_such_block",
     'named_exceptions[0].block_id: "no_such_block" is not a hard block id in this file.'),
])
def test_references_resolve(base, section, index, field, value, expected):
    base[section][index][field] = value
    assert errors_of(base) == [expected]


def test_known_gap_skill_reference(base):
    base["lanes"][0]["known_gaps"][0]["skill_id"] = "no_skill"
    assert errors_of(base) == ['lanes[0].known_gaps[0].skill_id: "no_skill" is not a skill id in this file.']


def test_personal_project_evidence_may_have_null_employer(base):
    base["evidence"][0]["employer_id"] = None
    assert errors_of(base) == []


def test_duplicate_ids_and_lane_names(base):
    base["evidence"].append(copy.deepcopy(base["evidence"][0]))
    base["lanes"][1]["name"] = "docs-platform"
    errors = errors_of(base)
    assert 'evidence[3].id: "ev-northwind-api-rebuild" is already used by evidence[0].' in errors
    assert 'lanes[1].name: "docs-platform" is already used by lanes[0].' in errors
    assert len(errors) == 2


def test_pay_order_skips_missing_numbers(base):
    base["comp"]["open_ask"] = None
    base["comp"]["target"] = None
    assert errors_of(base) == []
    base["comp"]["stretch_ceiling"] = 78000
    assert errors_of(base) == [
        "comp: pay numbers out of order: min (80000) is above stretch_ceiling (78000). "
        "Expected floor <= min <= open_ask <= target <= stretch_ceiling."]


def test_reference_source_cannot_be_checked(base):
    base["evidence"][0]["source"] = {"type": "reference", "ref": "former manager at Northwind"}
    errors = errors_of(base)
    assert len(errors) == 1 and errors[0].startswith("evidence[0].proof: source.type reference cannot carry")


@pytest.mark.parametrize("where", ["person.display_name", "evidence.details", "nested"])
def test_email_shape_is_caught_without_echoing_it(base, where):
    shape = "robin" + "@" + "example" + ".com"
    if where == "person.display_name":
        base["person"]["display_name"] = f"Robin {shape}"
        path = "person.display_name"
    elif where == "evidence.details":
        base["evidence"][1]["details"] = f"Ask {shape} for the logs."
        path = "evidence[1].details"
    else:
        base["lanes"][0]["autonomy"]["positive_signals"].append(shape)
        path = "lanes[0].autonomy.positive_signals[2]"
    errors = errors_of(base)
    assert errors == [f"{path}: holds an email-shaped string. Contact details do not belong in this file."]
    assert shape not in errors[0]


def test_phone_shape_is_caught(base):
    digits = "555" + "-" + "010" + "-" + "4477"
    base["employers"][0]["summary"] = f"Call {digits} for a reference."
    assert errors_of(base) == [
        "employers[0].summary: holds a phone-shaped string. Contact details do not belong in this file."]


def test_dates_and_months_are_not_phone_shaped(base):
    assert errors_of(base) == []


def test_high_score_with_last_never(base):
    base["skills"][0]["last"] = "never"
    errors = errors_of(base)
    assert errors == ["skills[0]: self_score 4 with last: never is a contradiction. "
                      "A score of 4 or 5 needs some real use; lower the score or fix last."]
    base["skills"][0]["self_score"] = 3
    assert errors_of(base) == []


def test_fixture_mode_needs_banner_and_example_urls(base, tmp_path):
    base["evidence"][0]["source"]["ref"] = "https://real-site.test/page"
    path = tmp_path / "p.yaml"
    path.write_text(yaml.safe_dump(base, sort_keys=False, allow_unicode=True), encoding="utf-8")
    code, out, _ = run_cli("--fixture", path)
    assert code == 1
    assert out.splitlines() == [
        f"line 1: first line must be the banner '{BANNER}'.",
        "evidence[0].source.ref: URL is not on example.com, example.org or example.net.",
    ]
    code, out, _ = run_cli(path)
    assert code == 0 and out == ""


def test_example_subdomains_are_allowed_in_fixture_mode(base):
    base["evidence"][0]["source"]["ref"] = "https://docs.example.org/fictional"
    raw = BANNER + "\n" + yaml.safe_dump(base, allow_unicode=True)
    assert errors_of(base, raw_text=raw, fixture=True) == []


# ---------------------------------------------------------------- warnings


def test_each_warning_kind(base):
    base["skills"][0]["evidence_ids"] = []
    del base["evidence"][2]["dates"]
    del base["lanes"][0]["requirements"][0]["why"]
    base["culture"]["perks"] = []
    base["lanes"][1]["requirements"] = []
    errors, warnings = vp.validate(base)
    assert errors == []
    rules = sorted(w.rule for w in warnings)
    assert rules == ["empty-lane", "no-dates", "no-perks", "no-why", "unproven"]


def test_warnings_do_not_change_exit_code(base, tmp_path):
    base["skills"][0]["evidence_ids"] = []
    path = tmp_path / "p.yaml"
    path.write_text(yaml.safe_dump(base, sort_keys=False, allow_unicode=True), encoding="utf-8")
    code, out, _ = run_cli(path)
    assert code == 0
    assert out.startswith("warning: skills[0]:")


# ---------------------------------------------------------------- CLI behavior


def test_json_output():
    code, out, _ = run_cli("--json", FIXTURES / "broken-profile.yaml")
    assert code == 1
    result = json.loads(out)
    assert result["ok"] is False
    assert len(result["errors"]) == 5
    assert {e["rule"] for e in result["errors"]} == {"schema", "reference", "pay-order", "proof", "self-score"}


def test_missing_file_exits_2(tmp_path):
    code, _, err = run_cli(tmp_path / "nope.yaml")
    assert code == 2 and "could not run" in err


def test_not_yaml_exits_2(tmp_path):
    path = tmp_path / "bad.yaml"
    path.write_text("person: [unclosed\n", encoding="utf-8")
    code, _, err = run_cli(path)
    assert code == 2


def test_top_level_list_exits_2(tmp_path):
    path = tmp_path / "list.yaml"
    path.write_text("- a\n- b\n", encoding="utf-8")
    assert run_cli(path)[0] == 2


# ---------------------------------------------------------------- the schemas


@pytest.mark.parametrize("name", ["career-profile.schema.json", "findings.schema.json"])
def test_schemas_are_valid_json_schema(name):
    Draft202012Validator.check_schema(json.loads((SCHEMA_DIR / name).read_text(encoding="utf-8")))


def sample_findings() -> dict:
    """The section 3.4 example, with its placeholders filled."""
    return {
        "_banner": "FICTIONAL EXAMPLE DATA. Not a real person.",
        "posting_file": "fixtures/postings/03-unlisted-pay-perks.md",
        "lane": "tech-writing",
        "hard_block": {"tripped": False, "id": None, "quote": None, "named_exception": None},
        "job_type_override": {"fired": False, "skill": None, "quotes": [], "evidence_checked": []},
        "requirements": [{"id": "ai_forward", "rating": "strong", "quote": "we write with AI tools",
                          "read": "The team already works this way."}],
        "autonomy": {"net": "negative", "quotes": ["tickets are assigned daily"], "read": "Little room to plan."},
        "pay": {"stated": False, "tiers": [], "tier_used": None, "top": None, "other_pay_noted": []},
        "culture": {
            "perks": [{"perk_id": "unlimited_pto", "quote": "unlimited paid time off"}],
            "strong_positive_phrases": [],
            "low_time_off": None,
            "hustle": [],
            "soft_flags_tripped": [],
            "negative_phrases": [],
        },
        "qualifications": {
            "years_required": 12, "narrow_subdomain": False,
            "known_gaps_hit": [], "self_score_gaps": [],
            "working_style_mismatch": False,
            "matches": [{"requirement_quote": "experience with OpenAPI",
                         "evidence_ids": ["ev-northwind-api-rebuild"]}],
            "unproven": [{"skill_id": "graphql", "requirement_quote": "GraphQL a plus"}],
        },
        "avoid_core_skills": [],
        "company_read": {"status": "none", "name": "Fictional Hiring Co.", "stored_reason": None},
        "verdict_reason": "Good work, but the pay is not listed and it wants more years than Robin has.",
        "keyword_signals_found": [{"phrase": "docs as code", "read": "Matches how Robin works."}],
        "new_signals_to_consider": [],
    }


def findings_validator():
    return Draft202012Validator(json.loads((SCHEMA_DIR / "findings.schema.json").read_text(encoding="utf-8")))


def test_findings_example_from_the_design_validates():
    assert list(findings_validator().iter_errors(sample_findings())) == []


@pytest.mark.parametrize("mutate", [
    lambda f: f["requirements"][0].update(rating="excellent"),
    lambda f: f["qualifications"]["matches"][0].update(evidence_ids=[]),
    lambda f: f["qualifications"].update(strengths=["free text is not allowed"]),
    lambda f: f.pop("verdict_reason"),
    lambda f: f["company_read"].update(status="favourite"),
])
def test_findings_schema_rejects_bad_output(mutate):
    f = sample_findings()
    mutate(f)
    assert list(findings_validator().iter_errors(f))
