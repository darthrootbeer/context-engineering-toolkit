# RC-adapt on haiku

Prompt (inputs filled with made-up samples):

```text
I have attached the README for "docs-readability-check". I want to try it on one doc without losing my original.

webhook-retries.md

Write me a trial plan. Use the install commands and the slash command from the README. Say what I should copy first so the original is safe, what the report should contain, and one sign that the skill rewrote something it should have left alone. Do not invent commands, flags, or file paths that the README does not contain, and say where the README gives no undo step.

A good answer uses the README's install commands and the exact command `/docs-readability-check [folder-or-file]`, tells me to work on a copy because the skill edits in place, names the report folder the README gives, and does not promise a particular grade level for my doc.
```

Answer:

# Trial Plan for docs-readability-check on webhook-retries.md

## Step 1: Install the skill

Run these commands from the root of your repo (or use `./.claude/skills` if you want this project only):

```bash
SKILLS_DIR="$HOME/.claude/skills"
mkdir -p "$SKILLS_DIR/docs-readability-check"
cp skills/docs-readability-check/SKILL.md "$SKILLS_DIR/docs-readability-check/SKILL.md"
```

Then start a new Claude Code session and type `/docs-read` to confirm it appears.

## Step 2: Make a safe copy

Copy `webhook-retries.md` to a new file (e.g., `webhook-retries-trial.md`). **The skill edits in place**, so work on the copy, not the original.

## Step 3: Run the skill

Type:
```
/docs-readability-check webhook-retries-trial.md
```

## Step 4: Check the report

Look for a file at `_process/style-audit/readability-audit-{folder-name}.md` (relative to your project root). The report will show:
- Grade level **before** and **after** (in plain labels like "10th grade")
- The four sentence patterns it found: stacked clauses, too many facts in one sentence, jargon followed by explanatory clauses, and wall paragraphs

## Watch for improper rewrites

One sign the skill rewrote something it shouldn't have: **changes inside code blocks, tables, or callouts**. The README says it "never edits" these, so if you find modifications there, something went wrong.

## Note: No undo step

The README gives no undo or rollback step. If the skill changes something incorrectly, you'll need to restore from your copy. Keep `webhook-retries.md` untouched while you experiment on `webhook-retries-trial.md`.

