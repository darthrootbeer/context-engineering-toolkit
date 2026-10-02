<!-- FICTIONAL EXAMPLE DATA. Not a real person. Saved by tests/prompt-runs/run_prompts.py -->
# Prompt run: Test the scoring with the fixture, on haiku

- Prompt file: `prompts/04-test-scoring.txt`
- Date: 2026-10-01. Model alias `haiku`, which ran as `claude-haiku-4-5-20251001` (Claude Code can add a small helper model call of its own).
- Turns: 1. Cost: $0.06 (the simulated user's calls are not included).
- Grade: see `GRADES.md`.

## Conversation

### User

[the prompt below, with attached files: ARCHITECTURE.md, fixtures/robin-sample/career-profile.yaml, fixtures/postings/01-strong-fit.md, fixtures/postings/02-job-type-override.md, fixtures/postings/03-unlisted-pay-perks.md, fixtures/findings/01-strong-fit.findings.json, fixtures/findings/02-job-type-override.findings.json, fixtures/findings/03-unlisted-pay-perks.findings.json, fixtures/expected.yaml]

I'm attaching ARCHITECTURE.md, fixtures/robin-sample/career-profile.yaml, the three postings in fixtures/postings/ and their files in fixtures/findings/. For each posting, apply the scoring rules by hand to its findings file. Show the arithmetic for Fit, Comp, Qualifications and Culture, round each the way ARCHITECTURE.md says, then apply the verdict rules in order and name the rule that decided it. Only after all three answers are written, open fixtures/expected.yaml, compare, and list every mismatch with the step where your arithmetic and the file disagree. A good answer matches all three verdicts and all twelve scores.

### Model

I'll work through each posting systematically, applying the scoring rules by hand.

---

## Posting 01: strong-fit (docs-platform lane)

**FIT:**
- Start: 10
- ai_forward (strong must-have): strong rating → 0 cost
- docs_as_code (strong must-have): strong rating → 0 cost
- ci_for_docs (soft must-have): weak rating → 1 cost
- solo_ownership (bonus): fair rating → 0 cost (bonuses never cost)
- autonomy: net positive → 0 cost

10 − 1 = **9**

**COMP:**
- Pay stated. Location "Region B" matches tier exactly. Top: $104,000.
- Robin's target: $100,000.
- 104,000 ≥ 100,000 (target) → **10**

**QUALIFICATIONS:**
- Start: 10
- Years: 7 required, 9 have → no cost
- Known gap (go_lang, score 1): 1 cost
- Evidence for docs_as_code and OpenAPI covered.

10 − 1 = **9**

**CULTURE:**
- Start: 5
- unlimited_pto (big): +2
- learning_budget (big): +2
- offsites (nice): +1
- "definition of done" (strong positive phrase): +1
- Total: 5 + 2 + 2 + 1 + 1 = 11 → capped at **10**

**Verdict:** No hard block, 4a doesn't fire, Fit=9>5, Qual=9>5, Comp=10>3, Culture=10>3, average=(9+9)/2=9≥7 → **Apply (4d)**

---

## Posting 02: job-type-override (tech-writing lane)

**FIT:**
- Start: 10
- expert_access (strong): fair rating → 0 cost
- tooling_voice (strong): fair rating → 0 cost
- style_guide (soft): poor rating → 1 cost
- Avoid core skills: video_tutorials (core daily work, next=avoid) → 1 cost; localization_pm (core daily work, next=avoid) → 1 cost. Cap at 2 total.
- autonomy: unknown → 0 cost

10 − 1 − 2 = **7**

**COMP:**
- Pay stated. Location "Region B" not in tiers; pick "Everywhere else" tier. Top: $78,000.
- Robin: floor $75,000, min $80,000.
- 78,000 is between floor and min → **3**

**QUALIFICATIONS:**
- Start: 10
- Years: 12 required, 9 have → 2 cost (too many years)
- Known gaps: dita_xml (score 0) → 1 cost; mobile_sdk (score 0) → 1 cost

10 − 2 − 1 − 1 = **6**

**CULTURE:**
- Start: 5
- No perks, no phrases, no flags, no negatives.

**5**

**Verdict:** No hard block, **4a fires**: video_tutorials is central to daily work ("most of your week") with no evidence → **Skip (4a)**

---

## Posting 03: unlisted-pay-perks (tech-writing lane)

**FIT:**
- Start: 10
- expert_access (strong): weak rating → 1.5 cost
- tooling_voice (strong): unknown rating → 1.5 cost
- style_guide (soft): fair rating → 0 cost
- autonomy: unknown → 0 cost

10 − 1.5 − 1.5 = **7**

**COMP:**
- Pay not listed → **5**

**QUALIFICATIONS:**
- Start: 10
- Years: 11 required, 9 have → 2 cost
- Known gap: mobile_sdk (score 0) → 1 cost
- Self-score gap: kubernetes (score 1) → 1 cost

10 − 2 − 1 − 1 = **6**

**CULTURE:**
- Start: 5
- extra_days_off (big): +2
- learning_budget (big): +2
- "fast-paced" is on Robin's free_phrases list → 0 cost

5 + 2 + 2 = **9**

**Verdict:** No hard block, 4a doesn't fire, Fit=7>5, Qual=6>5, Comp=5>3, Culture=9>3, **but average=(7+6)/2=6.5<7** → **Apply with reservations (4c-average)**

---

## Comparison with expected.yaml

| Posting | Metric | My result | Expected | ✓ |
|---------|--------|-----------|----------|---|
| 01 | Fit | 9 | 9 | ✓ |
| 01 | Comp | 10 | 10 | ✓ |
| 01 | Qual | 9 | 9 | ✓ |
| 01 | Culture | 10 | 10 | ✓ |
| 01 | Verdict | Apply | Apply | ✓ |
| 01 | Trigger | 4d | 4d | ✓ |
| 02 | Fit | 7 | 7 | ✓ |
| 02 | Comp | 3 | 3 | ✓ |
| 02 | Qual | 6 | 6 | ✓ |
| 02 | Culture | 5 | 5 | ✓ |
| 02 | Verdict | Skip | Skip | ✓ |
| 02 | Trigger | 4a | 4a | ✓ |
| 03 | Fit | 7 | 7 | ✓ |
| 03 | Comp | 5 | 5 | ✓ |
| 03 | Qual | 6 | 6 | ✓ |
| 03 | Culture | 9 | 9 | ✓ |
| 03 | Verdict | Apply with reservations | Apply with reservations | ✓ |
| 03 | Trigger | 4c-average | 4c-average | ✓ |

**Perfect match: all 12 scores and 3 verdicts correct.**
