"""Every row of the scoring table, with inline data only.

FICTIONAL EXAMPLE DATA. Nothing here is a real person or posting.
"""
import json
import sys
from pathlib import Path

import pytest
import yaml

SCRIPTS = Path(__file__).resolve().parents[1] / "assessment" / "scripts"
sys.path.insert(0, str(SCRIPTS))

import score_helpers as sh  # noqa: E402


def make_profile(**over):
    profile = {
        "person": {"display_name": "Robin Sample", "years_experience": 9,
                   "location_label": "Region B"},
        "comp": {"floor": 90000, "min": 110000, "open_ask": 125000,
                 "target": 140000, "stretch_ceiling": 170000},
        "culture": {
            "perks": [
                {"id": "unlimited_pto", "kind": "big"},
                {"id": "learning_budget", "kind": "big"},
                {"id": "extra_days_off", "kind": "big"},
                {"id": "offsites", "kind": "nice"},
                {"id": "home_office", "kind": "nice"},
                {"id": "parental_leave", "kind": "nice"},
            ],
            "low_time_off_days": 15,
            "hustle_phrases": ["rockstar"],
            "free_phrases": ["fast-paced"],
        },
        "lanes": [{
            "name": "lane-a",
            "requirements": [
                {"id": "strong_one", "label": "Strong one", "severity": "strong"},
                {"id": "strong_two", "label": "Strong two", "severity": "strong"},
                {"id": "soft_one", "label": "Soft one", "severity": "soft"},
                {"id": "bonus_one", "label": "Bonus one", "severity": "soft", "bonus": True},
            ],
            "known_gaps": [
                {"id": "gap_a", "label": "Gap A", "skill_id": "skill_a"},
                {"id": "gap_b", "label": "Gap B"},
                {"id": "gap_c", "label": "Gap C"},
                {"id": "gap_d", "label": "Gap D"},
                {"id": "gap_e", "label": "Gap E"},
            ],
        }],
    }
    profile.update(over)
    return profile


def make_findings(**over):
    """A findings file that rates everything Strong, silent on culture."""
    findings = {
        "lane": "lane-a",
        "requirements": [
            {"id": "strong_one", "rating": "strong", "quote": "q"},
            {"id": "strong_two", "rating": "strong", "quote": "q"},
            {"id": "soft_one", "rating": "strong", "quote": "q"},
            {"id": "bonus_one", "rating": "strong", "quote": "q"},
        ],
        "autonomy": {"net": "positive"},
        "pay": {"stated": False},
        "culture": {},
        "qualifications": {},
        "avoid_core_skills": [],
    }
    findings.update(over)
    return findings


def with_ratings(**ratings):
    items = [{"id": k, "rating": v, "quote": "q"} for k, v in ratings.items()]
    return make_findings(requirements=items)


P = make_profile()


# ------------------------------------------------------------ round_half_up

@pytest.mark.parametrize("value,expected", [
    (8.5, 9), (6.5, 7), (0.5, 1), (7.49, 7), (7.0, 7), (9.5, 10), (0, 0), (2.5, 3),
])
def test_round_half_up(value, expected):
    assert sh.round_half_up(value) == expected


def test_round_half_up_is_not_bankers_rounding():
    assert round(2.5) == 2  # Python's default goes to even
    assert sh.round_half_up(2.5) == 3


# ---------------------------------------------------------------- Fit

def test_fit_all_clean_is_ten():
    assert sh.fit_score(make_findings(), P) == 10


@pytest.mark.parametrize("rating,expected", [
    ("strong", 10), ("fair", 10), ("weak", 9), ("poor", 7), ("unknown", 9),
])
def test_fit_strong_requirement_costs(rating, expected):
    # Costs are 0, 0, 1.5, 3, 1.5. 10 - 1.5 = 8.5 rounds half up to 9.
    f = with_ratings(strong_one=rating, strong_two="strong", soft_one="strong")
    assert sh.fit_score(f, P) == expected


@pytest.mark.parametrize("rating,expected", [
    ("strong", 10), ("fair", 10), ("weak", 9), ("poor", 9), ("unknown", 10),
])
def test_fit_soft_requirement_costs(rating, expected):
    f = with_ratings(strong_one="strong", strong_two="strong", soft_one=rating)
    assert sh.fit_score(f, P) == expected


