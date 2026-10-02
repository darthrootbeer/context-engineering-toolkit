# block-and-tell-hooks prompt 3 (Adapt and test it) on haiku

Prompt (the document's full text was pasted where it says [PASTE FILE]; other inputs filled with made-up samples):

```text
Here is a design pattern document: [PASTE FILE]

My rule is: Before editing any file under migrations/, read docs/MIGRATIONS.md in the same session.. My tool is: Claude Code.

Write the guard and marker scripts for my rule in my tool's hook format. Then give me a three-step test plan: one test where the guard must block, one where it must allow after the marker is written, and one where I confirm the release path works. Tell me what output proves each test passed.

A good answer gives a guard that exits 2 with a message on stderr and a marker script keyed by session id, shows the exact settings entry for my tool, and watches every tool that can change the file (for example both Edit and Write). Its three tests cover block, allow after the marker, and the release path, each with the output that proves it passed.
```

Answer:

# Guard and marker scripts for migrations rule

I'll give you the two scripts, the settings entry, and a test plan.

## Guard script: `~/.claude/hooks/migrations-guard.sh`

```bash
#!/bin/bash
INPUT=$(cat)
SESSION_ID=$(echo "$INPUT" | jq -r '.session_id // "nosession"')
FILE=$(echo "$INPUT" | jq -r '.tool_input.file_path // ""')

# Fast path: only block migrations/ edits
case "$FILE" in
  migrations/*) ;;
  *) exit 0 ;;
esac

MARKER="/tmp/migrations-guide-read-${SESSION_ID}"
if [[ ! -f "$MARKER" ]]; then
  echo "Blocked: docs/MIGRATIONS.md must be read before editing migration files." >&2
  echo "Read docs/MIGRATIONS.md first to understand the migration guidelines." >&2
  exit 2
fi
exit 0
```

## Marker script: `~/.claude/hooks/migrations-marker.sh`

```bash
#!/bin/bash
INPUT=$(cat)
SESSION_ID=$(echo "$INPUT" | jq -r '.session_id // "nosession"')
FILE=$(echo "$INPUT" | jq -r '.tool_input.file_path // ""')

[[ "$FILE" == "docs/MIGRATIONS.md" ]] && touch "/tmp/migrations-guide-read-${SESSION_ID}"
exit 0
```

## Settings entry for `~/.claude/settings.json`

Add this to your `hooks` object:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          { "type": "command", "command": "~/.claude/hooks/migrations-guard.sh" }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Read",
        "hooks": [
          { "type": "command", "command": "~/.claude/hooks/migrations-marker.sh" }
        ]
      }
    ]
  }
}
```

## Three-step test plan

**Test 1: Block without reading (must fail)**
- Try to edit `migrations/001_initial.sql`
- Expected: Edit is blocked
- Proof: stderr shows exactly "Blocked: docs/MIGRATIONS.md must be read before editing migration files." followed by the instruction to read it

**Test 2: Allow after reading (must succeed)**
- Read `docs/MIGRATIONS.md` 
- Then try to edit `migrations/001_initial.sql` again in the same session
- Expected: Edit succeeds without the block message
- Proof: no stderr message about being blocked; the file content changes are applied

**Test 3: Escape hatch (the release path)**
- Start a fresh session and try editing `migrations/002_add_users.sql`
- Get blocked with the "Blocked" message (Test 1 state)
- Read `docs/MIGRATIONS.md`
- Edit `migrations/002_add_users.sql` again
- Expected: the second edit succeeds
- Proof: first attempt shows block message in stderr; second attempt shows no block message and the edit is applied; marker file `/tmp/migrations-guide-read-<SESSION_ID>` exists after the read

The guard watches both `Edit` and `Write` because migrations might be written programmatically. The marker watches only `Read` and checks for the exact filename, so grepping for "MIGRATIONS" in a commit message won't accidentally clear the block.
