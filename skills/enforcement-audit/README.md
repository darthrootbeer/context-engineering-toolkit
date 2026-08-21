# enforcement-audit

Audits an AI-agent project's enforcement stack — skills, hooks, config — and answers one question: **where is this system relying on the model's good behavior when it should be relying on code that cannot be argued with?**

Originally built as `anthropic-skill-improve` for a large personal Claude Code installation (about 100 skills and 60 hooks). This version keeps the core idea — the trust hierarchy — and genericizes the paths and process names so it drops into any project.

## The core idea: a trust hierarchy

Every enforcement mechanism has a trust level, from a harness-level hard block (Level 1 — cannot be bypassed) down to a fact the model recalls from memory (Level 7 — softest, can go stale or be misremembered). The cardinal rule: anything destructive, irreversible, or external-facing needs Level 1-2 enforcement. A destructive action sitting on Level 5-7 prose instructions is a bug waiting to happen — not a matter of writing clearer instructions, but of moving the check into code.

Full detail, the complete ladder, and the audit process (assess → plan → execute) live in `SKILL.md`.

## Commands

```
/enforcement-audit <skill-name | hook-name | process-name | all>
```

## What it produces

- A written findings file mapping every critical behavior to a trust level, with a verdict (well-enforced / partially enforced / dangerously under-enforced)
- A compact on-screen summary table (priority, problem, fix, effort)
- Optionally, an executable plan and — for non-destructive fixes — the fix applied directly, with git checkpoints and a hard "always pause" list for anything touching permissions, hook wiring, or exit-code logic

## Configuration

Set `SKILLS_DIR`, `HOOKS_DIR`, `SCRIPTS_DIR`, `SETTINGS_FILE`, and `FINDINGS_DIR` at the top of your working copy to match your project's layout. See `SKILL.md` for defaults.

## Install

Copy the `enforcement-audit/` folder into your project's Claude Code skills directory, adjust the configuration paths, and invoke `/enforcement-audit`.
