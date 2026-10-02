# RC-teach on haiku

Prompt (inputs filled with made-up samples):

```text
I have attached the README for "docs-readability-check", a Claude Code skill that rewrites dense sentences in docs. Teach it to me as if I am a technical writer who has never used it.

1. Say in plain language what it checks and what it changes.
2. Say what it never touches.
3. Say where its report goes.
4. Then ask me three questions to check that I understood, one at a time. Wait for my answer before the next one, and correct me where I am wrong.

A good answer names the four sentence patterns, gives the target grade for each doc type, says tables, code blocks and callouts are never edited, and does not invent a feature or a command that is not in the README.
```

Answer:

# What docs-readability-check does

## 1. What it checks and what it changes

The skill measures how hard your docs are to read by giving them a grade level (like "10th grade" or "college freshman"). It looks at a sample of 250 words from the middle of each doc and searches for four sentence patterns that make technical writing feel dense and heavy:

- **Stacked clauses** — too many dependent clauses chained together
- **Too many facts in one sentence** — when one sentence tries to do the work of three
- **Jargon followed by explanation** — when you use a term and then pause to explain what it means
- **Wall paragraphs** — very long paragraphs with no breaks

When it finds these patterns, it rewrites the sentences to be simpler and clearer — but it never changes your vocabulary, structure, or voice, and it never adds or removes information.

## 2. What it never touches

The skill **will not edit**:
- Tables
- Code blocks
- Callouts

If it finds a paragraph it isn't confident about, it flags that paragraph for you to fix by hand instead of rewriting it.

## 3. Where the report goes

The skill writes a report to `_process/style-audit/readability-audit-{folder-name}.md` (relative to your project root). If your docs are inside an Obsidian vault, the report goes to `_system-audits/` in the vault instead.

---

**Now, here's my first question:** The skill sets different target grade levels for different doc types. Which two doc types get the same target grade range? (You can find the answer in what I just told you.)

