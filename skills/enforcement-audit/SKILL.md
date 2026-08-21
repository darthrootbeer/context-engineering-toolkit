---
name: enforcement-audit
description: Audit the enforcement stack for a named skill, hook, or automated process — maps every guarded behavior to a trust level, finds gaps where critical behavior relies on the model's good judgment instead of code that cannot be argued with, writes an executable plan, and can carry it out end to end. Use when you want to know "why does this automation sometimes fail?", "what's the weakest link in this process?", or "what should be a hard block instead of a rule?".
argument-hint: <skill-name | hook-name | process-name | all>
allowed-tools: [Read, Bash, Glob, Grep, Write, Edit, Skill]
---

# /enforcement-audit

You are acting as a senior engineer auditing an AI-agent installation — a project's set of Claude Code skills, hooks, and configuration. Your job is not to ask "is this well-written?" It is to ask: **"Where is this system relying on the model's good behavior when it should be relying on code that cannot be argued with?"**

Agent instructions work most of the time. This skill exists to make the critical ones work all of the time.

This is a three-phase pattern: **assess → plan → execute**. Run all three without pausing between them unless a change hits the always-pause list in Phase 4b below — stopping after the assessment to ask permission defeats the point of automating the audit.

---

## The Trust Hierarchy

This is the core idea the whole skill is built on. Every enforcement mechanism in an agent-driven system has a trust level — how likely it is to actually stop a bad outcome, independent of how well-intentioned the model is in that moment.

```
LEVEL 1 — Harness-enforced (cannot be bypassed by the model or the user)
  A pre-action hook that hard-exits → the action is cancelled, period.
  No prompt engineering, no persuasion, no "just this once" gets past this.

LEVEL 2 — Hard block (stops execution, the model cannot proceed)
  A hook or gate that halts the run with a nonzero exit.
  A deny-listed action in the harness's permission config.

LEVEL 3 — Script logic (always runs the same way)
  Shell/Python/etc. scripts the model calls as a tool.
  Code is code — it runs identically every time, no hallucination possible.
  Data stored in a file is always the same data — no drift.

LEVEL 4 — Advisory hook (non-blocking, the model can ignore it)
  A message shown after the fact, or a reminder injected before an action —
  seen, but not enforced. The model may or may not act on it.

LEVEL 5 — Prose instructions in the skill/prompt itself (model-dependent)
  Written instructions the model usually follows — but fails under
  pressure, ambiguity, or a long context window. Writing "HARD RULE" in
  capital letters is better than nothing, but it is not reliable alone.

LEVEL 6 — Global/project-level instruction files (model-dependent, loaded broadly)
  Broader coverage than a single skill's prose, but the same underlying
  weakness: the model can drift, misapply, or forget under load.

LEVEL 7 — Memory / long-term context (softest — can go stale, can be misremembered)
  Anything the model "knows" from a persisted memory store rather than
  from a live read of current state. No enforcement weight at all.
```

**The cardinal rule:** any action that is destructive, irreversible, external-facing, or high-stakes must be enforced at Level 1 or 2. Finding that a destructive action only has Level 5–7 enforcement is the single highest-value thing this audit can surface.

This hierarchy generalizes past Claude Code — the same ladder applies to any agent framework with hooks/guardrails (a middleware layer that can reject a tool call) versus prompt-only instructions (text the model reads and usually follows).

---

## Arguments

The user invoked this skill with: `$ARGUMENTS`

Parse the argument:
- A skill/prompt name → assess that one skill and everything it does
- A hook or guard-script name → assess that hook and everything it guards
- A named process (a multi-step flow spanning several skills/hooks) → assess the full stack for that process
- `all` → sweep every skill and every wired hook in the project
- No argument → ask: "What should I assess? Provide a skill name, hook name, process name, or 'all'."

If the argument doesn't match a known name exactly, use fuzzy matching against the project's skills/hooks/scripts directories. If still no match, list candidates and ask for clarification.

---

## Configuration

This skill needs to know where things live in the host project. Set these once, near the top of your working copy, to match your project's actual layout:

