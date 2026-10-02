# block-and-tell-hooks prompt 2 (Review it against your setup) on sonnet

Prompt (the document's full text was pasted where it says [PASTE FILE]; other inputs filled with made-up samples):

```text
Here is a design pattern document: [PASTE FILE]

Below is a description of my own agent setup (tool, hook support, rules I currently rely on): I use Claude Code. Hooks are enabled in ~/.claude/settings.json. Today my rules are prose in a CLAUDE.md file: always run the tests before a merge, never edit files under migrations/ without reading docs/MIGRATIONS.md, and keep commit messages short.

List which parts of the pattern apply to my setup and which do not. Flag any claim that may be false for my tool, for example how it treats exit codes. Name one rule of mine that is a good candidate for a guard and one that is not, with a reason for each.

A good answer sorts the pattern into parts that apply and parts that do not for my stated tool, says plainly where the tool's exit-code behavior should be checked and does not assume it, and names one rule that suits a guard and one that does not, with a reason for each.
```

Answer:

## Applies to your setup

- **Paired guard and marker.** This fits Claude Code's `PreToolUse` and `PostToolUse` events. Your `~/.claude/settings.json` is the right place to register them.
- **Settings shape.** Event name as the key, a `matcher` string, and a `hooks` list of commands. This matches how Claude Code configures hooks.
- **Session-keyed marker.** `session_id` arrives in the JSON on stdin, so per-session state files work.
- **Block-and-tell.** Stderr from an exit-2 `PreToolUse` hook is surfaced to the agent, so the message-as-fix idea holds.
- **Fast path, release-path-first testing, and escape hatches.** These are tool-agnostic good practice.

## Does not apply, or needs adjusting

- **Write-back guards.** None of your three rules needs one.
- **The deploy example.** It is a template. Your matchers and paths will differ.
- **Cross-session shared state.** Your rules don't involve it, so that motivation is weaker for you.

## Claims to verify against your installed version

- **Exit codes.** Exit 2 blocks and exit 1 does not, per the Claude Code docs as I know them. Don't take my word or the document's for it. Write a throwaway `PreToolUse` hook that does `exit 1`, then another that does `exit 2`, and confirm that only the second stops the call.
- **"Hooks cannot rewrite a tool call's input."** This may be outdated. Newer Claude Code versions support structured JSON hook output, including a permission decision and possibly input modification. Check the current hooks docs. The block-and-print-the-corrected-value approach still works regardless.
- **PostToolUse timing.** The marker only runs after the tool succeeds, which is what you want. Exit 2 there cannot undo the call, so don't put enforcement in it.
- **Tool coverage.** The document says to list every tool that can touch the file. Beyond `Edit|Write`, check whether `MultiEdit` or `NotebookEdit` exist in your version. Also, `Bash` can modify files (`sed -i`, `>`, `tee`), so an `Edit|Write`-only guard has a hole. Decide whether to match `Bash` commands mentioning `migrations/` too, and watch for the false-block problem from sharp edge 3.

## Your rules

**Good candidate: "never edit files under migrations/ without reading docs/MIGRATIONS.md."**
- It is mechanically checkable: either a `Read` of that file happened this session or it didn't.
- A skip is costly, since a bad migration is hard to undo.
- Guard: `PreToolUse` on `Edit|Write`, which exits 2 if `file_path` contains `/migrations/` and the marker is absent. The stderr message should say "Read docs/MIGRATIONS.md, then retry."
- Marker: `PostToolUse` on `Read` that touches the session marker when the path ends in `docs/MIGRATIONS.md`.
- The release path is trivial, which is what you want.

**Poor candidate: "keep commit messages short."**
- "Short" is a judgment call, not an event. The pattern's own "when not to" section excludes this.
- You'd have to parse `git commit -m` out of arbitrary Bash, including heredocs and `-F`, which invites false blocks.
- The cost of a skip is trivial and easy to fix. Leave it in `CLAUDE.md`.

**In between: "always run the tests before a merge."**
- It is checkable, but "tests ran" is weaker than "tests passed." A marker keyed on a `Bash` call containing your test command would be satisfied by a failing run unless you also inspect the tool's result.
- It is also stale if code changes after the run. Consider adding a guard on `git merge`/`gh pr merge` only after you've confirmed the exit-code behavior and settled what counts as passing.

I'd start with the migrations guard, since it exercises the whole pattern with the least risk.
