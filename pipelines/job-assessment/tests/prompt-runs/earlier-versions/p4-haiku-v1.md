<!-- FICTIONAL EXAMPLE DATA. Not a real person. Saved by tests/prompt-runs/run_prompts.py -->
# Prompt run: Test the scoring with the fixture, on haiku

- Prompt file: `prompts/04-test-scoring.txt`
- Date: 2026-10-01. Model alias `haiku`, which ran as `claude-haiku-4-5-20251001` (Claude Code can add a small helper model call of its own).
- Turns: 1. Cost: $0.07 (the simulated user's calls are not included).
- Grade: see `GRADES.md`.

## Conversation

### User

[the prompt below, with attached files: ARCHITECTURE.md, fixtures/robin-sample/career-profile.yaml, fixtures/postings/01-strong-fit.md, fixtures/postings/02-job-type-override.md, fixtures/postings/03-unlisted-pay-perks.md, fixtures/findings/01-strong-fit.findings.json, fixtures/findings/02-job-type-override.findings.json, fixtures/findings/03-unlisted-pay-perks.findings.json, fixtures/expected.yaml]

I'm attaching ARCHITECTURE.md, fixtures/robin-sample/career-profile.yaml, the three postings in fixtures/postings/ and their files in fixtures/findings/. For each posting, apply the scoring rules by hand to its findings file. Show the arithmetic for Fit, Comp, Qualifications and Culture, round each the way ARCHITECTURE.md says, then apply the verdict rules in order and name the rule that decided it. Only after all three answers are written, open fixtures/expected.yaml, compare, and list every mismatch with the step where your arithmetic and the file disagree. A good answer matches all three verdicts and all twelve scores.

### Model

I'll work through each posting's scoring, showing all arithmetic, then compare with the expected file.

---

## Posting 01: 01-strong-fit.md (docs-platform lane)

**Fit:** Start at 10.
- `ai_forward` (strong): rating "strong" → 0
- `docs_as_code` (strong): rating "strong" → 0
- `ci_for_docs` (soft): rating "weak" → 1 (soft weak costs 1)
- `solo_ownership` (soft, bonus): rating "fair" → 0 (bonus never costs)
- Autonomy "positive" → 0

10 − 0 − 0 − 1 − 0 = **9**

**Comp:** Pay stated, Region B tier, top $150,000. Robin's target is $140,000. Top is at or above target. Score **10**.

**Qualifications:** Start at 10.
- Years required 7, Robin has 9 → 0 (not more, not narrow)
- Known gap hit: `go_lang` → 1

10 − 0 − 1 = **9**

**Culture:** Start at 5.
- `unlimited_pto` (big) → +2
- `learning_budget` (big) → +2
- `offsites` (nice) → +1
- "definition of done" (strong positive phrase) → +1

5 + 2 + 2 + 1 + 1 = 11, capped at 10 = **10**

**Verdict:** Hard block? No. Job-type override? No. Score floor (Fit or Qual ≤5)? No (both 9). Reservations band? Comp=10, Culture=10, avg(9,9)=9, all pass. → **Apply, rule 4d**

---

## Posting 02: 02-job-type-override.md (tech-writing lane)

**Fit:** Start at 10.
- `expert_access` (strong): rating "fair" → 0 (fair on strong costs nothing)
- `tooling_voice` (strong): rating "fair" → 0
- `style_guide` (soft): rating "poor" → 1 (soft poor costs 1)
- Autonomy "unknown" → 0
- Avoid skills: `video_tutorials` (core daily work, Robin wants to avoid) → 1; `localization_pm` (also core, coordinating vendors) → 1; capped at 2 total

10 − 0 − 0 − 1 − 2 = **7**

**Comp:** Pay stated, tier "Everywhere else," top $100,000. Floor $90K, min $110K. $100K is above floor but below min. Score **3**.

**Qualifications:** Start at 10.
- Years required 12, Robin has 9 → 2
- Known gaps hit: `dita_xml` (score 0, no evidence) and `mobile_sdk` (score 0, no evidence) → 1 + 1 = 2 total (shared cap is 4, so 2 cost)

10 − 2 − 2 = **6**

**Culture:** Start at 5.
- No perks quoted → 0
- No positive or negative phrases → 0

5 + 0 = **5**

**Verdict:** Hard block? No. Job-type override? Yes—video tutorials are core daily work and Robin has no evidence of that skill (Robin's self-score is 2, wanting to avoid it). → **Skip, rule 4a**

---

## Posting 03: 03-unlisted-pay-perks.md (tech-writing lane)

**Fit:** Start at 10.
- `expert_access` (strong): rating "weak" → 1.5
- `tooling_voice` (strong): rating "unknown" → 1.5
- `style_guide` (soft): rating "fair" → 0 (soft fair costs nothing)
- Autonomy "unknown" (only generic phrases) → 0

10 − 1.5 − 1.5 = **7**

**Comp:** Pay not stated. Score **5** (neutral middle).

**Qualifications:** Start at 10.
- Years required 11, Robin has 9 → 2
- Known gap `mobile_sdk` (score 0) → 1; self-score gap `kubernetes` (score 1) → 1; both count toward the shared cap of 4, so 2 total cost

10 − 2 − 2 = **6**

**Culture:** Start at 5.
- `extra_days_off` (big) → +2
- `learning_budget` (big) → +2

5 + 2 + 2 = **9**

**Verdict:** Hard block? No. Job-type override? No. Score floor? No (Fit=7, Qual=6, both >5). Reservations band? Comp=5 (>3), Culture=9 (>3), but avg(7, 6) = 6.5, which is **<7**. → **Apply with reservations, rule 4c-average**

---

## Comparison with fixtures/expected.yaml

| Posting | Check | My answer | Expected | Match? |
|---------|-------|-----------|----------|--------|
| 01 | Fit | 9 | 9 | ✓ |
| 01 | Comp | 10 | 10 | ✓ |
| 01 | Qualifications | 9 | 9 | ✓ |
| 01 | Culture | 10 | 10 | ✓ |
| 01 | Verdict | Apply | Apply | ✓ |
| 01 | Trigger | 4d | 4d | ✓ |
| 02 | Fit | 7 | 7 | ✓ |
| 02 | Comp | 3 | 3 | ✓ |
| 02 | Qualifications | 6 | 6 | ✓ |
| 02 | Culture | 5 | 5 | ✓ |
| 02 | Verdict | Skip | Skip | ✓ |
| 02 | Trigger | 4a | 4a | ✓ |
| 03 | Fit | 7 | 7 | ✓ |
| 03 | Comp | 5 | 5 | ✓ |
| 03 | Qualifications | 6 | 6 | ✓ |
| 03 | Culture | 9 | 9 | ✓ |
| 03 | Verdict | Apply with reservations | Apply with reservations | ✓ |
| 03 | Trigger | 4c-average | 4c-average | ✓ |

**Result: Perfect match on all twelve scores and all three verdicts.**
