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

## What the hook blocks

The hook runs before every Bash command (`PreToolUse`, matcher `Bash`). It does nothing unless the command has a subject (`-s` or `--subject`) containing "Job Assessment". For those commands it blocks with **exit code 2** when any of these is true:

1. **Subject**: it doesn't start with a verdict dot (green, yellow or red).
2. **HTML body**: there is no `-H` / `--html` body file, or the file doesn't exist.
3. **Job posting button**:
   - the HTML has no "View the job posting" button,
   - the button doesn't link to a real http or https address, or
   - the button sits below the verdict.
4. **Card structure**:
   - no Scores section,
   - no score bars, or
   - no Checks section.
5. **Placeholders**: any `{{FIELD}}` is left unfilled, which is what you get from sending the raw template.

Exit 2 is the code Claude Code treats as "block this tool call". Exit 0 lets it proceed.

## What it lets through

- Any command without a Job Assessment subject.
- Any Job Assessment email whose body is a card produced by `render_email.py`.

## How the script works

The `.sh` file is only a thin wrapper:

- It reads the hook payload from stdin.
- **Fast path:** it lowercases the payload, and if "job assessment" doesn't appear anywhere, it exits 0 immediately.
- Otherwise it pipes the payload to `../scripts/check_email.py --hook`, which does the real checks and returns 0 or 2. I haven't seen `check_email.py`, so the exact check logic is as described in the README, not verified by me.

## Adding it to your settings

Put this in `.claude/settings.json` (per project) or your user settings, replacing the path with where you cloned the repo:

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

Requirements: `python3` only. If you already have a `PreToolUse` array, add the new object to it rather than replacing it.

To run the check by hand:

```
python3 assessment/scripts/check_email.py out/example-co-docs-writer.html
```

It prints `check_email: card passes` and exits 0, or lists each problem and exits 2.

## Note

Nothing in this system sends email. `render_email.py` only writes a local HTML file, so the hook matters only if you or your AI tool run a mail command afterward.
