# plan-this

Captures what the current conversation has established and writes it to disk as a self-contained, agent-ready plan. The plan file is structured so any Claude Code instance can pick it up cold and execute it without the original conversation history.

## Commands

```
/plan-this [optional title or topic focus]
```

If no argument is given, the plan subject is inferred from conversation context.

## What it produces

A markdown plan file written to a configurable `PLANS_DIR` (see `SKILL.md` for how to set this per project). Plans are numbered sequentially (`plan-001`, `plan-002`, …).

Each plan contains:
- Agent instructions header (mandatory — tells any Claude instance how to execute)
- Problem statement and done-when criteria
- Tasks with status checkboxes, file paths, exact commands, and verification steps
- Known risks and blocker tracking section

## Output

After writing, prints the file path:

```
Plan saved: plan-NNN — [title]

[full file path]
```

## When to use

- Any time you want to hand off multi-step work to a fresh session
- Before ending a session on unfinished work — park the plan, resume later
- After a review or audit skill produces findings you want tracked as an executable checklist

## Install

Copy the `plan-this/` folder into your project's Claude Code skills directory (commonly `.claude/skills/` or symlinked from a shared skills repo), then invoke `/plan-this` in any Claude Code session.
