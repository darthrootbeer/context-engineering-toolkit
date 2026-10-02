# block-and-tell-hooks prompt 1 (Understand and teach it) on haiku

Prompt (the document's full text was pasted where it says [PASTE FILE]; other inputs filled with made-up samples):

```text
Here is a design pattern document: [PASTE FILE]

Explain it to me as if I know what a script is but have never used hooks. Use a different everyday analogy than the one in the document. Then ask me three questions, one at a time, that check I understand why exit code 2 matters and why a guard needs a release path. Wait for my answer before each next question.

A good answer uses an analogy that is not the document's, covers why exit 2 blocks and exit 1 does not, and explains why a guard with no release path locks the agent out. It asks exactly three questions, one at a time, and waits for my answer before the next.
```

Answer:

# Understanding Block-and-Tell Hooks

Let me explain this with a security checkpoint analogy. Imagine a building with a secure room. Before you enter to make a change, a guard at the door checks: "Have you read the current status board?" If no, the guard says "not yet—read it first, here's why it matters" and **blocks your entry**. Once you've read the board, you get a stamped pass. On your next visit that session, the guard sees the pass and lets you through.

The key insight: the guard can only **truly block** if they use a specific exit code (2 in Claude Code). Using the wrong code (like 1) is like a guard who steps aside anyway—looks official but doesn't actually stop you. And the guard's job is pointless if there's no way to get the stamp and enter. You'd be locked out forever.

Here's what happens technically:

1. **PreToolUse hook** (the guard): Checks if a marker file exists for this session. If not → exits with code 2 and explains what to do. If yes → exits 0, lets the tool run.
2. **PostToolUse hook** (the stamp machine): After you've read or edited the file, writes a marker file for this session.

The two hooks are a **matched pair**—one enforces, one releases.

---

**Question 1 of 3:**

In the security checkpoint analogy, why would it be a problem if the guard used a different signal instead of exit code 2? What would change about whether the tool call actually gets blocked?
