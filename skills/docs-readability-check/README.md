# docs-readability-check

A Claude Code skill that checks how hard a doc is to read and rewrites the dense sentences. It estimates a reading grade level for each doc, finds the sentence patterns that make technical writing feel heavy, and fixes them without changing the vocabulary, the structure or the voice.

It is Stage 3d of the [docs-pipeline](../../pipelines/docs-pipeline/README.md), where it runs after the "human" style pass and before the grammar pass. It also works on its own, on any folder of markdown files.

## Command

```
/docs-readability-check [folder-or-file]
```

The path is required. A folder means every `.md` file inside it. Files under `_archive/`, `_templates/` and `_attachments/` are skipped.

## What it does

1. Reads each doc and works out its target grade level from the `diataxis_type` in the frontmatter (explanation and overview 10th to 11th grade, how-to and tutorial 11th to 12th, reference 12th to college freshman). A doc with no type gets the 11th to 12th grade target.
2. Scores a 250-word sample from the middle of the prose, with code, tables, callouts and diagrams removed.
3. Finds four patterns: stacked clauses, too many facts in one sentence, jargon followed by a clause that explains it, and wall paragraphs.
4. Rewrites the sentences it can fix safely, in place. Paragraphs it cannot safely rewrite are flagged for a person.
5. Scores again and writes a report with the grade level before and after, in plain labels such as "10th grade".

It never edits tables, code blocks or callouts, and it does not add or remove information.

## Output

A report in `_process/style-audit/` named `readability-audit-{folder-name}.md`, relative to the project root. If the input sits inside a notes folder that has a `_system-audits/` folder, the report goes there instead.

## Install

Claude Code loads a skill from `<skills folder>/<name>/SKILL.md`. From the root of this repo:

```bash
SKILLS_DIR="$HOME/.claude/skills"   # use ./.claude/skills to install for one project only
mkdir -p "$SKILLS_DIR/docs-readability-check"
cp skills/docs-readability-check/SKILL.md "$SKILLS_DIR/docs-readability-check/SKILL.md"
```

Start a new Claude Code session and type `/docs-read`. The command should appear in the list.

## Limits

The grade level is an estimate from a sample, not a measurement of the whole doc. Reference docs full of technical terms will score high whatever you do, and the skill says so instead of forcing the number down. I have run it on my own documentation, not on yours.

---

### Prompt for your AI model

Paste this into any AI model, together with this document and the files it describes.

**Understand and teach**

```text
I have attached the README for "docs-readability-check", a Claude Code skill that rewrites dense sentences in docs. Teach it to me as if I am a technical writer who has never used it.

1. Say in plain language what it checks and what it changes, and give the target grade for each doc type.
2. Say what it never touches.
3. Say where its report goes.
4. Then ask me three questions to check that I understood, one at a time. Wait for my answer before the next one, and correct me where I am wrong.

A good answer names the four sentence patterns, gives the target grade for each doc type, says tables, code blocks and callouts are never edited, and does not invent a feature or a command that is not in the README.
```

**Review against your own setup**

```text
I have attached the README for "docs-readability-check". Below is a description of how I write and publish documentation.

[PASTE a short description of your docs: who reads them, which doc types you write, and how you review changes.]

Using only the README, tell me:
1. Which of my doc types match the doc types the README gives a target grade for, and which do not.
2. Whether the skill's target grades suit my readers. Say "my description does not say" if you cannot tell.
3. What I should check by hand after the skill runs.

A good answer ties every point to something in my description or in the README, uses the README's own doc types and grade ranges, and does not invent a target grade for a doc type the README does not list.
```

**Adapt and test**

```text
I have attached the README for "docs-readability-check". I want to try it on one doc without losing my original.

[PASTE the file name of one short markdown doc of yours.]

Write me a trial plan. Use the install commands and the slash command from the README. Say what I should copy first so the original is safe, what the report should contain, and one sign that the skill rewrote something it should have left alone. Do not invent commands, flags, or file paths that the README does not contain, and say where the README gives no undo step.

A good answer uses the README's install commands and the exact command `/docs-readability-check [folder-or-file]`, tells me to work on a copy because the skill edits in place, names the report folder the README gives, and does not promise a particular grade level for my doc.
```

**How these prompts were checked.** On 2026-10-01 every prompt in this document was run under my direction through the Claude Code command line, once against Claude Sonnet and once against Claude Haiku (the `sonnet` and `haiku` model names in Claude Code 2.1.287). Each run was a fresh session with no tools and no other instructions. This document was attached, each bracketed input was replaced with a made-up sample, and a Claude model (Sonnet 5.5) graded each answer against that prompt's "good answer" list, which was written before the run. I have not re-read every answer. One run per prompt per model: a Pass means that run met the list, not that the prompt always does. The answers are saved in [`pipelines/docs-pipeline/tests/prompt-runs/`](../../pipelines/docs-pipeline/tests/prompt-runs/README.md) (the files that start with `RC-`). I have not run them against models from other vendors, so "any AI model" means "should work", not "verified".

| Prompt | Sonnet | Haiku |
| --- | --- | --- |
| Understand and teach | Pass | Pass after a fix. The first version asked only what the skill checks and changes, and Haiku never stated the target grade for any doc type, then asked a quiz question whose answer it had not given. The prompt now asks for the target grade for each doc type. |
| Review against your own setup | Pass | Pass. It said all three of my sample's doc types match, where "conceptual pages" only loosely matches the README's "explanation". |
| Adapt and test | Pass | Pass. It suggested a name for the copy that is an example, not a path from the README. |
