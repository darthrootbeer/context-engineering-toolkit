"""The findings gate: each failure has its own message. Inline data only.

FICTIONAL EXAMPLE DATA. Nothing here is a real person or posting.
"""
import copy
import json
import sys
from pathlib import Path

import pytest
import yaml

SCRIPTS = Path(__file__).resolve().parents[1] / "assessment" / "scripts"
sys.path.insert(0, str(SCRIPTS))

import check_findings as cf  # noqa: E402

POSTING_BODY = (
    "# Senior Writer, Example Co.\n\n"
    "We offer unlimited PTO and a yearly learning budget.\n"
    "You will “own the docs” from first draft to launch.\n"
    "You will partner with product managers and work closely with engineering.\n"
    "Bring 12 years of experience with OpenAPI.\n"
    "We are a rockstar team that works hard.\n"
)
POSTING = "---\nlane: lane-a\n---\n" + POSTING_BODY

PROFILE = {
    "lanes": [{"name": "lane-a", "requirements": [
        {"id": "no_micromanagement", "severity": "strong"},
        {"id": "ai_forward", "severity": "strong"},
    ]}],
    "hard_blocks": [{"id": "gambling"}, {"id": "non_remote"}],
    "named_exceptions": [{"block_id": "non_remote", "company": "Example Co."}],
    "culture": {"perks": [{"id": "unlimited_pto", "kind": "big"}]},
    "skills": [{"id": "openapi"}],
    "evidence": [
        {"id": "ev-good", "proof": "checked", "authorship": "WROTE"},
        {"id": "ev-unchecked", "proof": "unchecked", "authorship": "DIRECTED"},
        {"id": "ev-banned", "proof": "do_not_use", "authorship": "WROTE"},
        {"id": "ev-other", "proof": "checked", "authorship": "OTHER-AUTHOR"},
    ],
}


def good():
    return {
        "lane": "lane-a",
        "hard_block": {"tripped": False, "id": None, "quote": None, "named_exception": None},
        "job_type_override": {"fired": False, "skill": None, "quotes": [], "evidence_checked": []},
        "requirements": [
            {"id": "no_micromanagement", "rating": "strong", "quote": "own the docs", "read": "r"},
            {"id": "ai_forward", "rating": "unknown", "quote": None, "read": "The posting is silent."},
        ],
        "autonomy": {"net": "positive", "quotes": ["own the docs"], "read": "r"},
        "pay": {"stated": False},
        "culture": {
            "perks": [{"perk_id": "unlimited_pto", "quote": "unlimited PTO"}],
            "strong_positive_phrases": [], "low_time_off": None, "hustle": [],
            "soft_flags_tripped": [], "negative_phrases": [],
        },
        "qualifications": {
            "matches": [{"requirement_quote": "12 years of experience with OpenAPI",
                         "evidence_ids": ["ev-good"]}],
            "unproven": [],
        },
        "verdict_reason": "This looks like a solid match, with one thing to confirm about the pay.",
    }


def problems(findings=None, posting=POSTING_BODY, lane="lane-a", profile=PROFILE):
    return cf.check(findings if findings is not None else good(), posting, lane, profile)


def only(findings, fragment):
    out = problems(findings)
    assert len(out) == 1, out
    assert fragment in out[0], out[0]


def mutate(fn):
    f = copy.deepcopy(good())
    fn(f)
    return f


def test_a_clean_file_passes():
    assert problems() == []


def test_curly_quotes_case_and_whitespace_are_normalised():
    f = mutate(lambda f: f["requirements"][0].update(quote='“OWN   the\ndocs”'))
    assert problems(f) == []
    assert cf.normalise("It’s — fine") == "it's - fine"


def test_a_missing_quote_fails():
    only(mutate(lambda f: f["requirements"][0].update(quote="")), "has no quote from the posting")


def test_an_invented_quote_fails():
    only(mutate(lambda f: f["requirements"][0].update(quote="We pay for lunch daily")),
         "was not found in the posting text")


def test_unknown_needs_no_quote():
    assert problems(mutate(lambda f: f["requirements"][1].update(quote=None))) == []


def test_generic_only_autonomy_requirement_quote_fails():
    f = mutate(lambda f: f["requirements"][0].update(
        rating="weak", quote="partner with product managers"))
    only(f, "rests only on generic phrases")


def test_a_real_autonomy_quote_is_not_generic():
    f = mutate(lambda f: f["requirements"][0].update(rating="weak", quote="own the docs"))
    assert problems(f) == []


def test_generic_only_autonomy_block_fails():
    f = mutate(lambda f: f["autonomy"].update(
        net="negative", quotes=["partner with product managers", "work closely with engineering"]))
    only(f, "rests only on generic phrases")


def test_autonomy_with_one_real_quote_among_generic_ones_passes():
    f = mutate(lambda f: f["autonomy"].update(
        net="negative", quotes=["partner with product managers", "own the docs"]))
    assert problems(f) == []


def test_negative_autonomy_with_no_quotes_fails():
    only(mutate(lambda f: f["autonomy"].update(net="negative", quotes=[])),
         "quotes nothing from the posting")


