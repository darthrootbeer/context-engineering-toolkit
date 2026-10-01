#!/usr/bin/env python3
"""Write a finished assessment block into an archived posting note.

The block goes directly under the note's `**Application status:**` line,
before the `---` divider, so the assessment is the first thing anyone sees.
Everything below that divider (the requirements table and the full posting
text) is left exactly as the archive step wrote it.

Also updates the frontmatter:
  - `how_to_use_this_file` now says an assessment exists.
  - `updated`, `state`, `state_updated`, `next_action`, `next_action_due`.

State follows the verdict. Skip sets `closed`. Apply and Apply with
reservations set `apply_ready` with the next action "Decide: apply, hold, or
skip". `pending` leaves the state alone. A good verdict never moves a note
past `apply_ready`: a note already further along (materials, applied,
interview, and so on) keeps its state, because moving on needs the person's
own decision.

Re-running replaces the block between its markers. There is one current
verdict per note, not a history, and the block says when it was re-assessed.

Exit codes: 0 written, 1 refused (the note is left untouched).

Usage:
    write_assessment.py NOTE.md --block assessment.md --verdict apply --date 2026-10-01
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

START = "<!-- assessment:start -->"
END = "<!-- assessment:end -->"

STATUS_LINE_RE = re.compile(r"^\*\*Application status:\*\*.*$", re.M)

OLD_HOW_TO = "The requirements split below is a reading aid, not a fit score."
NEW_HOW_TO = (
    "The assessment block at the top is the go/no-go read; the requirements "
    "split further down is a reading aid, not a fit score on its own."
)

# States this script may set. Anything else means the person has moved the
# note forward, and a re-run must not pull it back.
ADVANCEABLE_STATES = {
    "discovered", "captured", "needs_review",
    "assessed_green", "assessed_yellow", "assessed_red",
    "apply_ready", "closed",
}

NEXT_ACTION_APPLY = "Decide: apply, hold, or skip"


class Refused(Exception):
    """The note cannot be written safely. Nothing has been changed."""


def split_note(text: str) -> tuple[str, str]:
    """Return (frontmatter body, everything after the closing marker)."""
    match = re.match(r"\A---\n(.*?)\n---\n(.*)\Z", text, flags=re.S)
    if not match:
        raise Refused("the note has no frontmatter")
    return match.group(1), match.group(2)


def _yaml_str(value: str) -> str:
    import json

    return json.dumps(value, ensure_ascii=False)


def set_field(front: str, key: str, value: str) -> str:
    """Replace `key: ...` in the frontmatter, or add it at the end."""
    line = f"{key}: {value}"
    pattern = re.compile(rf"^{re.escape(key)}:.*$", re.M)
    if pattern.search(front):
        return pattern.sub(lambda _m: line, front, count=1)
    return front + "\n" + line


def current_state(front: str) -> str | None:
    match = re.search(r"^state:\s*(\S+)\s*$", front, flags=re.M)
    return match.group(1).strip("\"'") if match else None


def update_how_to(front: str) -> str:
    if OLD_HOW_TO in front:
        return front.replace(OLD_HOW_TO, NEW_HOW_TO, 1)
    return front


def apply_state(front: str, verdict: str, date: str) -> tuple[str, str]:
    """Return (new frontmatter, one-line note on what happened to the state)."""
    front = set_field(front, "updated", date)
    if verdict == "pending":
        return front, "state unchanged (pending)"
    state = current_state(front)
    if state is not None and state not in ADVANCEABLE_STATES:
        return front, f"state left at {state} (already past apply_ready)"
    if verdict == "skip":
        new_state, action = "closed", "none"
    else:
        new_state, action = "apply_ready", _yaml_str(NEXT_ACTION_APPLY)
    front = set_field(front, "state", new_state)
    front = set_field(front, "state_updated", date)
    front = set_field(front, "next_action", action)
    front = set_field(front, "next_action_due", "none")
    return front, f"state set to {new_state}"


def build_block(block: str, date: str, reassessed: bool) -> str:
    body = block.replace(START, "").replace(END, "").strip()
    stamp = f"*Re-assessed {date}.*" if reassessed else f"*Assessed {date}.*"
    return f"{START}\n{stamp}\n\n{body}\n{END}"


def write_into(text: str, block: str, verdict: str, date: str) -> tuple[str, str]:
    front, rest = split_note(text)

    if START in rest and END in rest:
        pattern = re.compile(re.escape(START) + r".*?" + re.escape(END), re.S)
        new_rest = pattern.sub(
            lambda _m: build_block(block, date, reassessed=True), rest, count=1
        )
    else:
        status = STATUS_LINE_RE.search(rest)
        if not status:
            raise Refused("no '**Application status:**' line to put the assessment under")
        block_text = build_block(block, date, reassessed=False)
        new_rest = rest[: status.end()] + "\n\n" + block_text + "\n" + rest[status.end():]

    front = update_how_to(front)
    front, state_note = apply_state(front, verdict, date)
    return f"---\n{front}\n---\n{new_rest}", state_note


def frontmatter_parses(text: str) -> bool:
    try:
        import yaml

        front, _ = split_note(text)
        return isinstance(yaml.safe_load(front), dict)
    except Exception:
        return False


def main(argv: list[str] | None = None) -> None:
    ap = argparse.ArgumentParser(description="Write an assessment block into an archived posting note.")
    ap.add_argument("note", type=Path, help="Archived posting note (.md).")
    ap.add_argument("--block", required=True, type=Path, help="File holding the finished assessment block.")
    ap.add_argument(
        "--verdict",
        required=True,
        choices=("apply", "reservations", "skip", "pending"),
    )
    ap.add_argument("--date", required=True, help="Assessment date, YYYY-MM-DD.")
    args = ap.parse_args(argv)

    def refuse(message: str) -> None:
        print(f"Refused: {message}. The note was not changed.", file=sys.stderr)
        sys.exit(1)

    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", args.date):
        refuse(f"date {args.date!r} must look like YYYY-MM-DD")
    for path in (args.note, args.block):
        if not path.exists():
            refuse(f"file not found: {path}")
    block = args.block.read_text(encoding="utf-8")
    if not block.strip():
        refuse("the block file is empty")

    original = args.note.read_text(encoding="utf-8")
    try:
        updated, state_note = write_into(original, block, args.verdict, args.date)
    except Refused as exc:
        refuse(str(exc))
    if not frontmatter_parses(updated):
        refuse("the frontmatter would not be valid YAML after the update")

    args.note.write_text(updated, encoding="utf-8")
    print(f"Assessment written to {args.note} ({state_note}).")


if __name__ == "__main__":
    main()
