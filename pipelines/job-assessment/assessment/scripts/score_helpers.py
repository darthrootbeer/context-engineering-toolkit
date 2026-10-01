#!/usr/bin/env python3
"""Fit, Comp, Qualifications and Culture scores, as plain functions.

This is a script port of the prose scoring rules in the assessment skill. The
model reads the posting and hands back a findings file (JSON). It never does
the arithmetic. This module does, the same way every time, so the numbers can
be tested.

The rules are written out in ARCHITECTURE.md (snapshot dated 2026-10-01).
Short version:

  Fit            Start 10. Strong requirement: Strong or Fair 0, Weak -1.5,
                 Poor -3, Unknown -1.5. Soft requirement: Weak or Poor -1,
                 everything else 0. Bonus items never subtract. Autonomy net
                 negative -2. Each "rather avoid" skill that is core daily
                 work -1, max -2. Floor 0.
  Comp           Base pay only, top of the range. Unstated 5. Top at or above
                 target 10. At or above min 8. At or above floor 3. Below
                 floor 1.
  Qualifications Start 10. Years above the person's figure, or years in a
                 narrow sub-domain: -2. Each load-bearing known gap -1, shared
                 -4 cap with self-score gaps (never counted twice). Working
                 style mismatch -3. Floor 0.
  Culture        Start 5 (unknown) and earn points. Big perk +2, nice perk +1,
                 strong positive phrase +1. Low stated time off -2. Hustle
                 phrase -1 each, max -3. Tripped soft flag -1 each (never for
                 unlisted pay). Negative phrase -1 each. Silence stays 5.
                 Floor 0, cap 10.
  Rounding       Each category is rounded half up to a whole number after its
                 floor and cap.

Usage:
    score_helpers.py FINDINGS --profile PROFILE [--json]

Exit: 0 scored, 1 findings or profile could not be scored, 2 could not run.
"""
import argparse
import json
import sys
from decimal import ROUND_HALF_UP, Decimal
from pathlib import Path

# Soft flags that mean "the posting does not list its pay". Pay is scored once,
# in Comp. It is never also a Culture penalty.
UNLISTED_PAY_FLAG_IDS = {
    "no_pay_transparency",
    "unlisted_pay",
    "pay_unlisted",
    "pay_not_listed",
    "no_pay_range",
}

# A tier label that contains one of these is a "nationwide" tier.
NATIONWIDE_WORDS = (
    "nationwide",
    "national",
    "everywhere else",
    "anywhere else",
    "all other",
    "all locations",
    "other locations",
    "rest of",
)

RATINGS = ("strong", "fair", "weak", "poor", "unknown")


def round_half_up(value):
    """Round to a whole number, halves going up (8.5 -> 9, 6.5 -> 7)."""
    return int(Decimal(str(value)).quantize(Decimal("1"), rounding=ROUND_HALF_UP))


def _clamp(value, low=0, high=10):
    return max(low, min(high, value))


def _finish(raw):
    """Floor at 0, cap at 10, then round half up."""
    return round_half_up(_clamp(raw))


def _lane(profile, lane_name):
    for lane in profile.get("lanes") or []:
        if lane.get("name") == lane_name:
            return lane
    raise ValueError(f'lane "{lane_name}" is not in the profile')


def _note(why, text):
    if why is not None:
        why.append(text)


# ---------------------------------------------------------------- Fit

def fit_score(findings, profile, why=None):
    """Fit: how well the job's shape matches what the person wants."""
    lane = _lane(profile, findings.get("lane"))
    by_id = {r["id"]: r for r in lane.get("requirements") or []}
    rated = {}
    for item in findings.get("requirements") or []:
        rid = item.get("id")
        if rid not in by_id:
            raise ValueError(f'requirement "{rid}" is not in lane "{lane["name"]}"')
        rating = str(item.get("rating", "unknown")).lower()
        if rating not in RATINGS:
            raise ValueError(f'requirement "{rid}" has rating "{rating}"')
        rated[rid] = rating

    score = 10.0
    for rid, req in by_id.items():
        if req.get("bonus"):
            continue  # bonus items never subtract
        # A requirement the findings never mention is silence, so Unknown.
        rating = rated.get(rid, "unknown")
        label = req.get("label", rid)
        if req.get("severity") == "strong":
            cost = {"strong": 0, "fair": 0, "weak": 1.5, "poor": 3, "unknown": 1.5}[rating]
        else:
            cost = {"weak": 1, "poor": 1}.get(rating, 0)
        if cost:
            score -= cost
            _note(why, f"{label}: {rating}, -{cost:g}")

    if (findings.get("autonomy") or {}).get("net") == "negative":
        score -= 2
        _note(why, "Autonomy reads net negative, -2")

    avoid = len(set(findings.get("avoid_core_skills") or []))
    if avoid:
        cost = min(avoid, 2)
        score -= cost
        _note(why, f"{avoid} rather-avoid skill(s) are core daily work, -{cost}")
    return _finish(score)


