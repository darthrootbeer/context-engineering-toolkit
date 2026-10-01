#!/usr/bin/env python3
"""Check that a findings file only claims what the posting and the profile support.

The model reads the posting and writes a findings file. This script is the gate
between that file and the scores. It exits 1, and the offline chain stops, when:

  - a rating other than Unknown has no quote, or the quote is not in the
    posting text (case, whitespace, curly quotes and dashes are normalised)
  - an autonomy or micromanagement read that leans negative rests only on
    generic phrases ("partner with", "work closely", "stakeholder" and so on).
    Silence is Unknown, not a bad rating.
  - a perk, hustle phrase, low-time-off note, soft flag or negative phrase has
    no quote found in the posting
  - an evidence id does not exist in the profile, or points at evidence marked
    do_not_use or written by someone else
  - the findings lane, the posting's lane and the profile's lanes disagree

Usage:
    check_findings.py FINDINGS --posting POSTING --profile PROFILE

Exit: 0 clean, 1 problems found (one plain line each), 2 could not run.
"""
import argparse
import json
import re
import sys
from pathlib import Path

RATINGS = {"strong", "fair", "weak", "poor", "unknown"}

# Phrases that appear in most senior postings whatever the real autonomy is.
GENERIC = [
    "partner with", "work closely", "collaborate", "cross-functional",
    "stakeholder", "align with", "drive alignment", "coordinate with",
    "liaise", "escalate", "set deadlines", "provide input", "work with",
]
# Language that genuinely says who decides, who reviews, who owns.
REAL = [
    "micromanage", "approval", "sign-off", "sign off", "review cycle",
    "oversight", "autonomy", "own the", "ownership", "trusted", "reports to",
    "approval chain", "gate", "permission", "supervis", "directed by",
    "reviewed by", "advocate", "decision is not", "not the decision",
    "influence", "buy-in", "convince", "persuade", "recommend", "propose",
    "cannot say", "can't say", "no mandate", "seat at",
]

# Words that belong to the scoring rules, not to a plain-language reason.
RUBRIC_TERMS = [
    "4a", "4b", "4c", "4d", "job-type override", "score floor",
    "autonomy_filter", "qualifications_match", "reservations band",
]

QUOTE_MARKS = str.maketrans({
    "‘": "'", "’": "'", "‚": "'", "‛": "'",
    "“": '"', "”": '"', "„": '"',
    "–": "-", "—": "-", "−": "-", " ": " ",
    "…": "...",
})


def normalise(text):
    """Lowercase, straighten quotes and dashes, collapse whitespace."""
    text = str(text).translate(QUOTE_MARKS).lower()
    return re.sub(r"\s+", " ", text).strip()


def split_posting(raw):
    """Return (frontmatter dict, posting text).

    A saved posting note starts with YAML frontmatter and may carry an
    assessment block above a "Full posting text" heading. Only the posting
    text counts as something a quote can come from.
    """
    import yaml

    meta = {}
    body = raw
    match = re.match(r"\A---\s*\n(.*?)\n---\s*\n?", raw, re.S)
    if match:
        try:
            meta = yaml.safe_load(match.group(1)) or {}
        except yaml.YAMLError:
            meta = {}
        body = raw[match.end():]
    heading = re.search(r"^#+\s*full posting text.*$", body, re.I | re.M)
    if heading:
        body = body[heading.end():]
    return (meta if isinstance(meta, dict) else {}), body


def _generic_only(quote):
    q = normalise(quote)
    return any(g in q for g in GENERIC) and not any(r in q for r in REAL)


