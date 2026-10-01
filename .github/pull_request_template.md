## Context

Why this change exists, in a few plain sentences. Put the ticket link inline here.

## Changes

What changed and what it affects. Say what existing behavior is untouched.

## Checks

- [ ] README.md and ROADMAP.md describe what is in the tree after this change, and nothing that is not
- [ ] `python3 .github/scripts/safety_scan.py --range origin/main...HEAD` is clean
- [ ] Tests for new scripts were run, and their real output is in the log
- [ ] Private gate: cet-gate.sh <date> — 0 hits
