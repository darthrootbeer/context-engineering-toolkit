<!-- FICTIONAL EXAMPLE DATA. Not a real person. Saved by tests/prompt-runs/run_prompts.py -->
# Prompt run: Review the rules for gaps (ARCHITECTURE.md), on haiku

- Prompt file: `prompts/r1-review-rules.txt`
- Date: 2026-10-01. Model alias `haiku`, which ran as `claude-haiku-4-5-20251001` (Claude Code can add a small helper model call of its own).
- Turns: 1. Cost: $0.10 (the simulated user's calls are not included).
- Grade: see `GRADES.md`.

## Conversation

### User

[the prompt below, with attached files: ARCHITECTURE.md]

I'm attaching ARCHITECTURE.md from a job assessment tool. Read its scoring and verdict rules. List every place where two careful readers could score the same posting differently, quote the rule, and propose one sentence that removes the ambiguity. Each sentence only clarifies: it keeps every number, band, cap and rule order exactly as the Scoring rules and Verdict rules tables state them, so check each sentence against those tables before you write it. If you think a rule itself is wrong, say so in a separate list instead of changing it. A good answer covers every item listed under Interpretations and does not invent new rules.

### Model

I'll work through each interpretation and note where the rule needs clarification to prevent two readers from scoring differently.

## Interpretations with rule ambiguities

**Interpretation 1:** "A fair rating on a soft must-have costs nothing."
- **Rule:** "For each **soft** must-have: weak or poor costs 1, anything else costs 0."
- **Ambiguity:** "Anything else" could mean fair, strong, or unknown; two readers might assume different ratings cost 0.
- **Clarification:** "For each **soft** must-have, weak or poor costs 1, and strong, fair, or unknown each cost 0."

**Interpretation 2:** "A pay top between the open ask and the target scores 8."
- **Rule:** "at or above target 10; at or above min 8; at or above floor 3; below floor 1."
- **Ambiguity:** The cascading conditions are unclear; two readers might assign different scores to pay between min and target.
- **Clarification:** "Score the tier's top as 10 if at or above target, 8 if at or above min but below target, 3 if at or above floor but below min, or 1 if below floor."

**Interpretation 4:** "A strong must-have the findings never mention counts as unknown and costs 1.5."
- **Rule:** "Start at 10. For each **strong** must-have in the lane: strong or fair costs 0, weak costs 1.5, poor costs 3, unknown costs 1.5."
- **Ambiguity:** The rule doesn't address must-haves absent from the findings; two readers might treat them as 0-cost or as unknown.
- **Clarification:** "For each **strong** must-have, if it appears in the findings rate it (strong or fair costs 0, weak costs 1.5, poor costs 3), and if not mentioned it counts as unknown and costs 1.5."

**Interpretation 5:** "Too many years and a narrow sub-domain cost 2 once in total, not 2 each."
- **Rule:** "Asking for more years than the person has, or for years in a narrow sub-domain, costs 2 (once)."
- **Ambiguity:** "(Once)" could mean one deduction, or could be read as applying to each scenario; two readers might subtract 2 or 4.
- **Clarification:** "Asking for more years than the person has, or for years in a narrow sub-domain, costs 2 total regardless of whether one or both conditions apply."

**Interpretation 6:** "Known gaps and self-score gaps are one set."
- **Rule:** "Each load-bearing known gap costs 1, and self-scores of 0 or 1 on load-bearing lines share the same cap of 4 (one skill is never counted twice)."
- **Ambiguity:** Two readers might differ on whether the same skill as both a known gap and self-score gap costs 1 or 2.
- **Clarification:** "Each load-bearing known gap and each self-score of 0 or 1 on a load-bearing line both cost 1, but the same skill cannot be subtracted twice; all such gaps cap at 4 total."

**Interpretation 7:** "The code picks the pay tier, not the model."
- **Rule:** "pick the tier (the person's named location, else a nationwide or 'everywhere else' tier, else the lowest tier)"
- **Ambiguity:** With multiple nationwide tiers or multiple lowest-top-tier options, two readers might pick differently.
- **Clarification:** "Pick the tier by this priority: first a tier whose label contains the person's location, then a tier labeled nationwide or everywhere else, then the tier with the lowest top salary."

**Interpretation 9:** "Hustle phrases. A phrase on the person's `free_phrases` list costs nothing."
- **Rule:** "Each hustle phrase costs 1, at most 3."
- **Ambiguity:** The rule doesn't mention that free_phrases are exempt; two readers might count them as costs.
- **Clarification:** "Each hustle phrase costs 1 except those on the person's free_phrases list cost nothing, with all hustle costs capped at 3 total."

**Interpretation 11:** "What counts as a generic autonomy phrase."
- **Rule:** "Autonomy that reads net negative costs 2."
- **Ambiguity:** "Net negative" is undefined; two readers might interpret different ratings as triggering the 2-point deduction.
- **Clarification:** "Autonomy rated as poor costs 2, while autonomy rated as strong, fair, weak, or unknown costs 0."

**Interpretation 12:** "Quotes must come from the posting text itself."
- **Rule:** "Every rating other than unknown carries a quote copied from the posting."
- **Ambiguity:** In a saved note format, two readers might differ on what counts as 'the posting'—note metadata, assessment block, or text body.
- **Clarification:** "Every rating other than unknown carries a quote copied from the posting text (text below the 'Full posting text' heading), not from the note's front matter or assessment block."

## Interpretations already clear in the rule

**Interpretation 3** — The rule already specifies "rounded half up" and gives the example (8.5 → 9).

**Interpretation 8** — The rule already states "(below the person's threshold, or accrual only)."

**Interpretation 10** — The rule already says "but unlisted pay is never a Culture cost."

**Interpretation 13** — The rule already states "quoted twice adds or costs once."

**Interpretation 14** — This is display-only; no scoring rule needs clarification.

## Potential issues with the rules themselves

**Open ask as a Comp boundary:** Interpretation 2 rests on the assumption that pay between the person's `open_ask` and `target` scores 8, but the rule never names `open_ask` as a boundary—only target, min, and floor. If this is not the intended behavior, the rule should explicitly define where open ask fits in the scoring tiers.
