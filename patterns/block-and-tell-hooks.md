# Pattern: block-and-tell hooks

A way to make an AI coding agent's "always do X first" instructions actually reliable, instead of hoping the model remembers.

## The problem

Say you want a rule like: "Before touching any file in this shared status document, read it first — someone else might have changed it since your last read." You can write that instruction into the agent's system prompt or a rules file. It will work most of the time. It will also, eventually, get skipped — under a long context window, mid-task pressure, or just an off moment. Prose instructions are Level 5 on the trust hierarchy (see `enforcement-audit` in this repo's `skills/` folder): the model usually follows them, but "usually" is not the same as "always," and the cost of a skip here is a silently overwritten file with no error and no merge conflict.

## The fix: a paired hook

Split the rule into two small pieces of code that run outside the model's judgment entirely:

1. **A `PreToolUse` guard.** Before the agent runs a command that touches the guarded file, this hook checks a condition (has the read actually happened this session?) and, if the condition fails, returns a nonzero exit code. That is not advisory — most agent harnesses treat a nonzero exit from a pre-action hook as a hard stop. The tool call never executes.
2. **A `PostToolUse` marker.** After the agent actually reads the target file (via whatever read tool the harness provides), this hook fires and clears the block — usually by writing a small state file (a timestamp, a flag) that the guard checks.

The two hooks are a matched pair. Neither one is useful alone: the guard without the marker locks the agent out permanently; the marker without the guard is inert, since nothing is enforcing the read in the first place.

```
PreToolUse (before Edit/Write/Bash on target file)
  → check: has the marker fired since session start / since last write?
  → if no: exit 2, print a plain-English explanation of what to read and why
  → if yes: allow the call through

PostToolUse (after Read/Grep/Glob touches the target file)
  → write/update the marker (a state file, a timestamp)
  → this clears the block for subsequent actions in the same session
```

## Why "block-and-tell," not just "block"

A bare hard stop with no explanation is worse than the problem it solves — the agent (or the human watching it work) has no idea what unblocks it. The guard's stderr output should always say, in plain language: what condition failed, what file to read, and why it matters. This turns a mysterious permission denial into a one-line fix the agent can execute on its own, in the same turn, without asking a human.

## A minimal, fully generic example

Say the rule is: "Before running any deploy command, confirm the changelog has been updated in this session."

**`hooks/deploy-changelog-guard.sh`** (PreToolUse, matched on the deploy command)

```bash
#!/bin/bash
# Blocks a deploy command until the changelog marker exists for this session.
MARKER="/tmp/changelog-checked-${SESSION_ID:-default}"

if [[ ! -f "$MARKER" ]]; then
  echo "🚫 Changelog not confirmed this session." >&2
  echo "   Read or edit CHANGELOG.md before deploying." >&2
  exit 2
fi

exit 0
```

**`hooks/deploy-changelog-marker.sh`** (PostToolUse, matched on edits/reads of `CHANGELOG.md`)

```bash
#!/bin/bash
# Clears the deploy block once CHANGELOG.md has actually been touched.
touch "/tmp/changelog-checked-${SESSION_ID:-default}"
```

Wire both into the harness's hook configuration, matched to the right tool events. The specific config shape depends on which agent framework you're using — the pattern (a paired guard + marker, hard exit vs. state write) is the part that transfers.

## A real failure this pattern needs to guard against

The pattern has a sharp edge worth naming, because it bit a real deployment of this exact idea: **a guard hook that arms on one condition but has no path to ever clear itself is worse than no hook at all.** If the guard's trigger condition is too broad, or the corresponding marker's trigger condition is too narrow, the agent can end up permanently locked out of an entire class of action mid-session, with no available fix. The postmortem lesson: whenever you write a guard, write its release condition *first*, and test the release path before the block path. A hook that can trap the agent with no way out is a bug, not a feature — "annoying but escapable" is the ceiling for how strict a block should feel.

## When to reach for this pattern

- The action is destructive, irreversible, or affects state shared with another process/session
- A prose instruction for the same rule has already been skipped once in practice
- The condition being checked is objectively verifiable (a file was read, a flag is set) — not a judgment call the model has to make correctly every time

## When not to

- The action is read-only or trivially reversible
- The "always do X first" instruction has never actually been skipped — don't build enforcement for a failure mode that hasn't happened
- The condition can't be checked mechanically (it requires judgment about content, not just "did an event occur")