def test_unknown_evidence_id_fails():
    f = mutate(lambda f: f["qualifications"]["matches"][0].update(evidence_ids=["ev-missing"]))
    only(f, '"ev-missing" is not an evidence id')


def test_do_not_use_evidence_fails():
    f = mutate(lambda f: f["qualifications"]["matches"][0].update(evidence_ids=["ev-banned"]))
    only(f, "do_not_use")


def test_other_author_evidence_fails():
    f = mutate(lambda f: f["qualifications"]["matches"][0].update(evidence_ids=["ev-other"]))
    only(f, "someone else wrote")


def test_unchecked_evidence_may_be_cited():
    f = mutate(lambda f: f["qualifications"]["matches"][0].update(evidence_ids=["ev-unchecked"]))
    assert problems(f) == []


def test_a_match_with_no_evidence_fails():
    f = mutate(lambda f: f["qualifications"]["matches"][0].update(evidence_ids=[]))
    only(f, "Write it as unproven instead")


def test_unproven_skill_must_exist():
    f = mutate(lambda f: f["qualifications"].update(
        unproven=[{"skill_id": "nope", "requirement_quote": "OpenAPI"}]))
    only(f, '"nope" is not a skill')


def test_unproven_skill_that_exists_passes():
    f = mutate(lambda f: f["qualifications"].update(
        unproven=[{"skill_id": "openapi", "requirement_quote": "OpenAPI"}]))
    assert problems(f) == []


def test_perk_quote_not_in_posting_fails():
    f = mutate(lambda f: f["culture"]["perks"][0].update(quote="free lunch every day"))
    only(f, "was not found in the posting text")


def test_unknown_perk_id_fails():
    f = mutate(lambda f: f["culture"]["perks"][0].update(perk_id="free_snacks"))
    only(f, '"free_snacks" is not a perk')


def test_hustle_quote_must_be_in_the_posting():
    f = mutate(lambda f: f["culture"].update(hustle=[{"phrase": "rockstar", "quote": "a ninja culture"}]))
    only(f, "was not found")
    ok = mutate(lambda f: f["culture"].update(hustle=[{"phrase": "rockstar", "quote": "rockstar team"}]))
    assert problems(ok) == []


def test_low_time_off_needs_a_quote_from_the_posting():
    f = mutate(lambda f: f["culture"].update(low_time_off={"days": 10, "quote": "ten days off"}))
    only(f, "was not found")
    f = mutate(lambda f: f["culture"].update(low_time_off="accrual only"))
    only(f, "culture.low_time_off: has no quote")


def test_soft_flag_and_negative_phrase_need_quotes():
    f = mutate(lambda f: f["culture"].update(soft_flags_tripped=[{"id": "x", "quote": "layoffs soon"}]))
    only(f, "soft_flags_tripped[0]")
    f = mutate(lambda f: f["culture"].update(negative_phrases=[{"phrase": "p", "quote": ""}]))
    only(f, "negative_phrases[0]")


def test_hard_block_needs_a_known_id_and_a_found_quote():
    f = mutate(lambda f: f["hard_block"].update(tripped=True, id="gambling", quote="casino floor"))
    only(f, "was not found")
    f = mutate(lambda f: f["hard_block"].update(tripped=True, id="made_up", quote="own the docs"))
    only(f, '"made_up" is not a hard block')


def test_named_exception_must_exist_in_the_profile():
    f = mutate(lambda f: f["hard_block"].update(
        tripped=True, id="gambling", quote="own the docs", named_exception="ok"))
    only(f, "no named exception")
    f = mutate(lambda f: f["hard_block"].update(
        tripped=True, id="non_remote", quote="own the docs", named_exception="ok"))
    assert problems(f) == []


def test_override_needs_a_skill_and_found_quotes():
    f = mutate(lambda f: f["job_type_override"].update(fired=True, skill="payments", quotes=[]))
    only(f, "quotes nothing")
    f = mutate(lambda f: f["job_type_override"].update(fired=True, skill=None, quotes=["own the docs"]))
    only(f, "names no skill")
    f = mutate(lambda f: f["job_type_override"].update(fired=True, skill="p", quotes=["payments daily"]))
    only(f, "was not found")


def test_lane_not_in_the_profile_fails():
    f = mutate(lambda f: f.update(lane="lane-z"))
    out = cf.check(f, POSTING_BODY, None, PROFILE)
    assert out == ['lane: "lane-z" is not a lane in the profile.']


def test_lane_that_disagrees_with_the_posting_fails():
    out = cf.check(good(), POSTING_BODY, "lane-b", PROFILE)
    assert any("but the posting says" in line for line in out)


def test_a_posting_with_no_lane_skips_that_comparison():
    assert cf.check(good(), POSTING_BODY, None, PROFILE) == []


def test_rating_outside_the_five_levels_fails():
    only(mutate(lambda f: f["requirements"][0].update(rating="great")), "is not strong, fair, weak, poor or unknown")


def test_requirement_not_in_the_lane_fails():
    only(mutate(lambda f: f["requirements"][0].update(id="made_up")), "is not a requirement in lane")


