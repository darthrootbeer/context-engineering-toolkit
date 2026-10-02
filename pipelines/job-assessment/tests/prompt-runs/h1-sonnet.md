<!-- FICTIONAL EXAMPLE DATA. Not a real person. Saved by tests/prompt-runs/run_prompts.py -->
# Prompt run: Understand the hook (assessment/hooks/README.md), on sonnet

- Prompt file: `prompts/h1-understand-hook.txt`
- Date: 2026-10-01. Model alias `sonnet`, which ran as `claude-sonnet-5-5` (Claude Code can add a small helper model call of its own).
- Turns: 1. Cost: $0.02 (the simulated user's calls are not included).
- Grade: see `GRADES.md`.

## Conversation

### User

[the prompt below, with attached files: assessment/hooks/README.md, assessment/hooks/assessment-email-template-guard.sh]

I'm attaching assessment/hooks/README.md and assessment-email-template-guard.sh. Explain what this hook blocks, what it lets through, and how to add it to my Claude Code settings. A good answer names every check the README lists and the exit code that blocks.

### Model

## What the hook does

It's a `PreToolUse` hook on the `Bash` tool. It runs before every shell command Claude Code tries, and its job is to stop a plain-text or half-built job assessment email from being sent. Nothing in the system sends email itself (`render_email.py` only writes a local HTML file), so the hook matters only if you or your AI tool run a mail command afterward.

## What it blocks

The hook only acts on commands with a subject (`-s` or `--subject`) containing "Job Assessment". For those, it **blocks with exit code 2** if any of these is true:

1. **Subject:** it doesn't start with a verdict dot (green, yellow, or red).
2. **HTML body:** there's no `-H`/`--html` body file, or the file doesn't exist.
3. **Job posting button:**
   - there's no "View the job posting" button,
   - the button doesn't link to a real http or https address, or
   - the button sits below the verdict.
4. **Card sections:**
   - there's no Scores section,
   - there are no score bars, or
   - there's no Checks section.
5. **Placeholders:** any `{{FIELD}}` is left unfilled, which is what you get from sending the raw template.

## What it lets through

- Any command without a "Job Assessment" subject.
- Any job assessment email whose HTML body is a card produced by `render_email.py`.

Exit code 0 allows the command.

## How the script works

The shell script is a thin wrapper:

1. It reads the hook payload from stdin.
2. As a fast path, it lowercases the payload and exits 0 immediately if "job assessment" doesn't appear anywhere.
3. Otherwise it pipes the payload to `python3 ../scripts/check_email.py --hook`, where all the actual checks live. Because of `set -e`, the script's exit status (2 on a failed check) is what the hook returns.

Note that the script itself doesn't contain the checks; the README's list describes what `check_email.py` does, and I haven't seen that file.

## Adding it to Claude Code settings

Put this in `.claude/settings.json` (project) or your user settings, replacing the path with where you cloned the repo:

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

The only requirement is `python3`.

## Testing it by hand

You can run the same check on a rendered card without the hook:

```
python3 assessment/scripts/check_email.py out/example-co-docs-writer.html
```

It prints `check_email: card passes` and exits 0, or lists each problem and exits 2.
