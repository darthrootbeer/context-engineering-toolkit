#!/usr/bin/env python3
"""Render the assessment block and the terminal summary.

Pure formatting. It takes the findings, the scores and the verdict that the
other scripts produced and lays them out. It decides nothing.

Score bars are ten segments. N segments in the score's tier color, then empty
squares. A 10 is ten stars. A 0 is ten empty squares.

  1-2 red, 3-4 orange, 5-6 yellow, 7-9 green, 10 stars

Usage:
    render_assessment.py FINDINGS --scores SCORES --verdict VERDICT
                         --profile PROFILE [--terminal] [--date YYYY-MM-DD]

SCORES is the JSON from score_helpers.py. VERDICT is the JSON from
verdict.py --json. Without --terminal it prints the markdown block that
write_assessment.py inserts into the saved note.

Exit: 0 rendered, 2 could not run.
"""
import argparse
import datetime
import json
import sys
from pathlib import Path

SCORE_ORDER = (("fit", "Fit"), ("comp", "Comp"),
               ("qualifications", "Qualifications"), ("culture", "Culture"))

RATING_TEXT = {
    "strong": "🟢 Strong",
    "fair": "🟡 Fair",
    "weak": "🟠 Weak",
    "poor": "🔴 Poor",
    "unknown": "❓ Unknown",
}
LEGEND = "🟢 Strong · 🟡 Fair · 🟠 Weak · 🔴 Poor · ❓ Unknown"
EMPTY = "⬛"
STAR = "🌟"


def tier_segment(score):
    """The colored segment for a score, or None when it has none (0, 10)."""
    if score <= 0:
        return None
    if score <= 2:
        return "🔴"
    if score <= 4:
        return "🟠"
    if score <= 6:
        return "🟡"
    if score <= 9:
        return "🟢"
    return STAR


def bar(score):
    """Ten segments. N filled in the tier color, the rest empty."""
    score = max(0, min(10, int(score)))
    segment = tier_segment(score)
    if segment is None:
        return EMPTY * 10
    return segment * score + EMPTY * (10 - score)


def score_lines(scores):
    """One line per category, always Fit, Comp, Qualifications, Culture."""
    return [f"{label} {scores[key]} {bar(scores[key])}" for key, label in SCORE_ORDER]


def _label_for(profile, lane_name, requirement_id):
    for lane in profile.get("lanes") or []:
        if lane.get("name") == lane_name:
            for req in lane.get("requirements") or []:
                if req.get("id") == requirement_id:
                    return req.get("label") or requirement_id
    return requirement_id


def _cell(text):
    """Keep a table cell on one line."""
    return " ".join(str(text or "").replace("|", "/").split())


def _rating_text(rating):
    return RATING_TEXT.get(str(rating).lower(), RATING_TEXT["unknown"])


def _autonomy_rating(net):
    return {"positive": "strong", "mixed": "fair", "negative": "weak"}.get(str(net).lower(), "unknown")


def _company_line(findings):
    read = findings.get("company_read") or {}
    status = read.get("status", "none")
    if status == "none":
        return None
    name = read.get("name", "This company")
    reason = read.get("stored_reason")
    kind = {"high_interest": "one you have said you want to work for",
            "good_not_dream": "a good company, not a dream one"}.get(status, status)
    text = f"{name} is {kind}."
    if reason:
        text += f" Your reason: {reason}"
    return text + " This did not change the scores or the verdict."


def _verdict_text(verdict, findings):
    reason = (findings.get("verdict_reason") or "").strip()
    return verdict["label"], reason


def render_block(findings, scores, verdict, profile, date):
    """The assessment block, as markdown."""
    lane = findings.get("lane")
    label, reason = _verdict_text(verdict, findings)
    out = ["## Assessment", "", f"**🚦 Verdict:** {label}"]
    if reason:
        out.append(reason)
    out += ["", "**Scores:**"] + [f"{line}  " for line in score_lines(scores)]
    out += ["", f"**Assessed:** {date}", ""]

    block = findings.get("hard_block") or {}
    out.append("### ⛔ Hard blocks")
    if block.get("tripped"):
        text = f'{block.get("id")} was tripped: "{block.get("quote")}"'
        if block.get("named_exception"):
            text += f" A named exception covers it: {block['named_exception']}."
        out.append(text)
    else:
        out.append("None tripped.")
    out.append("")

    company = _company_line(findings)
    out += ["### 🏢 The company itself",
            company or "No stored reaction for this company. This did not change the scores or the verdict.", ""]

    out += ["### ✅ / ⚠️ Requirements", "", "| Criterion | Rating | Read |", "|---|---|---|"]
    for item in findings.get("requirements") or []:
        read = item.get("read") or ""
        if item.get("quote"):
            read = f'"{item["quote"]}" {read}'.strip()
        out.append(f"| {_cell(_label_for(profile, lane, item.get('id')))} | "
                   f"{_rating_text(item.get('rating'))} | {_cell(read)} |")
    out.append("")

    autonomy = findings.get("autonomy") or {}
    out += ["### 🎯 How much say you'd actually have",
            autonomy.get("read") or "The posting does not say.", ""]

    signals = findings.get("keyword_signals_found") or []
    out += ["### 🔑 Language worth noticing", ""]
    if signals:
        out += ["| Phrase | What it signals |", "|---|---|"]
        out += [f'| "{_cell(s.get("phrase"))}" | {_cell(s.get("read"))} |' for s in signals]
    else:
        out.append("Nothing stood out.")
    new = findings.get("new_signals_to_consider") or []
    if new:
        out += ["", "Worth adding to your criteria: " + ", ".join(f'"{n}"' for n in new) + "."]
    out.append("")

    out += ["### 🧩 How well the skills line up"]
    out += _skills_lines(findings, profile)
    out.append("")

    out += ["### 🚩 Other things worth knowing", "", "| Item | Read |", "|---|---|"]
    rows = _other_rows(findings)
    out += rows if rows else ["| Nothing else | The posting raised nothing more. |"]
    return "\n".join(out).rstrip() + "\n"


