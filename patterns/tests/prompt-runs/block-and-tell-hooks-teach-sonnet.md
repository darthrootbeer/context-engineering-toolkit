# block-and-tell-hooks prompt 1 (Understand and teach it) on sonnet

Prompt (the document's full text was pasted where it says [PASTE FILE]; other inputs filled with made-up samples):

```text
Here is a design pattern document: [PASTE FILE]

Explain it to me as if I know what a script is but have never used hooks. Use a different everyday analogy than the one in the document. Then ask me three questions, one at a time, that check I understand why exit code 2 matters and why a guard needs a release path. Wait for my answer before each next question.

A good answer uses an analogy that is not the document's, covers why exit 2 blocks and exit 1 does not, and explains why a guard with no release path locks the agent out. It asks exactly three questions, one at a time, and waits for my answer before the next.
```

Answer:

## The idea in plain terms

Imagine a concert venue with a wristband rule: **you can't enter the VIP area until you've picked up a wristband at the ticket booth.**

You could put up a sign saying "Please get a wristband first." Most people would follow it, but some would forget or walk past it. That's the situation with an AI agent and a written rule.

A **hook** is a small script the harness runs automatically at certain moments, outside the model's judgment. There are two here:

- **The door guard (`PreToolUse`)** runs just before the agent does something, like editing a file or running a command. It checks for a wristband. If there isn't one, it stops the agent and says, "Go to the ticket booth and get one."
- **The booth (`PostToolUse`)** runs just after the agent does the thing you wanted, like reading a particular file. It slips a wristband on, which here is a small file saved on disk and labeled with the session ID.

The guard without the booth is a door nobody can ever get through. The booth without the guard is a free wristband nobody checks.

## Why exit code 2 matters

When a hook script finishes, it reports a number called an exit code. Claude Code reads that number like a guard's signal:

- **`0`** means all clear, so the action goes ahead.
- **`2`** means stop. The action does not happen, and the guard's written message (stderr) is shown to the agent.
- **Anything else, including `1`**, means the guard itself malfunctioned. Claude Code logs an error but lets the action through anyway.

So a guard that says `exit 1` looks like it's blocking, but the door stays open. The script is "refusing" while the system is waving everyone in.

## Why the message matters

A guard that just says "No" leaves the agent stuck. A good guard says what's missing and how to fix it, such as "Read CHANGELOG.md, then retry." The agent can then fix it in the same turn without bothering you.

## Why a guard needs a release path

Suppose the wristband booth is inside the VIP area. Nobody can get a wristband without already being in, so nobody gets in. The same thing happens when a guard blocks something, but the action that would clear the block is also blocked, or the marker's trigger is too narrow to ever fire. The agent is locked out of that whole class of action with no fix. That's why you write and test the way out before the way in.

## Question 1 of 3

A teammate writes a guard script that detects the missing marker, prints a clear "go read the changelog first" message to stderr, and ends with `exit 1`. They test it by watching the terminal and see the message appear. **Will the agent's deploy command actually be stopped? Why or why not?**
