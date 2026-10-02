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

# Email Guard Hook Explained

## What it blocks (exit code 2)

The hook intercepts shell commands with a subject containing "Job Assessment" and blocks them unless the HTML body is a valid assessment card. It specifically blocks when:

1. **Verdict missing** — subject doesn't start with a verdict dot (•, colored green/yellow/red)
2. **No HTML body** — missing `-H`/`--html` flag or the file doesn't exist
3. **View posting button invalid** — missing the "View the job posting" button, doesn't link to http/https, or appears below the verdict
4. **Missing Scores section** — no Scores section, no score bars, or no Checks section
5. **Template placeholders unfilled** — any `{{FIELD}}` placeholder remains (raw template sent)

All blocks use **exit code 2** to prevent the command.

## What it lets through (exit code 0)

- Any command with no "Job Assessment" subject (passes unchanged)
- Any job assessment email with a properly-rendered card from `render_email.py`

## How to add it to Claude Code settings

Add this to `.claude/settings.json` (project-level) or your user settings:

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

Replace `/path/to/context-engineering-toolkit/...` with the actual cloned repo path. The hook requires only `python3` — it delegates validation to `check_email.py`.
