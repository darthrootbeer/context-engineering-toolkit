# rules-index-architecture prompt 1 (Understand and teach it) on haiku

Prompt (the document's full text was pasted where it says [PASTE FILE]; other inputs filled with made-up samples):

```text
Here is a design pattern document: [PASTE FILE]

Explain it to me as if I have one long instructions file and have never split it. Use a different everyday analogy than the one in the document. Then ask me three questions, one at a time, that check I understand why splitting files does not shrink what is loaded, and what the two opt-outs are. Wait for my answer before each next question.

A good answer uses an analogy that is not the document's, says that splitting a file does not shrink what is loaded at startup, and names both opt-outs. It asks exactly three questions, one at a time, and waits for my answer before the next.
```

Answer:

## The Pattern Explained

Imagine your kitchen has one enormous junk drawer where you keep everything: scissors, recipe cards, batteries, instruction manuals, takeout menus, rubber bands, expired coupons. When you need scissors, you have to dig through the whole drawer. When you add a new item, you just shove it in wherever. And if you try to find the scissors again next week, you're digging again.

The rules-index pattern is like giving each category its own drawer: one for cooking tools, one for instruction manuals, one for supplies. Now when you need scissors, you know exactly which drawer to open. A new rule about cooking goes in the cooking drawer, not crammed between the batteries and rubber bands.

**But here's the key:** You still own the same amount of stuff. Moving scissors from the junk drawer to the cooking drawer didn't make the scissors disappear. In Claude Code, splitting one big `CLAUDE.md` into thirty smaller rule files doesn't shrink what gets loaded into memory at startup—it all still loads, you've just organized it so it's easier to find and edit.

To actually shrink what loads, you need one of two escape hatches: either mark a rule file to load only for certain files in your project (`paths:` frontmatter), or tell Claude Code to skip a whole folder via `claudeMdExcludes` in settings.

---

**Question 1:** If I take my 5,000-line `CLAUDE.md` file and split it into ten 500-line rule files in a `rules/` folder, what happens to the total amount of instructions Claude Code loads at startup?
