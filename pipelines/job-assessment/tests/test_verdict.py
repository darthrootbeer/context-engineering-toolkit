"""Every verdict trigger, in order, with inline data only.

FICTIONAL EXAMPLE DATA. Nothing here is a real person or posting.
"""
import inspect
import itertools
import json
import sys
from pathlib import Path

import pytest

SCRIPTS = Path(__file__).resolve().parents[1] / "assessment" / "scripts"
sys.path.insert(0, str(SCRIPTS))

import verdict as v  # noqa: E402


def run(fit=8, qual=8, comp=8, culture=8, **kw):
    return v.decide(fit, qual, comp, culture, **kw)


def test_4d_apply_when_nothing_fires():
    r = run()
    assert (r["label"], r["trigger"]) == ("Apply", "4d")


def test_4d_edge_scores_that_still_apply():
    # Fit and Qualifications both 7 average exactly 7. Comp and Culture at 4.
    r = run(fit=7, qual=7, comp=4, culture=4)
    assert (r["label"], r["trigger"]) == ("Apply", "4d")


def test_hard_block_is_skip_even_with_perfect_scores():
    r = run(10, 10, 10, 10, hard_block="gambling")
    assert (r["label"], r["trigger"]) == ("Skip", "hard block")


def test_4a_override_is_skip_even_with_perfect_scores():
    r = run(10, 10, 10, 10, override="payments")
    assert (r["label"], r["trigger"]) == ("Skip", "4a")


def test_4a_wins_over_what_4c_would_have_said():
    # Comp 3 would say reservations. The override says Skip first.
    r = run(7, 6, 3, 5, override="payments")
    assert (r["label"], r["trigger"]) == ("Skip", "4a")


@pytest.mark.parametrize("fit,qual", [(5, 10), (10, 5), (0, 10), (10, 0), (5, 5)])
def test_4b_fit_or_qualifications_at_five_or_lower_is_skip(fit, qual):
    r = run(fit=fit, qual=qual, comp=10, culture=10)
    assert (r["label"], r["trigger"]) == ("Skip", "4b")


@pytest.mark.parametrize("fit,qual", [(6, 6), (6, 10), (10, 6)])
def test_4b_six_clears_the_floor(fit, qual):
    assert run(fit=fit, qual=qual, comp=10, culture=10)["trigger"] != "4b"


def test_4b_comp_and_culture_never_force_a_skip():
    r = run(fit=9, qual=9, comp=0, culture=0)
    assert r["label"] == "Apply with reservations"


@pytest.mark.parametrize("comp", [0, 1, 2, 3])
def test_4c_comp_three_or_lower(comp):
    r = run(comp=comp)
    assert (r["label"], r["trigger"]) == ("Apply with reservations", "4c comp")


@pytest.mark.parametrize("culture", [0, 1, 2, 3])
def test_4c_culture_three_or_lower(culture):
    r = run(culture=culture)
    assert (r["label"], r["trigger"]) == ("Apply with reservations", "4c culture")


def test_4c_names_both_when_both_are_low():
    assert run(comp=2, culture=3)["trigger"] == "4c comp and culture"


def test_4c_four_is_not_low():
    assert run(comp=4, culture=4)["trigger"] == "4d"


@pytest.mark.parametrize("fit,qual", [(6, 7), (7, 6), (6, 6)])
def test_4c_average_under_seven(fit, qual):
    r = run(fit=fit, qual=qual, comp=9, culture=9)
    assert (r["label"], r["trigger"]) == ("Apply with reservations", "4c average")


def test_4c_average_of_exactly_seven_applies():
    assert run(fit=6, qual=8)["label"] == "Apply"


def test_4c_comp_or_culture_is_named_before_the_average():
    assert run(fit=6, qual=6, comp=3)["trigger"] == "4c comp"


