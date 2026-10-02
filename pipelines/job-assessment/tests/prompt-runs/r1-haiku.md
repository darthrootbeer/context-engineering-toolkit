<!-- FICTIONAL EXAMPLE DATA. Not a real person. Saved by tests/prompt-runs/run_prompts.py -->
# Prompt run: Review the rules for gaps (ARCHITECTURE.md), on haiku

- Prompt file: `prompts/r1-review-rules.txt`
- Date: 2026-10-01. Model alias `haiku`, which ran as `claude-haiku-4-5-20251001` (Claude Code can add a small helper model call of its own).
- Turns: 1. Cost: $0.07 (the simulated user's calls are not included).
- Grade: see `GRADES.md`.

## Conversation

### User

[the prompt below, with attached files: ARCHITECTURE.md]

I'm attaching ARCHITECTURE.md from a job assessment tool. Read its scoring and verdict rules. List every place where two careful readers could score the same posting differently, quote the rule, and propose one sentence that removes the ambiguity. Each sentence only clarifies: it keeps every number, band, cap and rule order exactly as the Scoring rules and Verdict rules tables state them, so check each sentence against those tables before you write it. If you think a rule itself is wrong, say so in a separate list instead of changing it. A good answer covers every item listed under Interpretations and does not invent new rules.

### Model

I'll go through the Interpretations systematically, quoting each rule and proposing one sentence that removes the ambiguity without changing the numbers, bands, caps or rule order.

---

**1. Fair ratings on soft must-haves**

Rule: "For each **soft** must-have: weak or poor costs 1, anything else costs 0."

Ambiguity: Does "anything else" include fair, strong, and unknown?

Clarifying sentence: "For each soft must-have, weak or poor costs 1 and fair, strong, and unknown each cost 0."

---

**2. Pay between min and target**

Rule: "...score the **top** of its range: at or above target 10; at or above min 8; at or above floor 3; below floor 1."

Ambiguity: When the top falls between two boundaries (e.g., between min and target), which score applies?

Clarifying sentence: "These boundaries nest: if at or above target score 10, else if at or above min score 8, else if at or above floor score 3, else score 1."

---

**3. Rounding before verdict**

Rule: "Each score is clamped to its floor and cap and then rounded half up to a whole number (8.5 becomes 9, not 8) before the verdict rules run."

Ambiguity: When exactly does rounding happen relative to verdict calculations like averages?

Clarifying sentence: "Clamping and half-up rounding to whole numbers happens before verdict rules are checked, and verdict rules compute averages from these rounded whole numbers."

---

**4. Unmentioned strong must-haves**

Rule: "For each **strong** must-have in the lane: strong or fair costs 0, weak costs 1.5, poor costs 3, unknown costs 1.5."

Ambiguity: If a finding never mentions a strong must-have (neither rating nor quoting), is it unknown and costs 1.5, or is it skipped?

Clarifying sentence: "A strong must-have the findings never mention is treated as unknown and costs 1.5; a soft must-have never mentioned costs nothing."

---

**5. Years and narrow sub-domain**

Rule: "Asking for more years than the person has, or for years in a narrow sub-domain, costs 2 (once)."

Ambiguity: Does "(once)" mean one combined cost or 2 per condition (4 total)?

Clarifying sentence: "Asking for more years than the person has, or for years in a narrow sub-domain, costs 2 once in total, not 2 each."

---

**6. Overlapping known gaps and self-score gaps**

Rule: "Each load-bearing known gap costs 1, and self-scores of 0 or 1 on load-bearing lines share the same cap of 4 (one skill is never counted twice)."

Ambiguity: If a skill appears both as a known gap and as a self-score gap, how is it counted under the cap of 4?

Clarifying sentence: "A load-bearing skill counts once toward the cap of 4, whether it appears as a known gap, a self-score of 0 or 1, or both."

---

**7. Tier selection order**

Rule: "When pay is listed, pick the tier (the person's named location, else a nationwide or "everywhere else" tier, else the lowest tier)..."

Ambiguity: When multiple tiers match one criterion (e.g., several have "nationwide"), which one is picked?

Clarifying sentence: "Pick the tier whose label contains the person's location label; if none, pick a tier labeled nationwide, national, everywhere else, all other or similar; if still none, pick the tier with the lowest top."

---

**8. Missing time-off statements**

Rule: "Low time off (below the person's threshold, or accrual only) costs 2."

Ambiguity: If the posting does not state how much time off is offered, what happens?

Clarifying sentence: "Time off costs 2 when stated as below the person's threshold or accrual only; if the posting does not state how much time off is offered, use the model's flag."

---

**9. Free phrases and hustle phrases**

Rule: "Each hustle phrase costs 1, at most 3."

Ambiguity: Must a phrase be on the `hustle_phrases` list to cost 1, and are there exceptions?

Clarifying sentence: "Each hustle phrase the model quotes costs 1 (at most 3 in total), except phrases on the person's `free_phrases` list cost nothing."

---

**10. Soft flags and unlisted pay**

Rule: "Each tripped soft flag costs 1, but unlisted pay is never a Culture cost because Comp already scored it."

Ambiguity: Is unlisted pay the only exception, or a specific example of a broader class?

Clarifying sentence: "Soft flags cost 1 each, but skip any soft flag with an id containing "unlisted_pay" or "no_pay_transparency" because Comp already scored unlisted pay as 5."

---

**11. Generic autonomy phrases**

Rule: "A read that autonomy is poor rests only on generic phrases ("partner with", "work closely", "collaborate", "stakeholder" and similar). Those appear in almost every senior posting. If that is all the posting says, the honest rating is unknown."

Ambiguity: What distinguishes a generic phrase from a non-generic one? What phrases disqualify a poor rating?

Clarifying sentence: "Rate autonomy as unknown, not poor, if the posting uses only generic phrases like "partner with", "work closely", "collaborate", or "stakeholder" without decision phrases like "approval", "sign-off", "reports to", or "ownership"."

---

**12. Quote source in saved notes**

Rule: "A rating other than unknown has no quote, or its quote is not in the posting text."

Ambiguity: In a saved note with multiple sections, what counts as "the posting text"?

Clarifying sentence: "Quotes must appear in the full posting text itself; in a saved note, this is the text below the "Full posting text" heading, not the assessment block or front matter."

---

**13. Repeating perks, phrases and flags**

Rule: There is no explicit rule.

Ambiguity: If the same perk, phrase, or soft flag appears twice in the findings, does it add or cost twice?

Clarifying sentence: "When the same perk, phrase, or soft flag is quoted multiple times in the findings, count or cost it once."

---

**14. No rules found.**

Item 14 in Interpretations ("The email card's autonomy row...") is display-only and does not affect scoring, so it creates no scoring ambiguity.
