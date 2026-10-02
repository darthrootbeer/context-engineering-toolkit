<!-- FICTIONAL EXAMPLE DATA. Not a real person. Saved by tests/prompt-runs/run_prompts.py -->
# Prompt run: Review the rules for gaps (ARCHITECTURE.md), on sonnet

- Prompt file: `prompts/r1-review-rules.txt`
- Date: 2026-10-01. Model alias `sonnet`, which ran as `claude-sonnet-5-5` (Claude Code can add a small helper model call of its own).
- Turns: 1. Cost: $0.13 (the simulated user's calls are not included).
- Grade: see `GRADES.md`.

## Conversation

### User

[the prompt below, with attached files: ARCHITECTURE.md]

I'm attaching ARCHITECTURE.md from a job assessment tool. Read its scoring and verdict rules. List every place where two careful readers could score the same posting differently, quote the rule, and propose one sentence that removes the ambiguity. Each sentence must keep every number, cap and rule order exactly as the document states them; if you think a rule itself is wrong, say so separately instead of changing it. A good answer covers every item listed under Interpretations and does not invent new rules.

### Model

I read only ARCHITECTURE.md, so I couldn't check the proposed sentences against the code or tests. Items 1-14 below match the 14 Interpretations. Each sentence restates the document's own rule and its stated resolution without changing any number, cap or rule order.

## Ambiguities listed under Interpretations

**1. Fair on a soft must-have**
Rule: "For each **soft** must-have: weak or poor costs 1, anything else costs 0."
Sentence: *For a soft must-have, weak or poor costs 1, and strong, fair or unknown costs 0.*

**2. Open ask and the Comp tiers**
Rule: "at or above target 10; at or above min 8; at or above floor 3; below floor 1."
Sentence: *The open ask is not a scoring boundary, so a pay top at or above min but below target scores 8 wherever it sits relative to the open ask.*

**3. Rounding and the average**
Rule: "rounded half up to a whole number (8.5 becomes 9, not 8) before the verdict rules run", and rule 4c: "the average of Fit and Qualifications is under 7."
Sentence: *Each score is clamped to its floor and cap and rounded half up to a whole number, and the 4c average is computed from those whole numbers and not rounded again, so 6.5 is under 7.*
The worked example (6.5 giving rule 4c) only holds if the average itself is not rounded. The document never says so outside that example.

**4. A strong must-have the findings never mention**
Rule: "strong or fair costs 0, weak costs 1.5, poor costs 3, unknown costs 1.5."
Sentence: *A strong must-have with no rating in the findings is scored as unknown and costs 1.5, while a silent soft must-have, perk or other item costs nothing.*

**5. Years and sub-domain**
Rule: "Asking for more years than the person has, or for years in a narrow sub-domain, costs 2 (once)."
Sentence: *If a posting asks for more years than the person has and also for years in a narrow sub-domain, the two together cost 2 in total, not 2 each.*

**6. Known gaps and self-score gaps**
Rule: "Each load-bearing known gap costs 1, and self-scores of 0 or 1 on load-bearing lines share the same cap of 4 (one skill is never counted twice)."
Sentence: *Load-bearing known gaps and self-score gaps of 0 or 1 form one set that costs 1 per skill and at most 4 in total, and a skill that is both is counted once.*
"The same cap" has no earlier cap to refer to. My sentence reads it as one combined cap of 4, which is the most natural reading but should be confirmed.

**7. Choosing the pay tier**
Rule: "the person's named location, else a nationwide or 'everywhere else' tier, else the lowest tier."
Sentence: *The code picks the tier: first one whose label contains the person's location label, else one whose label says nationwide, national, everywhere else, all other or similar, else the tier with the lowest top, and the model's tier_used is ignored.*
Two gaps remain: what counts as "similar", and what happens if two tiers match the location. The document doesn't say, so I haven't invented an answer.

**8. Low time off**
Rule: "Low time off (below the person's threshold, or accrual only) costs 2."
Sentence: *Time off is low, costing 2, when it is accrual only or when a stated number of days is under the person's threshold, and only if the posting gives neither does the model's flag decide.*

**9. Hustle phrases**
Rule: "Each hustle phrase costs 1, at most 3", with "Fast-paced" on a list of phrases that cost nothing.
Sentence: *A quoted hustle phrase on the person's free_phrases list costs nothing, and any other quoted hustle phrase costs 1, up to 3 in total, whether or not it is on the person's hustle_phrases list.*

**10. Unlisted pay in Culture**
Rule: "unlisted pay is never a Culture cost because Comp already scored it."
Sentence: *A soft flag whose id is no_pay_transparency or unlisted_pay, or which only says pay is not listed, costs nothing in Culture.*
The document says "ids such as", so the set is open-ended. The author should decide whether to list the ids exactly.

**11. Generic autonomy phrases**
Rule: "A read that autonomy is poor rests only on generic phrases... If that is all the posting says, the honest rating is unknown."
Sentence: *An autonomy quote is generic only if it contains a generic phrase such as "partner with", "work closely" or "stakeholder" and none of the decision phrases such as "approval", "sign-off", "reports to" or "ownership", and a poor read resting only on generic quotes must be rated unknown.*

**12. Where a quote may come from**
Rule: "Case, spaces, curly quotes and dashes are ignored. Words are not."
Sentence: *A quote must appear in the posting text itself, matching ignoring case, spaces, curly quotes and dashes but not words, and in a saved note only text below the "Full posting text" heading counts.*

**13. Repeats**
Rule: "A big perk adds 2... Each hustle phrase costs 1... Each tripped soft flag costs 1."
Sentence: *The same perk, phrase or soft flag quoted more than once adds or costs once, and the hustle cap of 3 and the Culture cap of 10 apply after that.*

**14. Email autonomy row**
Rule: "Autonomy that reads net negative costs 2", next to a card that shows autonomy on the strong-to-poor scale.
Sentence: *The email card's autonomy row shows net positive as strong, neutral as fair and net negative as poor, and this display mapping changes no score.*

## Further ambiguities not under Interpretations

These affect scoring, but the document doesn't pin an answer, so I can't write a sentence without inventing a rule. Each needs the author's decision.

- **"Net negative" autonomy (Fit)** is never defined against the five-level scale. Does only poor count, or does weak count too? Item 14 gives a mapping, but only for display.
- **"Load-bearing", "core daily work" and "central to the daily work"** (Fit, Qualifications, rule 4a) are left to the model's judgment, with no test.
- **"No evidence behind it at all" (rule 4a):** it is unclear whether `proof: unchecked` evidence counts, and whether a `{skill_id, status: unproven}` entry triggers 4a.
- **Hard block exceptions (rule 1):** the rule says "no named exception covers this company", but the document also says "The company's name is not an input" to verdict.py. Presumably the findings decide this before verdict.py runs, but it isn't stated.
- **Trigger label when several 4c conditions fire:** the labels are `4c comp`, `4c culture`, `4c comp and culture` and `4c average`. If Comp is low and the average is also under 7, the label is unspecified. The verdict is the same, but the label has to match fixtures/expected.yaml.
- **Pay shape:** "score the **top** of its range" doesn't say what to do with a single figure or an open-ended "from X" range.

## Rules that may be wrong (not changed above)

- **Comp 3 always triggers 4c.** Pay at or above floor but below min scores 3, and rule 4c fires at "Comp is 3 or lower". That makes the "at or above floor 3" tier a guaranteed reservation. It may be intended, but it's worth confirming.
- **Hustle phrases outside the person's list still cost 1.** This makes the `hustle_phrases` list pointless. It also lets the model add a cost from a phrase the profile never listed, which cuts against "the model reads, the code decides". The checker only requires a real quote.
- **Silent strong must-haves are allowed.** The document says "Every requirement in the lane gets a rating", yet item 4 prices a missing one and none of the seven checks rejects a missing rating. Either the checker should reject it, or the sentence about ratings should be softened.
- **Half-point costs plus half-up rounding** can move a verdict. A Fit of 5.5 rounds to 6 and escapes the floor in rule 4b, so a single 1.5 cost can decide the outcome. This follows from the stated rules, but the author should know it is there.
