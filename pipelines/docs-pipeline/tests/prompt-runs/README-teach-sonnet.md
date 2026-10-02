# README-teach on sonnet

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

# docs-pipeline, taught for a technical writer

## 1. The problem it solves, and its limits

**The problem.** Taking a documentation change from rough draft to published pull request involves many separate jobs: deciding what kind of content you have, fixing structure and voice, checking readability and grammar, adding diagrams and links, and checking accuracy. Done all at once, they blur together and it's hard to tell what changed or why. docs-pipeline is a chain of Claude Code skills. Each skill does one job, in a fixed order, and commits its output so every change traces back to the stage that made it.

**What it does not do or claim:**
- It is prompts, ordering, and checks. There is no model training, no machine-learning pipeline, no retrieval system, and no claim of production ML experience.
- It does not move on by itself. Nothing advances until a person says so.
- It does not publish with open questions. Every open recommendation gets an explicit apply, skip, or defer decision first.
- It is a generic export. You must fill in the placeholders and the knowledge files before it fits your docs. The bundled product knowledge describes a made-up product (the "Acme Orders API"), so replace it before trusting Stage 4c.
- The publish and verify stages assume a git-based docs repo.
- The author vouches only for how it behaved on their own docs, not on yours.

## 2. The stages, in order

| Stage | Command | One line |
|---|---|---|
| 0 | `/docs-workspace-setup` | Creates the workspace, copies in the knowledge files, writes starter files |
| 1 | `/docs-diataxis-audit` | Classifies content by Diataxis type; produces an audit report and JSON mapping |
| 2 | `/docs-diataxis-split` | Extracts mixed content into typed files (how-to, explanation, reference, tutorial) |
| 2b | `/docs-diataxis-create-overview` | Creates the overview/index entry-point doc after a split |
| 3a | `/docs-style-check-structure` | Checks required sections, headings, and Diataxis structural rules |
| 3b | `/docs-style-check-voice` | Applies voice, tone, list formatting, and terminology rules |
| 3c | `/docs-style-check-human` | Removes AI writing patterns (em dashes, filler, uniform sentences) |
| 3d | `/docs-readability-check` | Estimates reading grade level, finds dense sentences, rewrites to the target level for the doc type |
| 3e | `/docs-grammar-spelling` | Grammar, spelling, and domain terminology check |
| 4a | `/docs-visuals-review` | Recommends diagrams and visual aids, Mermaid-first |
| 4b | `/docs-links-review` | Finds cross-link candidates across the docs corpus |
| 4c | `/docs-sme-review` | Domain accuracy, reader journey, naming collisions, technical clarity |
| 4d | `/docs-changes-list` | Generates `editorial-changes.md` summarizing everything done |
| 5 | `/docs-decision-checkpoint` | Walks through every open recommendation: apply / skip / defer |
| 6 | `/docs-publish` | Copies output to the docs repo, adds frontmatter, creates branch and PR |
| Post | `/docs-work-verify` | Verifies the PR merged and the changes are live |

`/docs-pipeline` is the orchestrator that runs all of this stage by stage.

**Why style passes (3a to 3e) come before reviews (4a to 4c).** So the reviewers never read prose that still needs cleaning. A reviewer judging accuracy or links shouldn't spend effort on clumsy structure, AI-sounding filler, or typos.

## 3. Who does what

**Between every two stages, the person gives the go-ahead.** That is the one thing the README states for every transition: nothing moves to the next stage until a person says so. The README doesn't describe in more detail what you do at each gap. Reading the stage's committed output before approving is the natural use of that gate, but that part is my inference, not README text.

Other human actions the README does specify:
- **Before the first run:** install the skills (SETUP.md), fill in the placeholders and the three knowledge sources (glossary, product KB, style guide). Do this before Stage 0, because Stage 0 copies `_knowledge/` into each new workspace.
- **At Stage 5:** you decide apply, skip, or defer on every open recommendation. This is the main human decision, and it comes last, before publishing.

**Alone inside a stage, the AI does that stage's one job** (the table above), then commits its output. You are not editing inside a stage. Stage 5 is the exception: it is the AI walking you through items so you can decide. Stages 6 and Post are also AI work (branch, PR, verification), but only after your Stage 5 decisions.

## 4. Check your understanding

**Question 1 of 3.** Stage 3c removes AI writing patterns, and 3d and 3e come right after it. Using the README's reasoning, why does the pipeline run all of 3a to 3e before the Stage 4 reviews, and what would go wrong for a reviewer if the order were reversed?

Answer in your own words and I'll correct anything that's off before asking the next one.