@pytest.mark.parametrize("rating", ["strong", "fair", "weak", "poor", "unknown"])
def test_fit_bonus_items_never_subtract(rating):
    f = with_ratings(strong_one="strong", strong_two="strong", soft_one="strong", bonus_one=rating)
    assert sh.fit_score(f, P) == 10


def test_fit_silent_strong_requirement_costs_one_and_a_half():
    # The findings never mention strong_two, so it is silence, so Unknown.
    f = with_ratings(strong_one="strong", soft_one="strong", bonus_one="strong")
    assert sh.fit_score(f, P) == 9  # 8.5 rounds up


def test_fit_silent_soft_requirement_costs_nothing():
    f = with_ratings(strong_one="strong", strong_two="strong")
    assert sh.fit_score(f, P) == 10


def test_fit_autonomy_net_negative_costs_two():
    assert sh.fit_score(make_findings(autonomy={"net": "negative"}), P) == 8


@pytest.mark.parametrize("net", ["positive", "mixed", "unknown", None])
def test_fit_other_autonomy_costs_nothing(net):
    assert sh.fit_score(make_findings(autonomy={"net": net}), P) == 10


@pytest.mark.parametrize("avoid,expected", [([], 10), (["a"], 9), (["a", "b"], 8), (["a", "b", "c"], 8)])
def test_fit_rather_avoid_costs_one_each_max_two(avoid, expected):
    assert sh.fit_score(make_findings(avoid_core_skills=avoid), P) == expected


def test_fit_floors_at_zero():
    profile = make_profile()
    profile["lanes"][0]["requirements"].append({"id": "strong_three", "severity": "strong"})
    f = with_ratings(strong_one="poor", strong_two="poor", strong_three="poor", soft_one="poor")
    f["autonomy"] = {"net": "negative"}
    assert sh.fit_score(f, profile) == 0  # 10 - 9 - 1 - 2 is below zero


def test_fit_unknown_requirement_id_is_an_error():
    f = with_ratings(not_a_requirement="strong")
    with pytest.raises(ValueError):
        sh.fit_score(f, P)


def test_fit_unknown_lane_is_an_error():
    with pytest.raises(ValueError):
        sh.fit_score(make_findings(lane="nope"), P)


def test_fit_rating_is_case_insensitive():
    f = with_ratings(strong_one="Weak", strong_two="Strong", soft_one="Strong")
    assert sh.fit_score(f, P) == 9


# ---------------------------------------------------------------- Comp

def pay(top=None, tiers=None, stated=True):
    p = {"stated": stated}
    if top is not None:
        p["top"] = top
    if tiers is not None:
        p["tiers"] = tiers
    return make_findings(pay=p)


def test_comp_unlisted_pay_is_a_neutral_five_not_zero():
    assert sh.comp_score(make_findings(pay={"stated": False}), P) == 5


def test_comp_missing_pay_block_is_unlisted():
    f = make_findings()
    del f["pay"]
    assert sh.comp_score(f, P) == 5


@pytest.mark.parametrize("top,expected", [
    (170000, 10),   # above target
    (140000, 10),   # exactly the target
    (139999, 8),    # just under target
    (125000, 8),    # the open ask is still the 8 band
    (110000, 8),    # exactly the minimum
    (109999, 3),    # just under the minimum
    (90000, 3),     # exactly the floor
    (89999, 1),     # below the floor
    (1, 1),
])
def test_comp_top_of_range_bands(top, expected):
    assert sh.comp_score(pay(top=top), P) == expected


def test_comp_scores_the_top_of_a_range_not_the_bottom():
    tiers = [{"label": "Region B", "min": 95000, "max": 145000}]
    assert sh.comp_score(pay(tiers=tiers), P) == 10


def test_comp_named_location_tier_wins_over_nationwide():
    tiers = [
        {"label": "Nationwide", "min": 150000, "max": 180000},
        {"label": "Region B", "min": 80000, "max": 100000},
    ]
    assert sh.comp_score(pay(tiers=tiers), P) == 3


def test_comp_nationwide_tier_when_location_not_named():
    tiers = [
        {"label": "Region A", "min": 80000, "max": 95000},
        {"label": "Everywhere else", "min": 130000, "max": 150000},
    ]
    assert sh.comp_score(pay(tiers=tiers), P) == 10


