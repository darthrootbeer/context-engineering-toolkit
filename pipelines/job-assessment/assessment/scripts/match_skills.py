#!/usr/bin/env python3
"""List which of the person's skills a job posting mentions.

Reads the posting text, runs each skill's `match` patterns from the career
profile against it, and prints every hit with the self-score, the preference
for future work, recency, how the skill was used, whether it is backed by
evidence, and the sentence that matched. It does NOT score or judge.

Patterns are broad on purpose, so every hit must be read in its sentence
before it counts. A pattern for a computer-vision skill will match "vision"
in "medical, dental and vision insurance". The sentence is printed so that
false hit is easy to see and drop.

A skill is "backed" when at least one of its evidence ids points at an
evidence entry that can be used: not `proof: do_not_use` and not
`authorship: OTHER-AUTHOR`. Otherwise it is "unproven". A self-score is the
person's own claim, never evidence.

Usage:
    match_skills.py posting.md --profile career-profile.yaml
    match_skills.py - --profile career-profile.yaml --json    # text on stdin
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

NEXT = {"more": "want more", "neutral": "don't mind", "avoid": "RATHER AVOID"}
LAST = {"2y": "within 2 yrs", "5y": "2-5 yrs ago", "5plus": "5+ yrs ago", "never": "never used"}
HOW = {"self": "myself", "ai": "directed AI", "team": "taught/led others"}

UNUSABLE_PROOF = {"do_not_use"}
UNUSABLE_AUTHORSHIP = {"OTHER-AUTHOR"}

BUCKET_ORDER = [
    "strength (4-5)",
    "solid (3)",
    "stretch (2)",
    "gap (0-1)",
    "unscored",
]


def posting_text(arg: str) -> str:
    raw = sys.stdin.read() if arg == "-" else Path(arg).read_text(encoding="utf-8")
    marker = re.search(r"^## Full posting text\s*$", raw, re.M)
    if marker:
        raw = raw[marker.end():]
    # Drop file notes that are not claims: frontmatter, comments, headings.
    raw = re.sub(r"\A---\n.*?\n---\n", "", raw, flags=re.S)
    raw = re.sub(r"<!--.*?-->", "", raw, flags=re.S)
    return re.sub(r"^#{1,6} .*$", "", raw, flags=re.M)


def snippet(text: str, m: re.Match) -> str:
    start = max(text.rfind("\n", 0, m.start()), text.rfind(". ", 0, m.start()) + 1, m.start() - 110)
    end_candidates = [i for i in (text.find("\n", m.end()), text.find(". ", m.end())) if i != -1]
    end = min(end_candidates + [m.end() + 110])
    return " ".join(text[start:end].split())[:220]


def load_profile(path: Path) -> dict:
    import yaml

    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path} is not a career profile")
    return data


def bucket_for(score) -> str:
    if score is None:
        return "unscored"
    if score <= 1:
        return "gap (0-1)"
    if score == 2:
        return "stretch (2)"
    if score == 3:
        return "solid (3)"
    return "strength (4-5)"


def evidence_status(skill: dict, evidence_by_id: dict) -> tuple[str, bool]:
    """Return ("backed" | "unproven", only_unchecked).

    `only_unchecked` is True when the usable evidence is all `proof:
    unchecked`, which the read has to call "your own account, not yet backed
    by a document".
    """
    usable = []
    for ev_id in skill.get("evidence_ids") or []:
        ev = evidence_by_id.get(ev_id)
        if not ev:
            continue
        if ev.get("proof") in UNUSABLE_PROOF or ev.get("authorship") in UNUSABLE_AUTHORSHIP:
            continue
        usable.append(ev)
    if not usable:
        return "unproven", False
    return "backed", all(ev.get("proof") == "unchecked" for ev in usable)


def find_hits(text: str, profile: dict) -> list[dict]:
    evidence_by_id = {
        e.get("id"): e for e in profile.get("evidence") or [] if isinstance(e, dict)
    }
    hits = []
    for skill in profile.get("skills") or []:
        if not isinstance(skill, dict):
            continue
        for rx in skill.get("match") or []:
            try:
                m = re.search(rx, text, re.IGNORECASE)
            except re.error as exc:
                print(f"warning: skill {skill.get('id')!r} has a bad pattern {rx!r}: {exc}", file=sys.stderr)
                continue
            if m:
                status, only_unchecked = evidence_status(skill, evidence_by_id)
                score = skill.get("self_score")
                hits.append(
                    {
                        "skill_id": skill.get("id"),
                        "label": skill.get("label"),
                        "group": skill.get("group"),
                        "self_score": score,
                        "bucket": bucket_for(score),
                        "next": skill.get("next"),
                        "last": skill.get("last"),
                        "how": skill.get("how") or [],
                        "status": status,
                        "only_unchecked": only_unchecked,
                        "evidence_ids": skill.get("evidence_ids") or [],
                        "snippet": snippet(text, m),
                    }
                )
                break
    return hits


def print_text(hits: list[dict], profile: dict) -> None:
    total = len([s for s in profile.get("skills") or [] if isinstance(s, dict)])
    no_pattern = sum(
        1 for s in profile.get("skills") or [] if isinstance(s, dict) and not s.get("match")
    )
    print(
        f"Skill matches: {len(hits)} of {total} skills mentioned "
        f"(skills with no pattern can't match: {no_pattern}).\n"
    )
    print("Read every hit in its sentence. A broad pattern can match a word used in another sense.\n")
    for name in BUCKET_ORDER:
        rows = [h for h in hits if h["bucket"] == name]
        if not rows:
            continue
        print(f"== {name.upper()} ({len(rows)})")
        for h in sorted(rows, key=lambda r: -(r["self_score"] or 0)):
            tags = [
                NEXT.get(h["next"], ""),
                LAST.get(h["last"], ""),
                "/".join(HOW[x] for x in h["how"] if x in HOW),
            ]
            tag = " · ".join(t for t in tags if t)
            proof = h["status"].upper()
            if h["status"] == "backed" and h["only_unchecked"]:
                proof = "BACKED (own account, unchecked)"
            score = h["self_score"] if h["self_score"] is not None else "?"
            print(f"- [{score}] {h['label']}  <{proof}>" + (f"  ({tag})" if tag else ""))
            print(f"    \"{h['snippet']}\"")
        print()

    avoid = [h["label"] for h in hits if h["next"] == "avoid"]
    want = [h["label"] for h in hits if h["next"] == "more"]
    unproven = [h["label"] for h in hits if h["status"] == "unproven"]
    print("RATHER AVOID hits: " + (", ".join(avoid) if avoid else "none"))
    print("WANT MORE hits: " + (", ".join(want) if want else "none"))
    print("UNPROVEN hits (no usable evidence, cannot be claimed): " + (", ".join(unproven) if unproven else "none"))


def main(argv: list[str] | None = None) -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("posting", help="archived posting .md file, or - for stdin")
    ap.add_argument("--profile", required=True, type=Path, help="career-profile.yaml")
    ap.add_argument("--json", action="store_true", help="print the hits as JSON")
    args = ap.parse_args(argv)

    try:
        profile = load_profile(args.profile)
    except (OSError, ValueError) as exc:
        print(f"Could not read the profile: {exc}", file=sys.stderr)
        sys.exit(1)

    hits = find_hits(posting_text(args.posting), profile)

    if args.json:
        print(json.dumps({"hits": hits}, indent=2, ensure_ascii=False))
    else:
        print_text(hits, profile)


if __name__ == "__main__":
    main()
