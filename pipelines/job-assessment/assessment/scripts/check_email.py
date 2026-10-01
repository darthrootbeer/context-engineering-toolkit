#!/usr/bin/env python3
"""Check that an assessment email is the real card, not a plain body.

Used three ways:
  check_email.py CARD.html [--subject S]     check one file, exit 0 or 2
  check_email.py --hook < payload.json       Claude Code PreToolUse hook mode
  from check_email import card_problems      called by render_email.py

Nothing here sends mail. It only reads a local HTML file and says whether the
file has the shape of the card: a "View the job posting" button with a real
http(s) link that comes before the verdict, a Scores section with score bars,
a Checks section, and no leftover {{PLACEHOLDER}} fields. A subject, when
given, must start with a verdict dot (green, yellow or red).

Exit codes: 0 passes, 2 blocked (the same code a Claude Code hook uses to block).
"""
import argparse
import json
import re
import shlex
import sys
from pathlib import Path
from urllib.parse import urlparse

VERDICT_DOTS = ("\U0001F7E2", "\U0001F7E1", "\U0001F534")  # green, yellow, red

JOB_LINK_RE = re.compile(
    r'<a\b[^>]*?\bhref="([^"]*)"[^>]*>\s*View the job posting\s*</a>', re.I | re.S
)
PLACEHOLDER_RE = re.compile(r"\{\{\s*[A-Za-z_][A-Za-z0-9_]*\s*\}\}")
BAR_MARKUP = "border-radius:5px 0 0 5px"


def real_http_url(url):
    """True for an http(s) link with a real host. False for '#', empty, placeholders."""
    url = url.strip()
    if not url or "{{" in url:
        return False
    parts = urlparse(url)
    if parts.scheme not in ("http", "https") or not parts.hostname:
        return False
    host = parts.hostname
    return "." in host or host == "localhost"


def card_problems(html):
    """Return a list of plain-language problems. An empty list means the card passes."""
    problems = []

    match = JOB_LINK_RE.search(html)
    if not match:
        problems.append("no 'View the job posting' button")
    elif not real_http_url(match.group(1)):
        problems.append("the 'View the job posting' button does not link to a real http(s) URL")
    else:
        verdict_at = html.find('data-card="verdict"')
        if verdict_at != -1 and match.start() > verdict_at:
            problems.append("the job posting button must come above the verdict")

    if not re.search(r">\s*Scores\s*<", html):
        problems.append("Scores section")
    if BAR_MARKUP not in html:
        problems.append("score bar markup")
    if not re.search(r">\s*Checks\s*<", html):
        problems.append("Checks section")

    left = sorted(set(PLACEHOLDER_RE.findall(html)))
    if left:
        problems.append("unfilled placeholders: " + " ".join(left))
    return problems


def subject_problems(subject):
    if subject[:1] not in VERDICT_DOTS:
        return ["subject must start with a verdict dot (green, yellow or red), got: " + subject]
    return []


def _option(tokens, short, long):
    """Value of -x VALUE, --long VALUE or --long=VALUE in a token list, else None."""
    for i, tok in enumerate(tokens):
        if tok in (short, long) and i + 1 < len(tokens):
            return tokens[i + 1]
        if tok.startswith(long + "="):
            return tok[len(long) + 1:]
    return None


def split_command(command):
    lexer = shlex.shlex(command, posix=True, punctuation_chars=True)
    lexer.whitespace_split = True
    return list(lexer)


def check_file(path, subject=None):
    problems = []
    if subject is not None:
        problems += subject_problems(subject)
    p = Path(path)
    if not p.is_file():
        problems.append("HTML file does not exist: " + str(path))
    else:
        problems += card_problems(p.read_text(encoding="utf-8"))
    return problems


def block(problems, out=sys.stderr):
    print("BLOCK: this job assessment email is not the required card.", file=out)
    for item in problems:
        print("  - " + item, file=out)
    print("  Render the card with render_email.py and send that file as the HTML body.", file=out)
    return 2


def hook_main(stdin):
    """PreToolUse hook mode. Reads the hook payload, blocks bad assessment emails."""
    raw = stdin.read()
    if "job assessment" not in raw.lower():
        return 0
    try:
        command = json.loads(raw).get("tool_input", {}).get("command", "")
        tokens = split_command(command)
    except (ValueError, AttributeError):
        return 0
    subject = _option(tokens, "-s", "--subject")
    if subject is None or "job assessment" not in subject.lower():
        return 0
    html_path = _option(tokens, "-H", "--html")
    if not html_path:
        return block(subject_problems(subject) + ["no -H or --html file: the body must be the card"])
    problems = check_file(html_path, subject)
    return block(problems) if problems else 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("html", nargs="?", help="the card HTML file to check")
    ap.add_argument("--subject", help="the email subject, checked for a leading verdict dot")
    ap.add_argument("--hook", action="store_true", help="read a Claude Code PreToolUse payload on stdin")
    args = ap.parse_args(argv)
    if args.hook:
        return hook_main(sys.stdin)
    if not args.html:
        ap.error("an HTML file is required unless --hook is used")
    problems = check_file(args.html, args.subject)
    if problems:
        return block(problems)
    print("check_email: card passes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
