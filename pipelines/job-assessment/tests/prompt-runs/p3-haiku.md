<!-- FICTIONAL EXAMPLE DATA. Not a real person. Saved by tests/prompt-runs/run_prompts.py -->
# Prompt run: Run on my first posting, on haiku

- Prompt file: `prompts/03-run-first-posting.txt`
- Date: 2026-10-01. Model alias `haiku`, which ran as `claude-haiku-4-5-20251001` (Claude Code can add a small helper model call of its own).
- Turns: 1. Cost: $0.10 (the simulated user's calls are not included).
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
| ✨ AI-forward team | 🟢 Strong | The team uses AI to draft every day, and you'd decide what still needs human review. That's the AI-forward setup you want. |
| 📦 Docs live in version control | 🟢 Strong | Docs live in Git as Markdown with PR reviews, exactly your working style. |
| 🧪 Docs are built and checked automatically | 🟡 Fair | Docs build is manual now; they want you to automate it. You'd own that project from the start. |
| 🦸 Owns the docs system | 🟢 Strong | You own the system day one, with one peer reviewer. That's real ownership and autonomy. |
| How much say you'd have | 🟢 Strong | You choose the tools and set your own priorities, with a weekly check-in. That's substantial say in how the work happens. |

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

I'll assess this posting for Robin Sample against the docs-platform lane. Let me work through the checklist.

**Hard blocks:** Copperline is remote ("a remote company"), not gambling, weapons, or excluding locations. No blocks trip.

**Requirements match:**
- `ai_forward` (strong): The posting explicitly puts AI into daily workflow.
- `docs_as_code` (strong): "all docs live in a Git repository as Markdown and are reviewed in pull requests" — core to Robin's method.
- `ci_for_docs` (soft): Currently manual; they want Robin to automate it.
- `solo_ownership` (soft/bonus): Robin owns the system from week one with one peer reviewer.

**Autonomy:** "You choose the tools and set the priorities for the docs system; your manager checks in once a week." The profile's positive signals (chooses tools, sets priorities, weekly manager check-in) all appear. Net: positive.

**Keywords:** "definition of done" hits as strong positive. "Documentation is part of the definition of done for every feature."

**Qualifications:**
- Years required: 7; Robin has 9 total experience.
- Known gaps: "You can read Go code" — Robin scored 1 on Go. This is a lane known gap (`gap_go`).
- Skills: OpenAPI match (ev-northwind-api-rebuild). Docs-as-code match (ev-placeholder-docs-pipeline, ev-placeholder-ci-checks).

**Pay:** Base $100k–$104k for Region B (Robin's location). Matches Robin's target exactly.

**Culture:** Unlimited PTO with 3-week minimum, $3k learning budget, two annual meetups. No hustle language. The company is listed as high-interest in the profile: "Makes tools for writers, which is the work Robin cares about most."

Here's the findings JSON:

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
      "read": "The team uses AI to draft every day, and you'd decide what still needs human review. That's the AI-forward setup you want."
    },
    {
      "id": "docs_as_code",
      "rating": "strong",
      "quote": "Keep docs-as-code habits healthy: all docs live in a Git repository as Markdown and are reviewed in pull requests.",
      "read": "Docs live in Git as Markdown with PR reviews, exactly your working style."
    },
    {
      "id": "ci_for_docs",
      "rating": "fair",
      "quote": "The docs build is still run by hand before each release, and we want you to change that.",
      "read": "Docs build is manual now; they want you to automate it. You'd own that project from the start."
    },
    {
      "id": "solo_ownership",
      "rating": "strong",
      "quote": "You will own the documentation system from the first week, with one other engineer to review your work.",
      "read": "You own the system day one, with one peer reviewer. That's real ownership and autonomy."
    }
  ],
  "autonomy": {
    "net": "positive",
    "quotes": [
      "You choose the tools and set the priorities for the docs system; your manager checks in once a week."
    ],
    "read": "You choose the tools and set your own priorities, with a weekly check-in. That's substantial say in how the work happens."
  },
  "pay": {
    "stated": true,
    "tiers": [
      {
        "label": "Region B",
        "min": 100000,
        "max": 104000,
        "quote": "Base pay range for Region B: $100,000 to $104,000."
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
        "requirement_quote": "Keep docs-as-code habits healthy: all docs live in a Git repository as Markdown and are reviewed in pull requests.",
        "evidence_ids": [
          "ev-placeholder-docs-pipeline",
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
  "verdict_reason": "This is a strong fit. You'd build the docs platform for a company making writer tools, with AI drafting and docs-as-code already standard, real autonomy, and pay at your target. The main question is how deep your Go code reading needs to be.",
  "keyword_signals_found": [
    {
      "phrase": "definition of done",
      "read": "Documentation counts as part of finished work, not extra."
    }
  ],
  "new_signals_to_consider": []
}
```

---

**Judgment calls I'm least sure of:**

1. **CI for docs rated "fair"** — Posting says "The docs build is still run by hand before each release, and we want you to change that." I read this as an opportunity for Robin to own automating the docs build. But it could also be read as: "they haven't invested in CI yet, so this could be a gap they're not actually resourced to fix." The language "we want you to change that" pushed me toward fair (opportunity) rather than weak (unmet gap).

2. **Autonomy as "positive"** — The posting says "your manager checks in once a week." I took this as a sign of autonomy (frequent enough for alignment, infrequent enough for independence) because it matches the profile's positive signal exactly. But "checks in once a week" could mean either real autonomy between check-ins, or just routine oversight. The broader context ("You choose the tools and set the priorities") makes the autonomy reading solid, but that one phrase alone is ambiguous.

3. **Go code in known_gaps_hit, not self_score_gaps** — The posting requires "You can read Go code well enough to follow how our build tool works." Robin's self_score on Go is 1 (minimal). Go is also listed as a known gap for this lane (`gap_go`). I listed it only in `known_gaps_hit` per the instruction to "list it once only." But one could argue it should flag both as a gap and a skills gap separately for visibility.
