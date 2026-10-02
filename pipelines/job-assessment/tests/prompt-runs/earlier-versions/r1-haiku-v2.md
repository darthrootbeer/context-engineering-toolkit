<!-- FICTIONAL EXAMPLE DATA. Not a real person. Saved by tests/prompt-runs/run_prompts.py -->
# Prompt run: Review the rules for gaps (ARCHITECTURE.md), on haiku

- Prompt file: `prompts/r1-review-rules.txt`
- Date: 2026-10-01. Model alias `haiku`, which ran as `claude-haiku-4-5-20251001` (Claude Code can add a small helper model call of its own).
- Turns: 1. Cost: $0.10 (the simulated user's calls are not included).
- Grade: see `GRADES.md`.

## Conversation

### User

[the prompt below, with attached files: ARCHITECTURE.md]

I'm attaching ARCHITECTURE.md from a job assessment tool. Read its scoring and verdict rules. List every place where two careful readers could score the same posting differently, quote the rule, and propose one sentence that removes the ambiguity. Each sentence must keep every number, cap and rule order exactly as the document states them; if you think a rule itself is wrong, say so separately instead of changing it. A good answer covers every item listed under Interpretations and does not invent new rules.

### Model

I'll work through the Interpretations section systematically, identifying each ambiguity and proposing clarifications.

## 1. Soft must-have fair rating
**Quote:** "For each **soft** must-have: weak or poor costs 1, anything else costs 0."

**Ambiguity:** "Anything else" could include fair, strong, or unknown; a reader might score fair as costing 1 or 0 differently.

**Proposed clarification:** "For each **soft** must-have: weak or poor costs 1, and fair, strong, or unknown cost 0."

---

## 2. Pay tier boundaries
**Quote:** "When pay is listed, pick the tier (the person's named location, else a nationwide or "everywhere else" tier, else the lowest tier) and score the **top** of its range: at or above target 10; at or above min 8; at or above floor 3; below floor 1."

**Ambiguity:** The rule specifies three scoring bands (target, min, floor) but the profile holds five numbers (floor, min, open ask, target, stretch ceiling); two readers might place open ask differently within these bands.

**Proposed clarification:** "When pay is listed, the pay top at or above target scores 10, between open ask and target scores 8, at or above floor but below open ask scores 3, and below floor scores 1."

---

## 3. Rounding before verdict
**Quote:** "the average of Fit and Qualifications is under 7" (from rule 4c).

**Ambiguity:** A reader might compute the average from raw decimal scores and then round (e.g., (6.8 + 6.3)/2 = 6.55 rounds to 7), versus computing the average of already-rounded whole numbers (7 + 6 = 6.5 rounds to 6).

**Proposed clarification:** "the average of the rounded Fit and Qualifications scores is under 7."

---

## 4. Silent strong must-haves
**Quote:** "For each **strong** must-have in the lane: strong or fair costs 0, weak costs 1.5, poor costs 3, unknown costs 1.5."

**Ambiguity:** If a strong must-have is never mentioned in the findings, does it count as unknown (costs 1.5) or is it treated as having no rating (costs 0)?

**Proposed clarification:** "For each **strong** must-have: if mentioned, strong or fair costs 0, weak costs 1.5, poor costs 3, unknown costs 1.5; if never mentioned, it counts as unknown and costs 1.5."

---

## 5. Years and domain costs once
**Quote:** "Asking for more years than the person has, or for years in a narrow sub-domain, costs 2 (once)."

**Ambiguity:** Two readers might interpret "(once)" as "each condition costs 2 once" (total 2) or "each condition costs 2" (total 4).

**Proposed clarification:** "Asking for more years than the person has, or for years in a narrow sub-domain, costs 2 in total, not 2 each."

---

## 6. Known gaps and self-score gaps share a cap
**Quote:** "Each load-bearing known gap costs 1, and self-scores of 0 or 1 on load-bearing lines share the same cap of 4 (one skill is never counted twice)."

**Ambiguity:** A reader might count a skill that appears as both a known gap and a self-score gap of 0 or 1 as two separate 1-point deductions, totaling 2.

**Proposed clarification:** "Each load-bearing known gap costs 1, and self-scores of 0 or 1 on load-bearing lines share the same cap of 4, so a skill appearing as both a known gap and a self-score of 0 or 1 costs only 1 point total toward this cap."

---

## 7. Tier selection priority
**Quote:** "pick the tier (the person's named location, else a nationwide or "everywhere else" tier, else the lowest tier)."

**Ambiguity:** Two readers might apply different criteria for what "contains the person's location label," what counts as "nationwide," or which tier is "lowest."

**Proposed clarification:** "Pick the tier in this order: a tier whose label contains the person's location label, then a tier whose label says nationwide, national, everywhere else, or all other, then the tier with the lowest top."

---

## 8. Low time-off interpretations
**Quote:** "Low time off (below the person's threshold, or accrual only) costs 2."

**Ambiguity:** Readers might disagree on how to score accrual-only time off, stated days versus the threshold, or cases where neither is explicitly present.

**Proposed clarification:** "Low time off costs 2, whether described as accrual-only, stated as fewer days than the person's threshold, or flagged as low by the model."

---

## 9. Hustle phrases and free_phrases
**Quote:** "Each hustle phrase costs 1, at most 3."

**Ambiguity:** A reader might assume all hustle phrases cost 1, or that phrases on `free_phrases` still cost 1 because they appear in the posting.

**Proposed clarification:** "Each hustle phrase costs 1 unless it is on the person's `free_phrases` list, at most 3 total."

---

## 10. Soft flags for pay
**Quote:** "Each tripped soft flag costs 1, but unlisted pay is never a Culture cost because Comp already scored it."

**Ambiguity:** Two readers might disagree on whether soft flags with ids like `unlisted_pay` or `no_pay_transparency` are included in "each tripped soft flag" or are exceptions.

**Proposed clarification:** "Each tripped soft flag costs 1, except soft flags related to pay transparency (such as `unlisted_pay` or `no_pay_transparency`), which are skipped in Culture."

---

## 11. Generic vs. specific autonomy phrases
**Quote:** "Autonomy that reads net negative costs 2."

**Ambiguity:** Two readers might interpret "net negative" as any mention of collaboration, or specifically as references to lack of decision-making without offsetting autonomy signals.

**Proposed clarification:** "Autonomy that contains specific phrases indicating lack of decision-making (such as approval, sign-off, reports to others) without balancing specific phrases indicating autonomy (such as ownership, approval), reads net negative and costs 2."

---

## 12. Quote source boundaries
**Quote:** (implied in check_findings section) "A rating other than unknown has no quote, or its quote is not in the posting text."

**Ambiguity:** A reader might include quotes from the assessment block or note metadata alongside the posting text, treating the whole note as the source.

**Proposed clarification:** "A quote must appear in the posting text itself; in a saved note, only text below the 'Full posting text' heading counts."

---

## 13. Repeated perks and phrases
**Quote:** "A big perk adds 2, a nice perk adds 1, a strong positive phrase adds 1. ... Each hustle phrase costs 1, at most 3. Each tripped soft flag costs 1. ... Each negative phrase costs 1."

**Ambiguity:** A reader might count the same perk or phrase twice if it appears in multiple sentences, rather than once per unique item.

**Proposed clarification:** "Each unique big perk adds 2, each unique nice perk adds 1, each unique strong positive phrase adds 1, each unique hustle phrase (not on `free_phrases`) costs 1 (at most 3 total), each unique tripped soft flag costs 1, and each unique negative phrase costs 1."

---

## Outside Interpretations: Additional ambiguities in scoring rules

These are not addressed by Interpretations but create potential scoring differences:

**Fit – "Each skill the person would rather avoid that is core daily work in this job costs 1"**

**Ambiguity:** Two readers might disagree on what counts as "core daily work" versus peripheral or optional work.

**Proposed clarification:** "Each skill the person would rather avoid that appears in the posting's daily responsibilities (not as nice-to-have or occasional) costs 1, at most 2 in total."

---

**Qualifications – "Each load-bearing known gap costs 1"**

**Ambiguity:** Two readers might disagree on what counts as "load-bearing" (essential to the role) versus a nice-to-have gap.

**Proposed clarification:** "Each load-bearing known gap (a gap in a required or strongly preferred skill) costs 1."

---

**Qualifications – "A working-style mismatch costs 3"**

**Ambiguity:** Two readers might disagree on what counts as a mismatch between the person's stated working style and the job's implied style.

**Proposed clarification:** "A working-style mismatch, where the job's style (become an expert or gather from experts) contradicts the person's stated preference, costs 3."

---

**Culture – "a strong positive phrase adds 1"**

**Ambiguity:** Two readers might disagree on what distinguishes a "strong positive" phrase from a neutral or weak positive one.

**Proposed clarification:** "Each phrase indicating strong positive workplace culture (such as commitment to growth, explicit values, or specific support programs) adds 1."

---

**Culture – "Each negative phrase costs 1"**

**Ambiguity:** Two readers might disagree on what counts as "negative" (e.g., "high pressure" versus "fast-paced").

**Proposed clarification:** "Each phrase indicating negative workplace culture (such as burnout risk, unsustainable pace, or dismissive language) costs 1."

---

**Verdict rule 4a – "central to the daily work"**

**Ambiguity:** Two readers might disagree on which required skills are central versus peripheral.

**Proposed clarification:** "A required skill that is stated as essential or appears in the job's core responsibilities, with no evidence behind it at all, triggers the override."