```bash
SKILLS_DIR="${SKILLS_DIR:-.claude/skills}"
HOOKS_DIR="${HOOKS_DIR:-.claude/hooks}"
SCRIPTS_DIR="${SCRIPTS_DIR:-.claude/scripts}"
SETTINGS_FILE="${SETTINGS_FILE:-.claude/settings.json}"
FINDINGS_DIR="${FINDINGS_DIR:-.claude/assessments}"
```

Adjust these to wherever your project actually keeps its skills, hooks, and settings. If the project has no hook/guard mechanism at all (pure prompt-only setup), say so up front — Phase 1c–1f below simply find nothing to map, which is itself a finding.

---

## Phase 1 — Discovery: Map the Enforcement Stack

Before analyzing anything, build the complete picture for the target.

### 1a. Read source of truth first

```bash
cat "$SETTINGS_FILE"
ls "$HOOKS_DIR"
ls "$SKILLS_DIR"
ls "$SCRIPTS_DIR"
```

### 1b. If assessing a specific skill

```bash
cat "$SKILLS_DIR/<target>/SKILL.md"
```

Extract from it:
- Every action the skill takes (shell calls, file writes, API calls, external sends)
- Every condition the skill checks (guards, gates, status checks)
- Every file it reads as source of truth
- Any external services it touches (issue trackers, email, SSH, APIs)
- What it considers a "failure" and what happens then

### 1c. Find all hooks that guard this skill's actions

From the settings file, extract every wired hook. For each one, read it and map:
- What tool call it intercepts
- What condition it checks
- What exit/return code it uses (0 = advisory, nonzero = hard block, in most harnesses)
- Whether it requires an external token/service to function, and what happens when that's missing

### 1d. Find all scripts the skill calls

Grep the skill's instructions for script references and read each one. Note: script logic = Level 3 trust — it always runs the same way regardless of model state.

### 1e. Find all data files the skill reads

Any file read at runtime as source of truth is Level 3. Any fact the skill "knows" from prose alone (hardcoded assumptions, states it never actually checks) is Level 5–7.

### 1f. Check for unwired hooks

```bash
ls "$HOOKS_DIR" | while read f; do
  grep -q "$f" "$SETTINGS_FILE" || echo "UNWIRED: $f"
done
```

Unwired hook files are dead code — they do nothing, regardless of how they read.

---

## Phase 2 — Trust-Level Scoring

For each critical behavior identified in Phase 1, assign a trust level and build a table:

| Behavior | Current Enforcement | Trust Level | Verdict |
|---|---|---|---|
| [what the skill does] | [hook/script/prose/nothing] | [1–7] | [RED/YELLOW/GREEN] |

**Verdicts:**
- 🔴 RED — critical behavior sits at Level 5, 6, or 7. Needs to move up.
- 🟡 YELLOW — behavior sits at Level 4 (advisory only). Fine for non-critical actions; needs upgrading if the action is destructive or external-facing.
- 🟢 GREEN — behavior sits at Level 1, 2, or 3. Well-enforced.

**What counts as "critical":**
- Sends data to an external service (email, an API call that changes remote state)
- Deletes, overwrites, or publishes something that can't be undone
- Closes, merges, or marks something done in a tracker
- Skips a required quality check
- Makes a decision based on assumed state rather than freshly read state

**What does not need hard enforcement:**
- Formatting output
- Choosing which section of a report to generate first
- Reading files (reads are never destructive)
- Suggesting next steps

---

## Phase 3 — Findings Document

Write full findings to a file — before showing anything on screen:

```bash
mkdir -p "$FINDINGS_DIR"
FINDINGS_FILE="$FINDINGS_DIR/assess-[target]-$(date +%Y%m%d-%H%M).md"
```

The file must contain everything needed to build a plan without re-running the assessment:

```
# Assessment: [target name]
generated: [timestamp]
target: [name]
verdict: [well-enforced / partially enforced / dangerously under-enforced]

## Trust Table
[full behavior → enforcement → trust level → verdict table]

## Findings

### P0 — [title]
**Finding:** [what the skill does that's destructive]
**Current enforcement:** [prose/rule/nothing]
**Why this is P0:** [what goes wrong when the model has an off moment]
**Fix:** [exact fix — hook pattern, script change, config wiring]

### P1 — [title]
**Finding:** [hook name] is advisory-only on [action]
**Current enforcement:** Level 4 — surfaced, but the model can proceed anyway
**Why this matters:** [scenario where the model proceeds despite the warning]
**Fix:** [exact change — new exit behavior, config update]

[... P2-P5 for smaller gaps ...]

## Well-enforced
[list of behaviors already at Level 1-3]
```

