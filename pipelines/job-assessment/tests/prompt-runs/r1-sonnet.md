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

Each sentence below restates a number or order the Scoring rules and Verdict rules tables already give. I checked each against those tables. The numbering follows Interpretations 1 to 14.

## Ambiguities and clarifying sentences

**1. Soft must-have, fair rating**
Rule: "For each **soft** must-have: weak or poor costs 1, anything else costs 0."
Gap: "anything else" doesn't name fair or unknown.
> For a soft must-have, strong, fair and unknown all cost 0, and only weak or poor costs 1.

**2. Pay between open ask and target**
Rule: "at or above target 10; at or above min 8; at or above floor 3; below floor 1."
Gap: the open ask is one of the five stored numbers, but the tiers never mention it.
> A pay top at or above min and below target scores 8 wherever it sits relative to the open ask, which is not a scoring boundary.

**3. When rounding happens**
Rule: "clamped to its floor and cap and then rounded half up to a whole number (8.5 becomes 9, not 8) before the verdict rules run."
Gap: rule 4c says "the average of Fit and Qualifications", which could use raw or rounded inputs.
> Every verdict rule, including the 4c average of Fit and Qualifications, uses the already-rounded whole-number scores.

**4. Must-haves the findings never mention**
Rule: strong must-have "unknown costs 1.5"; soft must-have "anything else costs 0".
Gap: whether leaving a requirement out counts as unknown.
> A strong must-have missing from the findings is scored as unknown and costs 1.5, while a missing soft must-have, perk, phrase or flag costs or adds 0.

**5. Years versus narrow sub-domain**
Rule: "Asking for more years than the person has, or for years in a narrow sub-domain, costs 2 (once)."
Gap: "or" could mean both are charged.
> If a posting asks for too many years and for years in a narrow sub-domain, the combined cost is 2, not 4.

**6. Known gaps and self-score gaps**
Rule: "Each load-bearing known gap costs 1, and self-scores of 0 or 1 on load-bearing lines share the same cap of 4 (one skill is never counted twice)."
Gap: the cap of 4 is never stated before "the same cap", and the two kinds of gap could be capped separately.
> Load-bearing known gaps and load-bearing self-scores of 0 or 1 form one set that costs 1 per skill, at most 4 in total, and a skill that is both counts once.

**7. Pay tier selection**
Rule: "pick the tier (the person's named location, else a nationwide or 'everywhere else' tier, else the lowest tier)".
Gap: who picks, and whether "lowest" means the lowest label or the lowest pay.
> The code, not the model, picks the tier: one whose label contains the person's location label, else one labelled nationwide, national, everywhere else or all other, else the one with the lowest top of range.

**8. Low time off**
Rule: "Low time off (below the person's threshold, or accrual only) costs 2."
Gap: what happens when the posting gives neither a number nor "accrual".
> Time off is low, and costs 2, if the posting says accrual only or states a number of days under the person's threshold; if it states neither, the model's low-time-off flag decides.

**9. Hustle phrases**
Rule: "Each hustle phrase costs 1, at most 3."
Gap: whether a phrase must be on the profile's `hustle_phrases` list, and how `free_phrases` interacts.
> Each quoted hustle phrase costs 1, up to 3 in total, unless it is on the person's `free_phrases` list, whether or not it appears on their `hustle_phrases` list.

**10. Unlisted pay and soft flags**
Rule: "Each tripped soft flag costs 1, but unlisted pay is never a Culture cost because Comp already scored it."
Gap: how a pay flag is recognised.
> A soft flag about unlisted or non-transparent pay, such as `no_pay_transparency` or `unlisted_pay`, is left out of the tripped soft flags that cost 1 each in Culture.

**11. Generic autonomy phrases**
Rule: "Autonomy the findings mark `net: negative` ... costs 2", and a poor read resting only on generic phrases should be unknown.
Gap: what makes a quote generic.
> A quote is generic only if it contains a phrase like "partner with", "work closely" or "stakeholder" and none like "approval", "sign-off", "reports to" or "ownership", and autonomy supported only by generic quotes is unknown, which costs 0 in Fit.

**12. Where quotes may come from**
Rule: "Every rating other than unknown carries a quote copied from the posting."
Gap: in a saved note, the assessment block and front matter also contain text.
> In a saved note, a quote counts only if it appears below the "Full posting text" heading.

**13. Repeated quotes**
Rule: "A big perk adds 2, a nice perk adds 1 ... Each hustle phrase costs 1 ... Each tripped soft flag costs 1."
Gap: whether quoting the same item twice doubles it.
> A perk, hustle phrase or soft flag quoted more than once adds or costs its stated amount only once.

**14. Email card autonomy row**
Rule: Fit charges 2 only for `net: negative`.
Gap: the card shows "strong/fair/poor", which could be mistaken for a rating that feeds scoring.
> The card's autonomy row shows net positive as strong, neutral as fair and negative as poor for display only, and Fit still charges 2 only when net is negative.

## The three deliberate judgment calls

These are where the document says readers will differ, so I only pin down how the output is used.

- **Load-bearing line** (Qualifications): "Each load-bearing known gap costs 1."
  > Whether a line is load-bearing is the model's recorded call in the findings, and the scripts apply the Qualifications costs to that call without re-deciding it.
- **Core daily work** (Fit): "Each skill the person would rather avoid that is core daily work in this job costs 1, at most 2 in total."
  > Whether an avoided skill is core daily work is the model's recorded call, and the scripts charge 1 per skill so marked, up to 2.
- **Central to the daily work** (rule 2, 4a): "A required skill that is central to the daily work has no evidence behind it at all."
  > A skill has evidence only when a finding cites a valid evidence id for it, since a self-score is never evidence, and a skill marked `unproven` has none.

The last sentence assumes `proof: unchecked` evidence still counts as evidence, because the document only refuses ids that are missing, `do_not_use` or `OTHER-AUTHOR`. Confirm that's intended.

## Gaps I didn't resolve

Resolving these would mean inventing rules, so they need your decision:

- Interpretation 13 doesn't say whether a repeated negative phrase or strong positive phrase counts once.
- "Top of its range" for pay is undefined for a single figure or an open-ended range.
- Two tiers whose labels both match the person's location have no tie-break.
- "Strong positive phrase", "negative phrase" and "working-style mismatch" have no definition in this document.

## Rules that may be wrong (unchanged above)

- **Comp cliff:** pay at or above floor but below min scores 3, which triggers 4c Comp. So any top below min forces "Apply with reservations", and the 5-point jump from 3 to 8 sits at min.
- **Unknown costs differ:** a strong must-have unknown costs 1.5, the same as weak, while a soft one costs 0. Silence is penalised as if it were bad news, though Culture treats silence as neutral.
- **Hustle list is inert:** under Interpretation 9, `hustle_phrases` has no effect on scoring because any quoted hustle phrase costs 1. Only `free_phrases` matters.
- **Pay flags are hardcoded by id:** Interpretation 10 depends on flag ids like `no_pay_transparency`, so a differently named flag would double-count unlisted pay.
- **Rule 1 trusts the model:** the findings record whether a named exception applies, and `verdict.py` only learns whether a block is still tripped. The most severe verdict therefore rests on an unchecked model call.
