# SETUP-review on sonnet

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

## Prerequisites check

| Prerequisite | Status | Evidence |
|---|---|---|
| Claude Code available as `claude` | **Met** | `2.1.287 (Claude Code)` |
| GitHub CLI installed | **Met** | `Logged in to github.com account example-user (keyring)` |
| `gh` authenticated for the org that owns the docs repo | **Impossible to tell** | Your output shows a login (`Active account: true`) but not which org or repo that account can reach. |
| Git installed | **Met** | `git version 2.45.1` |
| Node.js installed | **Met** | `v22.3.0` |
| `markdownlint-cli` available | **Missing** | `zsh: command not found: markdownlint` |
| A docs repo with markdown files | **Impossible to tell** | None of the commands cover this. |
| A published docs site or staging environment | **Impossible to tell** | None of the commands cover this. |

## What to do before the first run

1. **Install markdownlint-cli:** `npm install -g markdownlint-cli`. Then re-run `markdownlint --version` to confirm. The guide says only `docs-publish` (Stage 6) needs it, so it doesn't block the smoke test, but you need it before a full pipeline run.
2. **Check `gh` access to the docs org.** Run `gh repo view {YOUR_ORG}/{YOUR_DOCS_REPO}` with your real names. If it fails, run `gh auth login` for the right account. Stages 4b, 4c (naming check) and 6 depend on this.
3. **Confirm you have a docs repo and a published or staging site.** Only you can check this.
4. **Install the skills (section 3).** Run the install loop, then confirm `/docs-` lists 17 skills.
5. **Run the smoke test (section 4).** It needs no placeholders and no markdownlint.
6. **Before running on real docs:** fill in the docs-repo placeholders from section 2 and replace the starter `_knowledge/` files from section 5 with your own.

