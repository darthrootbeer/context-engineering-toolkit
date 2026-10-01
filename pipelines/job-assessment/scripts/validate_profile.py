#!/usr/bin/env python3
"""Check a career-profile.yaml against its schema and the rules a schema cannot express.

Usage:
    validate_profile.py PROFILE [--fixture] [--json]

Exit codes:
    0  no errors (warnings may still be printed)
    1  one or more errors
    2  could not run (file missing, not YAML, schema missing)

Each problem is one plain line on stdout, starting with its YAML path, for example:
    skills[3].evidence_ids: "ev-missing" is not an evidence id in this file.
Warnings start with "warning: ". A one-line summary goes to stderr, so stdout holds
only the problems themselves.

Errors:
    1. Schema violations (types, allowed values, required fields, unknown fields).
    2. Every cross-reference resolves (skill -> evidence, evidence -> employer,
       known gap -> skill, writing sample -> evidence, named exception -> hard block).
    3. Ids are unique within their section. Lane names are unique.
    4. Pay numbers that are present run in order:
       floor <= min <= open_ask <= target <= stretch_ceiling.
    5. Evidence from an interview or a reference cannot be marked proof: checked,
       because nobody has read a document that backs it.
    6. No field holds an email-shaped or phone-shaped string.
    7. A self_score of 4 or 5 with last: never is a contradiction.
    8. --fixture only: the first line is the FICTIONAL banner and every URL is on
       example.com, example.org or example.net.

Warnings (exit stays 0): a skill at 3 or above with no evidence, evidence with no
dates, a strong requirement with no reason, an empty perks list, a lane with no
requirements of its own.
"""
from __future__ import annotations

import argparse
import datetime as _dt
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

try:
    import yaml
    from jsonschema import Draft202012Validator
except ImportError as exc:  # pragma: no cover - environment problem
    print(f"validate_profile: missing dependency ({exc.name}). Run: pip install -r requirements.txt", file=sys.stderr)
    sys.exit(2)

HERE = Path(__file__).resolve().parent
SCHEMA_PATH = HERE.parent / "schema" / "career-profile.schema.json"

BANNER = "# FICTIONAL EXAMPLE DATA. Not a real person."
PAY_ORDER = ["floor", "min", "open_ask", "target", "stretch_ceiling"]
UNCHECKABLE_SOURCES = ("interview", "reference")

EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}")
PHONE_RE = re.compile(
    r"(\(\d{3}\)\s?|\b\d{3}[-. ])\d{3}[-. ]\d{4}\b"
    r"|\+\d{1,3}[ -]\d{2,4}[ -]\d{3,4}[ -]\d{3,4}"
)
URL_RE = re.compile(r"https?://[^\s)>\"']+")
EXAMPLE_HOST_RE = re.compile(r"^https?://([A-Za-z0-9-]+\.)*example\.(com|org|net)(:\d+)?([/?#]|$)")


class CannotRun(Exception):
    """The check could not run at all (exit 2)."""


@dataclass
class Problem:
    path: str
    rule: str
    message: str

    def __str__(self) -> str:
        return f"{self.path}: {self.message}"


# ---------------------------------------------------------------- loading


