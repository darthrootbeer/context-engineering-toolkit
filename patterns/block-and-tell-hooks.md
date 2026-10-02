# Pattern: block-and-tell hooks

A way to make an AI coding agent's "always do X first" instructions reliable, instead of hoping the model remembers.

Written for Claude Code, where the hook events and exit codes below are real. Other agent tools have similar hooks, but check how each one treats exit codes before copying anything.

## The problem

Say you want a rule like: "Before touching a shared status document, read it first. Someone else may have changed it since your last read." You can write that into a rules file. It will work most of the time. It will also get skipped eventually: a long context, mid-task pressure, an off moment. The cost of one skip here is a silently overwritten file, with no error and no merge conflict.

Instructions sit on a ladder of how much you can trust them. From strongest to weakest: the harness itself refuses the action, a hook script refuses it, a script checks after the fact, a rule is loaded into context, a skill's prose asks nicely. The bottom rungs usually work. "Usually" is not "always."

## The fix: a paired hook

Split the rule into two small scripts that run outside the model's judgment:

1. **A `PreToolUse` guard.** Before the agent runs a tool call, the guard checks a condition (did the read happen this session?). If the condition fails, the guard exits with code **2**. In Claude Code, exit code 2 is the one that blocks the call. The tool never runs, and whatever the guard wrote to stderr is shown to the agent.
2. **A `PostToolUse` marker.** After the agent does the thing you wanted (reads the file), this hook fires and writes a small state file. The guard looks for that file.

**Exit 1 does not block.** Any non-zero code other than 2 is treated as a hook error, and the tool call goes ahead anyway. A guard that exits 1 looks like enforcement and enforces nothing. This was found the hard way in a real setup: guards written with `exit 1` had been letting calls through. Use `exit 2` to block and `exit 0` to allow.

The two hooks are a matched pair. The guard without the marker locks the agent out for good. The marker without the guard is inert, because nothing demands the read.

```
PreToolUse (before Edit/Write/Bash that touches the target)
  -> check: does the marker file exist for this session?
  -> no:  exit 2, print what to read and why
  -> yes: exit 0, let the call through

PostToolUse (after Read/Grep/Glob touches the target)
  -> write the marker file (keyed by session id)
  -> later calls in this session pass the guard
```

## Block-and-tell, not just block

A bare refusal is worse than the problem it solves. Nobody knows what unblocks it. The guard's stderr should say, in plain words: what condition failed, which file to read, and why it matters. That turns a mystery into a one-line fix the agent can do in the same turn without asking a human.

Some blocks cannot be fixed by reading. Hooks cannot rewrite a tool call's input, so a guard that wants a different value (for example, a task title that needs an ID prefix) blocks and prints the exact corrected value to retry with. Same idea, different payload.

## Two shapes of guard

- **Read-first.** Block until a marker proves the agent looked at the source of truth. This is the example below.
- **Write-back.** Arm the guard after a state change, and clear it only when the agent records that change. For example: after the agent restarts a service, block further commands against that machine until the status note has been updated. The guard writes a "pending" file when it sees the state change, and a PostToolUse marker clears it when the status note is edited. This keeps a notes file from drifting away from reality.

## A minimal, fully generic example

Rule: "Before running a deploy command, confirm the changelog was touched in this session."

**`hooks/deploy-changelog-guard.sh`** (PreToolUse, matched on Bash)

```bash
#!/bin/bash
# Blocks a deploy command until the changelog marker exists for this session.
INPUT=$(cat)                          # the hook receives JSON on stdin
SESSION_ID=$(echo "$INPUT" | jq -r '.session_id // "nosession"')
CMD=$(echo "$INPUT" | jq -r '.tool_input.command // ""')

# Fast path: this guard runs on every Bash call, so do a cheap test first.
case "$CMD" in
  *"deploy"*) ;;
  *) exit 0 ;;
esac

MARKER="/tmp/changelog-checked-${SESSION_ID}"
if [[ ! -f "$MARKER" ]]; then
  echo "Blocked: changelog not confirmed this session." >&2
  echo "Read or edit CHANGELOG.md, then run the deploy again." >&2
  exit 2
fi
exit 0
```

**`hooks/deploy-changelog-marker.sh`** (PostToolUse, matched on Read and Edit)

