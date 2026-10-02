# SETUP-review on haiku

Prompt (inputs filled with made-up samples):

```text
I have attached the setup guide for "docs-pipeline". Below is the output of the commands I ran on my machine.

2.1.287 (Claude Code)
github.com
  Logged in to github.com account example-user (keyring)
  Active account: true
git version 2.45.1
v22.3.0
zsh: command not found: markdownlint

Compare my output with the "Prerequisites" section. For each prerequisite, say whether it is met, missing, or impossible to tell from my output, and quote the line of my output that shows it. Then say what I must do before the first run.

A good answer has one line per prerequisite, never marks something as met without a line of output to show it, and does not guess about anything my output does not cover.
```

Answer:

Comparing your output to the Prerequisites section (section 1):

| Prerequisite | Status | Evidence |
|---|---|---|
| Claude Code installed | **Met** | `2.1.287 (Claude Code)` |
| GitHub CLI (`gh`) installed and authenticated | **Met** | `Logged in to github.com account example-user (keyring)` and `Active account: true` |
| Git installed | **Met** | `git version 2.45.1` |
| Node.js with `markdownlint-cli` | **Missing** | `zsh: command not found: markdownlint` |
| A docs repository with markdown files | **Impossible to tell** | No output shown |
| A published docs site | **Impossible to tell** | No output shown |

**What you must do before the first run:**

Install `markdownlint-cli` globally:
```bash
npm install -g markdownlint-cli
```

Then verify it is available:
```bash
markdownlint --version
```

This is required by the `docs-publish` skill (Stage 6). You can run the smoke test in section 4 without it (it stops before publishing), but you will need it for any full pipeline run.