def _plain(value):
    """Turn YAML dates into ISO strings so the schema sees text, as the file shows it."""
    if isinstance(value, dict):
        return {k: _plain(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_plain(v) for v in value]
    if isinstance(value, (_dt.date, _dt.datetime)):
        return value.isoformat()
    return value


def load_schema() -> dict:
    try:
        return json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise CannotRun(f"cannot read schema {SCHEMA_PATH.name}: {exc}") from exc


def load_profile(path: Path) -> tuple[dict, str]:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise CannotRun(f"cannot read {path}: {exc.strerror or exc}") from exc
    try:
        data = yaml.safe_load(text)
    except yaml.YAMLError as exc:
        raise CannotRun(f"{path} is not valid YAML: {exc}") from exc
    if not isinstance(data, dict):
        raise CannotRun(f"{path} does not hold a YAML mapping at the top level")
    return _plain(data), text


# ---------------------------------------------------------------- helpers


def yaml_path(parts) -> str:
    out = ""
    for part in parts:
        if isinstance(part, int):
            out += f"[{part}]"
        else:
            out += ("." if out else "") + str(part)
    return out or "(top level)"


def _show(value) -> str:
    if isinstance(value, str):
        return f'"{value}"'
    return json.dumps(value)


def _items(data: dict, key: str) -> list:
    value = data.get(key)
    return value if isinstance(value, list) else []


def _dicts(seq):
    for i, item in enumerate(seq):
        if isinstance(item, dict):
            yield i, item


def _walk_strings(value, parts=()):
    if isinstance(value, dict):
        for k, v in value.items():
            yield from _walk_strings(v, parts + (k,))
    elif isinstance(value, list):
        for i, v in enumerate(value):
            yield from _walk_strings(v, parts + (i,))
    elif isinstance(value, str):
        yield parts, value


# ---------------------------------------------------------------- rule 1: schema


def _schema_message(err) -> str:
    v = err.validator
    if v == "required":
        missing = err.message.split("'")[1] if "'" in err.message else err.message
        return f'missing required field "{missing}".'
    if v == "additionalProperties":
        extra = sorted(set(err.instance) - set(err.schema.get("properties", {})))
        names = ", ".join(f'"{e}"' for e in extra)
        return f"unknown field {names}. The schema has no such field."
    if v == "enum":
        allowed = ", ".join("null" if a is None else str(a) for a in err.validator_value)
        return f"{_show(err.instance)} is not an allowed value (allowed: {allowed})."
    if v == "const":
        return f"{_show(err.instance)} must be {_show(err.validator_value)}."
    if v == "type":
        want = err.validator_value
        want = " or ".join(want) if isinstance(want, list) else want
        return f"{_show(err.instance)} should be of type {want}."
    if v == "pattern":
        return f"{_show(err.instance)} does not match the expected format ({err.schema.get('description') or err.validator_value})."
    if v in ("minimum", "maximum"):
        word = "at least" if v == "minimum" else "at most"
        return f"{_show(err.instance)} should be {word} {err.validator_value}."
    if v == "minLength":
        return "should not be empty."
    if v == "minItems":
        return f"needs at least {err.validator_value} item(s)."
    if v == "uniqueItems":
        return "lists the same value more than once."
    if v == "anyOf":
        return f"{_show(err.instance)} is not an accepted value ({err.schema.get('description', 'see the schema')})."
    return err.message + "."


def check_schema(data: dict, schema: dict) -> list[Problem]:
    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(data), key=lambda e: [str(p) for p in e.absolute_path])
    return [Problem(yaml_path(e.absolute_path), "schema", _schema_message(e)) for e in errors]


# ---------------------------------------------------------------- rules 2 and 3


def _ids(data: dict, section: str, key: str = "id") -> set:
    return {item.get(key) for _, item in _dicts(_items(data, section)) if isinstance(item.get(key), str)}


def check_unique(data: dict) -> list[Problem]:
    problems = []
    sections = [
        ("sources", "key"), ("hard_blocks", "id"), ("soft_flags", "id"),
        ("benefits_and_terms", "id"), ("lanes", "name"), ("employers", "id"),
        ("evidence", "id"), ("skills", "id"), ("writing_samples", "id"),
    ]
    for section, key in sections:
        seen = {}
        for i, item in _dicts(_items(data, section)):
            value = item.get(key)
            if not isinstance(value, str):
                continue
            if value in seen:
                problems.append(Problem(f"{section}[{i}].{key}", "unique",
                                        f'{_show(value)} is already used by {section}[{seen[value]}].'))
            else:
                seen[value] = i
    culture = data.get("culture") if isinstance(data.get("culture"), dict) else {}
    seen = {}
    for i, perk in _dicts(culture.get("perks") or []):
        value = perk.get("id")
        if isinstance(value, str):
            if value in seen:
                problems.append(Problem(f"culture.perks[{i}].id", "unique",
                                        f'{_show(value)} is already used by culture.perks[{seen[value]}].'))
            else:
                seen[value] = i
    for li, lane in _dicts(_items(data, "lanes")):
        for sub in ("requirements", "known_gaps"):
            seen = {}
            for i, item in _dicts(lane.get(sub) or []):
                value = item.get("id")
                if not isinstance(value, str):
                    continue
                if value in seen:
                    problems.append(Problem(f"lanes[{li}].{sub}[{i}].id", "unique",
                                            f'{_show(value)} is already used by lanes[{li}].{sub}[{seen[value]}].'))
                else:
                    seen[value] = i
    return problems


