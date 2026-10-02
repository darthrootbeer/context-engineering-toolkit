# README-teach on haiku

Prompt (inputs filled with made-up samples):

```text
I have attached the README for "docs-pipeline", a set of Claude Code skills that improve documentation in fixed stages. Teach it to me as if I am a technical writer who has never used it.

1. In plain language, say what problem it solves and what it does not do.
2. List the stages in order, one line each, and explain why the style passes come before the reviews.
3. Say exactly what the person does between every two stages, and what the AI does alone inside a stage.
4. Then ask me three questions to check that I understood, one at a time. Wait for my answer before the next one, and correct me where I am wrong.

A good answer names every stage in order, names the readability check as Stage 3d and grammar as Stage 3e, explains that nothing moves forward without a person's go-ahead (so it never says the person does not touch a stage), and repeats the limits the README states. It must not invent a stage, a command, or a file that is not in the README.
```

Answer:

## What docs-pipeline does and does not do

**The problem it solves:** You have a documentation draft. You need it reviewed and improved in a reliable order before it goes live. Docs-pipeline automates that workflow. It works through seven stages—from classifying your content, to fixing style and grammar, to checking for accuracy—and gates each step: nothing moves forward until you say it's ready. This prevents reviewers from wasting time on prose that still needs basic grammar fixes, and makes sure every suggestion gets an explicit decision before publishing.

**What it does not do:** It does not train custom models or build machine-learning pipelines. It does not handle retrieval systems. The author used this on real documentation and can vouch for how it behaved on *their* docs, not on yours. You fill in placeholders and your own knowledge files (glossary, product info, style guide) before it fits your setup. It assumes your docs live in a git repo; if you use a different publish platform, you'd need to adapt the publish and verify stages. It does not claim production ML experience.

## The stages in order

| | |
|---|---|
| **Stage 0** | Workspace setup — creates directories and copies knowledge files |
| **Stage 1** | Audit — classifies content by Diataxis type (how-to, explanation, reference, tutorial) |
| **Stage 2** | Split — extracts content into separate typed files |
| **Stage 2b** | Create overview — writes an index entry-point after split |
| **Stage 3a** | Structure check — verifies required sections and headings |
| **Stage 3b** | Voice check — applies your style guide (tone, terminology, list formatting) |
| **Stage 3c** | Human check — removes AI writing patterns (em dashes, filler, uniform sentences) |
| **Stage 3d** | Readability check — estimates grade level, rewrites dense sentences to target level |
| **Stage 3e** | Grammar check — spelling, grammar, and domain terminology |
| **Stage 4a** | Visuals review — recommends diagrams and visual aids |
| **Stage 4b** | Links review — finds cross-link candidates across your docs |
| **Stage 4c** | SME review — checks accuracy, reader journey, naming, technical clarity |
| **Stage 4d** | Changes list — summarizes everything done |
| **Stage 5** | Decision checkpoint — walks through every recommendation to apply/skip/defer |
| **Stage 6** | Publish — copies output to repo, creates branch and PR |
| **Post** | Verify — confirms PR merged and changes are live |

**Why style passes (3a–3e) come before reviews (4a–4c):** Style stages run first because reviewers should never read prose that still needs cleaning. Once the structure, voice, readability, and grammar are fixed, the SME reviewer can focus on accuracy and content, not on sentences that need rewriting. As the README says: "Style passes run before reviews, so the reviewers never read prose that still needs cleaning."

## What the person does between stages vs. what the AI does alone

**Between every two stages, you decide whether to proceed.** The README states: "Nothing moves to the next stage until a person says so." You review the output from the stage that just finished, and if it's ready, you give the go-ahead to move forward. If it needs fixes, you stop and adjust. Nothing happens automatically.

**Inside each stage, the AI works alone.** The AI classifies content, splits files apart, checks structure and voice, rewrites for readability, marks grammar issues, suggests diagrams and links, and flags accuracy problems. Each stage's AI does one job and commits its output so the change can be traced back to that stage.

**At the very end (Stage 5):** Before anything publishes, every recommendation—from every stage—gets an explicit decision from you: apply it, skip it, or defer it. The README says: "Before anything is published, every open recommendation gets an explicit apply, skip, or defer decision." This is where your final judgment comes in.

---

Now let me check that you understand. **First question:**

Can you name the stage that comes right after the "Create overview" stage and tell me what it checks?

