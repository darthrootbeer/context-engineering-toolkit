<!-- FICTIONAL EXAMPLE DATA. Not a real person. Saved by tests/prompt-runs/run_prompts.py -->
# Prompt run: Understand the hook (assessment/hooks/README.md), on haiku

- Prompt file: `prompts/h1-understand-hook.txt`
- Date: 2026-10-01. Model alias `haiku`, which ran as `claude-haiku-4-5-20251001` (Claude Code can add a small helper model call of its own).
- Turns: 1. Cost: $0.02 (the simulated user's calls are not included).
- Grade: see `GRADES.md`.

## Conversation

### User

[the prompt below, with attached files: assessment/hooks/README.md, assessment/hooks/assessment-email-template-guard.sh]

I'm attaching assessment/hooks/README.md and assessment-email-template-guard.sh. Explain what this hook blocks, what it lets through, and how to add it to my Claude Code settings. A good answer names every check the README lists and the exit code that blocks.

### Model

## What this hook blocks

The hook runs before every Bash command and **blocks** (exit code **2**) any mail command with `"Job Assessment"` in the subject unless all nine checks pass:

1. **Subject starts with verdict dot** — must begin with green, yellow, or red dot
2. **HTML body file exists** — `-H` or `--html` flag points to an existing file
3. **"View the job posting" button exists** — the HTML contains it
4. **Button links to http/https** — not a malformed or missing URL
5. **Button sits above verdict** — button position is correct (not below)
6. **Scores section exists** — HTML has a scores section
7. **Score bars exist** — at least one score bar is present
8. **Checks section exists** — HTML has a checks section
9. **No template placeholders remain** — no unfilled `{{FIELD}}` tags

All nine must pass. If any fails, the command is blocked with exit code 2 and errors are listed.

## What it lets through

- **Any command without "Job Assessment" in the subject** — passes untouched
- **Valid job assessment emails** — commands where all nine checks pass

(The hook prevents accidentally sending raw, incomplete templates or emails with missing pieces.)

## How to add it to Claude Code settings

Add this to `.claude/settings.json` (project level in `.claude/` or user settings):

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "bash /path/to/context-engineering-toolkit/pipelines/job-assessment/assessment/hooks/assessment-email-template-guard.sh"
          }
        ]
      }
    ]
  }
}
```

Replace `/path/to/...` with the actual path to your cloned repo. The hook needs only `python3`; no other dependencies.
