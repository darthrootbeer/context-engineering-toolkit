#!/usr/bin/env python3
"""The one checked door every intake write goes through.

Usage:
    add_entry.py PROFILE --section NAME --entry -        (YAML entry on stdin)
    add_entry.py PROFILE --section NAME --entry FILE
    add_entry.py PROFILE --section NAME --entry - --replace

Exit codes:
    0  written (the full validator result is printed after the write)
    1  refused, and the profile file was not touched

What it does, in order:
    1. Reads one entry (a YAML mapping).
    2. Checks it against the schema for that section, plus the rules that only
       need the entry itself: no email- or phone-shaped text, no proof: checked
       on an interview or reference source, no self_score 4 or 5 with last: never.
    3. For list sections, refuses an id that is already in the file. With
       --replace it does the opposite: it replaces the entry that has that id,
       and refuses if there is none. This is how a stored entry is corrected
       instead of kept twice.
    4. Writes the file (atomically), then runs the full validator and prints
       its result. Cross-references are checked there, not here, because during
       an interview a skill can be written before the evidence it will point to.

List sections append one entry: sources, hard_blocks, named_exceptions,
soft_flags, benefits_and_terms, lanes, employers, evidence, skills,
writing_samples.
Mapping sections merge the entry's top-level keys into the stored mapping:
person, comp, culture, company_criteria, meta.

Note: the file is rewritten by a YAML library, so comments inside the body are
not kept. The leading comment block (for example the FICTIONAL banner on a
fixture) is kept.
"""
from __future__ import annotations

import argparse
import os
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import yaml  # noqa: E402
from jsonschema import Draft202012Validator  # noqa: E402

import validate_profile as vp  # noqa: E402

# How each list section identifies an entry.
KEY_FIELD = {"sources": "key", "lanes": "name"}
COMPOSITE_KEY = {"named_exceptions": ("company", "block_id")}


def _section_kind(schema: dict, section: str):
    """Return ('list'|'mapping', def_name) or None when the section is not editable."""
    prop = schema.get("properties", {}).get(section)
    if not prop or section == "schema_version":
        return None
    if prop.get("type") == "array" and "$ref" in prop.get("items", {}):
        return "list", prop["items"]["$ref"].rsplit("/", 1)[-1]
    if "$ref" in prop:
        return "mapping", prop["$ref"].rsplit("/", 1)[-1]
    return None


def _sub_validator(schema: dict, def_name: str) -> Draft202012Validator:
    sub = {"$schema": schema.get("$schema"), "$defs": schema["$defs"], "$ref": f"#/$defs/{def_name}"}
    return Draft202012Validator(sub)


def _entry_key(section: str, entry: dict):
    if section in COMPOSITE_KEY:
        return tuple(entry.get(f) for f in COMPOSITE_KEY[section])
    return entry.get(KEY_FIELD.get(section, "id"))


def _key_label(section: str, key) -> str:
    if isinstance(key, tuple):
        return " + ".join(f'"{k}"' for k in key)
    return f'"{key}"'


def _entry_rule_problems(section: str, kind: str, entry: dict) -> list:
    """Entry-local rules from the full validator, with paths rewritten to 'entry'."""
    wrapped = {section: [entry]} if kind == "list" else {section: entry}
    prefix = f"{section}[0]" if kind == "list" else section
    problems = (vp.check_contact(wrapped) + vp.check_proof(wrapped)
                + vp.check_score_contradictions(wrapped))
    for p in problems:
        p.path = "entry" + p.path[len(prefix):] if p.path.startswith(prefix) else p.path
    return problems


def _split_header(text: str) -> str:
    """The leading run of comment and blank lines, kept verbatim on rewrite."""
    header = []
    for line in text.splitlines(keepends=True):
        if line.lstrip().startswith("#") or not line.strip():
            header.append(line)
        else:
            break
    return "".join(header)


