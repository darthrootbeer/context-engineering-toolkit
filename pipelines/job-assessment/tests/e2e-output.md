<!-- FICTIONAL EXAMPLE DATA. Not a real person. Saved by tests/live/test_live_assessment.py -->
# Live run: assessment on the fictional postings

Date: 2026-10-01. Model: `sonnet`. A model followed `assessment/SKILL.md` and wrote its own findings. The test recomputes scores and the verdict with the scripts and does not trust the model's numbers. Tool output is cut to 500 characters. Folder names are replaced with `<work>` and `<tmp>`. One path to a saved tool-output file, which named a home folder, was replaced by hand with `<tool-output-file>` after the run.

## Posting 01-strong-fit

Commands run by the model: 12. Turns: 13. Cost: $0.24.

### Checks

- findings.json written: pass
- exactly one archived note: pass (['🟢 📋 🔧 Copperline Example Co. - Docs Platform Engineer - 2026-10-01.md'])
- email card written: pass
- check_findings.py passes on the model's findings: pass (check_findings: ok)
- verdict matches expected.yaml: pass (got Apply (4d), expected Apply)
- Scores from the model's findings: {'fit': 10, 'comp': 10, 'qualifications': 9, 'culture': 10}. Expected: {'fit': 9, 'comp': 10, 'qualifications': 9, 'culture': 10}. They differ: the model read the posting a little differently. The test requires the verdict, not identical scores.
- note name starts with the verdict dot: pass (🟢 📋 🔧 Copperline Example Co. - Docs Platform Engineer - 2026-10-01.md)

Result: PASS

### Transcript

*Read* `<work>/assessment/SKILL.md`

```text
$ cd <work>; ls -R . | head -50; mkdir -p archive work out
```

```text
1	---
2	name: job-assessment
3	description: >
4	  Go/no-go assessment of one job posting (a link or pasted text) against the
5	  user's own career-profile.yaml. Archives the posting, loads the one lane's
6	  checklist, reads the posting and writes a findings JSON file in which every
7	  rating quotes the posting and every claimed qualification cites an evidence
8	  id. Scripts then check the findings, compute the four scores (Fit, Comp,
9	  Qualifications, Culture), apply the verdict rules, writ
... (27092 more characters)
```

```text
assessment
career-profile.yaml
intake
posting.md
pytest.ini
README.md
requirements.txt
schema
scripts

./assessment:
hooks
README.md
scripts
SKILL.md
templates

./assessment/hooks:
assessment-email-template-guard.sh
README.md

./assessment/scripts:
check_email.py
check_findings.py
load_criteria.py
match_skills.py
parse_posting.py
rename_verdict.py
render_assessment.py
render_email.py
score_helpers.py
verdict.py
write_assessment.py

./assessment/templates:
assessment-email.html

./intake:
README.
... (129 more characters)
```

```text
$ cd <work>; cat posting.md; ls scripts schema; python3 scripts/validate_profile.py career-profile.yaml
```

```text
# FICTIONAL EXAMPLE DATA. Not a real person.

company: Copperline Example Co.
role: Docs Platform Engineer
lane: docs-platform
url: https://example.com/fictional/jobs/copperline-docs-platform
source: board-a

---

# Docs Platform Engineer, Copperline Example Co.

This is an invented job posting used to test a job assessment tool. Copperline Example Co. does not exist.

## About the team

Copperline makes writing tools for software teams. We are a remote company with about 60 people.

## What you
... (1370 more characters)
```

```text
$ cd <work>; python3 assessment/scripts/parse_posting.py posting.md --company "Copperline Example Co." --role "Docs Platform Engineer" --lane docs-platform --archive-dir archive --url "https://example.com/fictional/jobs/copperline-docs-platform" --source board-a
```

```text
POSTING PARSE: Copperline Example Co. / Docs Platform Engineer

POSTING READ
   9 requirements likely real, 1 likely filters

LIKELY REAL: these describe the actual work

   [responsibility] Build and run the system that turns our documentation into a public help site.
      -> Describes the actual work, not a screening filter.

   [responsibility] You will own the documentation system from the first week, with one other engineer to review your work.
      -> Describes the actual work, not a scr
... (1881 more characters)
```

```text
$ cd <work>; N="archive/Copperline Example Co. - Docs Platform Engineer - 2026-10-01.md"; python3 assessment/scripts/load_criteria.py --profile career-profile.yaml --lane docs-platform --posting "$N"; python3 assessment/scripts/match_skills.py "$N" --profile career-profile.yaml
```