# ---------------------------------------------------------------- Comp

def _tier_top(tier):
    for key in ("max", "top", "min"):
        if tier.get(key) is not None:
            return tier[key]
    raise ValueError(f'pay tier "{tier.get("label")}" has no number')


def pick_tier(tiers, location_label):
    """The person's named location, else a nationwide tier, else the lowest."""
    wanted = (location_label or "").strip().lower()
    if wanted:
        for tier in tiers:
            if wanted in str(tier.get("label", "")).lower():
                return tier
    for tier in tiers:
        label = str(tier.get("label", "")).lower()
        if any(word in label for word in NATIONWIDE_WORDS):
            return tier
    return min(tiers, key=_tier_top)


def comp_score(findings, profile, why=None):
    """Comp: base pay only, scored on the top of the range."""
    pay = findings.get("pay") or {}
    if not pay.get("stated"):
        _note(why, "Pay is not listed, neutral 5")
        return 5
    tiers = pay.get("tiers") or []
    if tiers:
        tier = pick_tier(tiers, (profile.get("person") or {}).get("location_label"))
        top = _tier_top(tier)
        _note(why, f'Tier used: {tier.get("label")}')
    elif pay.get("top") is not None:
        top = pay["top"]
    else:
        raise ValueError("pay.stated is true but there are no tiers and no top")
    comp = profile.get("comp") or {}
    for key in ("floor", "min", "target"):
        if comp.get(key) is None:
            raise ValueError(f"profile comp.{key} is missing")
    if top >= comp["target"]:
        score = 10
    elif top >= comp["min"]:
        score = 8
    elif top >= comp["floor"]:
        score = 3
    else:
        score = 1
    _note(why, f"Top of range {top} against target {comp['target']}, min {comp['min']}, floor {comp['floor']}")
    return score


# ---------------------------------------------------------- Qualifications

def _gap_identities(findings, lane):
    """Known gaps and self-score gaps as one set, so a skill is never counted twice."""
    gaps = lane.get("known_gaps") or []
    by_key = {}
    for gap in gaps:
        identity = gap.get("skill_id") or gap.get("id")
        for key in (gap.get("id"), gap.get("label"), gap.get("skill_id")):
            if key:
                by_key[str(key).lower()] = identity
    found = set()
    for name in findings.get("known_gaps_hit") or []:
        found.add(by_key.get(str(name).lower(), str(name).lower()))
    for skill in findings.get("self_score_gaps") or []:
        found.add(by_key.get(str(skill).lower(), str(skill).lower()))
    return found


def qualifications_score(findings, profile, why=None):
    """Qualifications: can the person do this job, judged against their evidence."""
    lane = _lane(profile, findings.get("lane"))
    qual = findings.get("qualifications") or {}
    score = 10.0

    years_required = qual.get("years_required")
    too_many_years = False
    if years_required is not None:
        years = (profile.get("person") or {}).get("years_experience")
        if years is None:
            raise ValueError("profile person.years_experience is missing")
        too_many_years = years_required > years
    if too_many_years or qual.get("narrow_subdomain"):
        score -= 2  # one deduction, whichever of the two reasons applies
        reason = "Asks for more years than the person has" if too_many_years else "Years are required in a narrow sub-domain"
        _note(why, f"{reason}, -2")

    # Findings for gaps live at the top level of the findings file as well as
    # under qualifications. Accept either place.
    merged = dict(findings)
    for key in ("known_gaps_hit", "self_score_gaps"):
        if key in qual:
            merged[key] = qual[key]
    gaps = _gap_identities(merged, lane)
    if gaps:
        cost = min(len(gaps), 4)
        score -= cost
        _note(why, f"{len(gaps)} load-bearing gap(s), -{cost} (cap 4)")

    if qual.get("working_style_mismatch"):
        score -= 3
        _note(why, "Posting expects the person to become the expert, -3")
    return _finish(score)


