<!-- FICTIONAL EXAMPLE DATA. Not a real person. Saved by tests/prompt-runs/run_prompts.py -->
# Prompt run: Find gaps in my central file, on haiku

- Prompt file: `prompts/05-find-gaps.txt`
- Date: 2026-10-01. Model alias `haiku`, which ran as `claude-haiku-4-5-20251001` (Claude Code can add a small helper model call of its own).
- Turns: 1. Cost: $0.03 (the simulated user's calls are not included).
- Grade: see `GRADES.md`.

## Conversation

### User

[the prompt below, with attached files: ARCHITECTURE.md, section 'What the validator checks', fixtures/gappy-profile.yaml]

I'm attaching the 'What the validator checks' section of ARCHITECTURE.md and my career-profile.yaml. Find the weak spots the validator cannot catch: skills scored 3 or higher that rest on thin evidence, unchecked evidence a posting would lean on, evidence with no dates, must-haves or hard blocks with no reason, and lanes whose requirements look copied from each other. For each, give the exact YAML path, why it matters for scoring, and one question you would ask me to fix it. Do not fill any gap yourself. A good answer on fixtures/gappy-profile.yaml finds all three planted gaps.

### Model

I found three planted gaps in the fixture:

## 1. Skill scored 5 on unchecked interview evidence alone

**Path:** `skills.docs_ci` (scored 5, evidence: `ev-placeholder-docs-ci`)

**Why it matters:** A skill at the top proficiency tier should rest on demonstrated competence, not unverified claims. The validator errors if `proof: checked` on interview/reference *sources*, but allows `proof: unchecked` from interviews. This skill's entire score rests on a single unchecked interview answer from 2023 with no additional corroboration.

**Question:** What concrete work can you point to (not an interview) that shows you designing and owning a docs CI pipeline end-to-end?

---

## 2. Both lanes have identical requirements and autonomy signals

**Path:** `lanes.docs-platform.requirements` vs. `lanes.tech-writing.requirements` (and both `autonomy` sections)

**Why it matters:** Two lanes that list the exact same must-haves and soft signals don't actually differentiate role types. A hiring manager or filter using these lanes can't tell why one would suit a platform engineer vs. a writer. The validator checks that lane *names* are unique, but can't detect when their requirements are copy-pasted.

**Question:** Which of these three requirements (`ai_forward`, `owns_pipeline`, `small_team`) actually matters only to the platform lane, and which only to writing?

---

## 3. Hard block with no reason

**Path:** `hard_blocks.weapons.why` (missing field)

**Why it matters:** A hard blocker without reasoning looks like placeholder data or a blocker you haven't thought through. The validator warns on strong must-haves in lanes with no reason—that same principle applies here. "Weapons makers" alone doesn't tell whether this is a values decision, a skill gap, or something else. Buyers will ask.

**Question:** Why is weapons-building off the table for you—values, skill mismatch, or something else?