def _skills_lines(findings, profile):
    qual = findings.get("qualifications") or {}
    evidence = {e.get("id"): e for e in profile.get("evidence") or []}
    lines = []
    for match in qual.get("matches") or []:
        notes = []
        for ev_id in match.get("evidence_ids") or []:
            entry = evidence.get(ev_id) or {}
            claim = entry.get("claim", ev_id)
            if entry.get("proof") == "unchecked":
                claim += " (your own account, not yet backed by a document)"
            notes.append(claim)
        lines.append(f'- "{match.get("requirement_quote")}" lines up with: ' + "; ".join(notes))
    for item in qual.get("unproven") or []:
        lines.append(f'- "{item.get("requirement_quote")}": you rate yourself here, '
                     f'but nothing in your file proves it ({item.get("skill_id")}).')
    if qual.get("years_required") is not None:
        lines.append(f"- Years asked for: {qual['years_required']}.")
    if qual.get("working_style_mismatch"):
        lines.append("- This role expects you to become the expert, not to gather it from others.")
    return lines or ["Nothing in the posting lined up with your file either way."]


def _other_rows(findings):
    rows = []
    pay = findings.get("pay") or {}
    if not pay.get("stated"):
        rows.append("| Pay | Not listed. Scored as unknown, not as bad. |")
    for note in pay.get("other_pay_noted") or []:
        rows.append(f"| Other pay | {_cell(note)} |")
    for flag in (findings.get("culture") or {}).get("soft_flags_tripped") or []:
        rows.append(f'| {_cell(flag.get("id"))} | "{_cell(flag.get("quote"))}" |')
    return rows


def render_terminal(findings, scores, verdict, profile):
    """The short table printed to the screen."""
    lane = findings.get("lane")
    label, _ = _verdict_text(verdict, findings)
    out = [f"ASSESSMENT: {findings.get('posting_file', 'posting')}", "",
           f"🚦 VERDICT: {label}", ""]
    company = _company_line(findings)
    if company:
        out += [f"🏢 {company}", ""]
    out += ["**Scores:**"] + [f"{line}  " for line in score_lines(scores)]
    out += ["", "| Check | Rating | Read |", "|---|---|---|"]
    block = findings.get("hard_block") or {}
    if block.get("tripped"):
        out.append(f"| Hard block | 🔴 Poor | {_cell(block.get('id'))} |")
    for item in findings.get("requirements") or []:
        out.append(f"| {_cell(_label_for(profile, lane, item.get('id')))} | "
                   f"{_rating_text(item.get('rating'))} | {_cell(item.get('read'))} |")
    autonomy = findings.get("autonomy") or {}
    if autonomy:
        out.append(f"| How much say you'd have | {_rating_text(_autonomy_rating(autonomy.get('net')))} | "
                   f"{_cell(autonomy.get('read'))} |")
    out += ["", LEGEND]
    return "\n".join(out) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(description="Render the assessment block or terminal summary.")
    ap.add_argument("findings")
    ap.add_argument("--scores", required=True)
    ap.add_argument("--verdict", required=True)
    ap.add_argument("--profile", required=True)
    ap.add_argument("--terminal", action="store_true")
    ap.add_argument("--date", default=None, help="YYYY-MM-DD, default today")
    args = ap.parse_args(argv)
    try:
        import yaml

        findings = json.loads(Path(args.findings).read_text(encoding="utf-8"))
        scores = json.loads(Path(args.scores).read_text(encoding="utf-8"))
        verdict = json.loads(Path(args.verdict).read_text(encoding="utf-8"))
        profile = yaml.safe_load(Path(args.profile).read_text(encoding="utf-8")) or {}
    except Exception as exc:
        print(f"render_assessment: could not read inputs: {exc}", file=sys.stderr)
        return 2
    date = args.date or datetime.date.today().isoformat()
    if args.terminal:
        sys.stdout.write(render_terminal(findings, scores, verdict, profile))
    else:
        sys.stdout.write(render_block(findings, scores, verdict, profile, date))
    return 0


if __name__ == "__main__":
    sys.exit(main())
