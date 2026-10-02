<!-- FICTIONAL EXAMPLE DATA. Not a real person. Saved by tests/prompt-runs/run_prompts.py -->
# Prompt run: Review the rules for gaps (ARCHITECTURE.md), on sonnet

- Prompt file: `prompts/r1-review-rules.txt`
- Date: 2026-10-01. Model alias `sonnet`, which ran as `claude-sonnet-5-5` (Claude Code can add a small helper model call of its own).
- Turns: 1. Cost: $0.07 (the simulated user's calls are not included).
- Grade: see `GRADES.md`.

## Conversation

### User

[the prompt below, with attached files: ARCHITECTURE.md]

I'm attaching ARCHITECTURE.md from a job assessment tool. Read its scoring and verdict rules. List every place where two careful readers could score the same posting differently, quote the rule, and propose one sentence that removes the ambiguity. A good answer finds the items listed under Interpretations and does not invent new rules.

### Model

The 14 items under Interpretations are the ambiguities. For each one I quote the rule text that leaves room for two readings, then give a one-sentence fix to add next to it. I haven't added any new rules.

**1. Soft must-have rated fair**
- Rule: "For each **soft** must-have: weak or poor costs 1, anything else costs 0."
- Fix: "A soft must-have rated strong, fair or unknown costs 0, and only weak or poor costs 1."

**2. Pay top between open ask and target**
- Rule: "at or above target 10; at or above min 8; at or above floor 3; below floor 1", although `comp` holds five numbers.
- Fix: "Open ask and stretch ceiling are never score boundaries, so any top at or above min and below target scores 8."

**3. When rounding happens**
- Rule: "clamped to its floor and cap and then rounded half up to a whole number … before the verdict rules run."
- Fix: "The 4b and 4c thresholds and the Fit/Qualifications average use the rounded whole-number scores, and the average itself is not rounded."

**4. Requirements the findings never mention**
- Rule: "unknown costs 1.5" for strong must-haves, but nothing is said about missing ones.
- Fix: "A strong must-have missing from the findings counts as unknown and costs 1.5, while a missing soft must-have, perk or phrase costs nothing."

**5. Years and sub-domain**
- Rule: "Asking for more years than the person has, or for years in a narrow sub-domain, costs 2 (once)."
- Fix: "If a posting triggers either or both, the total cost is 2, never 4."

**6. Known gaps vs. self-score gaps**
- Rule: "Each load-bearing known gap costs 1, and self-scores of 0 or 1 on load-bearing lines share the same cap of 4 (one skill is never counted twice)."
- Fix: "Known gaps and self-score gaps form one set keyed by skill, each skill costs 1 once, and the set costs at most 4 in total."

**7. Choosing the pay tier**
- Rule: "the person's named location, else a nationwide or 'everywhere else' tier, else the lowest tier."
- Fix: "The code picks the tier: a label containing the person's location label wins, then a nationwide-type label, then the tier with the lowest top, and the model's `tier_used` is ignored."

**8. Low time off**
- Rule: "Low time off (below the person's threshold, or accrual only) costs 2."
- Fix: "Accrual-only counts as low, a stated number of days counts as low only if under the threshold, and with neither the model's flag decides."

**9. Hustle phrases**
- Rule: "Each hustle phrase costs 1, at most 3."
- Fix: "Any hustle phrase the model quotes costs 1 unless it is on the person's `free_phrases` list, whether or not it is on their `hustle_phrases` list."

**10. Unlisted pay in Culture**
- Rule: "each tripped soft flag costs 1, but unlisted pay is never a Culture cost because Comp already scored it."
- Fix: "Any soft flag about missing or unlisted pay, such as `no_pay_transparency` or `unlisted_pay`, is skipped in Culture."

**11. Generic autonomy phrases**
- Rule: "Autonomy that reads net negative costs 2", and a poor read cannot rest only on generic phrases.
- Fix: "A quote is generic only if it contains a generic phrase and none of the decision-naming phrases such as approval, sign-off, reports to or ownership, and the lists live in `check_findings.py`."

**12. Where a quote may come from**
- Rule: "its quote is not in the posting text."
- Fix: "In a saved note, only text below the 'Full posting text' heading counts as the posting."

**13. Repeated perks, phrases and flags**
- Rule: "A big perk adds 2 … Each negative phrase costs 1", with no mention of duplicates.
- Fix: "The same perk, phrase or soft flag quoted more than once adds or costs once."

**14. Email card autonomy row**
- Rule: autonomy appears on the card but no rule says how it is labeled.
- Fix: "The card shows net-positive autonomy as strong, neutral as fair and negative as poor, for display only, with no effect on any score."

Some terms in the rules rely on judgment and aren't listed under Interpretations: "load-bearing" (Qualifications), "core daily work" (Fit), and "central to the daily work" (rule 4a). I left them out because you asked me not to add rules, but they could still split two careful readers.