def test_verdict_reason_missing_or_full_of_rubric_words_fails():
    only(mutate(lambda f: f.pop("verdict_reason")), "verdict_reason: is missing")
    only(mutate(lambda f: f.update(verdict_reason="Job-type override fired.")), "rubric term")
    only(mutate(lambda f: f.update(verdict_reason="Rule 4b decided it.")), "rubric term")


def test_not_an_object_fails():
    assert "not a JSON object" in cf.check([], POSTING_BODY, "lane-a", PROFILE)[0]


def test_split_posting_ignores_frontmatter_and_the_assessment_above_the_heading():
    raw = ("---\nlane: lane-a\n---\n## Assessment\nA hidden phrase here.\n\n"
           "## Full posting text\n\nThe real posting words.\n")
    meta, text = cf.split_posting(raw)
    assert meta["lane"] == "lane-a"
    assert "real posting words" in text
    assert "hidden phrase" not in text


def test_a_quote_from_the_assessment_block_is_not_found_in_the_posting():
    raw = "## Assessment\nA hidden phrase.\n\n## Full posting text\nOnly this.\n"
    _, text = cf.split_posting(raw)
    f = mutate(lambda f: f["requirements"][0].update(quote="a hidden phrase"))
    assert any("not found" in p for p in cf.check(f, text, None, PROFILE))


def test_cli_exit_codes(tmp_path, capsys):
    (tmp_path / "p.md").write_text(POSTING)
    (tmp_path / "prof.yaml").write_text(yaml.safe_dump(PROFILE))
    (tmp_path / "ok.json").write_text(json.dumps(good()))
    bad = good()
    bad["requirements"][0]["quote"] = "invented words"
    (tmp_path / "bad.json").write_text(json.dumps(bad))
    args = ["--posting", str(tmp_path / "p.md"), "--profile", str(tmp_path / "prof.yaml")]
    assert cf.main([str(tmp_path / "ok.json")] + args) == 0
    assert "ok" in capsys.readouterr().out
    assert cf.main([str(tmp_path / "bad.json")] + args) == 1
    assert "was not found in the posting text" in capsys.readouterr().out
    assert cf.main([str(tmp_path / "missing.json")] + args) == 2


# A culture list holding plain strings instead of objects used to end in a Python
# traceback. These pin the clean one-line report and exit code 1.
@pytest.mark.parametrize("key", ["strong_positive_phrases", "hustle",
                                 "negative_phrases", "soft_flags_tripped", "perks"])
def test_a_culture_list_of_strings_is_reported_not_a_crash(key):
    f = mutate(lambda f: f["culture"].update({key: ["a plain string"]}))
    problems = cf.check(f, POSTING_BODY, "lane-a", PROFILE)
    assert any(p.startswith(f"culture.{key}[0]: must be an object") for p in problems)


@pytest.mark.parametrize("mutator", [
    lambda f: f.update(requirements=["no_micromanagement"]),
    lambda f: f.update(culture="great"),
    lambda f: f.update(hard_block="none"),
    lambda f: f["qualifications"].update(matches=["a string"]),
    lambda f: f["qualifications"].update(unproven="a string"),
])
def test_other_wrong_shapes_report_problems_without_crashing(mutator):
    problems = cf.check(mutate(mutator), POSTING_BODY, "lane-a", PROFILE)
    assert problems and all(isinstance(p, str) for p in problems)


def test_cli_wrong_shape_prints_clean_lines_and_exits_1(tmp_path, capsys):
    (tmp_path / "p.md").write_text(POSTING)
    (tmp_path / "prof.yaml").write_text(yaml.safe_dump(PROFILE))
    bad = good()
    bad["culture"]["strong_positive_phrases"] = ["Documentation is part of the definition of done."]
    (tmp_path / "bad.json").write_text(json.dumps(bad))
    args = ["--posting", str(tmp_path / "p.md"), "--profile", str(tmp_path / "prof.yaml")]
    assert cf.main([str(tmp_path / "bad.json")] + args) == 1
    out = capsys.readouterr()
    assert "Traceback" not in out.out + out.err
    assert "culture.strong_positive_phrases[0]: must be an object" in out.out
    assert len(out.out.strip().splitlines()) == 2  # the problem, then the count


def test_unknown_shape_failure_is_one_clean_line_and_exit_1(tmp_path, capsys, monkeypatch):
    (tmp_path / "p.md").write_text(POSTING)
    (tmp_path / "prof.yaml").write_text(yaml.safe_dump(PROFILE))
    (tmp_path / "f.json").write_text(json.dumps(good()))

    def boom(*a, **k):
        raise AttributeError("'str' object has no attribute 'get'")
    monkeypatch.setattr(cf, "check", boom)
    args = ["--posting", str(tmp_path / "p.md"), "--profile", str(tmp_path / "prof.yaml")]
    assert cf.main([str(tmp_path / "f.json")] + args) == 1
    out = capsys.readouterr().out.strip().splitlines()
    assert len(out) == 1 and out[0].startswith("check_findings: the findings file has a shape")
