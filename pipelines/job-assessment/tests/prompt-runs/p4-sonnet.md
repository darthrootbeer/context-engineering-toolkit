<!-- FICTIONAL EXAMPLE DATA. Not a real person. Saved by tests/prompt-runs/run_prompts.py -->
# Prompt run: Test the scoring with the fixture, on sonnet

- Prompt file: `prompts/04-test-scoring.txt`
- Date: 2026-10-01. Model alias `sonnet`, which ran as `claude-sonnet-5-5` (Claude Code can add a small helper model call of its own).
- Turns: 1. Cost: $0.12 (the simulated user's calls are not included).
- Grade: see `GRADES.md`.

## Conversation

### User

[the prompt below, with attached files: ARCHITECTURE.md, fixtures/robin-sample/career-profile.yaml, fixtures/postings/01-strong-fit.md, fixtures/postings/02-job-type-override.md, fixtures/postings/03-unlisted-pay-perks.md, fixtures/findings/01-strong-fit.findings.json, fixtures/findings/02-job-type-override.findings.json, fixtures/findings/03-unlisted-pay-perks.findings.json, fixtures/expected.yaml]

I'm attaching ARCHITECTURE.md, fixtures/robin-sample/career-profile.yaml, the three postings in fixtures/postings/ and their files in fixtures/findings/. For each posting, apply the scoring rules by hand to its findings file. Show the arithmetic for Fit, Comp, Qualifications and Culture, round each the way ARCHITECTURE.md says, then apply the verdict rules in order and name the rule that decided it. Only after all three answers are written, open fixtures/expected.yaml, compare, and list every mismatch with the step where your arithmetic and the file disagree. A good answer matches all three verdicts and all twelve scores.

### Model

I scored all three from the findings files, then compared with `fixtures/expected.yaml`. The expected file was already pasted in your message, so I didn't open anything. I wrote the arithmetic before comparing.

## Posting 01: Copperline, docs-platform lane

| Score | Arithmetic | Result |
|---|---|---|
| Fit | 10. Strong must-haves `ai_forward` and `docs_as_code` are both rated strong: 0. Soft `ci_for_docs` is rated weak: -1. `solo_ownership` is a bonus: 0. Autonomy is positive: 0. No avoid-skills: 0. 10 - 1 = 9. | **9** |
| Comp | Robin's location is Region B, which matches a tier label. The top is 104,000, which is at or above the 100,000 target. | **10** |
| Qualifications | 10. The posting asks for 7 years and Robin has 9: 0. Known gap `go_lang`: -1. There are no separate self-score gaps, and Go would count once anyway. 10 - 1 = 9. | **9** |
| Culture | 5. Unlimited PTO (big) +2, learning budget (big) +2, meetups (nice) +1, "definition of done" +1. That is 11, capped at 10. | **10** |

**Verdict:**
1. No hard block.
2. The override is not fired.
3. Fit 9 and Qualifications 9 are both above 5.
4. Comp 10 and Culture 10 are both above 3, and the average of Fit and Qualifications is 9, which is not under 7.
5. Nothing fired, so rule 4d applies: **Apply**.

## Posting 02: Driftmark, tech-writing lane

| Score | Arithmetic | Result |
|---|---|---|
| Fit | 10. `expert_access` and `tooling_voice` are strong must-haves rated fair: 0. Soft `style_guide` is rated poor: -1. Autonomy is unknown: 0. Avoid-skills `video_tutorials` and `localization_pm` cost 1 each, within the cap of 2: -2. 10 - 1 - 2 = 7. | **7** |
| Comp | No tier label contains "Region B", so the code takes the "Everywhere else" tier. Its top is 78,000, which is at or above the 75,000 floor but below the 80,000 min. | **3** |
| Qualifications | 10. 12 years asked against Robin's 9: -2. Known gaps `dita_xml` and `mobile_sdk`: -1 each, -2 in total, under the cap of 4. 10 - 2 - 2 = 6. | **6** |
| Culture | 5. There are no perks, hustle phrases, flags or negative phrases. | **5** |

**Verdict:**
1. No hard block.
2. The findings mark `job_type_override.fired = true` for `video_tutorials`, which has no evidence behind it. Rule 4a fires and decides: **Skip**.
3. Nothing after rule 2 is checked. Fit 7 and Qualifications 6 would have passed 4b anyway, and Comp 3 would have triggered 4c.

## Posting 03: Ashgrove, tech-writing lane

| Score | Arithmetic | Result |
|---|---|---|
| Fit | 10. `expert_access` is a strong must-have rated weak: -1.5. `tooling_voice` is strong and unknown: -1.5. Soft `style_guide` is rated fair: 0. Autonomy is unknown: 0. 10 - 1.5 - 1.5 = 7. | **7** |
| Comp | Pay is not listed. | **5** |
| Qualifications | 10. 11 years asked against Robin's 9: -2. Known gap `mobile_sdk`: -1. Self-score gap `kubernetes`: -1. 10 - 2 - 1 - 1 = 6. | **6** |
| Culture | 5. Extra days off (big) +2, learning budget (big) +2. "Fast-paced" is a free phrase: 0. 5 + 2 + 2 = 9. | **9** |

**Verdict:**
1. No hard block.
2. The override is not fired.
3. Fit 7 and Qualifications 6 are both above 5.
4. Comp 5 and Culture 9 are both above 3, but the average of Fit and Qualifications is (7 + 6) / 2 = 6.5, which is under 7.
5. Rule 4c (average) fires: **Apply with reservations**.

## Comparison with `fixtures/expected.yaml`

| Posting | Fit | Comp | Qual | Culture | Verdict | Trigger |
|---|---|---|---|---|---|---|
| 01 | 9 = 9 | 10 = 10 | 9 = 9 | 10 = 10 | Apply = Apply | 4d = 4d |
| 02 | 7 = 7 | 3 = 3 | 6 = 6 | 5 = 5 | Skip = Skip | 4a = 4a |
| 03 | 7 = 7 | 5 = 5 | 6 = 6 | 9 = 9 | Apply with reservations = same | 4c-average = 4c average |

**Mismatches: none.** All twelve scores and all three verdicts and triggers match.

A few steps depended on judgment or on the rules' fine print:
- **Posting 01 Culture:** the raw total is 11, so the match depends on clamping to the cap of 10 before rounding.
- **Posting 02 Comp:** it depends on Interpretation 7, where the code picks the "Everywhere else" tier. Using Region A (top 98,000) would have scored 8.
- **Posting 02 Fit:** it depends on the two avoid-skills being treated as core daily work, which the findings assert.
- **Qualifications gaps in all three:** I counted every known gap as load-bearing, as the findings imply. That is the judgment call the document says can vary.
