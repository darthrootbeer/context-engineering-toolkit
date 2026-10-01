#!/usr/bin/env python3
"""Fill the assessment card and write it as a local HTML file.

    render_email.py --note NOTE.md --findings F.json --scores S.json \
                    --verdict V --out DIR [--profile P.yaml] [--date YYYY-MM-DD]

This script never sends anything. It writes DIR/<slug>.html and prints the file
path and a suggested subject line. What you do with the file is up to you.

Inputs
  --note      the archived posting note. Its front matter supplies company, role
              and the posting URL (url, job_url, posting_url or source_url).
  --findings  the findings JSON (schema/findings.schema.json).
  --scores    JSON with fit, comp, qualifications, culture (whole numbers 0 to 10).
  --verdict   a JSON file with "label" (and optionally "trigger"), or one of the
              words apply, reservations, skip.
  --profile   optional career-profile YAML, used only to show requirement labels
              instead of ids.
Overrides: --job-url, --company, --role, --note-link, --next-prompt.

Exit codes: 0 card written, 1 input problem, 2 the finished card failed
check_email.py (nothing is written in that case).
"""
import argparse
import html
import json
import re
import sys
from datetime import date
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from check_email import card_problems, real_http_url  # noqa: E402

TEMPLATE = Path(__file__).resolve().parent.parent / "templates" / "assessment-email.html"

VERDICTS = {
    "apply": ("Apply", "#ecfdf5", "#059669", "\U0001F7E2"),
    "reservations": ("Apply with reservations", "#fffbeb", "#d97706", "\U0001F7E1"),
    "skip": ("Skip", "#fef2f2", "#dc2626", "\U0001F534"),
}
SCORE_ROWS = (("fit", "Fit"), ("comp", "Comp"), ("qualifications", "Qualifications"), ("culture", "Culture"))
RATING_COLORS = {
    "strong": "#16a34a", "fair": "#ca8a04", "weak": "#ea580c", "poor": "#dc2626", "unknown": "#9ca3af",
}
AUTONOMY_RATING = {"positive": "strong", "neutral": "fair", "negative": "poor"}
URL_KEYS = ("url", "job_url", "posting_url", "source_url")


class InputError(Exception):
    pass


def round_half_up(x):
    return int(float(x) + 0.5)


def score_color(n):
    if n >= 10:
        return "#7c3aed"
    if n >= 7:
        return "#16a34a"
    if n >= 5:
        return "#eab308"
    if n >= 3:
        return "#ea580c"
    return "#dc2626"


def esc(value):
    return html.escape(str(value), quote=True)


def read_json(path, what):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError) as err:
        raise InputError("cannot read %s %s: %s" % (what, path, err))


def read_front_matter(path):
    try:
        text = Path(path).read_text(encoding="utf-8")
    except OSError as err:
        raise InputError("cannot read note %s: %s" % (path, err))
    m = re.match(r"---\s*\n(.*?)\n---\s*(\n|$)", text, re.S)
    if not m:
        return {}
    try:
        data = yaml.safe_load(m.group(1))
    except yaml.YAMLError as err:
        raise InputError("note front matter is not valid YAML: %s" % err)
    return data if isinstance(data, dict) else {}


def parse_verdict(value):
    p = Path(value)
    raw = value
    if p.is_file():
        data = read_json(p, "verdict")
        raw = data.get("label") or data.get("verdict") or ""
    key = str(raw).strip().lower()
    if key.startswith("apply with") or key == "reservations":
        return VERDICTS["reservations"]
    if key in ("apply", "skip"):
        return VERDICTS[key]
    raise InputError("verdict must be Apply, Apply with reservations or Skip, got: %r" % raw)


def parse_scores(path):
    data = read_json(path, "scores")
    data = data.get("scores", data)
    out = {}
    for key, _ in SCORE_ROWS:
        if key not in data:
            raise InputError("scores file has no %r" % key)
        out[key] = max(0, min(10, round_half_up(data[key])))
    return out


def requirement_labels(profile_path, lane):
    if not profile_path:
        return {}
    try:
        profile = yaml.safe_load(Path(profile_path).read_text(encoding="utf-8")) or {}
    except (OSError, yaml.YAMLError) as err:
        raise InputError("cannot read profile %s: %s" % (profile_path, err))
    labels = {}
    for entry in profile.get("lanes", []):
        if entry.get("name") == lane:
            for req in entry.get("requirements", []):
                labels[req.get("id")] = req.get("label")
    return labels


