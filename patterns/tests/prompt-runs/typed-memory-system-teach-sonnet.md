# typed-memory-system prompt 1 (Understand and teach it) on sonnet

Prompt (the document's full text was pasted where it says [PASTE FILE]; other inputs filled with made-up samples):

```text
Here is a design pattern document: [PASTE FILE]

Explain it to me as if I have never given an AI tool long-term memory. Use a different everyday analogy than the one in the document. Then ask me three questions, one at a time, that check I understand the difference between a correction and a confirmation, why the index has a size limit, and why compaction never deletes topic files. Wait for my answer before each next question.

A good answer uses an analogy that is not the document's, explains the difference between a correction and a confirmation, why the index has a size limit, and why compaction never deletes topic files. It asks exactly three questions, one at a time, and waits for my answer before the next.
```

Answer:

# Long-term memory for an AI tool, explained with a kitchen

Imagine a talented chef who wakes up every morning with no memory of yesterday. They are skilled, but they don't know your restaurant, your regulars, or what went wrong last week. Every conversation with an AI coding tool starts like that morning.

**Long-term memory is the binder the chef reads before service.** Each day they read it, then work as if they remembered.

- **Each page is one topic.** One page might say "Table 4's customer is allergic to shellfish." Another might say "Supplier changes deliveries on 2026-11-01." These are the topic files, and each has a *type* (who the customer is, what to do or avoid, what's in progress, where things are kept).
- **The cover sheet is the index.** It's one line per page: a title, where to find it, and a few words of gist. The chef reads the whole cover sheet first and opens a page only when needed.

## Corrections vs. confirmations

Suppose the chef over-salts a dish and you say, "Too salty, use less." That's a **correction**: it tells the chef what to stop doing. Later the chef tries something unusual, like a lemon finish on the fish, and you say, "Yes, exactly that, keep doing it." That's a **confirmation**: it tells the chef what to keep doing.

If the binder only held corrections, the chef would grow timid. They'd avoid everything that ever got a complaint and never learn which risky choices were good. Confirmations stop tomorrow's chef from second-guessing a good call.

## Why the cover sheet has a size limit

The chef only gets the cover sheet in one glance before service starts, with no flipping back and forth. In this tool, the harness reads the index up to a fixed cutoff (in the document's version, 200 lines or 25,000 bytes, whichever comes first) and ignores the rest. If the cover sheet is too long, the bottom entries simply don't exist for that day. So the cover sheet stays short and the detail lives on the pages behind it.

## Why compaction never deletes topic files

When the cover sheet gets crowded, you tidy *the sheet*, not the binder. You merge several lines into one denser line or group related pages under a heading. The pages themselves stay, because deleting one destroys knowledge (the shellfish allergy) that you can't recover. A short pointer costs little, but a lost lesson means someone gets hurt again.

---

Let's check your understanding, one question at a time.

**Question 1:** Say the AI makes a mistake and you tell it, "Don't do that." Another day, it picks an unusual approach and you say, "Yes, that was right." What would the memory contain if it recorded only the first kind of feedback, and what problem would that cause in later sessions?