# ---------------------------------------------------------------- Culture

def _low_time_off(entry, threshold):
    """True when the stated time off counts as low."""
    if not entry:
        return False
    if isinstance(entry, str):
        return True
    if entry.get("accrual_only"):
        return True
    days = entry.get("days")
    if days is not None and threshold is not None:
        return days < threshold
    return True


def culture_score(findings, profile, why=None):
    """Culture: starts at 5 (unknown) and earns points from the posting's own words."""
    culture = findings.get("culture") or {}
    profile_culture = profile.get("culture") or {}
    kinds = {p["id"]: p.get("kind") for p in profile_culture.get("perks") or []}
    score = 5.0

    for perk_id in dict.fromkeys(p.get("perk_id") for p in culture.get("perks") or []):
        if perk_id not in kinds:
            raise ValueError(f'perk "{perk_id}" is not in the profile')
        points = {"big": 2, "nice": 1}.get(kinds[perk_id], 0)
        score += points
        _note(why, f"Perk {perk_id} ({kinds[perk_id]}), +{points}")

    positives = {str(p.get("phrase", "")).lower() for p in culture.get("strong_positive_phrases") or []}
    if positives:
        score += len(positives)
        _note(why, f"{len(positives)} strong positive phrase(s), +{len(positives)}")

    if _low_time_off(culture.get("low_time_off"), profile_culture.get("low_time_off_days")):
        score -= 2
        _note(why, "Low stated time off, -2")

    free = {str(p).lower() for p in profile_culture.get("free_phrases") or []}
    hustle = {
        str(h.get("phrase", "")).lower()
        for h in culture.get("hustle") or []
        if str(h.get("phrase", "")).lower() not in free
    }
    if hustle:
        cost = min(len(hustle), 3)
        score -= cost
        _note(why, f"{len(hustle)} hustle phrase(s), -{cost} (cap 3)")

    flags = {
        f.get("id")
        for f in culture.get("soft_flags_tripped") or []
        if f.get("id") not in UNLISTED_PAY_FLAG_IDS
    }
    if flags:
        score -= len(flags)
        _note(why, f"{len(flags)} soft flag(s) tripped, -{len(flags)}")

    negatives = {str(n.get("phrase", "")).lower() for n in culture.get("negative_phrases") or []}
    if negatives:
        score -= len(negatives)
        _note(why, f"{len(negatives)} negative phrase(s), -{len(negatives)}")
    return _finish(score)


# ---------------------------------------------------------------- all four

def score_all(findings, profile):
    """All four scores plus a short reason list for each."""
    why = {"fit": [], "comp": [], "qualifications": [], "culture": []}
    return {
        "fit": fit_score(findings, profile, why["fit"]),
        "comp": comp_score(findings, profile, why["comp"]),
        "qualifications": qualifications_score(findings, profile, why["qualifications"]),
        "culture": culture_score(findings, profile, why["culture"]),
        "why": why,
    }


def main(argv=None):
    ap = argparse.ArgumentParser(description="Score one findings file.")
    ap.add_argument("findings")
    ap.add_argument("--profile", required=True)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    try:
        import yaml

        findings = json.loads(Path(args.findings).read_text(encoding="utf-8"))
        profile = yaml.safe_load(Path(args.profile).read_text(encoding="utf-8"))
    except Exception as exc:  # unreadable file, bad JSON, bad YAML
        print(f"score_helpers: could not read inputs: {exc}", file=sys.stderr)
        return 2
    try:
        result = score_all(findings, profile)
    except (ValueError, KeyError, TypeError) as exc:
        print(f"score_helpers: could not score: {exc}", file=sys.stderr)
        return 1
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        for name in ("fit", "comp", "qualifications", "culture"):
            print(f"{name.capitalize()} {result[name]}")
            for line in result["why"][name]:
                print(f"  - {line}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
