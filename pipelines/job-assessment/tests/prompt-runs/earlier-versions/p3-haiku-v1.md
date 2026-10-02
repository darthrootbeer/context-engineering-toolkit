<!-- FICTIONAL EXAMPLE DATA. Not a real person. Saved by tests/prompt-runs/run_prompts.py -->
# Prompt run: Run on my first posting, on haiku

- Prompt file: `prompts/03-run-first-posting.txt`
- Date: 2026-10-01. Model alias `haiku`, which ran as `claude-haiku-4-5-20251001` (Claude Code can add a small helper model call of its own).
- Turns: 1. Cost: $0.12 (the simulated user's calls are not included).
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
culture/strong_positive_phrases/0: 'Documentation is part of the definition of done for every feature.' is not of type 'object'
keyword_signals_found/0: 'read' is a required property
(exit code 1)
```

## Conversation

### User

[the prompt below, with attached files: assessment/SKILL.md, ARCHITECTURE.md, fixtures/robin-sample/career-profile.yaml, fixtures/postings/01-strong-fit.md]

I'm attaching assessment/SKILL.md, ARCHITECTURE.md, my career-profile.yaml and one job posting. Assess the posting for the lane named in its lane field, following SKILL.md. Check hard blocks first and stop if one trips. Quote the posting's own words for every rating; if the posting says nothing on a point, rate it Unknown. Only claim a qualification when my file has an evidence entry for it, and name that entry's id. First give the findings as one JSON block in the shape SKILL.md step 4 shows, so I can run assessment/scripts/check_findings.py and scripts/assess_offline.py on it. Then give a preview: the four scores worked out with the rules in ARCHITECTURE.md, one line each on what moved them, the verdict (Apply, Apply with reservations or Skip), the rule that decided it, and one plain sentence a friend would understand. Label it a preview, because the scripts' answer is the real one. A good answer's JSON passes check_findings.py with no problems.

### Model

I'll assess this posting for Robin Sample against the docs-platform lane. Let me work through SKILL.md systematically.

## Hard blocks check
- Gambling/betting: no
- Weapons manufacturing: no
- Not remote: The posting says "We are a remote company" — no block

Proceeding with the full read.

---

## Findings JSON

```json
{
  "posting_file": "ARCHIVE/01-strong-fit.md",
  "lane": "docs-platform",
  "hard_block": {
    "tripped": false,
    "id": null,
    "quote": null,
    "named_exception": null
  },
  "job_type_override": {
    "fired": false,
    "skill": null,
    "quotes": [],
    "evidence_checked": []
  },
  "requirements": [
    {
      "id": "ai_forward",
      "rating": "strong",
      "quote": "Our writers and engineers draft with AI assistants every day, and you will help decide which checks a human must still make.",
      "read": "The team drafts with AI every day and you'd decide what still needs human review. That's exactly what you want."
    },
    {
      "id": "docs_as_code",
      "rating": "strong",
      "quote": "Keep docs-as-code habits healthy: all docs live in a Git repository as Markdown and are reviewed in pull requests.",
      "read": "Docs live in Git and go through pull-request review. This is your core way of working."
    },
    {
      "id": "ci_for_docs",
      "rating": "fair",
      "quote": "The docs build is still run by hand before each release, and we want you to change that.",
      "read": "They want you to automate the docs build. It's not there yet, but you could build it."
    },
    {
      "id": "solo_ownership",
      "rating": "strong",
      "quote": "You will own the documentation system from the first week, with one other engineer to review your work.",
      "read": "You'd own the platform end-to-end from the start, with a peer reviewer. Ownership is what you're looking for."
    }
  ],
  "autonomy": {
    "net": "positive",
    "quotes": [
      "You choose the tools and set the priorities for the docs system; your manager checks in once a week."
    ],
    "read": "You decide which tools to use and what to build next. Your manager checks in weekly, not daily."
  },
  "pay": {
    "stated": true,
    "tier_used": null,
    "top": null,
    "other_pay_noted": [],
    "tiers": [
      {
        "label": "Region B",
        "min": 125000,
        "max": 150000,
        "quote": "Base pay range for Region B: $125,000 to $150,000."
      },
      {
        "label": "Region A",
        "min": 140000,
        "max": 170000,
        "quote": "Region A: $140,000 to $170,000."
      }
    ]
  },
  "culture": {
    "perks": [
      {
        "perk_id": "unlimited_pto",
        "quote": "Unlimited paid time off, with a three-week minimum we ask everyone to take."
      },
      {
        "perk_id": "learning_budget",
        "quote": "A $3,000 yearly learning budget."
      },
      {
        "perk_id": "offsites",
        "quote": "Two team meetups a year."
      }
    ],
    "strong_positive_phrases": [
      "Documentation is part of the definition of done for every feature."
    ],
    "low_time_off": null,
    "hustle": [],
    "soft_flags_tripped": [],
    "negative_phrases": []
  },
  "qualifications": {
    "years_required": 7,
    "narrow_subdomain": false,
    "known_gaps_hit": ["gap_go"],
    "self_score_gaps": [],
    "working_style_mismatch": false,
    "unproven": [],
    "matches": [
      {
        "requirement_quote": "Experience generating API reference pages from an OpenAPI file.",
        "evidence_ids": ["ev-northwind-api-rebuild"]
      },
      {
        "requirement_quote": "Keep docs-as-code habits healthy: all docs live in a Git repository as Markdown and are reviewed in pull requests.",
        "evidence_ids": ["ev-placeholder-docs-pipeline", "ev-placeholder-ci-checks"]
      }
    ]
  },
  "avoid_core_skills": [],
  "company_read": {
    "status": "high_interest",
    "name": "Copperline Example Co.",
    "stored_reason": "Makes tools for writers, which is the work Robin cares about most."
  },
  "verdict_reason": "This is a strong fit. You'd own the docs platform end-to-end, the team uses AI for drafting daily like you want, and all docs go through pull-request review. You have the OpenAPI experience. The main thing to confirm is whether you can read Go code well enough to follow how their build tool works.",
  "keyword_signals_found": [
    {
      "phrase": "definition of done",
      "quote": "Documentation is part of the definition of done for every feature.",
      "type": "strong_positive"
    }
  ],
  "new_signals_to_consider": []
}
```

---

## Preview of scores and verdict

**Fit: 10** — All four requirements rated strong or better; autonomy reads positive; no avoidance conflicts.

**Comp: 8** — Region B top pay ($150k) falls between your open ask (125k) and target (140k), per the scoring rules.

**Qualifications: 9** — You have 9 years against their 7-year ask; OpenAPI and docs-as-code are backed. Go is a known gap for this lane; costs 1 point.

**Culture: 10** — Three perks (unlimited PTO, learning budget, offsites); "definition of done" is a strong positive signal. No hustle language, no soft flags.

**Verdict: Apply** — Hard block rule doesn't fire. Job-type override doesn't fire (Go is a known gap, not a missing skill with zero evidence). Fit (10) and Qualifications (9) are both above 5. Comp (8) and Culture (10) are both above 3. All paths to rejection fail.

**Decision rule: Default rule 5 (Apply)** — Nothing above it fired.

**In plain terms:** This is a clean fit. You'd own the platform, the team already works the way you want to work (AI daily, docs in Git, pull-request review), and it's a company you care about. Go is the one thing to confirm before the interview.
