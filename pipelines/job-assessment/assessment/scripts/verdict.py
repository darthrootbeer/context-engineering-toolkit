#!/usr/bin/env python3
"""The verdict, as a function of the four scores and two checks.

This is a script port of the prose verdict rules in the assessment skill. The
first rule that fires wins, and nothing after it is looked at:

  hard block   A hard block was tripped (and no named exception covers it).  Skip
  4a           Job-type override: a required, central skill has no evidence.  Skip
  4b           Fit is 5 or lower, or Qualifications is 5 or lower.            Skip
  4c comp      Comp is 3 or lower.                                            Apply with reservations
  4c culture   Culture is 3 or lower.                                         Apply with reservations
  4c average   (Fit + Qualifications) / 2 is under 7.                         Apply with reservations
  4d           Nothing above fired.                                           Apply

The employer read never goes in. This module takes four scores, an optional
override and an optional hard block, and nothing else. It cannot be moved by
who is hiring.

Usage:
    verdict.py --fit N --qual N --comp N --culture N [--override SKILL]
               [--hard-block ID] [--json]

Exit: 0 verdict printed, 2 bad input.
"""
import argparse
import json
import sys

SKIP = "Skip"
RESERVATIONS = "Apply with reservations"
APPLY = "Apply"

RULE_TEXT = {
    "hard block": "A hard block was tripped.",
    "4a": "A required skill that is central to the job has no evidence behind it.",
    "4b": "Fit or Qualifications is 5 or lower.",
    "4c comp": "Comp is 3 or lower.",
    "4c culture": "Culture is 3 or lower.",
    "4c comp and culture": "Comp and Culture are both 3 or lower.",
    "4c average": "Fit and Qualifications average under 7.",
    "4d": "Nothing above fired.",
}


def _check_score(name, value):
    if isinstance(value, bool) or not isinstance(value, int) or not 0 <= value <= 10:
        raise ValueError(f"{name} must be a whole number from 0 to 10, got {value!r}")


def decide(fit, qualifications, comp, culture, override=None, hard_block=None):
    """Return {"label", "trigger", "rule"} for the four scores."""
    for name, value in (("fit", fit), ("qualifications", qualifications),
                        ("comp", comp), ("culture", culture)):
        _check_score(name, value)

    if hard_block:
        trigger = "hard block"
        label = SKIP
    elif override:
        trigger = "4a"
        label = SKIP
    elif fit <= 5 or qualifications <= 5:
        trigger = "4b"
        label = SKIP
    elif comp <= 3 or culture <= 3:
        label = RESERVATIONS
        if comp <= 3 and culture <= 3:
            trigger = "4c comp and culture"
        elif comp <= 3:
            trigger = "4c comp"
        else:
            trigger = "4c culture"
    elif (fit + qualifications) / 2 < 7:
        trigger = "4c average"
        label = RESERVATIONS
    else:
        trigger = "4d"
        label = APPLY
    return {"label": label, "trigger": trigger, "rule": RULE_TEXT[trigger]}


def hard_block_id(findings):
    """The tripped hard block's id, or None. A named exception means not a block."""
    block = findings.get("hard_block") or {}
    if block.get("tripped") and not block.get("named_exception"):
        return block.get("id") or "unnamed"
    return None


def override_skill(findings):
    """The skill behind a fired job-type override, or None."""
    override = findings.get("job_type_override") or {}
    if override.get("fired"):
        return override.get("skill") or "unnamed"
    return None


def main(argv=None):
    ap = argparse.ArgumentParser(description="Compute the verdict from four scores.")
    ap.add_argument("--fit", type=int, required=True)
    ap.add_argument("--qual", type=int, required=True)
    ap.add_argument("--comp", type=int, required=True)
    ap.add_argument("--culture", type=int, required=True)
    ap.add_argument("--override", help="skill name when the job-type override fired")
    ap.add_argument("--hard-block", help="hard block id when one was tripped")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    try:
        result = decide(args.fit, args.qual, args.comp, args.culture,
                        override=args.override, hard_block=args.hard_block)
    except ValueError as exc:
        print(f"verdict: {exc}", file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps(result, ensure_ascii=False))
    else:
        print(f'{result["label"]} (trigger: {result["trigger"]})')
    return 0


if __name__ == "__main__":
    sys.exit(main())