def check(findings, posting_text, posting_lane, profile):
    """Return a list of problem lines. An empty list means clean."""
    problems = []
    posting_norm = normalise(posting_text)

    def add(path, message):
        problems.append(f"{path}: {message}")

    def quote_ok(path, quote):
        """True if the quote is present and found. Adds a problem if not."""
        if not isinstance(quote, str) or not quote.strip():
            add(path, "has no quote from the posting.")
            return False
        if normalise(quote) not in posting_norm:
            add(path, f'quote "{quote[:60]}" was not found in the posting text.')
            return False
        return True

    if not isinstance(findings, dict):
        return ["findings: the file is not a JSON object."]

    lanes = {l.get("name"): l for l in profile.get("lanes") or []}
    evidence = {e.get("id"): e for e in profile.get("evidence") or []}
    skills = {s.get("id") for s in profile.get("skills") or []}
    perks = {p.get("id") for p in (profile.get("culture") or {}).get("perks") or []}
    blocks = {b.get("id") for b in profile.get("hard_blocks") or []}
    exceptions = {e.get("block_id") for e in profile.get("named_exceptions") or []}

    # Lane: findings, posting and profile must agree.
    lane_name = findings.get("lane")
    if lane_name not in lanes:
        add("lane", f'"{lane_name}" is not a lane in the profile.')
    if posting_lane and lane_name != posting_lane:
        add("lane", f'findings say "{lane_name}" but the posting says "{posting_lane}".')
    lane = lanes.get(lane_name) or {}
    requirement_ids = {r.get("id") for r in lane.get("requirements") or []}

    # Hard block.
    block = findings.get("hard_block") or {}
    if block.get("tripped"):
        if block.get("id") not in blocks:
            add("hard_block.id", f'"{block.get("id")}" is not a hard block in the profile.')
        quote_ok("hard_block.quote", block.get("quote"))
        if block.get("named_exception") and block.get("id") not in exceptions:
            add("hard_block.named_exception",
                f'no named exception for "{block.get("id")}" exists in the profile.')

    # Job-type override.
    override = findings.get("job_type_override") or {}
    if override.get("fired"):
        if not override.get("skill"):
            add("job_type_override.skill", "fired but names no skill.")
        quotes = override.get("quotes") or []
        if not quotes:
            add("job_type_override.quotes", "fired but quotes nothing from the posting.")
        for i, q in enumerate(quotes):
            quote_ok(f"job_type_override.quotes[{i}]", q)

    # Requirement ratings. Silence is Unknown. Anything else needs a quote.
    for i, item in enumerate(findings.get("requirements") or []):
        path = f"requirements[{i}]"
        rating = str(item.get("rating", "")).lower()
        if rating not in RATINGS:
            add(f"{path}.rating", f'"{item.get("rating")}" is not strong, fair, weak, poor or unknown.')
            continue
        if lane and item.get("id") not in requirement_ids:
            add(f"{path}.id", f'"{item.get("id")}" is not a requirement in lane "{lane_name}".')
        if rating == "unknown":
            continue
        found = quote_ok(f"{path}.quote", item.get("quote"))
        rid = str(item.get("id", "")).lower()
        is_autonomy = "micromanag" in rid or "autonomy" in rid
        if found and is_autonomy and rating in ("fair", "weak", "poor") and _generic_only(item["quote"]):
            add(f"{path}.quote",
                "a read on autonomy rests only on generic phrases. The posting is silent, so rate it unknown.")

    # Autonomy read.
    autonomy = findings.get("autonomy") or {}
    if autonomy.get("net") in ("negative", "mixed"):
        quotes = autonomy.get("quotes") or []
        if not quotes:
            add("autonomy.quotes", "a read on autonomy quotes nothing from the posting.")
        found = [q for i, q in enumerate(quotes) if quote_ok(f"autonomy.quotes[{i}]", q)]
        if found and all(_generic_only(q) for q in found):
            add("autonomy.quotes",
                "the autonomy read rests only on generic phrases. The posting is silent, so it is unknown, not negative.")

    # Culture: every change needs a quote.
    culture = findings.get("culture") or {}
    for i, perk in enumerate(culture.get("perks") or []):
        if perk.get("perk_id") not in perks:
            add(f"culture.perks[{i}].perk_id", f'"{perk.get("perk_id")}" is not a perk in the profile.')
        quote_ok(f"culture.perks[{i}].quote", perk.get("quote"))
    for key in ("strong_positive_phrases", "hustle", "negative_phrases", "soft_flags_tripped"):
        for i, entry in enumerate(culture.get(key) or []):
            quote_ok(f"culture.{key}[{i}].quote", entry.get("quote"))
    low = culture.get("low_time_off")
    if isinstance(low, dict):
        quote_ok("culture.low_time_off.quote", low.get("quote"))
    elif low:
        add("culture.low_time_off", "has no quote from the posting.")

    # Qualifications: every claim points at real, usable evidence.
    qual = findings.get("qualifications") or {}
    for i, match in enumerate(qual.get("matches") or []):
        path = f"qualifications.matches[{i}]"
        quote_ok(f"{path}.requirement_quote", match.get("requirement_quote"))
        ids = match.get("evidence_ids") or []
        if not ids:
            add(f"{path}.evidence_ids", "a match with no evidence behind it. Write it as unproven instead.")
        for ev_id in ids:
            entry = evidence.get(ev_id)
            if entry is None:
                add(f"{path}.evidence_ids", f'"{ev_id}" is not an evidence id in the profile.')
            elif entry.get("proof") == "do_not_use":
                add(f"{path}.evidence_ids", f'"{ev_id}" is marked do_not_use and cannot back a claim.')
            elif entry.get("authorship") == "OTHER-AUTHOR":
                add(f"{path}.evidence_ids", f'"{ev_id}" is work someone else wrote and cannot back a claim.')
    for i, item in enumerate(qual.get("unproven") or []):
        path = f"qualifications.unproven[{i}]"
        if item.get("skill_id") not in skills:
            add(f"{path}.skill_id", f'"{item.get("skill_id")}" is not a skill in the profile.')
        quote_ok(f"{path}.requirement_quote", item.get("requirement_quote"))

    # The one-line reason is for a person, not for the rubric.
    reason = findings.get("verdict_reason")
    if not isinstance(reason, str) or not reason.strip():
        add("verdict_reason", "is missing.")
    else:
        lowered = reason.lower()
        for term in RUBRIC_TERMS:
            if re.search(rf"(?<![\w-]){re.escape(term)}(?![\w-])", lowered):
                add("verdict_reason", f'uses the rubric term "{term}". Write it in plain words.')
    return problems


def main(argv=None):
    ap = argparse.ArgumentParser(description="Check a findings file against its posting and profile.")
    ap.add_argument("findings")
    ap.add_argument("--posting", required=True)
    ap.add_argument("--profile", required=True)
    args = ap.parse_args(argv)
    try:
        import yaml

        findings = json.loads(Path(args.findings).read_text(encoding="utf-8"))
        raw = Path(args.posting).read_text(encoding="utf-8")
        profile = yaml.safe_load(Path(args.profile).read_text(encoding="utf-8")) or {}
    except Exception as exc:
        print(f"check_findings: could not read inputs: {exc}", file=sys.stderr)
        return 2
    meta, text = split_posting(raw)
    problems = check(findings, text, meta.get("lane"), profile)
    for line in problems:
        print(line)
    if problems:
        print(f"check_findings: {len(problems)} problem(s).")
        return 1
    print("check_findings: ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