def test_comp_lowest_tier_when_no_location_and_no_nationwide():
    tiers = [
        {"label": "Region A", "min": 150000, "max": 170000},
        {"label": "Region C", "min": 85000, "max": 100000},
    ]
    assert sh.comp_score(pay(tiers=tiers), P) == 3


def test_comp_tier_order_is_named_then_nationwide_then_lowest():
    tiers = [
        {"label": "Region A", "max": 90000},
        {"label": "All other locations", "max": 120000},
        {"label": "Region B", "max": 150000},
    ]
    assert sh.pick_tier(tiers, "Region B")["label"] == "Region B"
    assert sh.pick_tier(tiers, "Region Z")["label"] == "All other locations"
    assert sh.pick_tier(tiers[:1] + tiers[2:], "Region Z")["label"] == "Region A"


def test_comp_base_pay_only_other_pay_is_ignored():
    f = pay(top=100000)
    f["pay"]["other_pay_noted"] = ["Bonus up to 50000", "Stock grant 200000"]
    assert sh.comp_score(f, P) == 3


def test_comp_stated_with_no_number_is_an_error():
    with pytest.raises(ValueError):
        sh.comp_score(pay(), P)


def test_comp_needs_the_profile_numbers():
    profile = make_profile()
    del profile["comp"]["floor"]
    with pytest.raises(ValueError):
        sh.comp_score(pay(top=100000), profile)


# ---------------------------------------------------------- Qualifications

def qual(**q):
    return make_findings(qualifications=q)


def test_qualifications_clean_is_ten():
    assert sh.qualifications_score(qual(), P) == 10


@pytest.mark.parametrize("years,expected", [(5, 10), (9, 10), (10, 8), (15, 8)])
def test_qualifications_years_above_the_persons_figure(years, expected):
    assert sh.qualifications_score(qual(years_required=years), P) == expected


def test_qualifications_narrow_subdomain_costs_two():
    assert sh.qualifications_score(qual(narrow_subdomain=True), P) == 8


def test_qualifications_years_and_narrow_subdomain_cost_two_together():
    assert sh.qualifications_score(qual(years_required=15, narrow_subdomain=True), P) == 8


@pytest.mark.parametrize("n,expected", [(1, 9), (2, 8), (3, 7), (4, 6), (5, 6)])
def test_qualifications_known_gaps_cost_one_each_max_four(n, expected):
    hits = ["gap_a", "gap_b", "gap_c", "gap_d", "gap_e"][:n]
    assert sh.qualifications_score(qual(known_gaps_hit=hits), P) == expected


def test_qualifications_self_score_gaps_share_the_same_cap():
    f = qual(known_gaps_hit=["gap_b", "gap_c", "gap_d"], self_score_gaps=["skill_x", "skill_y"])
    assert sh.qualifications_score(f, P) == 6  # 5 gaps, capped at -4


def test_qualifications_a_skill_is_never_counted_twice():
    # gap_a is the known gap for skill_a. Naming both is one gap, not two.
    f = qual(known_gaps_hit=["gap_a"], self_score_gaps=["skill_a"])
    assert sh.qualifications_score(f, P) == 9


def test_qualifications_same_self_score_gap_listed_twice_counts_once():
    assert sh.qualifications_score(qual(self_score_gaps=["skill_x", "skill_x"]), P) == 9


def test_qualifications_working_style_mismatch_costs_three():
    assert sh.qualifications_score(qual(working_style_mismatch=True), P) == 7


def test_qualifications_every_deduction_at_once_still_scores_one():
    f = qual(years_required=20, known_gaps_hit=["gap_a", "gap_b", "gap_c", "gap_d"],
             working_style_mismatch=True)
    assert sh.qualifications_score(f, P) == 1  # 10 - 2 - 4 - 3
    f["qualifications"]["narrow_subdomain"] = True
    assert sh.qualifications_score(f, P) == 1  # still one years deduction, not two


def test_qualifications_gaps_may_sit_at_the_top_level():
    f = make_findings(known_gaps_hit=["gap_b"], self_score_gaps=["skill_x"])
    assert sh.qualifications_score(f, P) == 8


def test_qualifications_years_need_the_profile_figure():
    profile = make_profile()
    del profile["person"]["years_experience"]
    with pytest.raises(ValueError):
        sh.qualifications_score(qual(years_required=5), profile)


