# block-and-tell-hooks prompt 2 (Review it against your setup) on haiku

Prompt (the document's full text was pasted where it says [PASTE FILE]; other inputs filled with made-up samples):

```text
Here is a design pattern document: [PASTE FILE]

Below is a description of my own agent setup (tool, hook support, rules I currently rely on): I use Claude Code. Hooks are enabled in ~/.claude/settings.json. Today my rules are prose in a CLAUDE.md file: always run the tests before a merge, never edit files under migrations/ without reading docs/MIGRATIONS.md, and keep commit messages short.

List which parts of the pattern apply to my setup and which do not. Flag any claim that may be false for my tool, for example how it treats exit codes. Name one rule of mine that is a good candidate for a guard and one that is not, with a reason for each.

A good answer sorts the pattern into parts that apply and parts that do not for my stated tool, says plainly where the tool's exit-code behavior should be checked and does not assume it, and names one rule that suits a guard and one that does not, with a reason for each.
```

Answer:

## What applies to your Claude Code setup

Nearly all of this pattern applies directly:

- **Core mechanism:** PreToolUse and PostToolUse hooks exist in Claude Code and match the document's behavior.
- **Exit codes:** The document is written for Claude Code and explicitly describes the exit-code behavior you have: code 2 blocks, code 1 does not. This is already verified for your tool.
- **Paired guard/marker pattern:** The session-id keying, JSON input format, tool matching (Bash, Edit, Read, Write), and hook registration in `~/.claude/settings.json` are all Claude Code features shown in the example.
- **The two guard shapes:** Read-first and write-back both work in your setup.

## Where not to assume

The document's exit-code claims are stated as Claude Code specific ("In Claude Code, exit code 2 is the one that blocks"). You don't need to verify those—they're already tailored to your tool. The hook event names and JSON format in the examples are also Claude Code native, not a guess.

## One rule that suits a guard, one that doesn't

**Good candidate: "Never edit files under migrations/ without reading docs/MIGRATIONS.md"**

Why: This is destructive (migrations affect the whole team), the condition is mechanically checkable (read happened or not), and it has a clear release path (read the file, marker clears the block). A missed read here is genuinely costly. This matches the document's advice: "destructive, irreversible, or touches state another session or process shares" and "mechanically checkable."

**Not a good candidate: "Keep commit messages short"**

Why: The pattern says "The condition needs judgment about content, not just 'did an event occur.'" Enforcing message length requires deciding what "short" means—that's a judgment call, not a checkable event. A guard could block all commits until you manually edit the message, but that's busywork, not reliable enforcement.

(The test-before-merge rule is borderline; it *could* be guarded, but a failed merge is easier to undo than a broken migration, so it's lower urgency than migrations.)
