# RC-teach on sonnet

Prompt (inputs filled with made-up samples):

```text
I have attached the README for "docs-readability-check", a Claude Code skill that rewrites dense sentences in docs. Teach it to me as if I am a technical writer who has never used it.

1. Say in plain language what it checks and what it changes, and give the target grade for each doc type.
2. Say what it never touches.
3. Say where its report goes.
4. Then ask me three questions to check that I understood, one at a time. Wait for my answer before the next one, and correct me where I am wrong.

A good answer names the four sentence patterns, gives the target grade for each doc type, says tables, code blocks and callouts are never edited, and does not invent a feature or a command that is not in the README.
```

Answer:

# docs-readability-check, taught from the README

## What it checks and what it changes

The skill measures how hard your docs are to read, then rewrites the sentences that make them heavy. It keeps your vocabulary, structure and voice as they are.

For each doc it does this:

1. **Sets a target grade** from the `diataxis_type` in the frontmatter:

   | Doc type | Target grade |
   |---|---|
   | Explanation, overview | 10th to 11th |
   | How-to, tutorial | 11th to 12th |
   | Reference | 12th to college freshman |
   | No type in frontmatter | 11th to 12th |

2. **Scores a sample.** It takes 250 words from the middle of the prose, with code, tables, callouts and diagrams removed.
3. **Looks for four patterns:**
   - stacked clauses
   - too many facts in one sentence
   - jargon followed by a clause that explains it
   - wall paragraphs
4. **Rewrites in place** the sentences it can fix safely. Paragraphs it can't safely rewrite are flagged for a person.
5. **Scores again** and reports the grade before and after, in plain labels like "10th grade".

Because it edits in place, the README gives no undo step. Work from a copy or have version control ready.

## What it never touches

- Tables
- Code blocks
- Callouts

It also doesn't add or remove information. Files under `_archive/`, `_templates/` and `_attachments/` are skipped entirely.

## Where the report goes

The report is `readability-audit-{folder-name}.md` in `_process/style-audit/`, relative to the project root. If the input is inside an Obsidian vault, it goes to `_system-audits/` in the vault instead.

## Using it

The command is `/docs-readability-check [folder-or-file]`. The path is required. A folder means every `.md` file inside it.

Two limits to remember: the grade is an estimate from a sample, not a measure of the whole doc. And reference docs full of technical terms will score high regardless, and the skill says so rather than forcing the number down.

---

## Check your understanding

**Question 1 of 3:** A doc has `diataxis_type: tutorial` in its frontmatter. What grade range is the skill aiming for, and which part of the doc does it score to find the current grade?

Answer when you're ready and I'll give you the next question.

