# RC-adapt on sonnet

Prompt (inputs filled with made-up samples):

```text
I have attached the README for "docs-readability-check". I want to try it on one doc without losing my original.

webhook-retries.md

Write me a trial plan. Use the install commands and the slash command from the README. Say what I should copy first so the original is safe, what the report should contain, and one sign that the skill rewrote something it should have left alone. Do not invent commands, flags, or file paths that the README does not contain, and say where the README gives no undo step.

A good answer uses the README's install commands and the exact command `/docs-readability-check [folder-or-file]`, tells me to work on a copy because the skill edits in place, names the report folder the README gives, and does not promise a particular grade level for my doc.
```

Answer:

# Trial plan: docs-readability-check on `webhook-retries.md`

## 1. Install (README commands, run from the repo root)

```bash
SKILLS_DIR="$HOME/.claude/skills"   # use ./.claude/skills to install for one project only
mkdir -p "$SKILLS_DIR/docs-readability-check"
cp skills/docs-readability-check/SKILL.md "$SKILLS_DIR/docs-readability-check/SKILL.md"
```

Start a new Claude Code session and type `/docs-read`. The command should appear in the list. If it doesn't, stop here, because the install didn't take.

## 2. Copy first, then work on the copy

The README says the skill rewrites sentences **in place**, so the original is at risk if you point it at the real file. Before running anything:

1. Make a backup of `webhook-retries.md` somewhere the skill won't touch, and leave it alone. Any plain copy works; the README gives no copy command for this, so use your usual one.
2. Make a second copy to be the trial file, for example in a new folder of its own. Run the skill on that copy only.

A separate folder helps in two ways. The skill accepts a folder or a file, and the report filename is built from the folder name (`readability-audit-{folder-name}.md`), so a dedicated folder keeps the report easy to find. Also avoid placing the copy under `_archive/`, `_templates/` or `_attachments/`, since the README says those are skipped.

## 3. Run

```
/docs-readability-check [folder-or-file]
```

Replace the bracket with the path to your trial copy (the path is required). Run it once.

## 4. What the report should contain

The report is written to `_process/style-audit/readability-audit-{folder-name}.md`, relative to the project root. If your copy sits inside an Obsidian vault, it goes to `_system-audits/` in the vault instead.

Per the README, it should show:
- the grade level **before** and **after**, in plain labels such as "10th grade"
- paragraphs the skill could not safely rewrite, flagged for a person

The target grade comes from the `diataxis_type` in your doc's frontmatter. Without a type, the target is 11th to 12th grade. The README doesn't say what your doc will score, and the score is an estimate from a 250-word sample of the middle of the prose, so don't expect or require a particular result. Reference docs with many technical terms may score high regardless, and the skill is meant to say so rather than force the number down.

## 5. A sign it rewrote something it shouldn't have

Compare your trial copy with the backup. The README says the skill never edits tables, code blocks or callouts, and never adds or removes information. So the clearest warning sign is **any difference inside a table, a code block or a callout**. For a webhook retries doc, that means a changed retry interval, status code, header name or JSON example. A changed vocabulary, structure or voice in the prose would be a second sign, since the README says those stay the same.

## 6. Undo

**The README gives no undo step.** It describes no backup, dry-run, revert command or flag. Your only way back is the copy you made in step 2. If you're happy with the result, bring the changes over to the original by hand, after reviewing the differences.

One caveat: the README's author says they have run it on their own documentation, not on yours, so treat this as a real trial.