# ---------------------------------------------------------------- Culture

def cult(**c):
    return make_findings(culture=c)


def perks(*ids):
    return [{"perk_id": i, "quote": "q"} for i in ids]


def test_culture_silence_stays_five():
    assert sh.culture_score(cult(), P) == 5


def test_culture_missing_block_stays_five():
    f = make_findings()
    del f["culture"]
    assert sh.culture_score(f, P) == 5


@pytest.mark.parametrize("perk,expected", [
    ("unlimited_pto", 7), ("learning_budget", 7), ("extra_days_off", 7),
    ("offsites", 6), ("home_office", 6), ("parental_leave", 6),
])
def test_culture_perks_big_two_nice_one(perk, expected):
    assert sh.culture_score(cult(perks=perks(perk)), P) == expected


def test_culture_unknown_perk_id_is_an_error():
    with pytest.raises(ValueError):
        sh.culture_score(cult(perks=perks("free_snacks")), P)


def test_culture_same_perk_quoted_twice_counts_once():
    assert sh.culture_score(cult(perks=perks("unlimited_pto", "unlimited_pto")), P) == 7


def test_culture_strong_positive_phrase_adds_one_each():
    c = cult(strong_positive_phrases=[{"phrase": "we do not micromanage", "quote": "q"},
                                      {"phrase": "work sample", "quote": "q"}])
    assert sh.culture_score(c, P) == 7


def test_culture_cap_at_ten():
    # 5 + 2 + 2 + 1 + 1 = 11, capped at 10.
    c = cult(perks=perks("unlimited_pto", "learning_budget", "offsites"),
             strong_positive_phrases=[{"phrase": "p", "quote": "q"}])
    assert sh.culture_score(c, P) == 10


def test_culture_big_perks_over_the_cap_still_ten():
    c = cult(perks=perks("unlimited_pto", "learning_budget", "extra_days_off", "offsites", "home_office"))
    assert sh.culture_score(c, P) == 10


@pytest.mark.parametrize("low,expected", [
    ({"days": 10, "quote": "q"}, 3),                    # under the 15 day threshold
    ({"days": 15, "quote": "q"}, 5),                    # at the threshold is not low
    ({"days": 20, "quote": "q"}, 5),
    ({"days": 30, "accrual_only": True, "quote": "q"}, 3),  # accrual-only is low whatever the days
    ({"accrual_only": True, "quote": "q"}, 3),
    ({"quote": "q"}, 3),                                # flagged with no number
    (None, 5),
])
def test_culture_low_time_off(low, expected):
    assert sh.culture_score(cult(low_time_off=low), P) == expected


def test_culture_hustle_costs_one_each_max_three():
    def hustle(n):
        return [{"phrase": f"h{i}", "quote": "q"} for i in range(n)]
    assert sh.culture_score(cult(hustle=hustle(1)), P) == 4
    assert sh.culture_score(cult(hustle=hustle(3)), P) == 2
    assert sh.culture_score(cult(hustle=hustle(5)), P) == 2


def test_culture_free_phrases_cost_nothing():
    c = cult(hustle=[{"phrase": "Fast-Paced", "quote": "q"}])
    assert sh.culture_score(c, P) == 5


def test_culture_tripped_soft_flag_costs_one_each():
    c = cult(soft_flags_tripped=[{"id": "org_instability", "quote": "q"},
                                 {"id": "title_ambiguity", "quote": "q"}])
    assert sh.culture_score(c, P) == 3


@pytest.mark.parametrize("flag_id", ["no_pay_transparency", "unlisted_pay"])
def test_culture_unlisted_pay_is_never_a_soft_flag_penalty(flag_id):
    assert sh.culture_score(cult(soft_flags_tripped=[{"id": flag_id, "quote": "q"}]), P) == 5


def test_culture_negative_phrase_costs_one_each():
    c = cult(negative_phrases=[{"phrase": "a", "quote": "q"}, {"phrase": "b", "quote": "q"}])
    assert sh.culture_score(c, P) == 3


def test_culture_floor_at_zero():
    c = cult(low_time_off={"days": 5, "quote": "q"},
             hustle=[{"phrase": f"h{i}", "quote": "q"} for i in range(3)],
             soft_flags_tripped=[{"id": "a", "quote": "q"}, {"id": "b", "quote": "q"}],
             negative_phrases=[{"phrase": "n", "quote": "q"}])
    assert sh.culture_score(c, P) == 0  # 5 - 2 - 3 - 2 - 1


