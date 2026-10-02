<!-- FICTIONAL EXAMPLE DATA. Not a real person. Saved by tests/prompt-runs/run_prompts.py -->
# Prompt run: Review the rules for gaps (ARCHITECTURE.md), on sonnet

- Prompt file: `prompts/r1-review-rules.txt`
- Date: 2026-10-01. Model alias `sonnet`, which ran as `claude-sonnet-5-5` (Claude Code can add a small helper model call of its own).
- Turns: 1. Cost: $0.12 (the simulated user's calls are not included).
- Grade: see `GRADES.md`.

## Conversation

### User

[the prompt below, with attached files: ARCHITECTURE.md]

I'm attaching ARCHITECTURE.md from a job assessment tool. Read its scoring and verdict rules. List every place where two careful readers could score the same posting differently, quote the rule, and propose one sentence that removes the ambiguity. Each sentence only clarifies: it keeps every number, band, cap and rule order exactly as the Scoring rules and Verdict rules tables state them, so check each sentence against those tables before you write it. If you think a rule itself is wrong, say so in a separate list instead of changing it. A good answer covers every item listed under Interpretations and does not invent new rules.

### Model

I checked each sentence below against the Scoring rules and Verdict rules tables. None changes a number, band, cap or rule order. Items 1-14 follow the Interpretations list in order, then the three judgment calls, then gaps the Interpretations list doesn't cover.

## Clarifying sentences

**1. Fair on a soft must-have.**
Rule: "For each **soft** must-have: weak or poor costs 1, anything else costs 0."
Split: "anything else" could be read to leave unknown or fair open.
Sentence: *A soft must-have costs 1 when rated weak or poor and 0 when rated strong, fair or unknown.*

**2. Pay between open ask and target.**
Rule: "at or above target 10; at or above min 8; at or above floor 3; below floor 1."
Split: the profile stores five pay numbers, so a reader might treat the open ask or stretch ceiling as a band edge.
Sentence: *Only target, min and floor are score boundaries, so any top at or above min and below target scores 8 regardless of the open ask.*

**3. Rounding before the verdict.**
Rule: "rounded half up to a whole number (8.5 becomes 9, not 8) before the verdict rules run" and "the average of Fit and Qualifications is under 7".
Split: the average could be taken from unrounded scores, and the 5-or-lower floor could be tested on raw values.
Sentence: *Every verdict test, including the Fit and Qualifications average, uses the rounded whole-number scores, so an average of 6.5 is under 7 and an average of 7 is not.*

**4. Silent must-haves.**
Rule: "unknown costs 1.5" (strong must-have), and "anything else costs 0" (soft).
Split: it is unclear whether a requirement the findings omit is skipped or scored as unknown.
Sentence: *A strong must-have missing from the findings is scored as unknown and costs 1.5, while a missing soft must-have, perk, phrase or flag costs 0.*

**5. Years and narrow sub-domain.**
Rule: "Asking for more years than the person has, or for years in a narrow sub-domain, costs 2 (once)."
Split: "or" could mean both conditions together cost 4.
Sentence: *If the posting asks for too many years, for years in a narrow sub-domain, or both, the total cost is 2.*

**6. Known gaps and self-score gaps.**
Rule: "Each load-bearing known gap costs 1, and self-scores of 0 or 1 on load-bearing lines share the same cap of 4 (one skill is never counted twice)."
Split: it is unclear whether the cap is per type or shared, and what a self-score gap costs. The worked example's Kubernetes line shows 1.
Sentence: *Load-bearing known gaps and load-bearing self-scores of 0 or 1 form one set with one entry per skill, each entry costs 1, and the set costs at most 4 in total.*

**7. Pay tier selection.**
Rule: "the person's named location, else a nationwide or 'everywhere else' tier, else the lowest tier".
Split: "lowest tier" could mean the lowest label, the lowest floor or the lowest top, and the model might choose the tier itself.
Sentence: *The code picks the tier, ignoring the model's tier_used: the tier whose label contains the person's location label, otherwise one labelled nationwide, national, everywhere else or all other, otherwise the tier with the lowest top.*
Note: Interpretation 7 ends with "or similar", which stays open-ended. The author should either close that list or accept it as a judgment call.

**8. Low time off.**
Rule: "Low time off (below the person's threshold, or accrual only) costs 2."
Split: it is unclear whether a number equal to the threshold is low, and what happens when the posting gives no number.
Sentence: *Time off costs 2 when it is accrual-only or states a number of days strictly under the person's threshold, and when neither applies, the model's low-time-off flag decides.*

**9. Hustle phrases.**
Rule: "Each hustle phrase costs 1, at most 3", with free phrases "cost nothing".
Split: it is unclear whether only phrases on the person's hustle list count.
Sentence: *Each distinct quoted hustle phrase not on the person's free_phrases list costs 1, whether or not it is on their hustle_phrases list, and the hustle total is at most 3.*

**10. Unlisted pay and soft flags.**
Rule: "unlisted pay is never a Culture cost because Comp already scored it."
Split: a soft flag about pay transparency could be read as a separate Culture cost.
Sentence: *A soft flag that concerns unlisted pay costs nothing in Culture; unlisted pay is scored only by Comp, as 5.*

**11. Generic autonomy phrases.**
Rule (from the `check_findings.py` list): "A read that autonomy is poor rests only on generic phrases".
Split: a quote that contains both a generic phrase and a decision phrase is ambiguous.
Sentence: *An autonomy quote is generic only if it contains a generic collaboration phrase and no phrase that says who decides, so a quote containing both is not generic.*

**12. Where quotes must come from.**
Rule: "its quote is not in the posting text".
Split: in a saved note, "posting text" could include the front matter or the assessment block.
Sentence: *A quote counts only if it appears in the posting text itself, which in a saved note is only the text below the "Full posting text" heading.*

**13. Repeats.**
Rule: "A big perk adds 2... Each hustle phrase costs 1... Each tripped soft flag costs 1."
Split: the same item quoted twice could count twice.
Sentence: *The same perk, phrase or soft flag quoted more than once adds or costs once, and any cap is applied after duplicates are removed.*

**14. Email card autonomy row.**
Rule: none in the tables, and the card is display only.
Split: a reader might think the card's strong/fair/poor labels feed Fit.
Sentence: *The email card's autonomy row shows net positive as strong, neutral as fair and negative as poor, and changes no score.*

## The three judgment calls

The tables name three phrases that the code can't decide. I can't see the `assessment/SKILL.md` step 3e definitions, so these sentences point to them rather than restate them.

**15. "Load-bearing" (Qualifications).**
Rule: "Each load-bearing known gap costs 1".
Sentence: *"Load-bearing" is decided by the definition in assessment/SKILL.md step 3e, applied the same way to every posting.*

**16. "Core daily work" (Fit).**
Rule: "Each skill the person would rather avoid that is core daily work in this job costs 1, at most 2 in total."
Sentence: *"Core daily work" is decided by the definition in assessment/SKILL.md step 3e, applied the same way to every posting.*

**17. "Central to the daily work" and "no evidence behind it at all" (rule 4a).**
Rule: "A required skill that is central to the daily work has no evidence behind it at all."
Split: the "no evidence" half is checkable, so it needs its own sentence.
Sentence: *A skill has evidence only when a finding cites an existing, usable evidence id for work the person did themself, and a self-score or an unproven status never counts as evidence.*
This follows the central-file section ("A self-score is the person's own claim, never evidence"). "Central to the daily work" stays a step 3e judgment. The author should say whether it is the same test as item 16.

## Gaps the Interpretations list doesn't cover

I can't resolve these with a clarifying sentence, because any answer would be a new rule. The author has to choose.

- **"Autonomy that reads net negative costs 2."** It's unclear whether only a poor rating counts or weak does too. Item 14's display mapping suggests poor only, but that is display, not scoring.
- **"Top of its range" for a single figure or an open-ended "$X+" posting.** The rule doesn't say what the top is.
- **"Strong positive phrase", "negative phrase", "working-style mismatch" and whether a hard block is tripped.** These are model judgments with no stated definition here.

## Rules that may be wrong

I haven't changed any of these.

1. **Unlisted pay scores 5 and avoids rule 4c, while listed pay just above floor scores 3 and can trigger it.** Hiding pay can produce a better verdict than disclosing low pay.
2. **Rounding before the thresholds.** A raw Fit of 5.4 rounds to 5 and fires the floor ("5 or lower"), while 5.5 does not. Items 3 and the table together create a cliff at an arbitrary half-point.
3. **Unknown costs the same as weak on a strong must-have (1.5 each).** Silence in the posting is penalised like a real shortfall, which conflicts with Culture's "silence tells you nothing".
4. **Negative phrases are uncapped, while hustle phrases are capped at 3.** Nothing explains the difference.
5. **The open ask is stored but never used in scoring**, and per item 9 the `hustle_phrases` list has no effect on cost. Both fields suggest rules the code doesn't apply.
6. **Rule 1 depends on the company.** Hard blocks are skipped when "a named exception covers this company", but the document says "The company's name is not an input" to `verdict.py`. Presumably the exception is resolved upstream, but the document should say so.
