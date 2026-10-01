#!/usr/bin/env python3
"""Print one lane's checklist from a career profile, ready to judge a posting.

Does no matching, no scoring, no fetching. Phrase hints and keyword signals
need a reader who sees the sentence around them, not a regex. This script only
hands back the global rules plus the ONE lane asked for, in full, so the
judgment happens against a complete and correctly read checklist instead of a
half-remembered one.

The lane gate is the point of the script. Judging a posting against the wrong
lane's rules gives a number that looks real and means nothing. So the lane is
a required argument, it must exist in the profile, and when a posting file is
given its own `lane:` field must match. A mismatch exits non-zero and prints
no rubric.

Exit codes: 0 printed, 1 profile missing or unreadable, 2 unknown lane,
3 the posting's lane does not match the lane asked for.

Usage:
    load_criteria.py --profile career-profile.yaml --lane docs-platform
    load_criteria.py --profile career-profile.yaml --lane docs-platform \\
        --posting "archive/Examplon Co - Docs Lead - 2026-10-01.md"
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

EXIT_OK = 0
EXIT_ERROR = 1
EXIT_UNKNOWN_LANE = 2
EXIT_MISMATCH = 3

RULE = "=" * 70


def load_profile(path: Path) -> dict:
    try:
        import yaml
    except ImportError:
        print("PyYAML is not installed. Run: pip install -r requirements.txt", file=sys.stderr)
        sys.exit(EXIT_ERROR)
    if not path.exists():
        print(f"Profile not found: {path}", file=sys.stderr)
        sys.exit(EXIT_ERROR)
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        print(f"Profile is not valid YAML: {exc}", file=sys.stderr)
        sys.exit(EXIT_ERROR)
    if not isinstance(data, dict) or not isinstance(data.get("lanes"), list):
        print(f"{path} has no lanes list, so it is not a career profile.", file=sys.stderr)
        sys.exit(EXIT_ERROR)
    return data


def find_lane(profile: dict, name: str) -> dict:
    """Return the lane entry, or exit 2 listing the valid names."""
    names = [str(lane.get("name")) for lane in profile["lanes"] if isinstance(lane, dict)]
    for lane in profile["lanes"]:
        if isinstance(lane, dict) and lane.get("name") == name:
            return lane
    print(
        f"Unknown lane {name!r}. Lanes in this profile: {', '.join(sorted(names)) or 'none'}.\n"
        "The lane comes from the posting being assessed. It is not a choice "
        "made at run time.",
        file=sys.stderr,
    )
    sys.exit(EXIT_UNKNOWN_LANE)


def posting_lane(path: Path) -> str | None:
    """Read `lane:` from a posting note's frontmatter."""
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    front = re.match(r"\A---\n(.*?)\n---", text, flags=re.S)
    if not front:
        return None
    match = re.search(r"^lane:\s*[\"']?(.+?)[\"']?\s*$", front.group(1), flags=re.M)
    return match.group(1) if match else None


def assert_posting_lane(requested: str, posting: Path) -> None:
    """Hard gate: the posting must say it belongs to the lane asked for."""
    if not posting.exists():
        print(f"Posting not found: {posting}", file=sys.stderr)
        sys.exit(EXIT_ERROR)
    declared = posting_lane(posting)
    if declared == requested:
        return
    print(
        "LANE MISMATCH. Refusing to print a rubric.\n"
        f"  asked for lane : {requested}\n"
        f"  posting says   : {declared!r}\n"
        f"  posting        : {posting}\n\n"
        "Judging a posting against the wrong lane's rules gives a score that "
        "looks real and means nothing. Fix the lane field in the posting note, "
        "or pass the lane the posting belongs to.",
        file=sys.stderr,
    )
    sys.exit(EXIT_MISMATCH)


def heading(title: str) -> None:
    print()
    print(RULE)
    print(title)
    print(RULE)


def print_global(profile: dict) -> None:
    person = profile.get("person") or {}
    heading("PERSON (context for Qualifications and Comp)")
    for key in ("years_experience", "working_style", "location_label"):
        if key in person:
            print(f"  {key}: {person[key]}")
    if person.get("target_roles"):
        print(f"  target_roles: {', '.join(map(str, person['target_roles']))}")

    heading("HARD BLOCKS: any single true match means do not surface at all")
    for block in profile.get("hard_blocks") or []:
        print(f"\n[{block.get('id')}] {block.get('label', '')}")
        if block.get("match_hints"):
            print(f"  hints: {', '.join(map(str, block['match_hints']))}")
        if block.get("why"):
            print(f"  why: {block['why']}")
    exceptions = profile.get("named_exceptions") or []
    if exceptions:
        print("\nNamed exceptions (check these BEFORE declaring a block):")
        for item in exceptions:
            print(
                f"  [{item.get('block_id')}] {item.get('company')}: {item.get('why', '')}"
            )


