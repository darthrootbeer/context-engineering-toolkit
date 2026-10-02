<!-- FICTIONAL EXAMPLE DATA. Not a real person. Saved by tests/prompt-runs/run_prompts.py -->
# Prompt run: Run on my first posting, on sonnet

Note: the pay figures in this record were changed after the run to fictional ones. Nothing else was edited; the scores and verdicts are as recorded.

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
| ✨ AI-forward team | 🟢 Strong | The team drafts with AI every day. A person still checks the output, and you would help decide those checks. This is what you want. |
| 📦 Docs live in version control | 🟢 Strong | The docs are kept in Git and reviewed like code. A miss here would matter a lot, and this clearly passes. |
| 🧪 Docs are built and checked automatically | 🟡 Fair | The build is not automatic yet, so the checking you like is not in place. They want you to build it, which is work you can do. |
| 🦸 Owns the docs system | 🟢 Strong | You would own the docs system from week one, with one engineer to review your work. This is a bonus and it is clearly there. |
| How much say you'd have | 🟢 Strong | You would pick the tools and set your own priorities, and your manager checks in weekly. That is a lot of say. |

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

I haven't run `check_findings.py` or `assess_offline.py`, and I computed no scores or verdict. No hard block trips: the posting says "We are a remote company with about 60 people," and there is no gambling or weapons content.

```json
{
  "posting_file": "fixtures/postings/01-strong-fit.md",
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
      "read": "The team drafts with AI every day. A person still checks the output, and you would help decide those checks. This is what you want."
    },
    {
      "id": "docs_as_code",
      "rating": "strong",
      "quote": "all docs live in a Git repository as Markdown and are reviewed in pull requests",
      "read": "The docs are kept in Git and reviewed like code. A miss here would matter a lot, and this clearly passes."
    },
    {
      "id": "ci_for_docs",
      "rating": "fair",
      "quote": "The docs build is still run by hand before each release, and we want you to change that.",
      "read": "The build is not automatic yet, so the checking you like is not in place. They want you to build it, which is work you can do."
    },
    {
      "id": "solo_ownership",
      "rating": "strong",
      "quote": "You will own the documentation system from the first week, with one other engineer to review your work.",
      "read": "You would own the docs system from week one, with one engineer to review your work. This is a bonus and it is clearly there."
    }
  ],
  "autonomy": {
    "net": "positive",
    "quotes": [
      "You choose the tools and set the priorities for the docs system; your manager checks in once a week.",
      "You will own the documentation system from the first week"
    ],
    "read": "You would pick the tools and set your own priorities, and your manager checks in weekly. That is a lot of say."
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
        "requirement_quote": "Build and run the system that turns our documentation into a public help site.",
        "evidence_ids": ["ev-placeholder-docs-pipeline"]
      },
      {
        "requirement_quote": "all docs live in a Git repository as Markdown and are reviewed in pull requests",
        "evidence_ids": ["ev-placeholder-docs-pipeline"]
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
  "verdict_reason": "This looks like a strong match. You would own the docs system, choose the tools and work with AI drafting every day. The pay range for your region is listed, and the time off and learning budget are good. The one thing to prepare for is reading Go code, which you have not done in years.",
  "keyword_signals_found": [
    {
      "phrase": "definition of done",
      "read": "Documentation counts as part of finished work for every feature, so docs are not an afterthought here."
    }
  ],
  "new_signals_to_consider": []
}
```

**Judgment calls I was least sure of**

1. **Go as a gap that counts (`known_gaps_hit: ["gap_go"]`).**
   - Posting words: "You can read Go code well enough to follow how our build tool works." It sits under "What we are looking for."
   - I counted it because it is a required line. The other reading is that "well enough to follow" is a light ask, not load-bearing, so it should not count. Dropping it would raise Qualifications. It is named once in a list and not in the duties, so I did not fire the job-type override.

2. **`ci_for_docs` rated `fair`.**
   - Posting words: "The docs build is still run by hand before each release, and we want you to change that."
   - I read this as automatic checking missing today, but wanted in the role. It could instead be `strong`, because the job is to build exactly what you listed and you have evidence for it. It could also be `weak`, because the posting confirms the opposite of the current state.

3. **`working_style_mismatch: false`.**
   - Posting words: "You will own the documentation system from the first week." Your profile says you gather knowledge from experts.
   - I read this as owning a system, not becoming the subject expert on a product. If the posting meant you would be the sole authority on how the platform works, it could be read as a mismatch.

I did not cite `ev-placeholder-ci-checks` or the AI prompt evidence for any match, to avoid stretching the claims. I also left the pay-range benefits term out, because the schema has no field for it.
