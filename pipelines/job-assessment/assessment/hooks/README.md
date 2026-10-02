# Email card guard (optional hook)

This folder holds a small Claude Code hook that stops a plain-text job assessment email from going out. It was built by directing Claude Code: the author wrote the rules, reviewed the output and checked it with the tests in `../../tests/test_email_guard.py`.

Nothing in this system sends email. `render_email.py` writes the card to a local HTML file and stops. The hook only matters if you, or your AI tool, run a mail command of your own afterward.

## What it blocks

The hook runs before any shell command. It does nothing unless the command has a subject (`-s` or `--subject`) containing "Job Assessment". For those commands it blocks, with exit code 2, when any of these is true:

- The subject does not start with a verdict dot (green, yellow or red).
- There is no HTML body file (`-H` or `--html`), or the file does not exist.
- The HTML has no "View the job posting" button, the button does not link to a real http or https address, or the button sits below the verdict.
- The HTML has no Scores section, no score bars, or no Checks section.
- Any `{{FIELD}}` placeholder was left unfilled, which is what you get from sending the raw template.

Everything else passes through untouched.

## What it lets through

Any command without a job assessment subject, and any job assessment email whose body is a card that `render_email.py` produced.

## Turn it on

Add it to your Claude Code settings (`.claude/settings.json` in a project, or the user settings), using the path where you cloned this repo:

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

The guard needs `python3` and nothing else. You can also run the same check by hand. This example checks the card the quickstart in the main README wrote:

```text
python3 assessment/scripts/check_email.py /tmp/ja-out/email/*.html
```

It prints `check_email: card passes` and exits 0, or lists each problem and exits 2.

---

### Prompt for your AI model

Paste this into any AI model, together with this document and `assessment-email-template-guard.sh`.

**Understand the hook**

<!-- prompt: prompts/h1-understand-hook.txt -->
```text
I'm attaching assessment/hooks/README.md and assessment-email-template-guard.sh. Explain what this hook blocks, what it lets through, and how to add it to my Claude Code settings. A good answer names every check the README lists and the exit code that blocks.
```

**Tested on:** Claude Sonnet and Claude Haiku through the Claude Code command line, 2026-10-01. Both models passed. Every run, every rewrite and every grade is in `../../tests/prompt-runs/GRADES.md`.