**A clean bill of health is a real, expected outcome — not a failure to find something.** If every behavior scores 🟢 GREEN, say so plainly and stop. Do not manufacture a low-priority finding just to have something to report.

---

## Phase 4 — Screen Output, Then Plan and Execute

Show only a compact summary table on screen (priority, one-line problem, one-line fix, rough effort) — the full detail lives in the findings file, not in the chat transcript.

If Phase 3 found zero findings, print that plainly and stop here — there is nothing to plan or execute.

### 4a. Turn findings into a plan

Use a plan-capture skill (see the `plan-this` skill in this repo, or your project's equivalent) to turn the findings file into a stored, executable task list. Read the resulting plan file — you need its task list to execute next.

### 4b. Always-pause list

Before executing any task that edits enforcement code, check it against this enumerated list — do not judge "is this risky enough to pause for" case by case, check the list itself:

- Adds, removes, or edits a permission entry (allow/deny/ask) in the project's settings
- Adds, removes, or reorders a hook wiring entry
- Changes a hook's exit/return-code logic (what triggers a hard stop versus a pass-through)
- Touches a file the project has explicitly marked protected
- Deletes a hook, script, or skill file rather than editing it
- Any other action that is destructive or irreversible

Everything else in the plan: execute without pausing. The list exists precisely so "is this risky enough to pause for" is never a judgment call made under the same pressure that causes the gaps this skill hunts for elsewhere.

### 4c. Per-task execution

Work through the plan's tasks in dependency order. For any task that edits a hook, script, or settings file:

1. Create a git checkpoint (a working branch, if not already on one) before the first such edit.
2. Apply the change.
3. Run the task's verification step. If it fails, do not mark the task done — log the failure instead of continuing silently.
4. Run the strengthens-not-weakens check below.
5. Commit that task's change on its own — never batch multiple enforcement edits into one commit. This is the rollback path: if task 4 of 7 fails, tasks 1-3 are already safe on disk individually.

### 4d. Strengthens-not-weakens check (mandatory for every enforcement edit)

A "fix" that touches enforcement code must move the affected behavior *up* the trust hierarchy, never down, while being reported as resolved.

- If the fix turned a hard stop into a pass-through, or removed a deny rule, or removed a condition that used to block an action — that is a regression, not a fix. Stop; do not mark it done; log it as needing a different approach.
- If the fix added a new hard stop, added a deny rule, or moved logic from prose into a script/hook — that is a genuine strengthening. Proceed.
- When genuinely unsure which way a change moves the needle, treat it as a 4b pause case rather than guessing.

---

## Phase 5 — Final Report

The last thing shown, always — the point of running end to end is that the user sees the outcome, not a promise of one.

**If findings existed and were executed:**
```
## Improved: [target name]

- [what changed, one line per task]

Before: [verdict from Phase 2]
After: [new verdict]
```

**If a task hit a blocker:** include it in the list with what happened — never drop it silently.

**If Phase 3 found zero findings:**
```
## Assessed: [target name]

No changes made — every critical behavior is already enforced at Level 1-3.
```

---

## What This Skill Does Not Do

- Does not fabricate a fix when none is needed
- Does not pause for confirmation before applying a fix, except for the enumerated always-pause list in Phase 4b
- Does not mark an enforcement fix complete without the strengthens-not-weakens check
- Does not batch multiple enforcement edits into one commit
- Does not delete or archive existing hooks or scripts as a side effect
- Does not grade style or prose quality — only enforcement reliability
- Does not produce findings for read-only operations

**Honesty about this skill's own limits:** the always-pause list and the strengthens-not-weakens check are themselves prose-level controls (Level 5 on the hierarchy above) — they are followed by the same model doing the editing, with no external hard block stopping a skipped pause or a misjudged call. The per-task git commit is the real hard mitigation: it makes any bad edit trivially revertible. A future audit of this skill should not mistake "enumerated" for "enforced."
