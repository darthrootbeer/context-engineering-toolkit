# rules-index-architecture prompt 1 (Understand and teach it) on sonnet

Prompt (the document's full text was pasted where it says [PASTE FILE]; other inputs filled with made-up samples):

```text
Here is a design pattern document: [PASTE FILE]

Explain it to me as if I have one long instructions file and have never split it. Use a different everyday analogy than the one in the document. Then ask me three questions, one at a time, that check I understand why splitting files does not shrink what is loaded, and what the two opt-outs are. Wait for my answer before each next question.

A good answer uses an analogy that is not the document's, says that splitting a file does not shrink what is loaded at startup, and names both opt-outs. It asks exactly three questions, one at a time, and waits for my answer before the next.
```

Answer:

## The idea, using a different analogy

Imagine you keep every recipe you own in one giant stained notebook. Appetizers, desserts, your grandmother's soup, and a note about not using the blue pan are all jumbled together. Finding anything means flipping through pages, and when you add a new recipe you squeeze it into whatever blank space is nearest. Eventually the two banana bread recipes are forty pages apart, and a correction you scribble for one smudges into the recipe next to it.

The fix is to move to a recipe box with dividers. Each recipe gets its own card, cards are grouped by type, and a short table of contents at the front tells you which divider to look under. Now you can find things fast, add a card without disturbing its neighbors, and edit one without touching the rest.

Here is the catch, and it's the part people get wrong. Imagine that every morning, before you start cooking, you are required to read **every card in the box aloud**. The box is better organized, but the reading takes just as long as it did with the notebook. If you add a drawer of long, detailed cards, the reading takes even longer.

That's how Claude Code behaves. At startup it loads `CLAUDE.md` plus every markdown file under `rules/`, including subfolders. Splitting makes your rules easier to find and edit, but it doesn't make the startup load smaller. There are two ways to actually cut it:

1. Give a rule file `paths:` frontmatter, so it only loads when you're working on matching files.
2. Add a `claudeMdExcludes` entry in `settings.json`, so a whole folder (for example, a `reference/` folder of long history and examples) is skipped at startup.

## Check your understanding

**Question 1 of 3:** You take your single 2,000-line instructions file and split it into 30 smaller files under `rules/`, changing nothing else. Roughly how does the amount of text loaded at startup change, and why?

I'll wait for your answer before asking the next one.
