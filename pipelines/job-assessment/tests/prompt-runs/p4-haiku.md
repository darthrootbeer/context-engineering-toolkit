<!-- FICTIONAL EXAMPLE DATA. Not a real person. Saved by tests/prompt-runs/run_prompts.py -->
# Prompt run: Test the scoring with the fixture, on haiku

Note: the pay figures in this record were changed after the run to fictional ones. Nothing else was edited; the scores and verdicts are as recorded.

- Prompt file: `prompts/04-test-scoring.txt`
- Date: 2026-10-01. Model alias `haiku`, which ran as `claude-haiku-4-5-20251001` (Claude Code can add a small helper model call of its own).
- Turns: 1. Cost: $0.06 (the simulated user's calls are not included).
- Grade: see `GRADES.md`.

## Conversation

### User

[the prompt below, with attached files: ARCHITECTURE.md, fixtures/robin-sample/career-profile.yaml, fixtures/postings/01-strong-fit.md, fixtures/postings/02-job-type-override.md, fixtures/postings/03-unlisted-pay-perks.md, fixtures/findings/01-strong-fit.findings.json, fixtures/findings/02-job-type-override.findings.json, fixtures/findings/03-unlisted-pay-perks.findings.json, fixtures/expected.yaml]

I'm attaching ARCHITECTURE.md, fixtures/robin-sample/career-profile.yaml, the three postings in fixtures/postings/ and their files in fixtures/findings/. For each posting, apply the scoring rules by hand to its findings file. Show the arithmetic for Fit, Comp, Qualifications and Culture, round each the way ARCHITECTURE.md says, then apply the verdict rules in order and name the rule that decided it. Only after all three answers are written, open fixtures/expected.yaml, compare, and list every mismatch with the step where your arithmetic and the file disagree. A good answer matches all three verdicts and all twelve scores.

### Model

I'll work through each posting systematically, applying the scoring rules from ARCHITECTURE.md.

---

## **Posting 01: strong-fit (docs-platform lane)**

**Fit:** Start at 10.
- `ai_forward` (strong): "strong" rating → 0
- `docs_as_code` (strong): "strong" rating → 0
- `ci_for_docs` (soft): "weak" rating → -1
- `solo_ownership` (soft, bonus): "fair" rating, but bonus never costs → 0
- Autonomy: "positive" → 0
- **10 - 1 = 9**

**Comp:** Pay listed. Region B tier: max $104,000. Robin's target is $78,000. $104,000 ≥ target → **10**

**Qualifications:** Start at 10.
- Years: 7+ required, Robin has 9 → 0
- Known gap `go_lang` → -1
- **10 - 1 = 9**

**Culture:** Start at 5.
- `unlimited_pto` (big) → +2
- `learning_budget` (big) → +2
- `offsites` (nice) → +1
- "definition of done" (strong positive phrase) → +1
- **5 + 2 + 2 + 1 + 1 = 11, capped at 10 = 10**

**Verdict:** Hard block: no. Override: no. Fit 9 > 5: no skip. Qualifications 9 > 5: no skip. Comp 10 > 3 and Culture 10 > 3 and average (9+9)/2 = 9 ≥ 7: no reservations. **Apply, rule 4d**

---

## **Posting 02: job-type-override (tech-writing lane)**

**Fit:** Start at 10.
- `expert_access` (strong): "fair" → 0
- `tooling_voice` (strong): "fair" → 0
- `style_guide` (soft): "poor" → -1
- Autonomy: "unknown" → 0
- Avoid skills: `video_tutorials` (core) -1, `localization_pm` (core) -1, capped at 2 total → -2
- **10 - 1 - 2 = 7**

**Comp:** Pay listed. Robin's location "Region B" doesn't match any tier. Falls back to "Everywhere else" tier: max $78,000. Robin's floor is $75,000, min is $80,000. $78,000 ≥ floor but below min → **3**

**Qualifications:** Start at 10.
- Years: 12+ required, Robin has 9 → -2
- Known gaps: `dita_xml` -1, `mobile_sdk` -1
- **10 - 2 - 1 - 1 = 6**

**Culture:** Start at 5.
- No perks, phrases, or flags → **5**

**Verdict:** Hard block: no. Override: yes, `video_tutorials` core daily work with no evidence → **Skip, rule 4a**

---

## **Posting 03: unlisted-pay-perks (tech-writing lane)**

**Fit:** Start at 10.
- `expert_access` (strong): "weak" → -1.5
- `tooling_voice` (strong): "unknown" → -1.5
- `style_guide` (soft): "fair" → 0
- Autonomy: "unknown" → 0
- **10 - 1.5 - 1.5 = 7**

**Comp:** Pay not stated → **5**

**Qualifications:** Start at 10.
- Years: 11+ required, Robin has 9 → -2
- Known gap `mobile_sdk` → -1
- Self-score gap `kubernetes` (score 1) → -1
- **10 - 2 - 1 - 1 = 6**

**Culture:** Start at 5.
- `extra_days_off` (big) → +2
- `learning_budget` (big) → +2
- **5 + 2 + 2 = 9**

**Verdict:** Hard block: no. Override: no. Fit 7 > 5, Qualifications 6 > 5: no skip. Comp 5 > 3, Culture 9 > 3, but average (7+6)/2 = 6.5 < 7 → **Apply with reservations, rule 4c-average**

---

## **Comparison to fixtures/expected.yaml:**

| Posting | Score | My answer | Expected | Match |
|---------|-------|-----------|----------|-------|
| **01** | Fit | 9 | 9 | ✓ |
| | Comp | 10 | 10 | ✓ |
| | Qualifications | 9 | 9 | ✓ |
| | Culture | 10 | 10 | ✓ |
| | Verdict | Apply | Apply | ✓ |
| | Trigger | 4d | 4d | ✓ |
| **02** | Fit | 7 | 7 | ✓ |
| | Comp | 3 | 3 | ✓ |
| | Qualifications | 6 | 6 | ✓ |
| | Culture | 5 | 5 | ✓ |
| | Verdict | Skip | Skip | ✓ |
| | Trigger | 4a | 4a | ✓ |
| **03** | Fit | 7 | 7 | ✓ |
| | Comp | 5 | 5 | ✓ |
| | Qualifications | 6 | 6 | ✓ |
| | Culture | 9 | 9 | ✓ |
| | Verdict | Apply with reservations | Apply with reservations | ✓ |
| | Trigger | 4c-average | 4c-average | ✓ |

**All twelve scores and three verdicts match.** No mismatches.