def print_lane(lane: dict) -> None:
    heading(f"LANE: {lane.get('name')} {lane.get('emoji', '')}")
    if lane.get("description"):
        print(f"\n{lane['description']}")

    heading("REQUIREMENTS: must-haves, judged and scored, never silently dropped")
    for req in lane.get("requirements") or []:
        bonus = " bonus" if req.get("bonus") else ""
        print(f"\n[{req.get('id')}] ({req.get('severity', '?')}{bonus}) {req.get('label', '')}")
        if req.get("why"):
            print(f"  why: {req['why']}")
    if not lane.get("requirements"):
        print("\n(this lane lists no requirements of its own)")

    heading("AUTONOMY: the core judgment call")
    autonomy = lane.get("autonomy") or {}
    print("  positive signals:")
    for sig in autonomy.get("positive_signals") or []:
        print(f"    + {sig}")
    print("  negative signals:")
    for sig in autonomy.get("negative_signals") or []:
        print(f"    - {sig}")

    heading("KEYWORD SIGNALS: language patterns, read in their sentence, never substring-matched")
    signals = lane.get("keyword_signals") or {}
    for tier in ("strong_positive", "positive", "negative", "strong_negative"):
        entries = signals.get(tier) or []
        if not entries:
            continue
        print(f"\n{tier}:")
        for entry in entries:
            print(f"  \"{entry.get('phrase')}\" - {entry.get('why', '')}")

    gaps = lane.get("known_gaps") or []
    heading("KNOWN GAPS: skills this lane wants that the profile says are missing")
    for gap in gaps:
        link = f" (skill: {gap['skill_id']})" if gap.get("skill_id") else ""
        print(f"  - [{gap.get('id')}] {gap.get('label', '')}{link}")
    if not gaps:
        print("  none listed")


def print_pay_and_culture(profile: dict) -> None:
    heading("PAY: base pay only, top of the range, tier by the person's location")
    comp = profile.get("comp") or {}
    print(f"  currency: {comp.get('currency', '?')}")
    for key in ("floor", "min", "open_ask", "target", "stretch_ceiling"):
        if key in comp:
            print(f"  {key}: {comp[key]}")

    heading("CULTURE: starts at 5, silence stays 5")
    culture = profile.get("culture") or {}
    print("  perks (big = +2, nice = +1):")
    for perk in culture.get("perks") or []:
        print(f"    [{perk.get('id')}] {perk.get('label', '')} ({perk.get('kind', '?')})")
    if "low_time_off_days" in culture:
        print(f"  low time off: below {culture['low_time_off_days']} days a year")
    if culture.get("hustle_phrases"):
        print(f"  hustle phrases: {', '.join(map(str, culture['hustle_phrases']))}")
    if culture.get("free_phrases"):
        print(f"  free phrases (read, cost nothing): {', '.join(map(str, culture['free_phrases']))}")

    heading("SOFT FLAGS: surfaced beside a posting, none disqualify alone")
    for flag in profile.get("soft_flags") or []:
        print(f"\n[{flag.get('id')}] {flag.get('label', '')}")
        if flag.get("why"):
            print(f"  why: {flag['why']}")

    heading("BENEFITS AND TERMS: worth checking, not auto-rejecting")
    for term in profile.get("benefits_and_terms") or []:
        print(f"\n[{term.get('id')}] {term.get('label', '')}")
        if term.get("why"):
            print(f"  why: {term['why']}")

    company = profile.get("company_criteria") or {}
    heading("COMPANY CRITERIA: company identity, never an input to a score or verdict")
    print("\nhigh interest:")
    for item in company.get("high_interest") or []:
        print(f"  [{item.get('name')}] {item.get('why', '')}")
    print("\ngood job, not high interest:")
    for item in company.get("good_not_dream") or []:
        print(f"  [{item.get('name')}] {item.get('why', '')}")

    avoid = [
        s for s in profile.get("skills") or []
        if isinstance(s, dict) and s.get("next") == "avoid"
    ]
    heading("RATHER AVOID: skilled at it is not wanting it")
    for skill in avoid:
        print(f"  [{skill.get('id')}] {skill.get('label', '')}")
    if not avoid:
        print("  none")


def main(argv: list[str] | None = None) -> None:
    ap = argparse.ArgumentParser(
        description="Print the criteria for ONE lane of a career profile."
    )
    ap.add_argument("--profile", required=True, type=Path, help="career-profile.yaml")
    ap.add_argument("--lane", required=True, help="Lane name. Must match the posting's lane.")
    ap.add_argument(
        "--posting",
        type=Path,
        help="Archived posting note. Its own `lane:` field must match --lane.",
    )
    args = ap.parse_args(argv)

    profile = load_profile(args.profile)
    lane = find_lane(profile, args.lane)
    if args.posting is not None:
        assert_posting_lane(args.lane, args.posting)

    print(f"CRITERIA SOURCE: {args.profile.name}")
    verified = "posting and profile agree" if args.posting else "profile lists this lane"
    print(f"LANE: {args.lane}  (verified: {verified})")
    print_global(profile)
    print_lane(lane)
    print_pay_and_culture(profile)


if __name__ == "__main__":
    main()