def check_references(data: dict) -> list[Problem]:
    problems = []
    evidence_ids = _ids(data, "evidence")
    employer_ids = _ids(data, "employers")
    skill_ids = _ids(data, "skills")
    block_ids = _ids(data, "hard_blocks")

    for i, skill in _dicts(_items(data, "skills")):
        refs = skill.get("evidence_ids")
        for ref in refs if isinstance(refs, list) else []:
            if isinstance(ref, str) and ref not in evidence_ids:
                problems.append(Problem(f"skills[{i}].evidence_ids", "reference",
                                        f"{_show(ref)} is not an evidence id in this file."))
    for i, ev in _dicts(_items(data, "evidence")):
        ref = ev.get("employer_id")
        if isinstance(ref, str) and ref not in employer_ids:
            problems.append(Problem(f"evidence[{i}].employer_id", "reference",
                                    f"{_show(ref)} is not an employer id in this file."))
    for li, lane in _dicts(_items(data, "lanes")):
        for gi, gap in _dicts(lane.get("known_gaps") or []):
            ref = gap.get("skill_id")
            if isinstance(ref, str) and ref not in skill_ids:
                problems.append(Problem(f"lanes[{li}].known_gaps[{gi}].skill_id", "reference",
                                        f"{_show(ref)} is not a skill id in this file."))
    for i, sample in _dicts(_items(data, "writing_samples")):
        ref = sample.get("evidence_id")
        if isinstance(ref, str) and ref not in evidence_ids:
            problems.append(Problem(f"writing_samples[{i}].evidence_id", "reference",
                                    f"{_show(ref)} is not an evidence id in this file."))
    for i, exc in _dicts(_items(data, "named_exceptions")):
        ref = exc.get("block_id")
        if isinstance(ref, str) and ref not in block_ids:
            problems.append(Problem(f"named_exceptions[{i}].block_id", "reference",
                                    f"{_show(ref)} is not a hard block id in this file."))
    return problems


# ---------------------------------------------------------------- rules 4 to 7


def check_pay_order(data: dict) -> list[Problem]:
    comp = data.get("comp")
    if not isinstance(comp, dict):
        return []
    present = [(k, comp[k]) for k in PAY_ORDER
               if isinstance(comp.get(k), (int, float)) and not isinstance(comp.get(k), bool)]
    problems = []
    for (lo_key, lo), (hi_key, hi) in zip(present, present[1:]):
        if lo > hi:
            problems.append(Problem("comp", "pay-order",
                                    f"pay numbers out of order: {lo_key} ({lo}) is above {hi_key} ({hi}). "
                                    "Expected floor <= min <= open_ask <= target <= stretch_ceiling."))
    return problems


def check_proof(data: dict) -> list[Problem]:
    problems = []
    for i, ev in _dicts(_items(data, "evidence")):
        source = ev.get("source") if isinstance(ev.get("source"), dict) else {}
        kind = source.get("type")
        if kind in UNCHECKABLE_SOURCES and ev.get("proof") == "checked":
            problems.append(Problem(f"evidence[{i}].proof", "proof",
                                    f"source.type {kind} cannot carry proof: checked. Nothing was read to back it; "
                                    "use unchecked, or point source at a document, link or artifact."))
    return problems


def check_contact(data: dict) -> list[Problem]:
    problems = []
    for parts, value in _walk_strings(data):
        if EMAIL_RE.search(value):
            problems.append(Problem(yaml_path(parts), "contact",
                                    "holds an email-shaped string. Contact details do not belong in this file."))
        elif PHONE_RE.search(value):
            problems.append(Problem(yaml_path(parts), "contact",
                                    "holds a phone-shaped string. Contact details do not belong in this file."))
    return problems


def check_score_contradictions(data: dict) -> list[Problem]:
    problems = []
    for i, skill in _dicts(_items(data, "skills")):
        score = skill.get("self_score")
        if isinstance(score, int) and score >= 4 and skill.get("last") == "never":
            problems.append(Problem(f"skills[{i}]", "self-score",
                                    f"self_score {score} with last: never is a contradiction. "
                                    "A score of 4 or 5 needs some real use; lower the score or fix last."))
    return problems


# ---------------------------------------------------------------- rule 8: fixtures


