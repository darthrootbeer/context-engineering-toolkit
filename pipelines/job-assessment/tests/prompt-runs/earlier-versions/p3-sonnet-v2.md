<!-- FICTIONAL EXAMPLE DATA. Not a real person. Saved by tests/prompt-runs/run_prompts.py -->
# Prompt run: Run on my first posting, on sonnet

Note: the pay figures in this record were changed after the run to fictional ones. Nothing else was edited; the scores and verdicts are as recorded.

- Prompt file: `prompts/03-run-first-posting.txt`
- Date: 2026-10-01. Model alias `sonnet`, which ran as `claude-sonnet-5-5` (Claude Code can add a small helper model call of its own).
- Turns: 1. Cost: $0.18 (the simulated user's calls are not included).
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
| ✨ AI-forward team | 🟢 Strong | The team drafts with AI every day, and people still check the output. That is the setup you want. |
| 📦 Docs live in version control | 🟢 Strong | Docs sit in Git as Markdown and go through pull request review. That matches how you work. |
| 🧪 Docs are built and checked automatically | 🟡 Fair | The build is manual today, so this is not in place yet. Automating it is part of the job, and you have built this kind of check before. |
| 🦸 Owns the docs system | 🟢 Strong | You would own the whole docs system from the start. That is a bonus for you, not a requirement. |
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

[the prompt below, with attached files: assessment/SKILL.md, ARCHITECTURE.md, schema/findings.schema.json, fixtures/robin-sample/career-profile.yaml, fixtures/postings/01-strong-fit.md]

I'm attaching assessment/SKILL.md, ARCHITECTURE.md, schema/findings.schema.json, my career-profile.yaml and one job posting. Assess the posting for the lane named in its lane field, following SKILL.md. Check hard blocks first and stop if one trips. Quote the posting's own words for every rating; if the posting says nothing on a point, rate it Unknown. Only claim a qualification when my file has an evidence entry for it, and name that entry's id. First give the findings as one JSON block that matches schema/findings.schema.json exactly, including the shape of every list item, so I can run assessment/scripts/check_findings.py and scripts/assess_offline.py on it. Then give a preview: the four scores worked out with the rules in ARCHITECTURE.md, one line each on what moved them, the verdict (Apply, Apply with reservations or Skip), the rule that decided it, and one plain sentence a friend would understand. Label it a preview, because the scripts' answer is the real one. A good answer's JSON passes check_findings.py with no problems.

### Model

I couldn't run `check_findings.py` or `assess_offline.py` from here, so none of this is script-verified. The `posting_file` path assumes the fixture location; change it if you archived the note somewhere else.

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
      "read": "The team drafts with AI every day, and people still check the output. That is the setup you want."
    },
    {
      "id": "docs_as_code",
      "rating": "strong",
      "quote": "all docs live in a Git repository as Markdown and are reviewed in pull requests",
      "read": "Docs sit in Git as Markdown and go through pull request review. That matches how you work."
    },
    {
      "id": "ci_for_docs",
      "rating": "fair",
      "quote": "The docs build is still run by hand before each release, and we want you to change that.",
      "read": "The build is manual today, so this is not in place yet. Automating it is part of the job, and you have built this kind of check before."
    },
    {
      "id": "solo_ownership",
      "rating": "strong",
      "quote": "You will own the documentation system from the first week, with one other engineer to review your work.",
      "read": "You would own the whole docs system from the start. That is a bonus for you, not a requirement."
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
    "tier_used": null,
    "top": null,
    "other_pay_noted": [],
    "tiers": [
      {"label": "Region B", "min": 100000, "max": 104000, "quote": "Base pay range for Region B: $100,000 to $104,000."},
      {"label": "Region A", "min": 102000, "max": 118000, "quote": "Region A: $102,000 to $118,000."}
    ]
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
        "requirement_quote": "all docs live in a Git repository as Markdown and are reviewed in pull requests",
        "evidence_ids": ["ev-placeholder-docs-pipeline", "ev-placeholder-ci-checks"]
      },
      {
        "requirement_quote": "The docs build is still run by hand before each release, and we want you to change that.",
        "evidence_ids": ["ev-placeholder-docs-pipeline", "ev-placeholder-ci-checks"]
      },
      {
        "requirement_quote": "Our writers and engineers draft with AI assistants every day, and you will help decide which checks a human must still make.",
        "evidence_ids": ["ev-placeholder-style-prompts"]
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
  "verdict_reason": "You would own the docs system from the first week and choose the tools, with AI drafting and docs kept in Git every day. The pay range reaches $104,000 for your region, and the one thing to check is how much Go code you would need to read.",
  "keyword_signals_found": [
    {
      "phrase": "definition of done",
      "read": "Documentation counts as part of finished work, which is what you look for."
    }
  ],
  "new_signals_to_consider": []
}
```

## Preview (the scripts' answer is the real one)

**Hard blocks:** none tripped. The posting says "We are a remote company with about 60 people", and Copperline makes writing tools, so none of the three blocks applies.

| Score | Result | What moved it |
|---|---|---|
| Fit | **10** | Both strong must-haves are rated strong, so there are no deductions. The soft item (automatic docs checks) is fair and costs 0, the bonus item never costs anything, and autonomy is net positive. No avoid-skills are core work. |
| Comp | **10** | The Region B tier tops out at $104,000, which is above your $100,000 target. |
| Qualifications | **9** | 10 minus 1 for the Go known gap (`gap_go`). The posting asks for 7+ years and you have 9, and there is no working-style mismatch. |
| Culture | **10** | 5, plus 2 for unlimited PTO, 2 for the learning budget, 1 for meetups and 1 for "definition of done". That is 11, capped at 10. |

**Verdict: Apply.** Rule 4d decided it. No hard block, no job-type override and no score floor fired, Comp and Culture are well above 3, and Fit and Qualifications average 9.5, which is not under 7.

**For a friend:** This is a remote job where you would run the docs system yourself, choose the tools and work with AI every day, and the pay is above what you're aiming for.

Judgment calls to check if the scripts disagree:
- **Go gap:** I counted the Go line ("You can read Go code well enough to follow how our build tool works.") as load-bearing, since it sits under "What we are looking for". If you read it as a nice-to-have, Qualifications goes to 10. Apply either way.
- **Automatic checks:** I rated this fair because the gap is the job itself. Rating it weak would cost 1 and make Fit 9, with the same verdict.
- **Unchecked evidence:** The AI-drafting match cites `ev-placeholder-style-prompts`, which is `proof: unchecked`. The note will present it as your own account.
- **Copperline is high interest:** The stored reason is "Makes tools for writers, which is the work Robin cares about most." Move fast and check for a warm introduction. This changes no score.
- **Outside checks:** I did not look up reviews or funding. Whether Copperline pays at the top of its band and how deep the health plan goes are not in the posting, so you'd need to confirm them.