def test_culture_perks_and_penalties_net_out():
    c = cult(perks=perks("unlimited_pto"), low_time_off={"days": 10, "quote": "q"})
    assert sh.culture_score(c, P) == 5


# ------------------------------------------------- rounding and the whole run

def test_rounding_happens_after_the_floor_not_before():
    assert sh._finish(8.5) == 9
    assert sh._finish(-0.5) == 0
    assert sh._finish(10.4) == 10


def test_a_half_point_fit_rounds_up_through_the_public_function():
    f = with_ratings(strong_one="unknown", strong_two="strong", soft_one="strong")
    assert sh.fit_score(f, P) == 9  # 8.5


def test_two_half_points_make_a_whole_one():
    f = with_ratings(strong_one="unknown", strong_two="weak", soft_one="strong")
    assert sh.fit_score(f, P) == 7  # 10 - 1.5 - 1.5 = 7.0


def test_score_all_returns_four_scores_and_reasons():
    result = sh.score_all(make_findings(pay={"stated": False}), P)
    assert [result[k] for k in ("fit", "comp", "qualifications", "culture")] == [10, 5, 10, 5]
    assert set(result["why"]) == {"fit", "comp", "qualifications", "culture"}
    assert any("not listed" in line for line in result["why"]["comp"])


def test_why_lists_what_drove_a_miss():
    why = []
    sh.fit_score(with_ratings(strong_one="weak", strong_two="strong", soft_one="strong"), P, why)
    assert why == ["Strong one: weak, -1.5"]


def test_cli_prints_json(tmp_path, capsys):
    (tmp_path / "f.json").write_text(json.dumps(make_findings()))
    (tmp_path / "p.yaml").write_text(yaml.safe_dump(P))
    code = sh.main([str(tmp_path / "f.json"), "--profile", str(tmp_path / "p.yaml"), "--json"])
    out = json.loads(capsys.readouterr().out)
    assert code == 0
    assert (out["fit"], out["comp"], out["qualifications"], out["culture"]) == (10, 5, 10, 5)


def test_cli_exit_one_when_it_cannot_score(tmp_path, capsys):
    (tmp_path / "f.json").write_text(json.dumps(make_findings(lane="nope")))
    (tmp_path / "p.yaml").write_text(yaml.safe_dump(P))
    assert sh.main([str(tmp_path / "f.json"), "--profile", str(tmp_path / "p.yaml")]) == 1


def test_cli_exit_two_when_a_file_is_missing(tmp_path):
    assert sh.main([str(tmp_path / "none.json"), "--profile", str(tmp_path / "none.yaml")]) == 2


# ------------------------------------------- pay range keys: schema vs scorer

SCHEMA_PATH = Path(__file__).resolve().parents[1] / "schema" / "findings.schema.json"


def _schema_tier_properties():
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    tier = schema["properties"]["pay"]["properties"]["tiers"]["items"]
    return tier["properties"]


def test_schema_and_scorer_agree_on_pay_range_keys():
    props = _schema_tier_properties()
    assert {"min", "max"} <= set(props)
    assert "low" not in props and "high" not in props
    # every number key the schema describes is one the scorer reads
    number_keys = {k for k, v in props.items() if "number" in v.get("type", [])}
    for key in number_keys:
        assert sh._tier_top({"label": "x", key: 123456}) == 123456


def test_a_pay_range_written_as_the_schema_describes_scores_end_to_end(tmp_path):
    props = _schema_tier_properties()
    lo_key, hi_key = "min", "max"
    assert lo_key in props and hi_key in props
    tier = {"label": "all other US locations", lo_key: 100000, hi_key: 150000,
            "quote": "q"}
    findings = pay(tiers=[tier])
    # top 150000 is above the profile target of 140000, so comp is 10
    assert sh.comp_score(findings, P) == 10
    # and through the command line entry point, as the skill runs it
    fpath = tmp_path / "findings.json"
    ppath = tmp_path / "profile.yaml"
    fpath.write_text(json.dumps(findings), encoding="utf-8")
    ppath.write_text(yaml.safe_dump(P), encoding="utf-8")
    assert sh.main([str(fpath), "--profile", str(ppath), "--json"]) == 0
