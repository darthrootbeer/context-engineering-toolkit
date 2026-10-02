<!-- FICTIONAL EXAMPLE DATA. Not a real person. Saved by tests/prompt-runs/run_prompts.py -->
# Prompt run: Find gaps in my central file (held-out profile), on haiku

- Prompt file: `prompts/05-find-gaps.txt`
- Date: 2026-10-01. Model alias `haiku`, which ran as `claude-haiku-4-5-20251001` (Claude Code can add a small helper model call of its own).
- Turns: 1. Cost: $0.04 (the simulated user's calls are not included).
- Grade: see `GRADES.md`.

## Conversation

### User

[the prompt below, with attached files: ARCHITECTURE.md, section 'What the validator checks', fixtures/held-out-gappy-profile.yaml]

I'm attaching the 'What the validator checks' section of ARCHITECTURE.md and my career-profile.yaml. The validator checks shape and consistency, not truth, so find what it cannot catch. Read my whole file the way a skeptical hiring manager and a careful editor would: look for places where the file claims more than its own evidence shows, says something that conflicts with another part of the file, or would make a posting score in a misleading way. Check every section, not only skills. For each weak spot, give the exact YAML path, quote the part that worries you, say why it matters for scoring, and give one question you would ask me to fix it. Do not fill any gap yourself, and do not report a problem you cannot point to in the file. A good answer names only things that are really in the file and gives a YAML path for each one.

### Model

I'll read through this carefully like a hiring manager would. Here are the actual gaps I found:

---

**1. Evidence predates claimed employment**
- **YAML path:** `evidence[0].dates` and `employers[0].dates`
- **Quote:** Evidence `ev-harbor-onboarding` has dates `2018-01` to `2018-06`, but Harbor employment is `2021-03` to `2023-06`
- **Why it matters:** A hiring manager will assume this work was done *at* Harbor. This gap makes the timeline confusing and raises questions about what "work at Harbor" actually means. Did Quinn write this before joining, or is there an employment gap?
- **Question to fix it:** When and where did Quinn actually write this onboarding guide—was it at a different employer, or during a gap before Harbor?

---

**2. Authorship claim contradicts authorship field**
- **YAML path:** `evidence[1].claim` vs `evidence[1].authorship`
- **Quote:** Claim says "Wrote every page of the help center again" but authorship field is `REVIEWED`
- **Why it matters:** Writing vs. reviewing are different skill demonstrations. A hiring manager hiring for a writer will score these very differently. The claim overstates what the field records.
- **Question to fix it:** Did Quinn write or review the help center pages? If reviewed, what percentage or which sections?

---

**3. Skill recency doesn't match evidence**
- **YAML path:** `skills[1]` (user_guides) and its `evidence_ids`
- **Quote:** Skill `user_guides` says `last: 2y` but references `ev-harbor-onboarding` with dates `2018-01` to `2018-06`
- **Why it matters:** Claiming recent use (2y) but showing 8-year-old evidence makes the skill look either stale or inaccurately dated. Scoring algorithms may assume a recent reference means recent use.
- **Question to fix it:** Has Quinn written user guides in the past 2 years? If the last example is from 2018, should this say `last: 8y`?

---

**4. "Fast-paced" appears in both avoid and accept lists**
- **YAML path:** `culture.hustle_phrases` and `culture.free_phrases`
- **Quote:** `hustle_phrases: [rockstar, fast-paced, always on]` and `free_phrases: [fast-paced, flexible hours]`
- **Why it matters:** These lists help recruiters filter opportunities. Listing the same phrase in both "red flag" and "acceptable" signals contradicts itself and blocks filtering logic.
- **Question to fix it:** Does Quinn like fast-paced environments or want to avoid them? It can only be one.

---

**5. Vague-title soft flag doesn't match actual titles**
- **YAML path:** `soft_flags[0]` against `employers[*].title`
- **Quote:** Soft flag warns "Vague job title" but titles are "Technical Writer" and "Senior Technical Writer"
- **Why it matters:** These are standard, non-vague titles. Flagging this raises a false red flag on Quinn's profile and suggests confusion about what vagueness means.
- **Question to fix it:** Are there specific titles Quinn wants to avoid or find unclear? If not, remove this flag.

---

**6. High-interest company claim is unsupported**
- **YAML path:** `company_criteria.high_interest[0]`
- **Quote:** "Builds tools Quinn already uses"
- **Why it matters:** Hiring managers want to know *which* tools Quinn uses. This is too vague to be credible and looks like generic interest rather than informed research.
- **Question to fix it:** What specific tools does Fictional Api Tools Inc. build that Quinn actually uses? Can you name them?

---

**7. Years of experience gap**
- **YAML path:** `person.years_experience` vs `employers` and `evidence`
- **Quote:** `years_experience: 14` but employer history runs 2021–present (~5.5 years shown) and evidence traces back to 2018 (~8 years total)
- **Why it matters:** The 14-year claim doesn't align with the work history provided. Either there's 6 years of employment not listed, or the number is overstated.
- **Question to fix it:** Does Quinn have employment history before 2018, or should `years_experience` reflect the evidence actually shown?
