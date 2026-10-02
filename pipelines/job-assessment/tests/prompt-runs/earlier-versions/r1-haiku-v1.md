<!-- FICTIONAL EXAMPLE DATA. Not a real person. Saved by tests/prompt-runs/run_prompts.py -->
# Prompt run: Review the rules for gaps (ARCHITECTURE.md), on haiku

- Prompt file: `prompts/r1-review-rules.txt`
- Date: 2026-10-01. Model alias `haiku`, which ran as `claude-haiku-4-5-20251001` (Claude Code can add a small helper model call of its own).
- Turns: 1. Cost: $0.07 (the simulated user's calls are not included).
- Grade: see `GRADES.md`.

## Conversation

### User

[the prompt below, with attached files: ARCHITECTURE.md]

I'm attaching ARCHITECTURE.md from a job assessment tool. Read its scoring and verdict rules. List every place where two careful readers could score the same posting differently, quote the rule, and propose one sentence that removes the ambiguity. A good answer finds the items listed under Interpretations and does not invent new rules.

### Model

I'll trace each item from the Interpretations section back to where it creates ambiguity in the main scoring or verdict rules.

1. **Interpretation: "A fair rating on a soft must-have costs nothing. Only weak and poor cost 1."**
   - Rule quoted: "For each **soft** must-have: weak or poor costs 1, anything else costs 0."
   - Ambiguity: "Anything else" is unclear — does it include fair, or could someone argue fair has a cost?
   - Fix: "For each soft must-have: weak or poor cost 1; strong, fair, and unknown cost 0."

2. **Interpretation: "A pay top between the open ask and the target scores 8."**
   - Rule quoted: "at or above target 10; at or above min 8; at or above floor 3; below floor 1."
   - Ambiguity: No boundary is given for the range between min and target, leaving the score undefined for pay in that gap.
   - Fix: "Score the top as 10 if at or above target, else 8 if at or above min, else 3 if at or above floor, else 1."

3. **Interpretation: "Each score is rounded half up before the verdict rules run."**
   - Rule quoted: "the average of Fit and Qualifications is under 7" (in verdict rule 4c).
   - Ambiguity: The verdict rule doesn't specify whether to average rounded or unrounded scores.
   - Fix: "the average of the rounded Fit and Qualifications scores is under 7."

4. **Interpretation: "A strong must-have the findings never mention counts as unknown and costs 1.5."**
   - Rule quoted: "For each **strong** must-have in the lane: strong or fair costs 0, weak costs 1.5, poor costs 3, unknown costs 1.5."
   - Ambiguity: If the findings don't mention a strong must-have at all, does it cost 1.5 or nothing?
   - Fix: "For each strong must-have, whether mentioned or not: strong or fair costs 0; weak, poor, or unknown costs 1.5."

5. **Interpretation: "Too many years and a narrow sub-domain cost 2 once in total, not 2 each."**
   - Rule quoted: "Asking for more years than the person has, or for years in a narrow sub-domain, costs 2 (once)."
   - Ambiguity: The "(once)" is parenthetical and easy to miss; the "or" could be read as two separate costs.
   - Fix: "Asking for more years than the person has and/or for years in a narrow sub-domain costs 2 total, not 2 per condition."

6. **Interpretation: "Known gaps and self-score gaps are one set, counted once under the shared cap of 4."**
   - Rule quoted: "Each load-bearing known gap costs 1, and self-scores of 0 or 1 on load-bearing lines share the same cap of 4 (one skill is never counted twice)."
   - Ambiguity: It's unclear whether known gaps and self-scores are counted separately or pooled together.
   - Fix: "Load-bearing known gaps and self-scores of 0 or 1 share a single cap of 4, with each skill counted at most once."

7. **Interpretation: "The code picks the pay tier by a priority order: location, then nationwide, then lowest top."**
   - Rule quoted: "pick the tier (the person's named location, else a nationwide or "everywhere else" tier, else the lowest tier)"
   - Ambiguity: "Else" suggests fallbacks, but if multiple tiers match one criterion, the tiebreaker is unspecified.
   - Fix: "Pick the tier in this order: first, one whose label contains the person's location; second, a nationwide or everywhere-else tier; third, the tier with the lowest top."

8. **Interpretation: "Accrual-only time off counts as low. A stated number counts as low when it is under the person's threshold."**
   - Rule quoted: "Low time off (below the person's threshold, or accrual only)"
   - Ambiguity: The "or" leaves ambiguous whether accrual-only is automatically low, or must also fall below some threshold.
   - Fix: "Low time off means accrual-only time off, or a stated number of days below the person's threshold."

9. **Interpretation: "A phrase on the person's `free_phrases` list costs nothing. Any other hustle phrase costs 1."**
   - Rule quoted: "Each hustle phrase costs 1, at most 3."
   - Ambiguity: No mention of free_phrases, so a reader wouldn't know any hustle phrases are exempt.
   - Fix: "Each hustle phrase costs 1 unless it appears in the person's free_phrases list, capped at 3 total."

10. **Interpretation: "Soft flags with ids such as `no_pay_transparency` or `unlisted_pay` are skipped in Culture."**
    - Rule quoted: "Each tripped soft flag costs 1, but unlisted pay is never a Culture cost because Comp already scored it."
    - Ambiguity: The rule mentions only "unlisted pay" but the code skips all pay-related soft flags.
    - Fix: "Each tripped soft flag costs 1, except soft flags with pay-related ids cost nothing because Comp already scored them."

11. **Interpretation: "A quote is generic only when it holds a generic phrase and none of the phrases that really say who decides."**
    - Rule quoted: "A read that autonomy is poor rests only on generic phrases ("partner with", "work closely", "collaborate", "stakeholder" and similar)."
    - Ambiguity: "Only on generic phrases" doesn't clarify whether a quote with both generic and decision-phrases counts as generic.
    - Fix: "A read that autonomy is poor is generic if the quote contains only phrases like "partner with" or "stakeholder," with no decision phrases like "approval," "sign-off," or "ownership.""

12. **Interpretation: "In a saved note, only the text below the 'Full posting text' heading counts for quotes."**
    - Rule quoted: "A rating other than unknown has no quote, or its quote is not in the posting text."
    - Ambiguity: "The posting text" is undefined for notes that archive the posting in a section.
    - Fix: "A rating other than unknown must have a quote from the posting; in a saved note, only text below the 'Full posting text' heading qualifies."

13. **Interpretation: "The same perk, phrase or soft flag quoted twice adds or costs once."**
    - Rule quoted: "A big perk adds 2, a nice perk adds 1, ... Each hustle phrase costs 1, at most 3. Each tripped soft flag costs 1, ... Each negative phrase costs 1."
    - Ambiguity: "Each" could mean each instance, even duplicates; no rule says to deduplicate.
    - Fix: "Each unique perk, hustle phrase, soft flag and negative phrase counts once, even if quoted multiple times."
