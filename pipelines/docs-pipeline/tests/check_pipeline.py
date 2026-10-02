#!/usr/bin/env python3
"""Offline check that the docs-pipeline folder is self-contained.

Run from anywhere:  python3 pipelines/docs-pipeline/tests/check_pipeline.py

It needs no model and no network. It checks four things:
1. Every `./_knowledge/...` path a skill file names exists in this folder.
2. Every skill file has the frontmatter name the install loop relies on.
3. No file mentions a private tool, home path, or leftover setup.
4. The sample doc, the .gitignore template and the product knowledge starters ship.

Exit code 0 means clean, 1 means problems were printed.
"""
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent.parent
REPO = HERE.parent.parent
READABILITY = REPO / "skills" / "docs-readability-check"

# Words that must not appear anywhere in the shipped folders.
BANNED = [r"TOOLBOX", r"/Users/", r"~/Downloads", r"\.cursor", r"example-docs-repo", r"_extras/style-guides"]

problems = []

skill_files = sorted(HERE.glob("docs-*.md")) + [READABILITY / "SKILL.md"]
TESTS = HERE / "tests"
all_files = [p for p in list(HERE.rglob("*")) + list(READABILITY.rglob("*"))
             if p.is_file() and TESTS not in p.parents and p.suffix in {".md", ".yaml", ".template"}]

# 1. knowledge paths named in skill files must exist
for f in skill_files:
    for m in re.finditer(r"\./_knowledge/[A-Za-z0-9_./-]+", f.read_text(encoding="utf-8")):
        target = m.group(0).rstrip(".")
        if not (HERE / target[2:]).exists():
            problems.append(f"{f.name}: names {target}, which does not exist in this folder")

# 2. frontmatter names match file names
for f in skill_files:
    text = f.read_text(encoding="utf-8")
    m = re.match(r"---\nname: (\S+)\n", text)
    expected = f.stem if f.name != "SKILL.md" else "docs-readability-check"
    if not m or m.group(1) != expected:
        problems.append(f"{f.name}: frontmatter name is not {expected}")

# 3. banned strings
for f in all_files:
    text = f.read_text(encoding="utf-8")
    for pat in BANNED:
        if re.search(pat, text):
            problems.append(f"{f.relative_to(REPO)}: contains {pat}")

# 4. shipped starter files
for rel in ["sample/acme-orders-cancellations.md", "workspace-gitignore.template",
            "_knowledge/product-kb/index.md", "_knowledge/product-kb/integration-types.md",
            "_knowledge/product-kb/endpoints.md", "_knowledge/product-kb/domain-models.md",
            "_knowledge/product-kb/error-codes.md", "_knowledge/product-kb/webhooks.md",
            "_knowledge/product-kb/recent-changes.md",
            "_knowledge/style-guides/general/style-guide_general.md"]:
    if not (HERE / rel).is_file():
        problems.append(f"missing shipped file: {rel}")
if not (READABILITY / "README.md").is_file():
    problems.append("missing skills/docs-readability-check/README.md")

if problems:
    print(f"check_pipeline: {len(problems)} problem(s)")
    for p in problems:
        print("  " + p)
    sys.exit(1)
print(f"check_pipeline: clean ({len(skill_files)} skill files, {len(all_files)} files scanned)")
