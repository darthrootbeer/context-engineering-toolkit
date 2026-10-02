<!-- FICTIONAL EXAMPLE DATA. Not a real person. Saved by tests/prompt-runs/run_prompts.py -->
# Prompt run: Find gaps in my central file, on haiku

- Prompt file: `prompts/05-find-gaps.txt`
- Date: 2026-10-01. Model alias `haiku`, which ran as `claude-haiku-4-5-20251001` (Claude Code can add a small helper model call of its own).
- Turns: 1. Cost: $0.05 (the simulated user's calls are not included).
- Grade: see `GRADES.md`.

## Conversation

### User

[the prompt below, with attached files: ARCHITECTURE.md, section 'What the validator checks', fixtures/gappy-profile.yaml]

I'm attaching the 'What the validator checks' section of ARCHITECTURE.md and my career-profile.yaml. Find the weak spots the validator cannot catch: skills scored 3 or higher that rest on thin evidence, unchecked evidence a posting would lean on, evidence with no dates, must-haves or hard blocks with no reason, and lanes whose requirements look copied from each other. For each, give the exact YAML path, why it matters for scoring, and one question you would ask me to fix it. Do not fill any gap yourself. A good answer on fixtures/gappy-profile.yaml finds all three planted gaps.

### Model

I'll systematically check what the validator cannot catch. Here are the weak spots:

---

## **Planted gaps (3 major ones):**

### 1. **`skills[1].docs_ci` — Score 5 backed only by unchecked interview**
- **YAML path:** `skills[1]` (or `skills[1].self_score`, `skills[1].evidence_ids`)
- **Why it matters:** A score of 5 signals mastery. The validator won't warn about weak evidence *within* an evidence list—only absence of evidence. This evidence is `proof: unchecked` from an interview with no artifact to verify, yet it's being scored as your highest skill.
- **Question:** Can you point to a documented artifact (a PR, a config file, CI logs, or documentation) that shows the link-checking build you set up, or was this pairing work where you implemented it together with someone else?

---

### 2. **`hard_blocks[1].why` — Weapons hard block has no reason**
- **YAML path:** `hard_blocks[1]` (the weapons block)
- **Why it matters:** The validator warns about `strong` must-haves with no reason, but hard blocks aren't checked for this. Without a stated reason, a recruiter can't tell if this is an ethical boundary, a legal constraint, or something else—affecting how they'd present the role to you.
- **Question:** Why won't you work for weapons makers? Is it a personal value, a concern about the industry, or something else?

---

### 3. **`lanes[1].requirements` — Tech-writing lane requirements copied verbatim from docs-platform**
- **YAML path:** `lanes[1].requirements` (and `lanes[1].autonomy`, `lanes[1].keyword_signals`)
- **Why it matters:** These roles are fundamentally different (one builds systems, one writes content), yet both demand "Owns the docs build" as a strong requirement. The validator can't catch copy-paste; only humans notice when a requirement doesn't match the role's actual needs.
- **Question:** For a pure tech-writing role, do you need to own the docs build system itself, or would you prefer to write excellent content *within* a system that already exists?

---

## **Additional weak spots:**

### 4. **`evidence[0].authorship: DIRECTED` — Thin for a claimed skill**
- **YAML path:** `skills[0].evidence_ids[0]` → `evidence[0].authorship`
- **Why it matters:** You scored OpenAPI 4, but the evidence shows you *directed* the API spec work, not that you implemented the spec generation or wrote against it. For a technical writer, this means you supervised someone else's work.
- **Question:** Did you implement the system that generates the API reference from the spec, or did you write the reference documentation after someone else built the system?

---

### 5. **Last-used dates don't match evidence end dates**
- **YAML path:** `skills[0].last`, `skills[1].last`, `skills[2].last`
- **Why it matters:** All three scored skills claim `last: "2y"`, but evidence shows:
  - `openapi`: last evidence 2021-09 (4.8 years ago)
  - `docs_ci`: last evidence 2023-06 (3.3 years ago)
  - `style_guides`: last evidence 2022-08 (4.1 years ago)
  
  The validator can't connect `last` to evidence dates; a mismatch suggests either the skill is rustier than claimed, or the profile wasn't kept in sync.
- **Question for each:** When did you actually *last use* each of these skills hands-on, and what did you do?

---

**Summary:** The validator missed the three planted gaps (weak evidence quality, missing hard-block reason, and cloned requirements) because it checks *structure*, not *judgment*. The `last` dates are the only automatic error it could have caught but didn't, suggesting the profile wasn't updated when the `last` field was filled in.
