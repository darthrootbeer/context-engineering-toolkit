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
ASSESSMENT: ARCHIVE/2026-10-01-copperline-example-co-docs-platform-engineer.md

🚦 VERDICT: Apply

🏢 Copperline Example Co. is one you have said you want to work for. Your reason: Makes tools for writers, which is the work Robin cares about most. This did not change the scores or the verdict.

**Scores:**
Fit 9 🟢🟢🟢🟢🟢🟢🟢🟢🟢⬛  
Comp 10 🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟  
Qualifications 9 🟢🟢🟢🟢🟢🟢🟢🟢🟢⬛  
Culture 10 🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟  

| Check | Rating | Read |
|---|---|---|
| ✨ AI-forward team | 🟢 Strong | The team uses AI tools every day for drafting, which is exactly what you want. You would help decide what review rules they need. |
| 📦 Docs live in version control | 🟢 Strong | Docs are stored in Git as Markdown and go through pull request review, which matches your preference for working where review and automation matter. |
| 🧪 Docs are built and checked automatically | 🟠 Weak | Docs are currently built by hand, not automatically. You'd build the automation from scratch, but it doesn't exist yet. |
| 🦸 Owns the docs system | 🟢 Strong | You would own the docs system from day one with just peer review from one engineer. This is the ownership you're looking for. |
| How much say you'd have | 🟢 Strong | You would have wide say in how the docs system works. Your manager checks in weekly and one engineer reviews your work, but you choose tools and set priorities. |

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

[the prompt below, with attached files: assessment/SKILL.md, schema/findings.schema.json, fixtures/robin-sample/career-profile.yaml, fixtures/postings/01-strong-fit.md]

I'm attaching assessment/SKILL.md, schema/findings.schema.json, my career-profile.yaml and one job posting. Assess the posting for the lane named in its lane field, following SKILL.md. Check hard blocks first and stop if one trips. Quote the posting's own words for every rating; if the posting says nothing on a point, rate it Unknown. Only claim a qualification when my file has an evidence entry for it, and name that entry's id. Give the findings as one JSON block that matches schema/findings.schema.json exactly, including the shape of every list item, so I can run assessment/scripts/check_findings.py and scripts/assess_offline.py on it. Do not work out scores or a verdict yourself: the scripts do that, the same way every time. After the JSON, list the two or three judgment calls you were least sure of, each with the posting's words and the other way it could be read. A good answer's JSON passes check_findings.py with no problems, and assess_offline.py then gives the verdict.

### Model

```json
{
  "posting_file": "ARCHIVE/2026-10-01-copperline-example-co-docs-platform-engineer.md",
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
      "read": "The team uses AI tools every day for drafting, which is exactly what you want. You would help decide what review rules they need."
    },
    {
      "id": "docs_as_code",
      "rating": "strong",
      "quote": "all docs live in a Git repository as Markdown and are reviewed in pull requests",
      "read": "Docs are stored in Git as Markdown and go through pull request review, which matches your preference for working where review and automation matter."
    },
    {
      "id": "ci_for_docs",
      "rating": "weak",
      "quote": "The docs build is still run by hand before each release, and we want you to change that.",
      "read": "Docs are currently built by hand, not automatically. You'd build the automation from scratch, but it doesn't exist yet."
    },
    {
      "id": "solo_ownership",
      "rating": "strong",
      "quote": "You will own the documentation system from the first week, with one other engineer to review your work.",
      "read": "You would own the docs system from day one with just peer review from one engineer. This is the ownership you're looking for."
    }
  ],
  "autonomy": {
    "net": "positive",
    "quotes": ["You choose the tools and set the priorities for the docs system; your manager checks in once a week."],
    "read": "You would have wide say in how the docs system works. Your manager checks in weekly and one engineer reviews your work, but you choose tools and set priorities."
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
    "known_gaps_hit": ["gap_go"],
    "self_score_gaps": [],
    "working_style_mismatch": false,
    "matches": [
      {
        "requirement_quote": "Experience generating API reference pages from an OpenAPI file.",
        "evidence_ids": ["ev-northwind-api-rebuild"]
      },
      {
        "requirement_quote": "The docs build is still run by hand before each release, and we want you to change that.",
        "evidence_ids": ["ev-placeholder-ci-checks"]
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
  "verdict_reason": "This is a strong fit. You would own the docs platform from day one with real autonomy, the team already uses AI tools daily, and docs are part of done. The main thing to check is whether reading Go code to follow the build tool is something you want to take on.",
  "keyword_signals_found": [
    {
      "phrase": "definition of done",
      "read": "Documentation is treated as part of finished work for every feature, which means the docs team has real weight."
    }
  ],
  "new_signals_to_consider": []
}
```

---

## Judgment calls least certain about:

1. **CI automation rated "weak"** — The posting says "The docs build is still run by hand before each release, and we want you to change that." I read this as a gap (they don't have automation now), but it could also be read as an opportunity or a "fair" rating: the company clearly values automation, recognizes it matters, and is asking you to build it. The team isn't indifferent; they're asking for the fix.

2. **Go language only appears once, but I weighted it in the verdict** — The requirement is "You can read Go code well enough to follow how our build tool works." This is reading, not writing, and appears only in one sentence. Robin's self_score is 1, which is low. I included it as the main caution in the verdict reason, but one could argue this is overstated (it's just code reading to understand a tool, not writing Go) or understated (the skill gap is real).

3. **Autonomy based on one strong quote** — "You choose the tools and set the priorities for the docs system; your manager checks in once a week" is explicit and clear, but it's a single sentence. The context "with one other engineer to review your work" adds a governance layer that might read as closer to neutral autonomy rather than the strongly positive reading I gave it. However, peer code review is standard practice, not a signal of restricted autonomy.
