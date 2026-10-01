#!/usr/bin/env python3
"""Public safety scan for this repo.

Reads rules from .github/safety-patterns.yaml and exits 1 on any hit.
It prints file, line and rule id only, never the matched text, so a hit
cannot leak the thing it found into a CI log.

    safety_scan.py                       scan every tracked file (same as --tree)
    safety_scan.py --tree                scan every tracked file
    safety_scan.py --range origin/main..HEAD   scan only lines added in that range
    safety_scan.py --history             scan lines added by every commit, all branches

Exit codes: 0 clean, 1 hits found, 2 could not run.
"""
import argparse
import fnmatch
import json
import re
import subprocess
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("safety_scan: pyyaml is required (pip install pyyaml)", file=sys.stderr)
    sys.exit(2)

PATTERNS = Path(__file__).resolve().parent.parent / "safety-patterns.yaml"


def git(*args):
    r = subprocess.run(["git", *args], capture_output=True, text=True, errors="replace")
    if r.returncode != 0:
        print(f"safety_scan: git {' '.join(args)} failed: {r.stderr.strip()}", file=sys.stderr)
        sys.exit(2)
    return r.stdout


def load_rules():
    try:
        cfg = yaml.safe_load(PATTERNS.read_text())
    except Exception as e:  # noqa: BLE001
        print(f"safety_scan: cannot read {PATTERNS}: {e}", file=sys.stderr)
        sys.exit(2)
    return cfg


def in_scope(path, scope):
    return not scope or any(fnmatch.fnmatch(path, g) for g in scope)


class Scanner:
    def __init__(self, cfg):
        self.cfg = cfg
        self.ignore = set(cfg.get("ignore_files", []))
        self.allow_tokens = cfg.get("ticket_allowlist", [])
        self.line_rules = []
        self.check_rules = []
        for r in cfg["rules"]:
            if "check" in r:
                self.check_rules.append(r)
            else:
                rr = dict(r)
                rr["_re"] = re.compile(r["regex"])
                rr["_allow"] = re.compile(r["allow_regex"]) if r.get("allow_regex") else None
                self.line_rules.append(rr)
        self.hits = []

    def scan_line(self, path, lineno, text, where=""):
        if path in self.ignore:
            return
        for tok in self.allow_tokens:
            text = text.replace(tok, "")
        for r in self.line_rules:
            if not in_scope(path, r.get("scope")):
                continue
            for m in r["_re"].finditer(text):
                if r["_allow"] and r["_allow"].search(m.group(0)):
                    continue
                self.hits.append((path, lineno, r["id"], r["message"], where))
                break  # one hit per rule per line is enough

    def scan_file_checks(self, path, content):
        if path in self.ignore:
            return
        for r in self.check_rules:
            if not in_scope(path, r.get("scope")):
                continue
            if r["check"] == "fixture-banner":
                head = content[:300]
                first = content.split("\n", 1)[0]
                ok = r["banner"] in first or ('"_banner"' in head and r["banner"] in head)
                if not ok:
                    self.hits.append((path, 1, r["id"], r["message"], ""))
            elif r["check"] == "attribution":
                if r["phrase"] not in content:
                    self.hits.append((path, 1, r["id"], r["message"], ""))


def read_text(path):
    try:
        return Path(path).read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return None


def scan_tree(sc):
    for path in git("ls-files").splitlines():
        text = read_text(path)
        if text is None:
            continue
        for i, line in enumerate(text.split("\n"), 1):
            sc.scan_line(path, i, line)
        sc.scan_file_checks(path, text)


def scan_diff_text(sc, diff, where_from_commit=False):
    """Walk `git diff -U0` or `git log -p -U0` output, scan added lines."""
    path, lineno, commit = None, 0, ""
    for raw in diff.split("\n"):
        if raw.startswith("COMMIT "):
            commit = raw[7:19]
        elif raw.startswith("+++ "):
            path = raw[6:] if raw.startswith("+++ b/") else None
        elif raw.startswith("@@"):
            m = re.search(r"\+(\d+)", raw)
            lineno = int(m.group(1)) if m else 0
        elif raw.startswith("+") and path:
            sc.scan_line(path, lineno, raw[1:], commit if where_from_commit else "")
            lineno += 1


def scan_range(sc, rng):
    diff = git("diff", "-U0", "--no-color", "--no-ext-diff", rng)
    scan_diff_text(sc, diff)
    for path in git("diff", "--name-only", "--diff-filter=AM", rng).splitlines():
        text = read_text(path)
        if text is not None:
            sc.scan_file_checks(path, text)


def scan_history(sc):
    diff = git("log", "--all", "-p", "-U0", "--no-color", "--no-ext-diff", "--format=COMMIT %H")
    scan_diff_text(sc, diff, where_from_commit=True)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--tree", action="store_true", help="scan every tracked file (default)")
    g.add_argument("--range", metavar="A..B", help="scan lines added in a git range")
    g.add_argument("--history", action="store_true", help="scan lines added in all history")
    ap.add_argument("--json", action="store_true", help="print hits as JSON")
    args = ap.parse_args()

    root = git("rev-parse", "--show-toplevel").strip()
    import os
    os.chdir(root)
    sc = Scanner(load_rules())
    if args.range:
        scan_range(sc, args.range)
        mode = f"range {args.range}"
    elif args.history:
        scan_history(sc)
        mode = "history"
    else:
        scan_tree(sc)
        mode = "tree"

    if args.json:
        print(json.dumps([dict(zip(("file", "line", "rule", "message", "commit"), h)) for h in sc.hits], indent=2))
    for path, lineno, rid, msg, where in sorted(set(sc.hits)):
        suffix = f" (commit {where})" if where else ""
        print(f"{path}:{lineno}: [{rid}] {msg}{suffix}")
    if sc.hits:
        print(f"safety_scan: {len(set(sc.hits))} hit(s) in {mode}")
        return 1
    print(f"safety_scan: clean ({mode})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
