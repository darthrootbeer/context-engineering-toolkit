<!-- FICTIONAL EXAMPLE DATA. Not a real person. Saved by tests/prompt-runs/run_prompts.py -->
# Prompt run: Test the scoring with the fixture, on sonnet

Note: the pay figures in this record were changed after the run to fictional ones. Nothing else was edited; the scores and verdicts are as recorded.

- Prompt file: `prompts/04-test-scoring.txt`
- Date: 2026-10-01. Model alias `sonnet`, which ran as `claude-sonnet-5-5` (Claude Code can add a small helper model call of its own).
- Turns: 1. Cost: $0.12 (the simulated user's calls are not included).
- Grade: see `GRADES.md`.

## Conversation

### User

[the prompt below, with attached files: ARCHITECTURE.md, fixtures/robin-sample/career-profile.yaml, fixtures/postings/01-strong-fit.md, fixtures/postings/02-job-type-override.md, fixtures/postings/03-unlisted-pay-perks.md, fixtures/findings/01-strong-fit.findings.json, fixtures/findings/02-job-type-override.findings.json, fixtures/findings/03-unlisted-pay-perks.findings.json, fixtures/expected.yaml]

I'm attaching ARCHITECTURE.md, fixtures/robin-sample/career-profile.yaml, the three postings in fixtures/postings/ and their files in fixtures/findings/. For each posting, apply the scoring rules by hand to its findings file. Show the arithmetic for Fit, Comp, Qualifications and Culture, round each the way ARCHITECTURE.md says, then apply the verdict rules in order and name the rule that decided it. Only after all three answers are written, open fixtures/expected.yaml, compare, and list every mismatch with the step where your arithmetic and the file disagree. A good answer matches all three verdicts and all twelve scores.

### Model

I did all three by hand from the findings files, the profile and ARCHITECTURE.md. I compared against `fixtures/expected.yaml` only after finishing the arithmetic. I didn't call a tool to open it because you attached its contents, so I read it from the attachment.

## Posting 01: Copperline, docs-platform lane

| Score | Arithmetic | Result |
|---|---|---|
| Fit | 10. `ai_forward` (strong must-have) rated strong: 0. `docs_as_code` (strong) rated strong: 0. `ci_for_docs` (soft) rated weak: -1. `solo_ownership` is a bonus: 0. Autonomy net positive: 0. No avoid-core skills: 0. | **9** |
| Comp | The tier is Region B, matching Robin's location label. Top is 104,000, which is at or above the target of 78,000. | **10** |
| Qualifications | 10. Asks for 7 years and Robin has 9: 0. Known gap `go_lang`: -1. No self-score gaps. No style mismatch. | **9** |
| Culture | 5. Unlimited PTO (big) +2, learning budget (big) +2, meetups (nice) +1, "definition of done" (strong positive) +1. That is 11, capped at 10. | **10** |

**Verdict:**
- Rule 1: no hard block.
- Rule 2: override not fired.
- Rule 3: Fit 9 and Qualifications 9 are both above 5.
- Rule 4: Comp 10 and Culture 10 are above 3, and the average of Fit and Qualifications is 9, which is at least 7.
- Rule 5 decides: **Apply (4d)**.

## Posting 02: Driftmark, tech-writing lane

| Score | Arithmetic | Result |
|---|---|---|
| Fit | 10. `expert_access` (strong) fair: 0. `tooling_voice` (strong) fair: 0. `style_guide` (soft) poor: -1. Autonomy unknown: 0. Avoid-core skills are `video_tutorials` and `localization_pm`, -1 each, which is within the cap of 2: -2. 10 - 1 - 2 = 7. | **7** |
| Comp | No tier label contains "Region B", so the code uses the "Everywhere else" tier. Top is 78,000, which is at or above the floor of 75,000 but below the min of 80,000. | **3** |
| Qualifications | 10. Asks for 12 years and Robin has 9: -2, once. Known gaps `dita_xml` and `mobile_sdk`: -2. Nothing else. 10 - 2 - 2 = 6. | **6** |
| Culture | 5. No perks, phrases, flags or hustle language. | **5** |

**Verdict:**
- Rule 1: no hard block.
- Rule 2 decides: the findings say a required skill central to the daily work, video tutorials, has no evidence behind it (`evidence_checked` is empty). **Skip (4a)**.

The scores would not have changed this outcome: Comp is 3 (so 4c would also apply) and the Fit/Qualifications average is 6.5. But rule 2 comes before rule 4, so 4a decides.

## Posting 03: Ashgrove, tech-writing lane

| Score | Arithmetic | Result |
|---|---|---|
| Fit | 10. `expert_access` (strong) weak: -1.5. `tooling_voice` (strong) unknown: -1.5. `style_guide` (soft) fair: 0. Autonomy unknown: 0. 10 - 1.5 - 1.5 = 7. | **7** |
| Comp | Pay is not listed, so the neutral score applies. | **5** |
| Qualifications | 10. Asks for 11 years and Robin has 9: -2. `mobile_sdk` known gap: -1. `kubernetes` self-score gap on a required line: -1. Total 3, within the cap of 4. 10 - 2 - 1 - 1 = 6. | **6** |
| Culture | 5. Extra days off (big) +2, learning budget (big) +2. "Fast-paced" is on Robin's free-phrases list, so it costs nothing. 5 + 2 + 2 = 9. | **9** |

**Verdict:**
- Rule 1: no hard block.
- Rule 2: override not fired.
- Rule 3: Fit 7 and Qualifications 6 are both above 5.
- Rule 4 decides: Comp 5 and Culture 9 are above 3, but the average of Fit and Qualifications is (7 + 6) / 2 = 6.5, which is under 7. **Apply with reservations (4c-average)**.

## Comparison with `fixtures/expected.yaml`

| Posting | Fit | Comp | Qual | Culture | Verdict | Trigger |
|---|---|---|---|---|---|---|
| 01 | 9 ✓ | 10 ✓ | 9 ✓ | 10 ✓ | Apply ✓ | 4d ✓ |
| 02 | 7 ✓ | 3 ✓ | 6 ✓ | 5 ✓ | Skip ✓ | 4a ✓ |
| 03 | 7 ✓ | 5 ✓ | 6 ✓ | 9 ✓ | Apply with reservations ✓ | 4c-average ✓ |

**Mismatches: none.** All twelve scores, all three verdicts and all three trigger labels agree with the file. Posting 03 also matches the worked example in ARCHITECTURE.md.

Three steps could have gone differently:
- **01 Culture:** the raw sum is 11, so the cap at 10 matters.
- **02 Comp:** it only lands on 3 if you pick the "Everywhere else" tier, which is what Interpretation 7 says to do when no tier names Region B. Using Region A's top of 98,000 would give 8.
- **02 Fit:** it needs the avoid-skills cap of 2 applied across both listed skills, with no stacking beyond that.