```bash
#!/bin/bash
# Clears the deploy block once CHANGELOG.md has actually been touched.
INPUT=$(cat)
SESSION_ID=$(echo "$INPUT" | jq -r '.session_id // "nosession"')
FILE=$(echo "$INPUT" | jq -r '.tool_input.file_path // ""')
[[ "$FILE" == *CHANGELOG.md ]] && touch "/tmp/changelog-checked-${SESSION_ID}"
exit 0
```

Register both in `~/.claude/settings.json` under `hooks`, each with a `matcher` for the tool names it should watch. The marker is keyed by session id so one session's read does not clear another session's block.

## Three sharp edges

**1. A guard that arms with no way to clear is worse than no guard.** If the trigger is too broad or the marker's trigger is too narrow, the agent can end up locked out of a whole class of action with no fix. Write the release condition first. Test the release path before the block path. "Annoying but escapable" is the ceiling for how strict a block should feel. For write-back guards, also keep one narrow escape hatch: a command whose only job is deleting the pending file must be allowed through.

**2. Guards run on every call, so keep them cheap.** A guard on Bash fires for every shell command in the session. Do a quick substring test first and `exit 0` immediately when the command has nothing to do with the rule.

**3. Matching words in prose causes false blocks.** A guard that greps the whole command for a word like "deploy" will also fire on a commit message or a heredoc that merely mentions it. Match on the command shape where you can, and treat a false block as a bug to fix, not a cost of doing business.

## When to reach for this pattern

- The action is destructive, irreversible, or touches state another session or process shares.
- A prose rule for the same thing has already been skipped once in practice.
- The condition is mechanically checkable (a file was read, a flag exists), not a judgment call.

## When not to

- The action is read-only or easy to undo. A real setup exempts read tools from its guards for exactly this reason.
- The rule has never been skipped. Do not build enforcement for a failure that has not happened.
- The condition needs judgment about content, not just "did an event occur."

## Related

- The same gate idea works for workflows, not just tool calls. The [docs pipeline](../pipelines/docs-pipeline/) stops between stages and waits for a human reply before moving on, which is a guard whose "marker" is the reply.
- [Rules-index architecture](rules-index-architecture.md): rule files can state what a hook enforces, so the prose and the enforcement stay linked.

## How this was checked

Every claim here was compared against a working Claude Code setup with dozens of hooks: the exit-2 behavior (a past fix for guards exiting 1), the guard and marker pairing, the per-session marker file, the write-back variant with its pending file and escape hatch, and the fast-path check. The example scripts above are generic and written for this page.

## Prompt for your AI model

Give any AI model this file plus one of the prompts below. Paste the file text where the prompt says `[PASTE FILE]`.

**1. Understand and teach it**

```
Here is a design pattern document: [PASTE FILE]

Explain it to me as if I know what a script is but have never used hooks. Use a different everyday analogy than the one in the document. Then ask me three questions, one at a time, that check I understand why exit code 2 matters and why a guard needs a release path. Wait for my answer before each next question.
```

**2. Review it against your setup**

```
Here is a design pattern document: [PASTE FILE]

Below is a description of my own agent setup (tool, hook support, rules I currently rely on): [DESCRIBE YOUR SETUP]

List which parts of the pattern apply to my setup and which do not. Flag any claim that may be false for my tool, for example how it treats exit codes. Name one rule of mine that is a good candidate for a guard and one that is not, with a reason for each.
```

**3. Adapt and test it**

```
Here is a design pattern document: [PASTE FILE]

My rule is: [YOUR "ALWAYS DO X FIRST" RULE]. My tool is: [YOUR AGENT TOOL].

Write the guard and marker scripts for my rule in my tool's hook format. Then give me a three-step test plan: one test where the guard must block, one where it must allow after the marker is written, and one where I confirm the release path works. Tell me what output proves each test passed.
```

**How these prompts were checked.** Each of the three prompts was run once with a small model (Claude Haiku) through the `claude` command line, with the full text of this file pasted in and sample details filled in. All three gave an on-topic answer that matched what this file says. In two runs a placeholder was left unfilled by my test setup, and the model noticed and said so or asked for the missing text instead of making something up. That is the behavior you want. One run per prompt is a light check, not a benchmark, so read the answers critically. I did not save those answers, so there is no record to read here, unlike the saved runs in `pipelines/job-assessment/tests/`.