def test_precedence_order_hard_block_then_4a_then_4b_then_4c():
    assert run(2, 2, 0, 0, override="x", hard_block="g")["trigger"] == "hard block"
    assert run(2, 2, 0, 0, override="x")["trigger"] == "4a"
    assert run(2, 2, 0, 0)["trigger"] == "4b"
    assert run(8, 8, 0, 0)["trigger"] == "4c comp and culture"
    assert run(6, 6, 9, 9)["trigger"] == "4c average"
    assert run(8, 8, 9, 9)["trigger"] == "4d"


def test_every_score_combination_gives_one_of_three_labels():
    for combo in itertools.product([0, 3, 4, 5, 6, 7, 10], repeat=4):
        assert run(*combo)["label"] in ("Skip", "Apply with reservations", "Apply")


@pytest.mark.parametrize("bad", [-1, 11, 7.5, "8", None, True])
def test_scores_must_be_whole_numbers_from_zero_to_ten(bad):
    with pytest.raises(ValueError):
        run(fit=bad)


def test_the_verdict_takes_no_employer_input():
    names = set(inspect.signature(v.decide).parameters)
    assert names == {"fit", "qualifications", "comp", "culture", "override", "hard_block"}
    source = Path(v.__file__).read_text(encoding="utf-8").lower()
    assert "company" not in source


def test_helpers_read_only_the_block_and_override_fields():
    assert v.hard_block_id({"hard_block": {"tripped": True, "id": "gambling"}}) == "gambling"
    assert v.hard_block_id({"hard_block": {"tripped": False, "id": "gambling"}}) is None
    assert v.hard_block_id({}) is None
    assert v.override_skill({"job_type_override": {"fired": True, "skill": "payments"}}) == "payments"
    assert v.override_skill({"job_type_override": {"fired": False, "skill": "payments"}}) is None
    assert v.override_skill({}) is None


def test_a_named_exception_means_the_block_does_not_count():
    findings = {"hard_block": {"tripped": True, "id": "non_remote", "named_exception": "approved 2026-10-01"}}
    assert v.hard_block_id(findings) is None


def test_the_company_read_in_findings_changes_nothing():
    base = {"company_read": {"status": "none"}}
    loved = {"company_read": {"status": "high_interest", "name": "Example Co"}}
    assert v.hard_block_id(base) == v.hard_block_id(loved)
    assert v.override_skill(base) == v.override_skill(loved)


def test_cli_text_and_json(capsys):
    assert v.main(["--fit", "7", "--qual", "6", "--comp", "5", "--culture", "9"]) == 0
    assert capsys.readouterr().out.strip() == "Apply with reservations (trigger: 4c average)"
    assert v.main(["--fit", "9", "--qual", "9", "--comp", "9", "--culture", "9", "--json"]) == 0
    out = json.loads(capsys.readouterr().out)
    assert (out["label"], out["trigger"]) == ("Apply", "4d")


def test_cli_override_and_hard_block_flags(capsys):
    v.main(["--fit", "9", "--qual", "9", "--comp", "9", "--culture", "9", "--override", "payments", "--json"])
    assert json.loads(capsys.readouterr().out)["trigger"] == "4a"
    v.main(["--fit", "9", "--qual", "9", "--comp", "9", "--culture", "9", "--hard-block", "gambling", "--json"])
    assert json.loads(capsys.readouterr().out)["trigger"] == "hard block"


def test_cli_exit_two_on_a_bad_score(capsys):
    assert v.main(["--fit", "11", "--qual", "9", "--comp", "9", "--culture", "9"]) == 2


@pytest.mark.parametrize("scores,kw,label,trigger", [
    ((9, 9, 10, 10), {}, "Apply", "4d"),                                   # strong fit
    ((7, 6, 3, 5), {"override": "payments"}, "Skip", "4a"),                # override beats reservations
    ((7, 6, 5, 9), {}, "Apply with reservations", "4c average"),           # 6.5 average
])
def test_expected_shapes_of_three_typical_postings(scores, kw, label, trigger):
    fit, qual, comp, culture = scores
    r = v.decide(fit, qual, comp, culture, **kw)
    assert (r["label"], r["trigger"]) == (label, trigger)