```text
CRITERIA SOURCE: career-profile.yaml
LANE: docs-platform  (verified: posting and profile agree)

======================================================================
PERSON (context for Qualifications and Comp)
======================================================================
  years_experience: 9
  working_style: gather_from_experts
  location_label: Region B
  target_roles: Senior Technical Writer, Docs Platform Engineer

=================================================================
... (6111 more characters)
```

```text
$ cd <work>; grep -n -B2 -A14 "^evidence" career-profile.yaml | head -120; grep -n "go_lang\|openapi\|docs_as_code" career-profile.yaml
```

```text
90-  - {id: northwind, name: Northwind Example Co., title: Technical Writer, start: "2017-02", end: "2021-12", summary: "Wrote and maintained the help center and API reference for a small invented software product."}
91-  - {id: placeholder_labs, name: Placeholder Labs, title: Senior Technical Writer, start: "2022-01", summary: "Leads documentation for an invented developer tool and runs the system that builds and checks the docs."}
92:evidence:
93-  - id: ev-northwind-api-rebuild
94-    employe
... (1538 more characters)
```

Status: the posting is archived and the checklist and skill match are done. I'm writing the findings file now, then I'll run the checks, scores, verdict, note, summary and email card.

```text
$ cd <work>; N="archive/Copperline Example Co. - Docs Platform Engineer - 2026-10-01.md"
cat > work/findings.json <<EOF
{
"posting_file": "$N",
"lane": "docs-platform",
"hard_block": {"tripped": false, "id": null, "quote": null, "named_exception": null},
"job_type_override": {"fired": false, "skill": null, "quotes": [], "evidence_checked": []},
"requirements": [
 {"id":"ai_forward","rating":"strong","quote":"Our writers and engineers draft with AI assistants every day, and you will help decide which checks a human must still make.","read":"The team drafts with AI every day and people still check the result. That is the setup you want."},
 {"id":"docs_as_code","rating":"strong","quote":"all docs live in a Git repository as Markdown and are reviewed in pull requests","read":"Docs sit in Git and go through pull request review. This matters a lot to you and it is clearly met."},
 {"id":"ci_for_docs","rating":"fair","quote":"The docs build is still run by hand before each release, and we want you to change that.","read":"Docs are not built and checked automatically yet. The job is to b
... (2484 more characters)
```

```text
Exit code 1
Traceback (most recent call last):
  File "<work>/assessment/scripts/check_findings.py", line 259, in <module>
    sys.exit(main())
             ^^^^^^
  File "<work>/assessment/scripts/check_findings.py", line 248, in main
    problems = check(findings, text, meta.get("lane"),
... (417 more characters)
```

```text
$ cd <work>; python3 - <<'E'
import json
s=json.load(open('schema/findings.schema.json'))
c=s['properties']['culture']['properties']
print(json.dumps(c['strong_positive_phrases']));print(json.dumps(s['properties']['keyword_signals_found']))
E
```

```text
{"$ref": "#/$defs/phrase_quotes"}
{"type": "array", "items": {"type": "object", "required": ["phrase", "read"], "properties": {"phrase": {"type": "string"}, "read": {"type": "string"}}}}
```

```text
$ cd <work>; python3 -c "
import json;s=json.load(open('schema/findings.schema.json'));print(json.dumps(s['\$defs']['phrase_quotes']))"
```

```text
{"type": "array", "items": {"type": "object", "additionalProperties": false, "required": ["phrase", "quote"], "properties": {"phrase": {"type": "string"}, "quote": {"type": "string"}}}}
```

```text
$ cd <work>; N="archive/Copperline Example Co. - Docs Platform Engineer - 2026-10-01.md"
python3 - <<'E'
import json
p='work/findings.json';f=json.load(open(p))
f['culture']['strong_positive_phrases']=[{"phrase":"definition of done","quote":"Documentation is part of the definition of done for every feature."}]
f['keyword_signals_found']=[{"phrase":"definition of done","read":"Documentation counts as part of finished work, which is a strong good sign."}]
json.dump(f,open(p,'w'),indent=1)
E
P=career-profile.yaml
python3 assessment/scripts/check_findings.py work/findings.json --posting "$N" --profile $P && python3 assessment/scripts/score_helpers.py work/findings.json --profile $P --json > work/scores.json && cat work/scores.json && python3 -c "import json,sys; sys.path.insert(0,'assessment/scripts'); import verdict as v; \
s=json.load(open('work/scores.json')); f=json.load(open('work/findings.json')); \
print(json.dumps(v.decide(s['fit'],s['qualifications'],s['comp'],s['culture'], \
override=v.override_skill(f),hard_block=v.hard_block_id(f))))" > work/verdict.json; cat work/verdict.
... (4 more characters)
```