def build_checks(findings, labels):
    rows = []
    for req in findings.get("requirements", []):
        rating = str(req.get("rating", "unknown")).lower()
        name = labels.get(req.get("id")) or str(req.get("id", "")).replace("_", " ").capitalize()
        rows.append((name, rating, req.get("read", "")))
    autonomy = findings.get("autonomy")
    if autonomy:
        rows.append(("Autonomy", AUTONOMY_RATING.get(autonomy.get("net"), "unknown"), autonomy.get("read", "")))
    pay = findings.get("pay")
    if pay:
        if pay.get("stated") and pay.get("top") is not None:
            rows.append(("Pay", "unknown", "The posting lists base pay up to %s." % pay["top"]))
        else:
            rows.append(("Pay", "unknown", "The posting does not list pay."))
    return rows


def expand(template, name, rows):
    """Replace the BEGIN/END block called name with one copy per dict in rows."""
    pat = re.compile(r"<!-- BEGIN %s -->\n?(.*?)<!-- END %s -->\n?" % (name, name), re.S)
    m = pat.search(template)
    if not m:
        raise InputError("template has no %s block" % name)
    body = "".join(fill(m.group(1), row) for row in rows)
    return template[:m.start()] + body + template[m.end():]


def fill(text, values):
    for key, val in values.items():
        text = text.replace("{{%s}}" % key, val)
    return text


def slugify(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-") or "assessment"


def render(args):
    template = TEMPLATE.read_text(encoding="utf-8")
    fm = read_front_matter(args.note)
    findings = read_json(args.findings, "findings")
    scores = parse_scores(args.scores)
    label, bg, color, dot = parse_verdict(args.verdict)

    company = args.company or fm.get("company") or ""
    role = args.role or fm.get("role") or ""
    if not company or not role:
        raise InputError("company and role are needed: put them in the note front matter or pass --company and --role")
    job_url = args.job_url or next((str(fm[k]) for k in URL_KEYS if fm.get(k)), "")
    if not real_http_url(job_url):
        raise InputError("no real http(s) job posting URL: put url in the note front matter or pass --job-url")

    checks = build_checks(findings, requirement_labels(args.profile, findings.get("lane")))
    next_prompt = args.next_prompt or (
        "Open the saved assessment for %s, %s. Check each claim in it against the posting "
        "text, then help me decide whether to apply." % (company, role)
    )

    score_rows = [
        {
            "SCORE_LABEL": esc(name), "SCORE_COLOR": score_color(scores[key]),
            "SCORE_PCT": str(scores[key] * 10), "SCORE_REMAINDER_PCT": str(100 - scores[key] * 10),
            "SCORE_VALUE": str(scores[key]),
        }
        for key, name in SCORE_ROWS
    ]
    check_rows = [
        {
            "CHECK_NAME": esc(name), "CHECK_DOT_COLOR": RATING_COLORS.get(rating, RATING_COLORS["unknown"]),
            "CHECK_RATING": esc(rating.capitalize()), "CHECK_READ": esc(read),
        }
        for name, rating, read in checks
    ]

    page = expand(template, "score-row", score_rows)
    page = expand(page, "check-row", check_rows)
    if args.note_link:
        page = expand(page, "note-link", [{"NOTE_URL": esc(args.note_link)}])
    else:
        page = expand(page, "note-link", [])
    page = fill(page, {
        "JOB_URL": esc(job_url), "VERDICT_BG": bg, "VERDICT_COLOR": color, "VERDICT_LABEL": esc(label),
        "COMPANY": esc(company), "ROLE": esc(role),
        "VERDICT_REASON": esc(findings.get("verdict_reason", "")), "NEXT_PROMPT": esc(next_prompt),
    })
    subject = "%s Job Assessment: %s - %s - %s" % (dot, company, role, args.date)
    return page, subject, slugify("%s %s" % (company, role))


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--note", required=True)
    ap.add_argument("--findings", required=True)
    ap.add_argument("--scores", required=True)
    ap.add_argument("--verdict", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--profile")
    ap.add_argument("--date", default=date.today().isoformat())
    ap.add_argument("--job-url")
    ap.add_argument("--company")
    ap.add_argument("--role")
    ap.add_argument("--note-link", help="optional link to the saved note; the button is left out without it")
    ap.add_argument("--next-prompt")
    args = ap.parse_args(argv)
    try:
        page, subject, slug = render(args)
    except InputError as err:
        print("render_email: %s" % err, file=sys.stderr)
        return 1
    problems = card_problems(page)
    if problems:
        print("render_email: the finished card failed the card check, nothing written:", file=sys.stderr)
        for item in problems:
            print("  - " + item, file=sys.stderr)
        return 2
    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / (slug + ".html")
    target.write_text(page, encoding="utf-8")
    print("wrote %s" % target)
    print("subject: %s" % subject)
    return 0


if __name__ == "__main__":
    sys.exit(main())
