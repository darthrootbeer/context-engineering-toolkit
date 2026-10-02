<!-- FICTIONAL EXAMPLE DATA. Not a real person. Saved by tests/prompt-runs/run_prompts.py -->
# Prompt run: Run on my first posting, on sonnet

Note: the pay figures in this record were changed after the run to fictional ones. Nothing else was edited; the scores and verdicts are as recorded.

- Prompt file: `prompts/03-run-first-posting.txt`
- Date: 2026-10-01. Model alias `sonnet`, which ran as `claude-sonnet-5-5` (Claude Code can add a small helper model call of its own).
- Turns: 1. Cost: $0.17 (the simulated user's calls are not included).
- Grade: see `GRADES.md`.
- Paths and addresses were shortened to labels such as <home>, <tmp> and <repo-url> before saving.

## Checks run by code on the reply

```text
$ python3.11 assessment/scripts/check_findings.py <tmp>/findings.json --posting fixtures/postings/01-strong-fit.md --profile fixtures/robin-sample/career-profile.yaml
Traceback (most recent call last):
  File "<tmp>", line 259, in <module>
    sys.exit(main())
             ^^^^^^
  File "<tmp>", line 248, in main
    problems = check(findings, text, meta.get("lane"), profile)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<tmp>", line 191, in check
    quote_ok(f"culture.{key}[{i}].quote", entry.get("quote"))
                                          ^^^^^^^^^
AttributeError: 'str' object has no attribute 'get'
(exit code 1)
```

```text
$ python3.11 scripts/assess_offline.py fixtures/postings/01-strong-fit.md --findings <tmp>/findings.json --profile fixtures/robin-sample/career-profile.yaml --out <tmp>/out --date 2026-10-01
1/10 validate the profile
2/10 check the findings against the schema
assess_offline: step 'findings schema' stopped the run.
culture/strong_positive_phrases/0: 'definition of done' is not of type 'object'
keyword_signals_found/0: 'definition of done' is not of type 'object'
(exit code 1)
```

## Conversation

### User

[the prompt below, with attached files: assessment/SKILL.md, ARCHITECTURE.md, fixtures/robin-sample/career-profile.yaml, fixtures/postings/01-strong-fit.md]

I'm attaching assessment/SKILL.md, ARCHITECTURE.md, my career-profile.yaml and one job posting. Assess the posting for the lane named in its lane field, following SKILL.md. Check hard blocks first and stop if one trips. Quote the posting's own words for every rating; if the posting says nothing on a point, rate it Unknown. Only claim a qualification when my file has an evidence entry for it, and name that entry's id. First give the findings as one JSON block in the shape SKILL.md step 4 shows, so I can run assessment/scripts/check_findings.py and scripts/assess_offline.py on it. Then give a preview: the four scores worked out with the rules in ARCHITECTURE.md, one line each on what moved them, the verdict (Apply, Apply with reservations or Skip), the rule that decided it, and one plain sentence a friend would understand. Label it a preview, because the scripts' answer is the real one. A good answer's JSON passes check_findings.py with no problems.

### Model

## Findings

No hard block trips. The posting says "We are a remote company", so the non-remote block doesn't apply, and it is not about gambling or weapons.

```json
{
  "posting_file": "fixtures/postings/01-strong-fit.md",
  "lane": "docs-platform",
  "hard_block": {"tripped": false, "id": null, "quote": null, "named_exception": null},
  "job_type_override": {"fired": false, "skill": null, "quotes": [], "evidence_checked": []},
  "requirements": [
    {"id": "ai_forward", "rating": "strong",
     "quote": "Our writers and engineers draft with AI assistants every day",
     "read": "The team drafts with AI every day and you would help decide which checks a person still makes. That is the AI-forward setup you want."},
    {"id": "docs_as_code", "rating": "strong",
     "quote": "all docs live in a Git repository as Markdown and are reviewed in pull requests",
     "read": "The docs live in version control and go through review. That matches the way you already work."},
    {"id": "ci_for_docs", "rating": "fair",
     "quote": "The docs build is still run by hand before each release, and we want you to change that.",
     "read": "The build is not automated yet. This is a small miss on a nice-to-have, and the job is to build it, which you have done before."},
    {"id": "solo_ownership", "rating": "strong",
     "quote": "You will own the documentation system from the first week",
     "read": "You would own the docs system from day one. That is a bonus for you."}
  ],
  "autonomy": {"net": "positive",
               "quotes": ["You choose the tools and set the priorities for the docs system; your manager checks in once a week.",
                          "You will own the documentation system from the first week"],
               "read": "You would pick the tools and set your own priorities, with a weekly check-in from your manager."},
  "pay": {"stated": true, "tier_used": null, "top": null, "other_pay_noted": [],
          "tiers": [
            {"label": "Region B", "min": 100000, "max": 104000,
             "quote": "Base pay range for Region B: $100,000 to $104,000"},
            {"label": "Region A", "min": 102000, "max": 118000,
             "quote": "Region A: $102,000 to $118,000"}]},
  "culture": {"perks": [
                {"perk_id": "unlimited_pto", "quote": "Unlimited paid time off"},
                {"perk_id": "learning_budget", "quote": "A $3,000 yearly learning budget"},
                {"perk_id": "offsites", "quote": "Two team meetups a year"}],
              "strong_positive_phrases": ["definition of done"],
              "low_time_off": null, "hustle": [], "soft_flags_tripped": [], "negative_phrases": []},
  "qualifications": {"years_required": 7, "narrow_subdomain": false,
                     "known_gaps_hit": ["gap_go"],
                     "self_score_gaps": [], "working_style_mismatch": false, "unproven": [],
                     "matches": [
                       {"requirement_quote": "Experience generating API reference pages from an OpenAPI file.",
                        "evidence_ids": ["ev-northwind-api-rebuild"]},
                       {"requirement_quote": "all docs live in a Git repository as Markdown and are reviewed in pull requests",
                        "evidence_ids": ["ev-placeholder-docs-pipeline"]},
                       {"requirement_quote": "The docs build is still run by hand before each release, and we want you to change that.",
                        "evidence_ids": ["ev-placeholder-ci-checks", "ev-placeholder-docs-pipeline"]}]},
  "avoid_core_skills": [],
  "company_read": {"status": "high_interest", "name": "Copperline Example Co.",
                   "stored_reason": "Makes tools for writers, which is the work Robin cares about most."},
  "verdict_reason": "This looks like a great fit: you would own the docs system, pick the tools and work with AI every day, and the pay tops out above your target. The one thing to check is how much Go code you would need to read, since you have little experience with it.",
  "keyword_signals_found": ["definition of done"],
  "new_signals_to_consider": []
}
```

Before you run the scripts:
- **`posting_file`:** I used the fixture path because I haven't archived a note. Swap in the archived note's path if you run `parse_posting.py` first.
- **Phrase fields:** I don't have `findings.schema.json`, so I guessed that `strong_positive_phrases` and `keyword_signals_found` take plain phrase strings. If `check_findings.py` complains, that is where I'd look.
- **`ci_for_docs`:** rating it `fair` rather than `weak` is a judgment call. The scale treats a small miss on a soft item as `fair`, and the job is to build the automation. Under `weak` it would cost 1 Fit point (Fit 9, verdict unchanged).
- **Go:** the Go line is a known gap on a required line, so I listed `gap_go` once and left `self_score_gaps` empty. It appears only in the requirements list, not the duties, so it is not a job-type override.
- **Years:** I cited no evidence for "7+ years". Your 9 years comes from the profile, and the script compares the numbers.

## Preview (the scripts' answer is the real one)

| Score | Arithmetic | Result |
|---|---|---|
| Fit | Start at 10. Strong must-haves `ai_forward` and `docs_as_code` cost 0. Soft `ci_for_docs` rated fair costs 0. Bonus `solo_ownership` costs 0. Autonomy is positive and no avoid-skills are core, so 0. | **10** |
| Comp | Region B tier, top $104,000, which is at or above the $100,000 target. | **10** |
| Qualifications | Start at 10. Asks for 7 years against your 9, so 0. `gap_go` costs 1. No working-style mismatch. | **9** |
| Culture | Start at 5. Unlimited PTO +2, learning budget +2, meetups +1, "definition of done" +1 gives 11, capped at 10. Time off is not low and there is no hustle language. | **10** |

- **Fit:** it is full marks because the posting confirms both strong must-haves and gives you real say over tools and priorities.
- **Comp:** the Region B range tops out above your target.
- **Qualifications:** the only deduction is reading Go, a known gap with no evidence behind it.
- **Culture:** the perks and the "definition of done" language push it past the cap.

**Verdict: Apply.** Rule 5 decided it. No hard block, no job-type override, Fit and Qualifications are above 5, Comp and Culture are above 3, and the Fit and Qualifications average is 9.5, which is not under 7.

**In plain words:** this job lets you own a docs system, pick your tools and work with AI, with pay above your target, and the only real question is whether the bit of Go reading is a problem.

Copperline is on your high-interest list ("Makes tools for writers, which is the work Robin cares about most."). It doesn't change any score. Move quickly, look for a warm introduction, and be upfront about Go.

Skill notes for the block: OpenAPI and docs-as-code are both things you want more of, and your Go is both a known gap and last used 5+ years ago.
