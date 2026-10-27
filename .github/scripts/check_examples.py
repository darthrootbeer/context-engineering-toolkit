#!/usr/bin/env python3
"""Check that the code examples in the Markdown docs are well formed.

Run from the repo root:  python3 .github/scripts/check_examples.py

For every fenced block tagged json, yaml/yml or bash/sh, it checks that the block
parses (json.loads, yaml.safe_load, bash -n). Blocks tagged with anything else are
skipped. Saved model outputs under tests/ are skipped: they quote examples on purpose.
A block that holds placeholders on purpose can opt out with an HTML comment on the
line above the fence:  <!-- example-check: skip -->

Exit code 0 means clean, 1 means problems were printed.
"""
import json
import pathlib
import re
import subprocess
import sys

import yaml

ROOT = pathlib.Path(__file__).resolve().parents[2]
SKIP_DIRS = {".git", "tests", "node_modules"}
FENCE = re.compile(r"^(?P<ind>\s*)```(?P<lang>[A-Za-z0-9_+-]*)\s*$")

problems = []
checked = 0


def check(lang, body):
    if lang == "json":
        json.loads(body)
    elif lang in ("yaml", "yml"):
        list(yaml.safe_load_all(body))
    elif lang in ("bash", "sh", "shell"):
        r = subprocess.run(["bash", "-n"], input=body, text=True, capture_output=True)
        if r.returncode:
            raise ValueError(r.stderr.strip().splitlines()[-1] if r.stderr.strip() else "bash -n failed")


for md in sorted(ROOT.rglob("*.md")):
    rel = md.relative_to(ROOT)
    if SKIP_DIRS & set(rel.parts):
        continue
    lines = md.read_text(encoding="utf-8").splitlines()
    i = 0
    while i < len(lines):
        m = FENCE.match(lines[i])
        if m and m.group("lang"):
            lang, start = m.group("lang").lower(), i
            skip = i > 0 and "example-check: skip" in lines[i - 1]
            j = i + 1
            while j < len(lines) and not FENCE.match(lines[j]):
                j += 1
            ind = len(m.group("ind"))
            body = "\n".join(l[ind:] if l[:ind].isspace() else l for l in lines[i + 1:j]) + "\n"
            if lang in {"json", "yaml", "yml", "bash", "sh", "shell"} and not skip:
                checked += 1
                try:
                    check(lang, body)
                except Exception as e:  # any parse error is a finding
                    problems.append(f"{rel}:{start + 1}: {lang} block does not parse: {str(e).splitlines()[0]}")
            i = j + 1
        else:
            i += 1

if problems:
    print(f"check_examples: {len(problems)} problem(s)")
    for p in problems:
        print("  " + p)
    sys.exit(1)
print(f"check_examples: clean ({checked} blocks checked)")
