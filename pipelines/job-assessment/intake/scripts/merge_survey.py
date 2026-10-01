#!/usr/bin/env python3
"""Merge a saved skills-survey file into the skills list of career-profile.yaml.

Usage
  merge_survey.py PROFILE SURVEY_JSON [--catalog FILE] [--out FILE] [--dry-run]
  merge_survey.py --build-html [--catalog FILE] [--html FILE]
  merge_survey.py --check-html [--catalog FILE] [--html FILE]

Merge mode
  Reads the JSON file the survey page saved, looks each answered item up in the
  catalog, and writes it into the profile's skills list. Items the survey left
  blank are skipped, never written as zero. An existing skill with the same id
  keeps its evidence_ids and any extra fields; only the survey's own answers
  (self_score, next, last, how) are replaced. Skills that are not in the survey
  are left alone. Evidence links are never created, changed or removed here:
  linking a skill to evidence is a separate intake step.

  Only the skills: block of the YAML file is rewritten. Every other line,
  including comments and the banner, is kept as it was. Free-text notes typed
  into the survey have no field in the profile, so they are counted in the
  report and not stored. If any answered item is invalid, nothing is written.

  Exit codes: 0 merged (or dry run clean), 1 refused because of problems,
  2 could not run (missing file, unreadable file).

Build mode
  --build-html copies the catalog into the survey page, between the
  CATALOG-BEGIN and CATALOG-END markers, so the page works opened straight from
  disk (a page cannot read a neighbouring file from file://). --check-html does
  the same comparison without writing and exits 1 when the page is stale.

Needs only PyYAML.
"""
import argparse
import datetime
import json
import os
import re
import sys

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_CATALOG = os.path.join(HERE, "..", "templates", "skills-catalog.yaml")
DEFAULT_HTML = os.path.join(HERE, "..", "templates", "skills-survey.html")

SURVEY_FORMAT = "skills-survey"
NEXT_VALUES = ("more", "neutral", "avoid")
LAST_VALUES = ("2y", "5y", "5plus", "never")
HOW_VALUES = ("self", "ai", "team")
MARK_BEGIN = "/*CATALOG-BEGIN*/"
MARK_END = "/*CATALOG-END*/"

# Order in which the survey's answers are written for each skill.
OWNED_FIELDS = ("self_score", "next", "last", "how")


class MergeError(Exception):
    """The merge cannot run (bad input file), as opposed to bad answers."""


# ---------------------------------------------------------------- catalog


def load_catalog(path):
    try:
        with open(path, encoding="utf-8") as fh:
            cat = yaml.safe_load(fh)
    except (OSError, yaml.YAMLError) as exc:
        raise MergeError("cannot read catalog %s: %s" % (path, exc))
    if not isinstance(cat, dict) or not isinstance(cat.get("groups"), list):
        raise MergeError("catalog %s has no groups list" % path)
    return cat


def catalog_problems(cat):
    """Return a list of plain-text problems with the catalog itself."""
    problems = []
    seen = {}
    group_ids = set()
    if not isinstance(cat.get("catalog_version"), int):
        problems.append("catalog_version must be a whole number")
    for gi, g in enumerate(cat.get("groups", [])):
        where = "groups[%d]" % gi
        for key in ("id", "title", "blurb", "zero", "five"):
            if not str(g.get(key, "")).strip():
                problems.append("%s.%s is missing" % (where, key))
        if g.get("id") in group_ids:
            problems.append("%s: duplicate group id %r" % (where, g.get("id")))
        group_ids.add(g.get("id"))
        items = g.get("items") or []
        if not items:
            problems.append("%s has no items" % where)
        for ii, it in enumerate(items):
            iw = "%s.items[%d]" % (where, ii)
            for key in ("id", "label", "desc"):
                if not str(it.get(key, "")).strip():
                    problems.append("%s.%s is missing" % (iw, key))
            if it.get("id") in seen:
                problems.append("%s: duplicate item id %r" % (iw, it.get("id")))
            seen[it.get("id")] = g.get("id")
            if not re.match(r"^[a-z0-9]+(-[a-z0-9]+)*$", str(it.get("id", ""))):
                problems.append("%s: id %r is not lowercase words joined by hyphens" % (iw, it.get("id")))
            pats = it.get("match")
            if not isinstance(pats, list) or not pats:
                problems.append("%s.match must be a non-empty list" % iw)
                continue
            for p in pats:
                try:
                    re.compile(p, re.IGNORECASE)
                except (re.error, TypeError) as exc:
                    problems.append("%s.match %r does not compile: %s" % (iw, p, exc))
    return problems


