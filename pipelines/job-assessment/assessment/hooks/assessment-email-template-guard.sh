#!/usr/bin/env bash
# Optional Claude Code PreToolUse hook (matcher: Bash).
# Blocks a mail command whose subject contains "Job Assessment" unless its HTML
# body is the real card. The checks live in ../scripts/check_email.py; this file
# only hands the hook payload to it. Exit 2 blocks the command, exit 0 allows it.
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INPUT="$(cat)"

# Fast path: a payload that never mentions "job assessment" cannot apply.
case "$(printf '%s' "$INPUT" | tr '[:upper:]' '[:lower:]')" in
  *"job assessment"*) ;;
  *) exit 0 ;;
esac

printf '%s' "$INPUT" | python3 "$HERE/../scripts/check_email.py" --hook
