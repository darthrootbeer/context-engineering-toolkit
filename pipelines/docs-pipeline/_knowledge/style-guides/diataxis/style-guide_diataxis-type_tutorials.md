# Diátaxis Tutorial Formatting Rules

## Definition and Classification

**Purpose**: Teach new skills through safe, guided, hands-on practice. User must DO things, not just read.

**Use tutorials when:**

- Learning product/feature for the first time
- Building foundational skills before real work
- User needs confidence in a safe environment

**Do NOT use tutorials when:**

- User has basics and needs to solve specific problem → How-to Guide
- User needs technical details → Reference
- User needs concepts without doing → Explanation

**Core rule**: Focus on learning outcomes, not task completion. Sacrifice efficiency for pedagogical value.

---

## Required Structure

### Opening (MUST include all 4)

1. **What they'll learn**: 2-4 skills using "you will learn to..."
2. **What they'll build**: Concrete deliverable ("a working contact form" not "form functionality")
3. **Prerequisites**: Explicit knowledge, tools, setup. Be specific: "basic HTML familiarity" not "some coding experience"
4. **Time estimate**: Realistic for beginners ("approximately 30 minutes")

**Prohibited**: Technical background, multiple paths, approach justifications (link elsewhere)

### Step-by-Step Instructions

Each step needs:

1. **Action**: Imperative verb, specific ("Click blue 'Deploy' button in top right")
2. **Context** (optional): 1-2 sentences on what step accomplishes
3. **Expected result**: "You should see..." + screenshot if complex
4. **Troubleshooting** (if needed): "**Note:** If [X], [do Y]"

### Conclusion (MUST include)

1. **Recap**: Summarize accomplishments and skills
2. **Next steps**: Link to How-to Guides, Reference, Explanation, or next tutorial

**Prohibited**: Advanced variations, comprehensive lists, detailed explanations

---

## Writing Style

**Voice**: Second person ("you"), active voice, present tense, encouraging

- ✅ "You've just created your first API endpoint!"
- ❌ "The user has created an API endpoint"

**Specificity**: Be concrete, define terms on first use, avoid assumptions

- ✅ "Click green 'Save' button at bottom" | ❌ "Save your changes"
- ✅ "Open your terminal (command-line interface)" | ❌ "Open your terminal"

**Formatting**: ### for step groups, numbered lists for sequences, language-specified code blocks, bold for UI elements

---

## Content Boundaries

**❌ No explanations**: Minimal context only. Link to Explanation docs for "why"
**❌ No multiple paths**: One canonical path. Create separate tutorials for different approaches
**❌ No reference material**: Show only parameters used. Link to Reference for complete details
**❌ No problem-solving focus**: Teach concepts through examples, not solutions. Save "how to optimize X" for How-to Guides
**❌ No assumed steps**: Explicit every action. No "After configuring..." without showing how
**❌ No production concerns**: Use simple, safe examples with toy data. Security/optimization → How-to Guides

---

## Code and Command Formatting

**Code blocks**: Always specify language, include complete runnable code, show file context ("In `app.py`, add:"), no truncation. Use inline code for paths: `src/app.py`

**Commands**: Show full commands with `$`/`>` prompt, include expected output, specify directory

**Visual elements**: Screenshots for complex UI states, confirmation of success, first-time interfaces. Annotate with arrows, crop to relevant area, include alt text. Diagrams for workflow/relationships/before-after (keep simple)

---

## Validation Checklist

- [ ] Skills stated upfront | Prerequisites explicit | Time estimate included
- [ ] Each step actionable and specific | Expected results shown | One clear path only
- [ ] No explanations/reference material (or linked) | No assumed/skipped steps
- [ ] All code/commands complete and runnable | File locations specified
- [ ] Encouraging "you" + active voice | Conclusion recaps learning + links next steps

---

## Minimal Template

```markdown
# [Action Verb] Your First [Thing]

## What you'll learn

- [Skill 1]
- [Skill 2]

## What you'll build

[Concrete deliverable]

## Prerequisites

- [Knowledge/tool requirement]
- [Setup requirement]

Approximately [X] minutes.

## Step 1: [Action]

[Instruction]
[Expected result]

## Step 2: [Action]

[Continue...]

## What you learned

[Skills recap]

## Next steps

- [How-to Guide link]
- [Reference link]
- [Explanation link]
```