```text
check_findings: ok
{
  "fit": 10,
  "comp": 10,
  "qualifications": 9,
  "culture": 10,
  "why": {
    "fit": [],
    "comp": [
      "Tier used: Region B",
      "Top of range 150000 against target 140000, min 110000, floor 90000"
    ],
    "qualifications": [
      "1 load-bearing gap(s), -1 (cap 4)"
    ],
    "culture": [
      "Perk unlimited_pto (big), +2",
      "Perk learning_budget (big), +2",
      "Perk offsites (nice), +1",
      "1 strong positive phrase(s), +1"
    ]
  }
}
{"label
... (60 more characters)
```

Verdict is Apply, which matches my reason text. Next I'll write the note block, rename the note, and render the summary and card.

```text
$ cd <work>; N="archive/Copperline Example Co. - Docs Platform Engineer - 2026-10-01.md"; P=career-profile.yaml
python3 assessment/scripts/render_assessment.py work/findings.json --scores work/scores.json --verdict work/verdict.json --profile $P > work/block.md
cat >> work/block.md <<'E'

### 🗒️ Notes on your skills
- Go is a stretch: you scored it low and last used it over five years ago, and the posting asks you to read it well enough to follow the build tool.
- OpenAPI and docs as code are things you want more of, and both are core to this job.
- Your OpenAPI work was done by directing AI, so interviews may probe hands-on depth.
E
python3 assessment/scripts/write_assessment.py "$N" --block work/block.md --verdict apply --date 2026-10-01
python3 assessment/scripts/rename_verdict.py "$N" --verdict apply --profile $P
ls archive
```

```text
Assessment written to archive/Copperline Example Co. - Docs Platform Engineer - 2026-10-01.md (state set to apply_ready).
Renamed: archive/🟢 📋 🔧 Copperline Example Co. - Docs Platform Engineer - 2026-10-01.md
🟢 📋 🔧 Copperline Example Co. - Docs Platform Engineer - 2026-10-01.md
```

```text
$ cd <work>; P=career-profile.yaml; R="archive/🟢 📋 🔧 Copperline Example Co. - Docs Platform Engineer - 2026-10-01.md"
python3 assessment/scripts/render_assessment.py work/findings.json --scores work/scores.json --verdict work/verdict.json --profile $P --terminal
echo ----
python3 assessment/scripts/render_email.py --note "$R" --findings work/findings.json --scores work/scores.json --verdict work/verdict.json --profile $P --out out --next-prompt "Copperline Example Co., Docs Platform Engineer: Apply. Fit 10, Comp 10, Qualifications 9, Culture 10. Note: $PWD/$R. Next: check for a warm introduction, then draft the application."
```

```text
ASSESSMENT: archive/Copperline Example Co. - Docs Platform Engineer - 2026-10-01.md

🚦 VERDICT: Apply

🏢 Copperline Example Co. is one you have said you want to work for. Your reason: Makes tools for writers, which is the work Robin cares about most. This did not change the scores or the verdict.

**Scores:**
Fit 10 🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟  
Comp 10 🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟  
Qualifications 9 🟢🟢🟢🟢🟢🟢🟢🟢🟢⬛  
Culture 10 🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟  

| Check | Rating | Read |
|---|---|---|
| ✨ AI-forward team | 🟢 Strong | The team drafts with
... (896 more characters)
```

ASSESSMENT: Copperline Example Co. – Docs Platform Engineer (docs-platform lane)

🚦 **VERDICT: Apply**

🏢 Copperline is one of your high-interest companies. Your reason on file: "Makes tools for writers, which is the work Robin cares about most." This did not change any score or the verdict.

**Scores:**
Fit 10 🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟
Comp 10 🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟
Qualifications 9 🟢🟢🟢🟢🟢🟢🟢🟢🟢⬛
Culture 10 🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟

