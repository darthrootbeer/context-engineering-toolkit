#!/usr/bin/env python3
"""Rename an archived posting note so its verdict emoji sits at the far left.

The emoji goes first in two places: the first character of the filename and
the first character of the frontmatter `title:`. That makes the verdict the
first thing visible in a file list, however long the company name is. The
order is verdict, then source, then lane.

The naming rule lives in code, not in a prose instruction, because a prose
rule is followed most of the time and not every time. Here the insertion
point is fixed and testable.

Source emoji come from `sources[]` in the career profile and lane emoji from
`lanes[].emoji`. Verdict emoji are fixed.

Idempotent: re-running on a note that already carries emoji replaces them.
Nothing stacks and nothing is left in another position.

Exit codes: 0 renamed, 1 error.

Usage:
    rename_verdict.py NOTE.md --verdict apply --profile career-profile.yaml
    rename_verdict.py NOTE.md --verdict skip --profile career-profile.yaml \\
        --source board-a --lane docs-platform
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

VERDICT_EMOJI = {
    "apply": "🟢",
    "reservations": "🟡",
    "skip": "🔴",
    "pending": "⚪",
}

# `pending` is not a verdict. It marks a posting that was archived but never
# judged, most often because the text could not be fetched. It keeps that
# state visible in a file list. Re-run the assessment once the text is in
# hand, then rename again with the real verdict.


def _emoji_regex(emoji: list[str]) -> re.Pattern:
    alternation = "|".join(re.escape(e) for e in sorted(set(emoji), key=len, reverse=True))
    # An emoji with one adjacent space consumed on either side, so deleting it
    # leaves no double space.
    return re.compile(rf"(?: (?:{alternation}))|(?:(?:{alternation}) )")


def _strip_emoji(text: str, known: list[str]) -> str:
    """Remove every verdict, source and lane emoji, wherever it sits.

    Removing all of them and adding exactly one set at the front is what makes
    the script idempotent, with no need to know which position applied before.
    """
    return _emoji_regex(list(VERDICT_EMOJI.values()) + list(known)).sub("", text)


def _prefix(emoji: str, source_emoji: str | None, lane_emoji: str | None = None) -> str:
    """Verdict first, then source, then lane. The verdict has to be the
    leftmost character so it survives truncation in a file list."""
    parts = [emoji]
    if source_emoji:
        parts.append(source_emoji)
    if lane_emoji:
        parts.append(lane_emoji)
    return " ".join(parts) + " "


def lane_from_frontmatter(path: Path) -> str | None:
    """Read `lane:` from the note's own frontmatter, so the filename cannot
    disagree with the lane the note was archived under."""
    return _frontmatter_value(path, "lane")


def source_from_frontmatter(path: Path) -> str | None:
    return _frontmatter_value(path, "source")


def _frontmatter_value(path: Path, key: str) -> str | None:
    try:
        content = path.read_text(encoding="utf-8")
    except OSError:
        return None
    front = re.match(r"\A---\n(.*?)\n---", content, flags=re.S)
    if not front:
        return None
    match = re.search(rf"^{key}:\s*[\"']?(.+?)[\"']?\s*$", front.group(1), flags=re.M)
    return match.group(1) if match else None


def rename_file(
    path: Path,
    emoji: str,
    source_emoji: str | None = None,
    lane_emoji: str | None = None,
    known: list[str] | None = None,
) -> Path:
    """Rename `path` to carry the prefix. `known` lists every source and lane
    emoji the profile defines, so an old marker is removed even when this run
    names a different one."""
    if not path.name.endswith(".md"):
        raise ValueError(f"Filename doesn't end in '.md': {path.name}")
    pool = list(known or []) + [e for e in (source_emoji, lane_emoji) if e]
    stripped = _strip_emoji(path.name, pool)
    new_path = path.with_name(f"{_prefix(emoji, source_emoji, lane_emoji)}{stripped}")
    if new_path != path:
        path.rename(new_path)
    return new_path


def update_title(
    path: Path,
    emoji: str,
    source_emoji: str | None = None,
    lane_emoji: str | None = None,
    known: list[str] | None = None,
) -> None:
    content = path.read_text(encoding="utf-8")

    match = re.search(r'title: "((?:[^"\\]|\\.)*)"', content)
    if not match:
        print(
            f"WARNING: no 'title: \"...\"' line found in {path.name}. Title left unchanged.",
            file=sys.stderr,
        )
        return

    pool = list(known or []) + [e for e in (source_emoji, lane_emoji) if e]
    old_title = match.group(1)
    new_title = f"{_prefix(emoji, source_emoji, lane_emoji)}{_strip_emoji(old_title, pool)}"
    new_content = content.replace(f'title: "{old_title}"', f'title: "{new_title}"', 1)
    path.write_text(new_content, encoding="utf-8")


def emoji_maps(profile_path: Path) -> tuple[dict[str, str], dict[str, str]]:
    """Return (source key -> emoji, lane name -> emoji) from the profile."""
    import yaml

    data = yaml.safe_load(profile_path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{profile_path} is not a career profile")
    sources = {
        str(s["key"]): str(s["emoji"])
        for s in data.get("sources") or []
        if isinstance(s, dict) and s.get("key") and s.get("emoji")
    }
    lanes = {
        str(lane["name"]): str(lane["emoji"])
        for lane in data.get("lanes") or []
        if isinstance(lane, dict) and lane.get("name") and lane.get("emoji")
    }
    return sources, lanes


def fail(message: str) -> None:
    print(message, file=sys.stderr)
    sys.exit(1)


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        description="Rename an archived job posting with its verdict emoji "
        "at the far left, and update the matching frontmatter title."
    )
    parser.add_argument("path", type=Path, help="Path to the archived .md note.")
    parser.add_argument(
        "--verdict",
        required=True,
        choices=sorted(VERDICT_EMOJI),
        help="apply | reservations | skip | pending",
    )
    parser.add_argument("--profile", required=True, type=Path, help="career-profile.yaml")
    parser.add_argument(
        "--source",
        help="Source key from the profile's sources. Defaults to the note's `source:` field.",
    )
    parser.add_argument(
        "--lane",
        help="Lane name from the profile. Defaults to the note's `lane:` field.",
    )
    args = parser.parse_args(argv)

    if not args.path.exists():
        fail(f"File not found: {args.path}")
    try:
        sources, lanes = emoji_maps(args.profile)
    except (OSError, ValueError) as exc:
        fail(f"Could not read the profile: {exc}")
    except Exception as exc:  # malformed YAML
        fail(f"Could not read the profile: {exc}")

    source_key = args.source or source_from_frontmatter(args.path)
    if source_key is not None and source_key not in sources:
        fail(
            f"Unknown source {source_key!r}. Sources in this profile: "
            f"{', '.join(sorted(sources)) or 'none'}."
        )

    # An explicit --lane wins. Otherwise use what the archive step wrote into
    # the note, so the filename cannot disagree with the rubric used.
    lane = args.lane or lane_from_frontmatter(args.path)
    if lane is None:
        print(
            "WARNING: no lane found. Pass --lane, or add a `lane:` field to the "
            "note's frontmatter. Renaming without a lane marker.",
            file=sys.stderr,
        )
    elif lane not in lanes:
        fail(f"Unknown lane {lane!r}. Lanes in this profile: {', '.join(sorted(lanes)) or 'none'}.")

    emoji = VERDICT_EMOJI[args.verdict]
    source_emoji = sources.get(source_key) if source_key else None
    lane_emoji = lanes.get(lane) if lane else None
    known = list(sources.values()) + list(lanes.values())

    new_path = rename_file(args.path, emoji, source_emoji, lane_emoji, known)
    update_title(new_path, emoji, source_emoji, lane_emoji, known)

    print(f"Renamed: {new_path}")


if __name__ == "__main__":
    main()
