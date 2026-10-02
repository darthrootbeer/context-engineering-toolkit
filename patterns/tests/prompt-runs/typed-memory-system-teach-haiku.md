# typed-memory-system prompt 1 (Understand and teach it) on haiku

Prompt (the document's full text was pasted where it says [PASTE FILE]; other inputs filled with made-up samples):

```text
Here is a design pattern document: [PASTE FILE]

Explain it to me as if I have never given an AI tool long-term memory. Use a different everyday analogy than the one in the document. Then ask me three questions, one at a time, that check I understand the difference between a correction and a confirmation, why the index has a size limit, and why compaction never deletes topic files. Wait for my answer before each next question.

A good answer uses an analogy that is not the document's, explains the difference between a correction and a confirmation, why the index has a size limit, and why compaction never deletes topic files. It asks exactly three questions, one at a time, and waits for my answer before the next.
```

Answer:

I'll explain this pattern and check your understanding, one question at a time.

## The idea, with a different analogy

Imagine you're a journalist who writes articles across many topics. You keep a **desk notebook** that you open at the start of every assignment—it's your quick reference. In that notebook is a short index: "Recipe development (3 notes)", "Interview techniques (5 notes)", "Publishing deadlines (2 notes)". 

The actual detailed notes live in separate folders. You could stuff everything into the desk notebook instead, but then it gets too thick to flip open. Instead, you keep the index short and scannable by pointing to files elsewhere. Each file is typed by *why* you keep it: a correction you learned ("never rush an interview"), a confirmation ("open questions work better"), a project deadline, or a reference ("newsroom is in building 3").

The memory system works the same way: an index you read every session (must stay small), topic files you open as needed (the real content), and types that tell you *why* something matters.

---

**Question 1 of 3:**

What is the difference between recording a *correction* ("don't do X") and a *confirmation* ("yes, that approach was right")? Why does the document say you need both?