def catalog_index(cat):
    """Map item id to (item, group id)."""
    out = {}
    for g in cat["groups"]:
        for it in g.get("items", []):
            out[it["id"]] = (it, g["id"])
    return out


# ----------------------------------------------------------------- survey


def load_survey(path):
    try:
        with open(path, encoding="utf-8") as fh:
            data = json.load(fh)
    except (OSError, ValueError) as exc:
        raise MergeError("cannot read survey file %s: %s" % (path, exc))
    if not isinstance(data, dict) or data.get("format") != SURVEY_FORMAT:
        raise MergeError("%s is not a skills-survey file (format must be %r)" % (path, SURVEY_FORMAT))
    if not isinstance(data.get("items"), dict):
        raise MergeError("%s has no items object" % path)
    return data


def survey_answers(survey, index):
    """Validate the survey. Return (answers, problems, skipped, notes).

    answers maps item id to the fields to write, in the profile's names.
    skipped counts items with no score. notes counts items carrying a note.
    """
    answers = {}
    problems = []
    skipped = 0
    notes = 0
    for item_id, raw in survey["items"].items():
        if item_id not in index:
            problems.append("items.%s: not an item in the catalog" % item_id)
            continue
        if not isinstance(raw, dict):
            problems.append("items.%s: must be an object" % item_id)
            continue
        if str(raw.get("note", "")).strip():
            notes += 1
        score = raw.get("score")
        if score is None:
            skipped += 1
            continue
        if isinstance(score, bool) or not isinstance(score, int) or not 0 <= score <= 5:
            problems.append("items.%s.score: %r is not a whole number from 0 to 5" % (item_id, score))
            continue
        entry = {"self_score": score}
        nxt = raw.get("next")
        if nxt is not None:
            if nxt not in NEXT_VALUES:
                problems.append("items.%s.next: %r is not one of %s" % (item_id, nxt, "/".join(NEXT_VALUES)))
            else:
                entry["next"] = nxt
        last = raw.get("last")
        if last is not None:
            if last not in LAST_VALUES:
                problems.append("items.%s.last: %r is not one of %s" % (item_id, last, "/".join(LAST_VALUES)))
            else:
                entry["last"] = last
        how = raw.get("how")
        if how is not None:
            if not isinstance(how, list) or any(h not in HOW_VALUES for h in how):
                problems.append("items.%s.how: must be a list drawn from %s" % (item_id, "/".join(HOW_VALUES)))
            else:
                entry["how"] = [h for h in HOW_VALUES if h in how]
        if score >= 4 and entry.get("last") == "never":
            problems.append(
                "items.%s: a score of %d with last used 'never' does not fit; "
                "fix one of them in the survey" % (item_id, score)
            )
        answers[item_id] = entry
    return answers, problems, skipped, notes


# ------------------------------------------------------------------ merge


def merge_skills(existing, cat, answers):
    """Return (new skills list, added ids, updated ids)."""
    index = catalog_index(cat)
    out = [dict(s) for s in existing]
    by_id = {s.get("id"): s for s in out}
    added, updated = [], []
    for item_id in index:  # catalog order keeps new entries predictable
        if item_id not in answers:
            continue
        item, group_id = index[item_id]
        answer = answers[item_id]
        if item_id in by_id:
            entry = by_id[item_id]
            for field in OWNED_FIELDS:
                if field in answer:
                    entry[field] = answer[field]
                else:
                    entry.pop(field, None)
            updated.append(item_id)
        else:
            entry = {
                "id": item_id,
                "label": item["label"],
                "group": group_id,
                "match": list(item["match"]),
            }
            entry.update(answer)
            entry["evidence_ids"] = []
            out.append(entry)
            by_id[item_id] = entry
            added.append(item_id)
    return out, added, updated