| Check | Rating | Read |
|---|---|---|
| ✨ AI-forward team | 🟢 Strong | The team drafts with AI every day and people still check the result. That is the setup you want. |
| 📦 Docs live in version control | 🟢 Strong | Docs sit in Git and go through pull request review. This matters a lot to you and it is clearly met. |
| 🧪 Docs are built and checked automatically | 🟡 Fair | Docs are not built and checked automatically yet. The job is to build that, which suits you, but you would start from nothing. |
| 🦸 Owns the docs system | 🟢 Strong | You would own the docs system from week one, with one engineer reviewing your work. |
| How much say you'd have | 🟢 Strong | You would pick the tools and set the priorities. Your manager only checks in weekly, so you would have a lot of say. |

🟢 Strong · 🟡 Fair · 🟠 Weak · 🔴 Poor · ❓ Unknown

📄 Note: [file://…/pipeline/archive/🟢 📋 🔧 Copperline Example Co. - Docs Platform Engineer - 2026-10-01.md](file://<work>/archive/🟢%20📋%20🔧%20Copperline%20Example%20Co.%20-%20Docs%20Platform%20Engineer%20-%202026-10-01.md)
✉️ Email card: `out/copperline-example-co-docs-platform-engineer.html`

The verdict is Apply because no hard block, job-type override, score floor or reservations band fired. The one deduction is reading Go, a known gap for you, so Qualifications is 9. You meet the 7+ years ask with 9 years. Because Copperline is high-interest, move quickly and check for a warm introduction. Interviews may probe hands-on depth on OpenAPI, since that work was done by directing AI.


## Posting 03-unlisted-pay-perks

Commands run by the model: 9. Turns: 10. Cost: $0.22.

### Checks

- findings.json written: pass
- exactly one archived note: pass (['🟡 📋 ✍️ Ashgrove Example Software - Senior Technical Writer - 2026-10-01.md'])
- email card written: pass
- check_findings.py passes on the model's findings: pass (check_findings: ok)
- verdict matches expected.yaml: pass (got Apply with reservations (4c average), expected Apply with reservations)
- Scores from the model's findings: {'fit': 7, 'comp': 5, 'qualifications': 6, 'culture': 9}. Expected: {'fit': 7, 'comp': 5, 'qualifications': 6, 'culture': 9}. Identical.
- note name starts with the verdict dot: pass (🟡 📋 ✍️ Ashgrove Example Software - Senior Technical Writer - 2026-10-01.md)

Result: PASS

### Transcript

```text
$ cd <work>; ls -R . | head -50; cat assessment/SKILL.md; cat posting.md; cat career-profile.yaml
```

```text
<persisted-output>
Output too large (38KB). Full output saved to: <tool-output-file>

Preview (first 2KB):
assessment
career-profile.yaml
intake
posting.md
pytest.ini
README.md
requirements.txt
schema
scripts

./assessment:
hooks
README.md
scripts
SKILL.md
templates

./assessment/hooks:
assessment-e
... (1827 more characters)
```

```text
$ cd <work>; cat assessment/SKILL.md
```

```text
---
name: job-assessment
description: >
  Go/no-go assessment of one job posting (a link or pasted text) against the
  user's own career-profile.yaml. Archives the posting, loads the one lane's
  checklist, reads the posting and writes a findings JSON file in which every
  rating quotes the posting and every claimed qualification cites an evidence
  id. Scripts then check the findings, compute the four scores (Fit, Comp,
  Qualifications, Culture), apply the verdict rules, write the assessment
 
... (25204 more characters)
```

```text
$ cd <work>; cat posting.md; cat career-profile.yaml
```

```text
# FICTIONAL EXAMPLE DATA. Not a real person.

company: Ashgrove Example Software
role: Senior Technical Writer
lane: tech-writing
url: https://example.net/fictional/jobs/ashgrove-senior-writer
source: board-a

---

# Senior Technical Writer, Ashgrove Example Software

This is an invented job posting used to test a job assessment tool. Ashgrove Example Software does not exist.

## About the role

We are a fast-paced team that builds a mobile app and the services behind it. You will work closely w
... (12015 more characters)
```

```text
$ cd <work>; mkdir -p archive work out
python3 scripts/validate_profile.py career-profile.yaml
python3 assessment/scripts/parse_posting.py posting.md --company "Ashgrove Example Software" --role "Senior Technical Writer" --lane tech-writing --archive-dir archive --url "https://example.net/fictional/jobs/ashgrove-senior-writer" --source board-a
ls archive
```

```text
validate_profile: clean, 0 warning(s) in career-profile.yaml
POSTING PARSE: Ashgrove Example Software / Senior Technical Writer

POSTING READ
   6 requirements likely real, 1 likely filters

LIKELY REAL: these describe the actual work

   [responsibility] Write guides and reference pages for developers.
      -> Describes the actual work, not a screening filter.

   [responsibility] Engineers are busy and answer questions when they can.
      -> Describes the actual work, not a screening filter.
... (1176 more characters)
```

```text
$ cd <work>; N="archive/Ashgrove Example Software - Senior Technical Writer - 2026-10-01.md"
python3 assessment/scripts/load_criteria.py --profile career-profile.yaml --lane tech-writing --posting "$N" | head -60
python3 assessment/scripts/match_skills.py "$N" --profile career-profile.yaml
```

```text
CRITERIA SOURCE: career-profile.yaml
LANE: tech-writing  (verified: posting and profile agree)

======================================================================
PERSON (context for Qualifications and Comp)
======================================================================
  years_experience: 9
  working_style: gather_from_experts
  location_label: Region B
  target_roles: Senior Technical Writer, Docs Platform Engineer

==================================================================
... (3043 more characters)
```

```text
$ cd <work>; N="archive/Ashgrove Example Software - Senior Technical Writer - 2026-10-01.md"
cat > work/findings.json <<EOF
{
  "posting_file": "$N",
  "lane": "tech-writing",
  "hard_block": {"tripped": false, "id": null, "quote": null, "named_exception": null},
  "job_type_override": {"fired": false, "skill": null, "quotes": [], "evidence_checked": []},
  "requirements": [
    {"id": "expert_access", "rating": "weak", "quote": "Engineers are busy and answer questions when they can.", "read": "This matters a lot to you. The posting says engineers are busy and answer when they can, so access to experts is not regular. A miss here is close to a dealbreaker for how you work."},
    {"id": "tooling_voice", "rating": "unknown", "quote": null, "read": "The posting says nothing about who chooses the authoring tools. You would have to ask."},
    {"id": "style_guide", "rating": "strong", "quote": "We keep a short style guide in our wiki.", "read": "A written style guide exists. It is short, but it is there."}
  ],
  "autonomy": {"net": "unknown", "quotes": [], "read": "The postin
... (1641 more characters)
```

```text
check_findings: ok
```

Findings pass the check; now running scores and verdict.

```text
$ cd <work>
python3 assessment/scripts/score_helpers.py work/findings.json --profile career-profile.yaml --json > work/scores.json
python3 -c "import json,sys; sys.path.insert(0,'assessment/scripts'); import verdict as v; \
s=json.load(open('work/scores.json')); f=json.load(open('work/findings.json')); \
print(json.dumps(v.decide(s['fit'],s['qualifications'],s['comp'],s['culture'], \
override=v.override_skill(f),hard_block=v.hard_block_id(f))))" > work/verdict.json
cat work/scores.json work/verdict.json
```

```text
{
  "fit": 7,
  "comp": 5,
  "qualifications": 6,
  "culture": 9,
  "why": {
    "fit": [
      "🧑‍🔬 Regular access to experts: weak, -1.5",
      "🛠️ A say in the authoring tools: unknown, -1.5"
    ],
    "comp": [
      "Pay is not listed, neutral 5"
    ],
    "qualifications": [
      "Asks for more years than the person has, -2",
      "2 load-bearing gap(s), -2 (cap 4)"
    ],
    "culture": [
      "Perk extra_days_off (big), +2",
      "Perk learning_budget (big), +2"
    ]
  }
}
{"labe
... (106 more characters)
```

```text
$ cd <work>; N="archive/Ashgrove Example Software - Senior Technical Writer - 2026-10-01.md"
python3 assessment/scripts/render_assessment.py work/findings.json --scores work/scores.json --verdict work/verdict.json --profile career-profile.yaml > work/block.md
cat >> work/block.md <<'EOF'

### 🗒️ Notes on your skills
- OpenAPI / Swagger is something you want more of, and it is a named requirement here.
- Kubernetes is a stretch. The posting only asks for "comfortable with concepts", and you have no proof of it yet.
- Mobile SDK documentation is a gap. The posting lists it as a duty, and you have not done it.
EOF
python3 assessment/scripts/write_assessment.py "$N" --block work/block.md --verdict reservations --date 2026-10-01
python3 assessment/scripts/rename_verdict.py "$N" --verdict reservations --profile career-profile.yaml
```

```text
Assessment written to archive/Ashgrove Example Software - Senior Technical Writer - 2026-10-01.md (state set to apply_ready).
Renamed: archive/🟡 📋 ✍️ Ashgrove Example Software - Senior Technical Writer - 2026-10-01.md
```

```text
$ cd <work>
python3 assessment/scripts/render_assessment.py work/findings.json --scores work/scores.json --verdict work/verdict.json --profile career-profile.yaml --terminal
python3 assessment/scripts/render_email.py --note "archive/🟡 📋 ✍️ Ashgrove Example Software - Senior Technical Writer - 2026-10-01.md" --findings work/findings.json --scores work/scores.json --verdict work/verdict.json --profile career-profile.yaml --out out --next-prompt "Ashgrove Example Software, Senior Technical Writer: Apply with reservations. Fit 7, Comp 5, Qualifications 6, Culture 9. Note: archive/🟡 📋 ✍️ Ashgrove Example Software - Senior Technical Writer - 2026-10-01.md. Next: if you apply, ask about pay, expert access and the mobile SDK work."
```

```text
ASSESSMENT: archive/Ashgrove Example Software - Senior Technical Writer - 2026-10-01.md

🚦 VERDICT: Apply with reservations

🏢 Ashgrove Example Software is a good company, not a dream one. Your reason: Solid product and a fair size, but nothing Robin would move for. This did not change the scores or the verdict.

**Scores:**
Fit 7 🟢🟢🟢🟢🟢🟢🟢⬛⬛⬛  
Comp 5 🟡🟡🟡🟡🟡⬛⬛⬛⬛⬛  
Qualifications 6 🟡🟡🟡🟡🟡🟡⬛⬛⬛⬛  
Culture 9 🟢🟢🟢🟢🟢🟢🟢🟢🟢⬛  

| Check | Rating | Read |
|---|---|---|
| 🧑‍🔬 Regular access to experts | 🟠 Weak
... (779 more characters)
```

ASSESSMENT: Ashgrove Example Software, Senior Technical Writer (tech-writing lane)

🚦 **VERDICT: Apply with reservations** 🟡

**Scores:**
Fit 7 🟢🟢🟢🟢🟢🟢🟢⬛⬛⬛
Comp 5 🟡🟡🟡🟡🟡⬛⬛⬛⬛⬛
Qualifications 6 🟡🟡🟡🟡🟡🟡⬛⬛⬛⬛
Culture 9 🟢🟢🟢🟢🟢🟢🟢🟢🟢⬛

| Check | Rating | Read |
|---|---|---|
| 🧑‍🔬 Regular access to experts | 🟠 Weak | Engineers "answer questions when they can", so access is not regular. This matters a lot for how you work. |
| 🛠️ A say in the authoring tools | ❓ Unknown | The posting doesn't say. |
| 📖 A written style guide | 🟢 Strong | A short style guide exists. |
| How much say you'd have | ❓ Unknown | Only generic teamwork phrases, so it's unclear. |

🟢 Strong · 🟡 Fair · 🟠 Weak · 🔴 Poor · ❓ Unknown

Note: [file://<work>/archive/🟡 📋 ✍️ Ashgrove Example Software - Senior Technical Writer - 2026-10-01.md](file://<work>/archive/🟡%20📋%20✍️%20Ashgrove%20Example%20Software%20-%20Senior%20Technical%20Writer%20-%202026-10-01.md)
Email card: `out/ashgrove-example-software-senior-technical-writer.html`. Its subject starts with 🟡.

**Why this verdict:** Fit and Qualifications average under 7, which puts it in the reservations band. No hard block or job-type override applied. Ashgrove is a "good, not dream" company, and that did not affect the scores.

**What to act on:**
- **Pay:** none is listed, so Comp is a neutral 5. Ask early.
- **Qualifications:** the posting asks for 11 years and you have 9, which is mostly a filter number. Mobile SDK documentation is a known gap, and Kubernetes has no proof behind it. Your OpenAPI work is backed by evidence.
- **Culture:** five extra paid days off and a learning budget score well.
- **Not checked:** I did no outside research, such as reviews or funding.

I treated the mobile SDK duty and the Kubernetes line as load-bearing, which is a judgment call. I dropped one false skill match: "Interviewing experts" matched on "assessment tool".

