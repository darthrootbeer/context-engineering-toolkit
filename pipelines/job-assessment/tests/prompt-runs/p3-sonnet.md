<!-- FICTIONAL EXAMPLE DATA. Not a real person. Saved by tests/prompt-runs/run_prompts.py -->
# Prompt run: Run on my first posting, on sonnet

- Prompt file: `prompts/03-run-first-posting.txt`
- Date: 2026-10-01. Model alias `sonnet`, which ran as `claude-sonnet-5-5` (Claude Code can add a small helper model call of its own).
- Turns: 1. Cost: $0.13 (the simulated user's calls are not included).
- Grade: see `GRADES.md`.

## Checks run by code on the reply

```text
$ python assessment/scripts/check_findings.py <tmp>/findings.json --posting fixtures/postings/01-strong-fit.md --profile fixtures/robin-sample/career-profile.yaml
check_findings: ok
(exit code 0)
```

```text
$ python scripts/assess_offline.py fixtures/postings/01-strong-fit.md --findings <tmp>/findings.json --profile fixtures/robin-sample/career-profile.yaml --out <tmp>/out --date 2026-10-01
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
| ✨ AI-forward team | 🟢 Strong | The team drafts with AI every day and still wants people to check the output. That is the setup you asked for. |
| 📦 Docs live in version control | 🟢 Strong | The docs already live in Git and go through pull request review. This is the way you like to work. |
| 🧪 Docs are built and checked automatically | 🟡 Fair | The build is not automatic today. That is a small miss on a nice-to-have, but the job is to fix it, and you have built checks like this before. |
| 🦸 Owns the docs system | 🟢 Strong | You would own the docs system, with one engineer reviewing. This is a bonus for you, not a requirement. |
| How much say you'd have | 🟢 Strong | You would pick the tools and set your own priorities. Your manager checks in once a week. That is a lot of say. |

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

Hard blocks: none tripped. The posting says "We are a remote company with about 60 people", so the not-remote block does not apply. Copperline makes writing tools, so gambling and weapons don't apply either. I assessed it in the `docs-platform` lane, the one named in its lane field.

I haven't run `check_findings.py` or `assess_offline.py`; that's for you. The `posting_file` path is the one you attached, not an archived note.

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
      "read": "The team drafts with AI every day and still wants people to check the output. That is the setup you asked for."
    },
    {
      "id": "docs_as_code",
      "rating": "strong",
      "quote": "all docs live in a Git repository as Markdown and are reviewed in pull requests",
      "read": "The docs already live in Git and go through pull request review. This is the way you like to work."
    },
    {
      "id": "ci_for_docs",
      "rating": "fair",
      "quote": "The docs build is still run by hand before each release, and we want you to change that.",
      "read": "The build is not automatic today. That is a small miss on a nice-to-have, but the job is to fix it, and you have built checks like this before."
    },
    {
      "id": "solo_ownership",
      "rating": "strong",
      "quote": "You will own the documentation system from the first week, with one other engineer to review your work.",
      "read": "You would own the docs system, with one engineer reviewing. This is a bonus for you, not a requirement."
    }
  ],
  "autonomy": {
    "net": "positive",
    "quotes": [
      "You choose the tools and set the priorities for the docs system; your manager checks in once a week."
    ],
    "read": "You would pick the tools and set your own priorities. Your manager checks in once a week. That is a lot of say."
  },
  "pay": {
    "stated": true,
    "tiers": [
      {
        "label": "Region B",
        "min": 100000,
        "max": 104000,
        "quote": "Base pay range for Region B: $100,000 to $104,000."
      },
      {
        "label": "Region A",
        "min": 102000,
        "max": 118000,
        "quote": "Region A: $102,000 to $118,000."
      }
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
    "unproven": [],
    "matches": [
      {
        "requirement_quote": "Experience generating API reference pages from an OpenAPI file.",
        "evidence_ids": ["ev-northwind-api-rebuild"]
      },
      {
        "requirement_quote": "all docs live in a Git repository as Markdown and are reviewed in pull requests",
        "evidence_ids": ["ev-placeholder-docs-pipeline"]
      },
      {
        "requirement_quote": "The docs build is still run by hand before each release, and we want you to change that.",
        "evidence_ids": ["ev-placeholder-docs-pipeline", "ev-placeholder-ci-checks"]
      },
      {
        "requirement_quote": "Our writers and engineers draft with AI assistants every day",
        "evidence_ids": ["ev-placeholder-style-prompts"]
      }
    ]
  },
  "avoid_core_skills": [],
  "company_read": {
    "status": "high_interest",
    "name": "Copperline Example Co.",
    "stored_reason": "Makes tools for writers, which is the work Robin cares about most."
  },
  "verdict_reason": "You would own the docs system, choose the tools and work with AI drafting every day, at a company that makes tools for writers. Two things still need checking: how well you can read Go, and which pay region applies to you.",
  "keyword_signals_found": [
    {
      "phrase": "definition of done",
      "read": "Documentation counts as part of finished work for every feature, so docs are not an afterthought here."
    }
  ],
  "new_signals_to_consider": []
}
```

## Judgment calls I was least sure of

1. **Go as a known gap.** The posting says: "You can read Go code well enough to follow how our build tool works." I counted it as a required line, so `gap_go` is in `known_gaps_hit`, and I left it out of `self_score_gaps`. It could also be read as a light, read-only ask that is not load-bearing, in which case `known_gaps_hit` would be empty. I did not fire the job-type override. Go appears once, in the requirements list, and never in the duties.

2. **`ci_for_docs` as `fair`.** The posting says: "The docs build is still run by hand before each release, and we want you to change that." I read it as a small miss on a soft item that the job is meant to fix. It could be `strong`, because the role is to build exactly this and you have done it. It could also be `weak`, because the team does not have this today.

3. **Time off left as `null`.** The posting says: "Unlimited paid time off, with a three-week minimum we ask everyone to take." I treated it as a perk, not a stated yearly day count. If you read "three-week minimum" as 15 paid days, `low_time_off` would be `{"days": 15, "quote": "..."}`. That sits exactly on your `low_time_off_days` threshold, so the script would decide whether it counts as low.
