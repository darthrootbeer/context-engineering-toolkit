<!-- FICTIONAL EXAMPLE DATA. Not a real person. Saved by tests/prompt-runs/run_prompts.py -->
# Prompt run: Run on my first posting, on sonnet

- Prompt file: `prompts/03-run-first-posting.txt`
- Date: 2026-10-01. Model alias `sonnet`, which ran as `claude-sonnet-5-5` (Claude Code can add a small helper model call of its own).
- Turns: 1. Cost: $0.14 (the simulated user's calls are not included).
- Grade: see `GRADES.md`.

## Checks run by code on the reply

```text
$ python3.11 assessment/scripts/check_findings.py <tmp>/findings.json --posting fixtures/postings/01-strong-fit.md --profile fixtures/robin-sample/career-profile.yaml
check_findings: ok
(exit code 0)
```

```text
$ python3.11 scripts/assess_offline.py fixtures/postings/01-strong-fit.md --findings <tmp>/findings.json --profile fixtures/robin-sample/career-profile.yaml --out <tmp>/out --date 2026-10-01
ASSESSMENT: fixtures/postings/01-strong-fit.md

🚦 VERDICT: Apply

🏢 Copperline Example Co. is one you have said you want to work for. Your reason: Makes tools for writers, which is the work Robin cares about most. This did not change the scores or the verdict.

**Scores:**
Fit 10 🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟  
Comp 10 🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟  
Qualifications 9 🟢🟢🟢🟢🟢🟢🟢🟢🟢⬛  
Culture 10 🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟  

| Check | Rating | Read |
|---|---|---|
| ✨ AI-forward team | 🟢 Strong | The team drafts with AI every day, and people still check the result. That is the setup you want. |
| 📦 Docs live in version control | 🟢 Strong | Docs sit in Git and go through review. This matters a lot to you, and the posting says it outright. |
| 🧪 Docs are built and checked automatically | 🟡 Fair | The checks are not automatic yet. Building them would be part of the job, which is work you can do. |
| 🦸 Owns the docs system | 🟢 Strong | You would own the system. This is a bonus for you, not a requirement. |
| How much say you'd have | 🟢 Strong | You would pick the tools and set your own priorities, with a weekly check-in from your manager. |

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

I read the posting directly and ran no scripts, so nothing below has been through `check_findings.py` or `assess_offline.py`. No hard block trips, so the full checklist was read.

```json
{
  "posting_file": "fixtures/postings/01-strong-fit.md",
  "lane": "docs-platform",
  "hard_block": {"tripped": false, "id": null, "quote": null, "named_exception": null},
  "job_type_override": {"fired": false, "skill": null, "quotes": [], "evidence_checked": []},
  "requirements": [
    {
      "id": "ai_forward",
      "rating": "strong",
      "quote": "Our writers and engineers draft with AI assistants every day, and you will help decide which checks a human must still make.",
      "read": "The team drafts with AI every day, and people still check the result. That is the setup you want."
    },
    {
      "id": "docs_as_code",
      "rating": "strong",
      "quote": "all docs live in a Git repository as Markdown and are reviewed in pull requests",
      "read": "Docs sit in Git and go through review. This matters a lot to you, and the posting says it outright."
    },
    {
      "id": "ci_for_docs",
      "rating": "fair",
      "quote": "The docs build is still run by hand before each release, and we want you to change that.",
      "read": "The checks are not automatic yet. Building them would be part of the job, which is work you can do."
    },
    {
      "id": "solo_ownership",
      "rating": "strong",
      "quote": "You will own the documentation system from the first week, with one other engineer to review your work.",
      "read": "You would own the system. This is a bonus for you, not a requirement."
    }
  ],
  "autonomy": {
    "net": "positive",
    "quotes": [
      "You choose the tools and set the priorities for the docs system; your manager checks in once a week.",
      "You will own the documentation system from the first week"
    ],
    "read": "You would pick the tools and set your own priorities, with a weekly check-in from your manager."
  },
  "pay": {
    "stated": true,
    "tiers": [
      {"label": "Region B", "min": 125000, "max": 150000, "quote": "Base pay range for Region B: $125,000 to $150,000."},
      {"label": "Region A", "min": 140000, "max": 170000, "quote": "Region A: $140,000 to $170,000."}
    ],
    "tier_used": null,
    "top": null,
    "other_pay_noted": []
  },
  "culture": {
    "perks": [
      {"perk_id": "unlimited_pto", "quote": "Unlimited paid time off, with a three-week minimum we ask everyone to take."},
      {"perk_id": "learning_budget", "quote": "A $3,000 yearly learning budget."},
      {"perk_id": "offsites", "quote": "Two team meetups a year."}
    ],
    "strong_positive_phrases": [
      {"phrase": "definition of done", "quote": "Documentation is part of the definition of done for every feature."}
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
        "requirement_quote": "Build and run the system that turns our documentation into a public help site.",
        "evidence_ids": ["ev-placeholder-docs-pipeline"]
      },
      {
        "requirement_quote": "all docs live in a Git repository as Markdown and are reviewed in pull requests",
        "evidence_ids": ["ev-placeholder-docs-pipeline"]
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
  "verdict_reason": "You would own the docs system, choose the tools and work with AI drafting every day, in a team that counts docs as part of finished work. The pay range for your region is listed. Reading Go code is the one thing to be ready to talk about.",
  "keyword_signals_found": [
    {"phrase": "definition of done", "read": "Docs count as part of finished work for every feature. That is the strongest sign the team respects documentation."}
  ],
  "new_signals_to_consider": []
}
```

**Judgment calls I was least sure of**

1. **Go as a known gap.** The posting says: "You can read Go code well enough to follow how our build tool works." I counted it as a required line, so `gap_go` is in `known_gaps_hit` and not in `self_score_gaps`. It could be read as a low bar, since it only asks you to follow the code and not write it. Then it would not be load-bearing and `known_gaps_hit` would be empty. Your profile scores Go at 1 with no evidence, so this choice could move the Qualifications score.

2. **Automatic docs checks rated `fair`.** The posting says: "The docs build is still run by hand before each release, and we want you to change that." One reading is `strong`: the team wants exactly what you built in `ev-placeholder-ci-checks`. The other is `weak`: the team does not have the practice today. I picked the middle because this item is soft and the gap is work you can do.

3. **Autonomy read as `positive`.** The posting says: "You choose the tools and set the priorities for the docs system; your manager checks in once a week." It also says "with one other engineer to review your work." The review line could be read as approval on changes, which is one of your negative signals. I read it as ordinary peer review next to a weekly check-in, so I stayed with positive.

**Before you run the checkers**
- `check_findings.py` looks for quotes under the note's "Full posting text" heading. This fixture has no such heading. If you archive it with `parse_posting.py` first, point `posting_file` at the archived note.
- Copperline is on your high-interest list. That affects only the note and what you do next, never a score or the verdict.