# ------------------------------------------------------ YAML text surgery


def _scalar(value):
    if isinstance(value, bool):
        return "true" if value else "false"
    if value is None:
        return "null"
    if isinstance(value, (int, float)):
        return repr(value)
    if isinstance(value, datetime.date):
        return value.isoformat()
    text = str(value)
    plain = re.match(r"^[A-Za-z0-9_][A-Za-z0-9_ ./-]*$", text) and not text.endswith(" ")
    if plain and yaml.safe_load(text) == text:
        return text
    return "'" + text.replace("'", "''") + "'"


def _value(value):
    if isinstance(value, list) and all(not isinstance(v, (list, dict)) for v in value):
        return "[" + ", ".join(_scalar(v) for v in value) + "]"
    if isinstance(value, (list, dict)):
        flow = yaml.safe_dump(value, default_flow_style=True, width=10 ** 6, allow_unicode=True)
        return flow.replace("\n...\n", "").strip()
    return _scalar(value)


def render_skills(skills):
    """Render the skills list as YAML lines, two-space indented under skills:."""
    if not skills:
        return ["skills: []\n"]
    lines = ["skills:\n"]
    for skill in skills:
        keys = list(skill.keys())
        for n, key in enumerate(keys):
            prefix = "  - " if n == 0 else "    "
            lines.append("%s%s: %s\n" % (prefix, key, _value(skill[key])))
    return lines


def replace_skills_block(text, skills):
    """Return text with its top-level skills: block replaced by `skills`."""
    lines = text.splitlines(keepends=True)
    if lines and not lines[-1].endswith("\n"):
        lines[-1] += "\n"
    start = next((i for i, ln in enumerate(lines) if re.match(r"^skills\s*:", ln)), None)
    new_block = render_skills(skills)
    if start is None:
        if lines and lines[-1].strip():
            lines.append("\n")
        return "".join(lines + new_block)
    end = start + 1
    while end < len(lines) and not re.match(r"^[A-Za-z_][\w-]*\s*:", lines[end]):
        end += 1
    # blank lines and column-0 comments just before the next key belong to it
    while end > start + 1 and (not lines[end - 1].strip() or lines[end - 1].startswith("#")):
        end -= 1
    # comment lines directly under "skills:" are the author's guidance; keep them
    keep = []
    k = start + 1
    while k < end and (not lines[k].strip() or lines[k].lstrip().startswith("#")):
        keep.append(lines[k])
        k += 1
    if k == end:  # block held only comments, so there was nothing to merge into
        keep = lines[start + 1:end]
    return "".join(lines[:start] + new_block[:1] + keep + new_block[1:] + lines[end:])


def merge_into_text(text, cat, answers):
    """Return (new text, added, updated). Verifies nothing else changed."""
    try:
        before = yaml.safe_load(text)
    except yaml.YAMLError as exc:
        raise MergeError("profile is not valid YAML: %s" % exc)
    if before is None:
        before = {}
    if not isinstance(before, dict):
        raise MergeError("profile must be a YAML mapping at the top level")
    existing = before.get("skills") or []
    if not isinstance(existing, list) or any(not isinstance(s, dict) for s in existing):
        raise MergeError("profile skills must be a list of mappings")
    merged, added, updated = merge_skills(existing, cat, answers)
    new_text = replace_skills_block(text, merged)
    after = yaml.safe_load(new_text)
    for key in set(before) | set(after):
        if key != "skills" and before.get(key) != after.get(key):
            raise MergeError("internal check failed: %r changed during the merge; nothing written" % key)
    if after.get("skills") != merged:
        raise MergeError("internal check failed: the written skills differ from the merge; nothing written")
    return new_text, added, updated


# --------------------------------------------------------------- survey page