def check_fixture(data: dict, raw_text: str) -> list[Problem]:
    problems = []
    first = raw_text.splitlines()[0].rstrip() if raw_text else ""
    if first != BANNER:
        problems.append(Problem("line 1", "fixture",
                                f"first line must be the banner '{BANNER}'."))
    for parts, value in _walk_strings(data):
        for url in URL_RE.findall(value):
            if not EXAMPLE_HOST_RE.match(url):
                problems.append(Problem(yaml_path(parts), "fixture",
                                        "URL is not on example.com, example.org or example.net."))
                break
    return problems


# ---------------------------------------------------------------- warnings


def collect_warnings(data: dict) -> list[Problem]:
    warnings = []
    for i, skill in _dicts(_items(data, "skills")):
        score = skill.get("self_score")
        if isinstance(score, int) and score >= 3 and not skill.get("evidence_ids"):
            warnings.append(Problem(f"skills[{i}]", "unproven",
                                    f"{_show(skill.get('id'))} is scored {score} but has no evidence_ids. "
                                    "Assessments will report it as unproven."))
    for i, ev in _dicts(_items(data, "evidence")):
        dates = ev.get("dates")
        if not isinstance(dates, dict) or not (dates.get("start") or dates.get("end")):
            warnings.append(Problem(f"evidence[{i}]", "no-dates",
                                    f"{_show(ev.get('id'))} has no dates, so it cannot be judged recent or stale."))
    for li, lane in _dicts(_items(data, "lanes")):
        reqs = lane.get("requirements")
        if isinstance(reqs, list) and not reqs:
            warnings.append(Problem(f"lanes[{li}].requirements", "empty-lane",
                                    f"lane {_show(lane.get('name'))} has no requirements of its own."))
        for ri, req in _dicts(reqs if isinstance(reqs, list) else []):
            why = req.get("why")
            if req.get("severity") == "strong" and not (isinstance(why, str) and why.strip()):
                warnings.append(Problem(f"lanes[{li}].requirements[{ri}]", "no-why",
                                        f"strong requirement {_show(req.get('id'))} has no why."))
    culture = data.get("culture")
    if isinstance(culture, dict) and not culture.get("perks"):
        warnings.append(Problem("culture.perks", "no-perks",
                                "the perks list is empty, so no perk can raise Culture."))
    return warnings


# ---------------------------------------------------------------- entry points


def validate(data: dict, raw_text: str = "", fixture: bool = False,
             schema: dict | None = None) -> tuple[list[Problem], list[Problem]]:
    """Return (errors, warnings) for an already-loaded profile."""
    data = _plain(data)
    errors = check_schema(data, schema if schema is not None else load_schema())
    errors += check_references(data)
    errors += check_unique(data)
    errors += check_pay_order(data)
    errors += check_proof(data)
    errors += check_contact(data)
    errors += check_score_contradictions(data)
    if fixture:
        errors += check_fixture(data, raw_text)
    return errors, collect_warnings(data)


def validate_file(path: Path, fixture: bool = False) -> tuple[list[Problem], list[Problem]]:
    data, text = load_profile(path)
    return validate(data, text, fixture=fixture)


def report(path: Path, errors: list[Problem], warnings: list[Problem], as_json: bool,
           out=sys.stdout, err=sys.stderr) -> int:
    code = 1 if errors else 0
    if as_json:
        json.dump({
            "file": str(path),
            "ok": not errors,
            "errors": [asdict(p) for p in errors],
            "warnings": [asdict(p) for p in warnings],
        }, out, indent=2)
        out.write("\n")
        return code
    for p in errors:
        print(str(p), file=out)
    for p in warnings:
        print(f"warning: {p}", file=out)
    state = f"{len(errors)} problem(s)" if errors else "clean"
    print(f"validate_profile: {state}, {len(warnings)} warning(s) in {path.name}", file=err)
    return code


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Check a career-profile.yaml.")
    parser.add_argument("profile", type=Path)
    parser.add_argument("--fixture", action="store_true",
                        help="also require the FICTIONAL banner and example-domain URLs only")
    parser.add_argument("--json", action="store_true", help="print the result as JSON")
    args = parser.parse_args(argv)
    try:
        errors, warnings = validate_file(args.profile, fixture=args.fixture)
    except CannotRun as exc:
        print(f"validate_profile: could not run: {exc}", file=sys.stderr)
        return 2
    return report(args.profile, errors, warnings, args.json)


if __name__ == "__main__":
    sys.exit(main())
