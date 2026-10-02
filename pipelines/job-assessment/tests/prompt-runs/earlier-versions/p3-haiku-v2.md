<!-- FICTIONAL EXAMPLE DATA. Not a real person. Saved by tests/prompt-runs/run_prompts.py -->
# Prompt run: Run on my first posting, on haiku

- Prompt file: `prompts/03-run-first-posting.txt`
- Date: 2026-10-01. Model alias `haiku`, which ran as `claude-haiku-4-5-20251001` (Claude Code can add a small helper model call of its own).
- Turns: 1. Cost: $0.10 (the simulated user's calls are not included).
- Grade: see `GRADES.md`.

## Checks run by code on the reply

```text
$ python3.11 assessment/scripts/check_findings.py <tmp>/findings.json --posting fixtures/postings/01-strong-fit.md --profile fixtures/robin-sample/career-profile.yaml
check_findings: ok
(exit code 0)
```

```text
$ python3.11 scripts/assess_offline.py fixtures/postings/01-strong-fit.md --findings <tmp>/findings.json --profile fixtures/robin-sample/career-profile.yaml --out <tmp>/out --date 2026-10-01
ASSESSMENT: ARCHIVE/01-strong-fit.md

🚦 VERDICT: Apply

🏢 Copperline Example Co. is one you have said you want to work for. Your reason: Makes tools for writers, which is the work Robin cares about most. This did not change the scores or the verdict.

**Scores:**
Fit 10 🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟  
Comp 10 🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟  
Qualifications 9 🟢🟢🟢🟢🟢🟢🟢🟢🟢⬛  
Culture 10 🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟  

| Check | Rating | Read |
|---|---|---|
| ✨ AI-forward team | 🟢 Strong | The team uses AI tools for drafting every day, which matches what you're looking for. |
| 📦 Docs live in version control | 🟢 Strong | Docs live in version control with pull-request review, which is your baseline. |
| 🧪 Docs are built and checked automatically | 🟢 Strong | They need someone to build automated docs builds from scratch—exactly what you've already done at Placeholder Labs. |
| 🦸 Owns the docs system | 🟢 Strong | You get solo ownership with light review, which is the bonus you want. |
| How much say you'd have | 🟢 Strong | You would decide how the docs system works and its priorities, with your manager checking in weekly rather than daily. |

🟢 Strong · 🟡 Fair · 🟠 Weak · 🔴 Poor · ❓ Unknown
1/10 validate the profile
2/10 check the findings against the schema
3/10 parse and archive the posting
4/10 load the lane and check the posting's lane matches
5/10 check every quote and id in the findings
6/10 score and decide
7/10 render the assessment block and write it into the note
8/10 rename the note with its verdict emoji
9/10 render the terminal summary
10/10 render the email card
Verdict: Apply (trigger 4d)
Saved note: <tmp>/out/archive/🟢 📋 🔧 Copperline Example Co. - Docs Platform Engineer - 2026-10-01.md
wrote <tmp>/out/email/copperline-example-co-docs-platform-engineer.html
subject: 🟢 Job Assessment: Copperline Example Co. - Docs Platform Engineer - 2026-10-01
(exit code 0)
```

## Conversation

### User

[the prompt below, with attached files: assessment/SKILL.md, ARCHITECTURE.md, schema/findings.schema.json, fixtures/robin-sample/career-profile.yaml, fixtures/postings/01-strong-fit.md]

I'm attaching assessment/SKILL.md, ARCHITECTURE.md, schema/findings.schema.json, my career-profile.yaml and one job posting. Assess the posting for the lane named in its lane field, following SKILL.md. Check hard blocks first and stop if one trips. Quote the posting's own words for every rating; if the posting says nothing on a point, rate it Unknown. Only claim a qualification when my file has an evidence entry for it, and name that entry's id. First give the findings as one JSON block that matches schema/findings.schema.json exactly, including the shape of every list item, so I can run assessment/scripts/check_findings.py and scripts/assess_offline.py on it. Then give a preview: the four scores worked out with the rules in ARCHITECTURE.md, one line each on what moved them, the verdict (Apply, Apply with reservations or Skip), the rule that decided it, and one plain sentence a friend would understand. Label it a preview, because the scripts' answer is the real one. A good answer's JSON passes check_findings.py with no problems.

### Model

I'll assess this posting for the **docs-platform** lane against Robin Sample's career profile.

**Checking hard blocks first:** The posting is from Copperline Example Co., a remote role. No hard blocks are tripped (not gambling, weapons, or a named exception to the remote requirement).

Now I'll read the posting systematically and write the findings.

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
      "read": "The team uses AI tools for drafting every day, which matches what you're looking for."
    },
    {
      "id": "docs_as_code",
      "rating": "strong",
      "quote": "all docs live in a Git repository as Markdown and are reviewed in pull requests",
      "read": "Docs live in version control with pull-request review, which is your baseline."
    },
    {
      "id": "ci_for_docs",
      "rating": "strong",
      "quote": "The docs build is still run by hand before each release, and we want you to change that.",
      "read": "They need someone to build automated docs builds from scratch—exactly what you've already done at Placeholder Labs."
    },
    {
      "id": "solo_ownership",
      "rating": "strong",
      "quote": "You will own the documentation system from the first week, with one other engineer to review your work.",
      "read": "You get solo ownership with light review, which is the bonus you want."
    }
  ],
  "autonomy": {
    "net": "positive",
    "quotes": [
      "You choose the tools and set the priorities for the docs system",
      "your manager checks in once a week"
    ],
    "read": "You would decide how the docs system works and its priorities, with your manager checking in weekly rather than daily."
  },
  "pay": {
    "stated": true,
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
    ],
    "tier_used": null,
    "top": null,
    "other_pay_noted": []
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
      {
        "phrase": "definition of done",
        "quote": "Documentation is part of the definition of done for every feature."
      }
    ],
    "low_time_off": null,
    "hustle": [],
    "soft_flags_tripped": [],
    "negative_phrases": []
  },
  "qualifications": {
    "years_required": 7,
    "narrow_subdomain": false,
    "known_gaps_hit": [
      "gap_go"
    ],
    "self_score_gaps": [],
    "working_style_mismatch": false,
    "matches": [
      {
        "requirement_quote": "Experience generating API reference pages from an OpenAPI file.",
        "evidence_ids": [
          "ev-northwind-api-rebuild"
        ]
      },
      {
        "requirement_quote": "all docs live in a Git repository as Markdown and are reviewed in pull requests",
        "evidence_ids": [
          "ev-placeholder-docs-pipeline"
        ]
      },
      {
        "requirement_quote": "The docs build is still run by hand before each release, and we want you to change that.",
        "evidence_ids": [
          "ev-placeholder-ci-checks"
        ]
      }
    ],
    "unproven": []
  },
  "avoid_core_skills": [],
  "company_read": {
    "status": "high_interest",
    "name": "Copperline Example Co.",
    "stored_reason": "Makes tools for writers, which is the work Robin cares about most."
  },
  "verdict_reason": "This is a great fit for what you're looking for. You would own the docs platform end-to-end, work with AI tools every day, and build exactly the automation system you've already done at Placeholder. Your one real gap is reading Go, but that's not core daily work and is something you can pick up on the job.",
  "keyword_signals_found": [
    {
      "phrase": "definition of done",
      "read": "Documentation is counted as part of finished work, which means the docs platform role is core to the engineering team, not a service function."
    }
  ],
  "new_signals_to_consider": []
}
```

---

## Preview

**Fit: 10** – All four must-haves (AI-forward, docs-as-code, CI automation, ownership) rate strong or better; you'd have real autonomy over tools and priorities.

**Comp: 8** – Region B tops out at $150,000, above your minimum ($110,000) but below your target ($140,000).

**Qualifications: 9** – You exceed the 7 years required, your API docs work matches the OpenAPI requirement (ev-northwind-api-rebuild), your CI pipeline matches the build automation they need (ev-placeholder-ci-checks), and your docs-as-code pipeline matches their current setup (ev-placeholder-docs-pipeline). Only gap: reading Go code is self-score 1, not load-bearing for daily work.

**Culture: 10** – Three strong perks (unlimited PTO, learning budget, team meetups), plus documentation is explicitly in the definition of done for every feature, making you a first-class engineer.

**Verdict: Apply** (rule 5 – no hard blocks, scores above floors, no reservations band triggered)

**One sentence:** You'd own the exact docs automation system you've built before, at a company that makes tools for writers—this is your kind of work.