def catalog_for_page(cat):
    """The slice of the catalog the page needs (no match patterns)."""
    return {
        "catalog_version": cat["catalog_version"],
        "groups": [
            {
                "id": g["id"],
                "title": g["title"],
                "blurb": g["blurb"],
                "zero": g["zero"],
                "five": g["five"],
                "items": [{"id": i["id"], "label": i["label"], "desc": i["desc"]} for i in g["items"]],
            }
            for g in cat["groups"]
        ],
    }


def page_json(cat):
    text = json.dumps(catalog_for_page(cat), ensure_ascii=False, sort_keys=True, indent=1)
    return text.replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026")


def embed_catalog(html, cat):
    """Return html with the catalog JSON placed between the two markers."""
    b = html.find(MARK_BEGIN)
    e = html.find(MARK_END)
    if b < 0 or e < 0 or e < b:
        raise MergeError("survey page is missing the %s and %s markers" % (MARK_BEGIN, MARK_END))
    return html[: b + len(MARK_BEGIN)] + page_json(cat) + html[e:]


# -------------------------------------------------------------------- CLI


def read_text(path):
    try:
        with open(path, encoding="utf-8") as fh:
            return fh.read()
    except OSError as exc:
        raise MergeError("cannot read %s: %s" % (path, exc))


def write_text(path, text):
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as fh:
        fh.write(text)
    os.replace(tmp, path)


def run_merge(args):
    cat = load_catalog(args.catalog)
    bad = catalog_problems(cat)
    if bad:
        for p in bad:
            print("catalog: " + p)
        return 1
    survey = load_survey(args.survey)
    if survey.get("catalog_version") != cat["catalog_version"]:
        print(
            "note: survey was saved against catalog version %r, this catalog is version %r"
            % (survey.get("catalog_version"), cat["catalog_version"])
        )
    index = catalog_index(cat)
    answers, problems, skipped, notes = survey_answers(survey, index)
    if problems:
        for p in problems:
            print(p)
        print("merge_survey: refused, %d problem(s); nothing written" % len(problems))
        return 1
    text = read_text(args.profile)
    new_text, added, updated = merge_into_text(text, cat, answers)
    print(
        "merge_survey: %d answered, %d skipped as blank; %d skills added, %d updated"
        % (len(answers), skipped, len(added), len(updated))
    )
    if notes:
        print("merge_survey: %d survey note(s) not stored; the profile has no field for them" % notes)
    if args.dry_run:
        print("merge_survey: dry run, nothing written")
        return 0
    target = args.out or args.profile
    write_text(target, new_text)
    print("merge_survey: wrote %s" % target)
    print("next: run scripts/validate_profile.py on it, then link each skill scored 3 or higher to its evidence")
    return 0


def run_html(args, check):
    cat = load_catalog(args.catalog)
    bad = catalog_problems(cat)
    if bad:
        for p in bad:
            print("catalog: " + p)
        return 1
    html = read_text(args.html)
    new_html = embed_catalog(html, cat)
    if check:
        if new_html != html:
            print("merge_survey: %s is out of date; run merge_survey.py --build-html" % args.html)
            return 1
        print("merge_survey: survey page matches the catalog")
        return 0
    write_text(args.html, new_html)
    print("merge_survey: wrote catalog into %s" % args.html)
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description="Merge a skills survey into career-profile.yaml.")
    ap.add_argument("profile", nargs="?", help="career-profile.yaml to update")
    ap.add_argument("survey", nargs="?", help="JSON file saved by the survey page")
    ap.add_argument("--catalog", default=DEFAULT_CATALOG)
    ap.add_argument("--out", help="write the merged profile here instead of in place")
    ap.add_argument("--dry-run", action="store_true", help="report what would change, write nothing")
    ap.add_argument("--build-html", action="store_true", help="copy the catalog into the survey page")
    ap.add_argument("--check-html", action="store_true", help="exit 1 when the survey page is stale")
    ap.add_argument("--html", default=DEFAULT_HTML)
    args = ap.parse_args(argv)
    try:
        if args.build_html or args.check_html:
            return run_html(args, check=args.check_html)
        if not args.profile or not args.survey:
            ap.error("PROFILE and SURVEY_JSON are required")
        return run_merge(args)
    except MergeError as exc:
        print("merge_survey: " + str(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
