# RC-teach on haiku

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

# What docs-readability-check does

**In plain language:** This skill grades how hard your docs are to read by measuring against a target for each doc type. It then hunts for four specific sentence patterns that make technical writing feel dense and heavy, and rewrites those sentences to be clearer. It does not change your word choices, your doc structure, or your voice — and it adds or removes nothing.

**The four sentence patterns it fixes:**
1. Stacked clauses (too many dependent clauses chained together)
2. Too many facts crammed into one sentence
3. Jargon introduced and then immediately explained in the same sentence
4. Wall paragraphs (very long, unbroken blocks of text)

**Target grade levels, by doc type:**
- **Explanation & Overview:** 10th to 11th grade
- **How-to & Tutorial:** 11th to 12th grade
- **Reference:** 12th to college freshman
- **Any doc without a type in the frontmatter:** 11th to 12th grade

---

## What it never touches

Tables, code blocks, and callouts are always left alone. The skill removes them from its reading-level sample (so code doesn't skew the grade), but it never edits them.

---

## Where the report goes

The skill writes a single report file to `_process/style-audit/readability-audit-{folder-name}.md` (measured from your project root). If your docs live in an Obsidian vault, the report goes to `_system-audits/` inside the vault instead.

---

## Now let me check that you understood

**Question 1 of 3:**

Your docs include an explanation doc that targets readers familiar with your domain. What grade level should the skill aim for when it checks that doc?

