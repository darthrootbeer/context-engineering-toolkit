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

I worked all three from the rules and findings first, then compared against `expected.yaml`. All three verdicts and all twelve scores match, with one wording difference on a trigger label.

## Posting 01: Copperline, Docs Platform Engineer (lane docs-platform)

| Score | Arithmetic | Result |
|---|---|---|
| Fit | 10. `ai_forward` (strong, rated strong): 0. `docs_as_code` (strong, rated strong): 0. `ci_for_docs` (soft, rated weak): -1. `solo_ownership` is a bonus: 0. Autonomy is net positive: 0. No avoided skills. 10 - 1 = 9. | **9** |
| Comp | Robin's label is Region B, so the Region B tier is used (not the model's choice, but the same). Top is $104,000, which is at or above the $78,000 target. | **10** |
| Qualifications | 10. The posting asks for 7 years and Robin has 9: 0. `go_lang` is a known gap: -1. Robin's self-score of 1 on Go is the same skill, so it counts once: 0. No working-style mismatch. 10 - 1 = 9. | **9** |
| Culture | 5. `unlimited_pto` (big): +2. `learning_budget` (big): +2. `offsites` (nice): +1. "definition of done" (strong positive phrase): +1. 5 + 2 + 2 + 1 + 1 = 11, clamped to the cap of 10. | **10** |

**Verdict:**
1. No hard block.
2. No job-type override.
3. Fit 9 and Qualifications 9 are both above 5.
4. Comp 10 and Culture 10 are above 3, and the average of Fit and Qualifications is 9, which is not under 7.
5. Nothing fired, so **Apply**, rule 4d.

## Posting 02: Driftmark, Technical Writer, Video Tutorials (lane tech-writing)

| Score | Arithmetic | Result |
|---|---|---|
| Fit | 10. `expert_access` (strong, fair): 0. `tooling_voice` (strong, fair): 0. `style_guide` (soft, poor): -1. Autonomy unknown: 0. Avoided skills that are core daily work: `video_tutorials` -1 and `localization_pm` -1, which is -2 and within the cap of 2. 10 - 1 - 2 = 7. | **7** |
| Comp | No tier label contains "Region B", so the "Everywhere else" tier is used. Top is $78,000: at or above the $75,000 floor, below the $80,000 min. | **3** |
| Qualifications | 10. 12 years asked against Robin's 9: -2 (once). Known gaps `dita_xml` and `mobile_sdk`: -2. No self-score gaps. 10 - 2 - 2 = 6. | **6** |
| Culture | 5. No perks, phrases, flags or negatives. | **5** |

**Verdict:**
1. No hard block.
2. The job-type override fired. `video_tutorials` is core daily work ("Most of your week…"), and Robin has no evidence for it (`evidence_ids: []`, `evidence_checked: []`). Rule 2 decides: **Skip**, rule 4a.

Rules 3 and 4 are never looked at. Without rule 2, Comp 3 would still have put this in the reservations band.

## Posting 03: Ashgrove, Senior Technical Writer (lane tech-writing)

| Score | Arithmetic | Result |
|---|---|---|
| Fit | 10. `expert_access` (strong, weak): -1.5. `tooling_voice` (strong, unknown): -1.5. `style_guide` (soft, fair): 0. Autonomy unknown: 0. 10 - 1.5 - 1.5 = 7. | **7** |
| Comp | Pay is not listed, so the neutral 5. | **5** |
| Qualifications | 10. 11 years asked against 9: -2. `mobile_sdk` known gap: -1. `kubernetes` self-score gap (score 1): -1. 10 - 2 - 1 - 1 = 6. | **6** |
| Culture | 5. `extra_days_off` (big): +2. `learning_budget` (big): +2. "Fast-paced" is on Robin's free list, so it costs nothing. 5 + 2 + 2 = 9. | **9** |

**Verdict:**
1. No hard block.
2. No override.
3. Fit 7 and Qualifications 6 are both above 5.
4. Comp 5 and Culture 9 are above 3, but the average of Fit and Qualifications is (7 + 6) / 2 = 6.5, which is under 7. **Apply with reservations**, rule 4c.

## Comparison with `fixtures/expected.yaml`

| Posting | Fit | Comp | Qual | Culture | Verdict | Trigger |
|---|---|---|---|---|---|---|
| 01 | 9 ✓ | 10 ✓ | 9 ✓ | 10 ✓ | Apply ✓ | 4d ✓ |
| 02 | 7 ✓ | 3 ✓ | 6 ✓ | 5 ✓ | Skip ✓ | 4a ✓ |
| 03 | 7 ✓ | 5 ✓ | 6 ✓ | 9 ✓ | Apply with reservations ✓ | 4c vs `4c-average` (label only) |

**Score and verdict mismatches: none.** All twelve scores and all three verdicts agree.

**One label difference:** for posting 03 the file says `4c-average`, and I wrote `4c`. The rules table in ARCHITECTURE.md has only one reservations rule, 4c, and doesn't define sub-labels. The file's label records which of the three 4c conditions fired, which was the average under 7. The rule is the same and no arithmetic step disagrees. If a test compares trigger strings exactly, ARCHITECTURE.md should name the `-average`, `-comp` and `-culture` suffixes.

Two arithmetic points could have gone wrong:
- **Posting 01 Culture** was 11 before the cap, so the clamp to 10 is what makes it match.
- **Posting 02 Fit** needs the avoided-skills cost (-2) to reach 7. Without it, Fit would be 9.