def _write_atomic(path: Path, text: str) -> None:
    fd, tmp = tempfile.mkstemp(prefix=f".{path.name}.", dir=str(path.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            fh.write(text)
        os.replace(tmp, path)
    except BaseException:
        if os.path.exists(tmp):
            os.unlink(tmp)
        raise


def refuse(lines) -> int:
    for line in lines:
        print(line)
    print("add_entry: refused. The profile file was not changed.", file=sys.stderr)
    return 1


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Add one checked entry to a career-profile.yaml.")
    parser.add_argument("profile", type=Path)
    parser.add_argument("--section", required=True)
    parser.add_argument("--entry", required=True, help="'-' for stdin, or a path to a YAML file")
    parser.add_argument("--replace", action="store_true",
                        help="replace the stored entry with the same id instead of adding one")
    args = parser.parse_args(argv)

    try:
        schema = vp.load_schema()
    except vp.CannotRun as exc:
        return refuse([f"could not run: {exc}"])

    kind_def = _section_kind(schema, args.section)
    if kind_def is None:
        editable = [s for s in schema["properties"] if _section_kind(schema, s)]
        return refuse([f'--section: "{args.section}" is not a section this tool writes. '
                       f"Choose one of: {', '.join(editable)}."])
    kind, def_name = kind_def

    try:
        raw_entry = sys.stdin.read() if args.entry == "-" else Path(args.entry).read_text(encoding="utf-8")
        entry = yaml.safe_load(raw_entry)
    except OSError as exc:
        return refuse([f"--entry: cannot read {args.entry}: {exc.strerror or exc}"])
    except yaml.YAMLError as exc:
        return refuse([f"entry: not valid YAML: {exc}"])
    if not isinstance(entry, dict) or not entry:
        return refuse(["entry: must be one YAML mapping (key: value lines), not empty and not a list."])

    if not args.profile.exists():
        return refuse([f"{args.profile}: file does not exist. Copy intake/templates/career-profile.template.yaml first."])
    try:
        original_text = args.profile.read_text(encoding="utf-8")
        data = yaml.safe_load(original_text)
    except (OSError, yaml.YAMLError) as exc:
        return refuse([f"{args.profile}: cannot read it as YAML: {exc}"])
    if not isinstance(data, dict):
        return refuse([f"{args.profile}: does not hold a YAML mapping at the top level."])

    validator = _sub_validator(schema, def_name)

    if kind == "list":
        problems = [vp.Problem("entry." + vp.yaml_path(e.absolute_path) if e.absolute_path else "entry",
                               "schema", vp._schema_message(e))
                    for e in validator.iter_errors(vp._plain(entry))]
        problems += _entry_rule_problems(args.section, kind, vp._plain(entry))
        if problems:
            return refuse(str(p) for p in problems)

        stored = data.get(args.section)
        if stored is None:
            stored = []
        if not isinstance(stored, list):
            return refuse([f"{args.section}: the stored value is not a list, so nothing can be added to it."])
        key = _entry_key(args.section, entry)
        match = [i for i, item in enumerate(stored)
                 if isinstance(item, dict) and _entry_key(args.section, item) == key]
        if args.replace:
            if not match:
                return refuse([f"entry: {_key_label(args.section, key)} is not in {args.section}, "
                               "so there is nothing to replace. Drop --replace to add it."])
            stored[match[0]] = entry
            action = "replaced"
        else:
            if match:
                return refuse([f"entry: {_key_label(args.section, key)} is already in "
                               f"{args.section}[{match[0]}]. Use a new id, or --replace to correct the stored entry."])
            stored.append(entry)
            action = "added"
        data[args.section] = stored
        label = _key_label(args.section, key)
    else:
        stored = data.get(args.section) or {}
        if not isinstance(stored, dict):
            return refuse([f"{args.section}: the stored value is not a mapping."])
        merged = dict(stored)
        merged.update(entry)
        problems = [vp.Problem(f"{args.section}.{vp.yaml_path(e.absolute_path)}" if e.absolute_path
                               else args.section, "schema", vp._schema_message(e))
                    for e in validator.iter_errors(vp._plain(merged))]
        problems += _entry_rule_problems(args.section, kind, vp._plain(entry))
        if problems:
            return refuse(str(p) for p in problems)
        data[args.section] = merged
        action = "updated"
        label = ", ".join(entry.keys())

    body = yaml.safe_dump(data, sort_keys=False, allow_unicode=True, default_flow_style=False, width=100)
    _write_atomic(args.profile, _split_header(original_text) + body)
    print(f"add_entry: {action} {args.section} {label} in {args.profile.name}")

    try:
        errors, warnings = vp.validate_file(args.profile)
    except vp.CannotRun as exc:  # pragma: no cover - we just wrote valid YAML
        print(f"validate_profile: could not run: {exc}")
        return 0
    vp.report(args.profile, errors, warnings, as_json=False, out=sys.stdout, err=sys.stdout)
    return 0


if __name__ == "__main__":
    sys.exit(main())
