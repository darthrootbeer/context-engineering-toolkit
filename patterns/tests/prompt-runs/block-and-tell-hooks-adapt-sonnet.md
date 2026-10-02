# block-and-tell-hooks prompt 3 (Adapt and test it) on sonnet

Prompt (the document's full text was pasted where it says [PASTE FILE]; other inputs filled with made-up samples):

```text
Here is a design pattern document: [PASTE FILE]

My rule is: Before editing any file under migrations/, read docs/MIGRATIONS.md in the same session.. My tool is: Claude Code.

Write the guard and marker scripts for my rule in my tool's hook format. Then give me a three-step test plan: one test where the guard must block, one where it must allow after the marker is written, and one where I confirm the release path works. Tell me what output proves each test passed.

A good answer gives a guard that exits 2 with a message on stderr and a marker script keyed by session id, shows the exact settings entry for my tool, and watches every tool that can change the file (for example both Edit and Write). Its three tests cover block, allow after the marker, and the release path, each with the output that proves it passed.
```

Answer:

# Migrations-doc guard for Claude Code

## Files

Save both in `.claude/hooks/` and run `chmod +x` on them.

**`.claude/hooks/migrations-guard.sh`** (PreToolUse)

```bash
#!/bin/bash
# Blocks edits under migrations/ until docs/MIGRATIONS.md has been read this session.
INPUT=$(cat)
SESSION_ID=$(echo "$INPUT" | jq -r '.session_id // "nosession"')
TOOL=$(echo "$INPUT" | jq -r '.tool_name // ""')
MARKER="/tmp/migrations-doc-read-${SESSION_ID}"

case "$TOOL" in
  Edit|Write|MultiEdit)
    TARGET=$(echo "$INPUT" | jq -r '.tool_input.file_path // ""')
    case "$TARGET" in
      */migrations/*|migrations/*) ;;
      *) exit 0 ;;                       # fast path: not a migrations file
    esac
    ;;
  Bash)
    CMD=$(echo "$INPUT" | jq -r '.tool_input.command // ""')
    case "$CMD" in
      *migrations/*) ;;
      *) exit 0 ;;                       # fast path: command never mentions migrations/
    esac
    # Only block write-shaped commands, so cat/ls/grep on migrations/ still work.
    echo "$CMD" | grep -Eq '(sed[[:space:]]+(-[A-Za-z]+[[:space:]]+)*-i|perl[[:space:]].*-i|tee[[:space:]]|(^|[;&|[:space:]])(mv|rm|cp|touch)[[:space:]]|[^0-9&>]>>?[[:space:]]*[^&[:space:]]*migrations/)' || exit 0
    ;;
  *) exit 0 ;;
esac

if [[ ! -f "$MARKER" ]]; then
  echo "Blocked: docs/MIGRATIONS.md has not been read this session." >&2
  echo "Read docs/MIGRATIONS.md with the Read tool, then retry this change to migrations/." >&2
  echo "Why: it holds the rules for writing and ordering migrations." >&2
  exit 2
fi
exit 0
```

**`.claude/hooks/migrations-marker.sh`** (PostToolUse)

```bash
#!/bin/bash
# Releases the migrations block once docs/MIGRATIONS.md has been read.
INPUT=$(cat)
SESSION_ID=$(echo "$INPUT" | jq -r '.session_id // "nosession"')
FILE=$(echo "$INPUT" | jq -r '.tool_input.file_path // ""')
[[ "$FILE" == *docs/MIGRATIONS.md ]] && touch "/tmp/migrations-doc-read-${SESSION_ID}"
exit 0
```

## Settings entry

Put this in `.claude/settings.json` (project) or `~/.claude/settings.json` (global):

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|Write|MultiEdit|Bash",
        "hooks": [
          { "type": "command", "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/migrations-guard.sh" }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Read",
        "hooks": [
          { "type": "command", "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/migrations-marker.sh" }
        ]
      }
    ]
  }
}
```

**Notes:**
- Only `Read` releases the block. A `cat docs/MIGRATIONS.md` through Bash won't, and the block message tells the agent to use Read.
- The Bash branch is a heuristic that recognizes write-shaped commands. If it blocks something harmless, treat that as a bug and tighten the regex.
- Prefer not to guard Bash at all? Remove `Bash` from the matcher and delete the `Bash)` branch. You'd then accept that `sed -i` on a migration can slip through.

## Test plan

Use a throwaway session id (`t1`) and clear any old marker first: `rm -f /tmp/migrations-doc-read-t1`.

**1. The guard must block**

```bash
echo '{"session_id":"t1","tool_name":"Edit","tool_input":{"file_path":"/repo/migrations/0042_add_users.sql"}}' \
  | .claude/hooks/migrations-guard.sh; echo "exit=$?"
```

Proof it passed:
- `exit=2`.
- stderr says `Blocked: docs/MIGRATIONS.md has not been read this session.` and tells you to read it.

Also check that unrelated edits and read-only commands are allowed (should print `exit=0`, no stderr):

```bash
echo '{"session_id":"t1","tool_name":"Edit","tool_input":{"file_path":"/repo/src/app.py"}}' | .claude/hooks/migrations-guard.sh; echo "exit=$?"
echo '{"session_id":"t1","tool_name":"Bash","tool_input":{"command":"ls migrations/"}}' | .claude/hooks/migrations-guard.sh; echo "exit=$?"
```

**2. The guard must allow after the marker is written**

```bash
echo '{"session_id":"t1","tool_name":"Read","tool_input":{"file_path":"/repo/docs/MIGRATIONS.md"}}' \
  | .claude/hooks/migrations-marker.sh; echo "exit=$?"
ls /tmp/migrations-doc-read-t1
echo '{"session_id":"t1","tool_name":"Write","tool_input":{"file_path":"/repo/migrations/0043_x.sql"}}' \
  | .claude/hooks/migrations-guard.sh; echo "exit=$?"
```

Proof it passed:
- The marker script prints `exit=0`.
- `ls` shows the marker file.
- The guard now prints `exit=0` with no stderr.

**3. The release path works**

This checks that the block can actually be cleared in a real session and doesn't leak across sessions.

1. Start a fresh `claude` session in the repo and ask it to edit a file in `migrations/`. It should be blocked, and the block message should be visible in the transcript.
2. The agent should then read `docs/MIGRATIONS.md` on its own and retry the edit in the same turn, with no human input.
3. In the same session, confirm the doc read itself was never blocked. The guard ignores paths outside `migrations/`.
4. Open a second session, which has a new session id. It should be blocked again, which shows the marker is per-session.

Proof it passed:
- The first edit attempt is refused with your stderr text.
- After the Read, the retried edit succeeds.
- `ls /tmp/migrations-doc-read-*` shows one marker per session that read the doc.
- The second session is blocked until it reads the doc.

If the first edit succeeds with no block, run `/hooks` to confirm both hooks are registered. Then rerun test 1 by hand, since a guard that exits anything other than 2 won't block.
