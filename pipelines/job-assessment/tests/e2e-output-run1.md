<!-- FICTIONAL EXAMPLE DATA. Not a real person. Saved by tests/live/test_live_assessment.py -->
# Live run, first attempt (posting 03 FAILED, kept as evidence of model variance)

Note: the pay figures in this record were changed after the run to fictional ones. Nothing else was edited; the scores and verdicts are as recorded.

The second attempt, which passed, is in `e2e-output.md`. Nothing was changed between the two runs.

Date: 2026-10-01. Model: `sonnet`. A model followed `assessment/SKILL.md` and wrote its own findings. The test recomputes scores and the verdict with the scripts and does not trust the model's numbers. Tool output is cut to 500 characters. Folder names are replaced with `<work>` and `<tmp>`.

## Posting 01-strong-fit

Commands run by the model: 11. Turns: 12. Cost: $0.25.

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
$ cd <work>; ls -R . | head -50; cat posting.md; cat career-profile.yaml
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
... (13077 more characters)
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
$ cd <work>; mkdir -p archive work out
python3 assessment/../scripts/validate_profile.py career-profile.yaml 2>&1 | tail -5; ls scripts
python3 assessment/scripts/parse_posting.py posting.md --company "Copperline Example Co." --role "Docs Platform Engineer" --lane docs-platform --archive-dir archive --url "https://example.com/fictional/jobs/copperline-docs-platform" --source board-a
```

```text
validate_profile: clean, 0 warning(s) in career-profile.yaml
add_entry.py
assess_offline.py
validate_profile.py
POSTING PARSE: Copperline Example Co. / Docs Platform Engineer

POSTING READ
   9 requirements likely real, 1 likely filters

LIKELY REAL: these describe the actual work

   [responsibility] Build and run the system that turns our documentation into a public help site.
      -> Describes the actual work, not a screening filter.

   [responsibility] You will own the documentation system
... (1993 more characters)
```

```text
$ cd <work>; N="archive/Copperline Example Co. - Docs Platform Engineer - 2026-10-01.md"
python3 assessment/scripts/load_criteria.py --profile career-profile.yaml --lane docs-platform --posting "$N" | tail -40
python3 assessment/scripts/match_skills.py "$N" --profile career-profile.yaml
```

```text
perks (big = +2, nice = +1):
    [unlimited_pto] Unlimited PTO (big)
    [learning_budget] Learning budget (big)
    [extra_days_off] Extra paid days off (big)
    [offsites] Regular meetups or offsites (nice)
    [home_office] Home-office or wellness stipend (nice)
    [parental_leave] Paid parental leave (nice)
  low time off: below 15 days a year
  hustle phrases: rockstar, work hard play hard, on-call, weekend work
  free phrases (read, cost nothing): fast-paced

============================
... (2340 more characters)
```

```text
$ cd <work>; N="archive/Copperline Example Co. - Docs Platform Engineer - 2026-10-01.md"
cat > work/findings.json <<EOF
{
"posting_file": "$N",
"lane": "docs-platform",
"hard_block": {"tripped": false, "id": null, "quote": null, "named_exception": null},
"job_type_override": {"fired": false, "skill": null, "quotes": [], "evidence_checked": []},
"requirements": [
 {"id":"ai_forward","rating":"strong","quote":"Our writers and engineers draft with AI assistants every day, and you will help decide which checks a human must still make.","read":"The team drafts with AI every day and people still check the work. That is what you want."},
 {"id":"docs_as_code","rating":"strong","quote":"all docs live in a Git repository as Markdown and are reviewed in pull requests","read":"Docs are in Git and reviewed in pull requests. This matches your best work."},
 {"id":"ci_for_docs","rating":"fair","quote":"The docs build is still run by hand before each release, and we want you to change that.","read":"Builds are not automatic today, but you would be the one to fix that. You have built automatic ch
... (2284 more characters)
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
$ cd <work>; grep -n -B2 -A12 "strong_positive_phrases\|keyword_signals_found" schema/findings.schema.json | head -70
```

```text
9-    "posting_file", "lane", "hard_block", "job_type_override", "requirements", "autonomy",
10-    "pay", "culture", "qualifications", "avoid_core_skills", "company_read",
11:    "verdict_reason", "keyword_signals_found", "new_signals_to_consider"
12-  ],
13-  "properties": {
14-    "_banner": {"type": "string", "description": "Fixture files only: the FICTIONAL banner, as the first key."},
15-    "posting_file": {"type": "string", "minLength": 1},
16-    "lane": {"type": "string", "minLength": 
... (1702 more characters)
```

```text
$ cd <work>; grep -n -A8 '"phrase_quotes"' schema/findings.schema.json
```

```text
207:    "phrase_quotes": {
208-      "type": "array",
209-      "items": {
210-        "type": "object",
211-        "additionalProperties": false,
212-        "required": ["phrase", "quote"],
213-        "properties": {"phrase": {"type": "string"}, "quote": {"type": "string"}}
214-      }
215-    }
```

Fixing the findings file's phrase format (the schema wants objects, and keyword signals need a `read`), then re-checking.

```text
$ cd <work>; N="archive/Copperline Example Co. - Docs Platform Engineer - 2026-10-01.md"
python3 - <<'EOF'
import json
p='work/findings.json'; f=json.load(open(p))
q="Documentation is part of the definition of done for every feature."
f['culture']['strong_positive_phrases']=[{"phrase":"definition of done","quote":q}]
f['keyword_signals_found']=[{"phrase":"definition of done","read":"Documentation counts as part of finished work, which is what you want.","quote":q}]
json.dump(f,open(p,'w'),indent=1)
EOF
python3 assessment/scripts/check_findings.py work/findings.json --posting "$N" --profile career-profile.yaml
```

```text
check_findings: ok
```

```text
$ cd <work>; P=career-profile.yaml
python3 assessment/scripts/score_helpers.py work/findings.json --profile $P --json > work/scores.json && cat work/scores.json
python3 -c "import json,sys; sys.path.insert(0,'assessment/scripts'); import verdict as v; \
s=json.load(open('work/scores.json')); f=json.load(open('work/findings.json')); \
print(json.dumps(v.decide(s['fit'],s['qualifications'],s['comp'],s['culture'], \
override=v.override_skill(f),hard_block=v.hard_block_id(f))))" > work/verdict.json; cat work/verdict.json
```

```text
{
  "fit": 10,
  "comp": 10,
  "qualifications": 9,
  "culture": 10,
  "why": {
    "fit": [],
    "comp": [
      "Tier used: Region B",
      "Top of range 104000 against target 100000, min 80000, floor 75000"
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
{"label": "Apply", "trigge
... (41 more characters)
```

```text
$ cd <work>; P=career-profile.yaml; N="archive/Copperline Example Co. - Docs Platform Engineer - 2026-10-01.md"
python3 assessment/scripts/render_assessment.py work/findings.json --scores work/scores.json --verdict work/verdict.json --profile $P > work/block.md
cat >> work/block.md <<'EOF'

### 🗒️ Notes on your skills
- OpenAPI / Swagger and Docs as code are both things you want to do more of, and both are core daily work here.
- Go is a gap: the posting wants you to read Go well enough to follow the build tool, and you have no proof of recent Go work. Expect a question about it.
EOF
python3 assessment/scripts/write_assessment.py "$N" --block work/block.md --verdict apply --date 2026-10-01
python3 assessment/scripts/rename_verdict.py "$N" --verdict apply --profile $P
```

```text
Assessment written to archive/Copperline Example Co. - Docs Platform Engineer - 2026-10-01.md (state set to apply_ready).
Renamed: archive/🟢 📋 🔧 Copperline Example Co. - Docs Platform Engineer - 2026-10-01.md
```

```text
$ cd <work>; P=career-profile.yaml
python3 assessment/scripts/render_assessment.py work/findings.json --scores work/scores.json --verdict work/verdict.json --profile $P --terminal
python3 assessment/scripts/render_email.py --note "archive/🟢 📋 🔧 Copperline Example Co. - Docs Platform Engineer - 2026-10-01.md" --findings work/findings.json --scores work/scores.json --verdict work/verdict.json --profile $P --out out --next-prompt "Copperline Example Co., Docs Platform Engineer: Apply. Fit 10, Comp 10, Qualifications 9, Culture 10. Note: archive/🟢 📋 🔧 Copperline Example Co. - Docs Platform Engineer - 2026-10-01.md. Next: check for a warm introduction and prepare to speak to reading Go."; pwd
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
... (928 more characters)
```

ASSESSMENT: Copperline Example Co., Docs Platform Engineer (docs-platform lane)

🚦 **VERDICT: Apply**

🏢 Copperline Example Co. is one you have said you want to work for. Your reason: Makes tools for writers, which is the work Robin cares about most. This did not change the scores or the verdict.

**Scores:**
Fit 10 🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟  
Comp 10 🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟  
Qualifications 9 🟢🟢🟢🟢🟢🟢🟢🟢🟢⬛  
Culture 10 🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟  

| Check | Rating | Read |
|---|---|---|
| ✨ AI-forward team | 🟢 Strong | The team drafts with AI every day and people still check the work. That is what you want. |
| 📦 Docs live in version control | 🟢 Strong | Docs are in Git and reviewed in pull requests. This matches your best work. |
| 🧪 Docs are built and checked automatically | 🟡 Fair | Builds are not automatic today, but you would be the one to fix that. You have built automatic checks before. |
| 🦸 Owns the docs system | 🟢 Strong | You would own the docs system from week one. That is a bonus. |
| How much say you'd have | 🟢 Strong | You would pick the tools and set priorities. Your manager only checks in weekly, so you would have a lot of say. |

🟢 Strong · 🟡 Fair · 🟠 Weak · 🔴 Poor · ❓ Unknown

`[Open the note](file://<work>/archive/🟢%20📋%20🔧%20Copperline%20Example%20Co.%20-%20Docs%20Platform%20Engineer%20-%202026-10-01.md)`

The verdict is Apply, and no earlier rule fired: there was no hard block, no job-type override, and no score below the floor or in the reservations band. Because Copperline is a high-interest company, move fast and check for a warm introduction. The one thing to prepare for is the Go line: the posting wants you to read Go code, and you have no recorded evidence of recent Go work. That cost one Qualifications point. The Fit, Comp and Culture bars are all at 10, and Comp is based on the Region B tier ($85k–$104k).

The email card is at `out/copperline-example-co-docs-platform-engineer.html`. It was written and passed its own check, and nothing was sent.

I skipped one thing: the pay-range-listed benefit isn't a field in the findings file, so I didn't record it.


## Posting 03-unlisted-pay-perks

Commands run by the model: 7. Turns: 8. Cost: $0.21.

### Checks

- findings.json written: pass
- exactly one archived note: pass (['🟢 📋 ✍️ Ashgrove Example Software - Senior Technical Writer - 2026-10-01.md'])
- email card written: pass
- check_findings.py passes on the model's findings: pass (check_findings: ok)
- verdict matches expected.yaml: FAIL (got Apply (4d), expected Apply with reservations)
- Scores from the model's findings: {'fit': 7, 'comp': 5, 'qualifications': 7, 'culture': 9}. Expected: {'fit': 7, 'comp': 5, 'qualifications': 6, 'culture': 9}. They differ: the model read the posting a little differently. The test requires the verdict, not identical scores.
- note name starts with the verdict dot: pass (🟢 📋 ✍️ Ashgrove Example Software - Senior Technical Writer - 2026-10-01.md)

Result: FAIL

### Transcript

```text
$ cd <work>; ls -R . | head -50; cat assessment/SKILL.md
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
... (25834 more characters)
```

```text
$ cd <work>; mkdir -p archive work out; cat posting.md; python3 scripts/validate_profile.py career-profile.yaml; echo; cat career-profile.yaml
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
... (12077 more characters)
```

```text
$ cd <work>; python3 assessment/scripts/parse_posting.py posting.md --company "Ashgrove Example Software" --role "Senior Technical Writer" --lane tech-writing --archive-dir archive --url "https://example.net/fictional/jobs/ashgrove-senior-writer" --source board-a; ls archive
```

```text
POSTING PARSE: Ashgrove Example Software / Senior Technical Writer

POSTING READ
   6 requirements likely real, 1 likely filters

LIKELY REAL: these describe the actual work

   [responsibility] Write guides and reference pages for developers.
      -> Describes the actual work, not a screening filter.

   [responsibility] Engineers are busy and answer questions when they can.
      -> Describes the actual work, not a screening filter.

   [responsibility] We keep a short style guide in our wiki
... (1115 more characters)
```

```text
$ cd <work>; N="archive/Ashgrove Example Software - Senior Technical Writer - 2026-10-01.md"; python3 assessment/scripts/load_criteria.py --profile career-profile.yaml --lane tech-writing --posting "$N"; python3 assessment/scripts/match_skills.py "$N" --profile career-profile.yaml; cat schema/findings.schema.json | head -5
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
... (6433 more characters)
```

```text
$ cd <work>; cat > work/findings.json <<'EOF'
{
  "posting_file": "archive/Ashgrove Example Software - Senior Technical Writer - 2026-10-01.md",
  "lane": "tech-writing",
  "hard_block": {"tripped": false, "id": null, "quote": null, "named_exception": null},
  "job_type_override": {"fired": false, "skill": null, "quotes": [], "evidence_checked": []},
  "requirements": [
    {"id": "expert_access", "rating": "weak", "quote": "Engineers are busy and answer questions when they can.",
     "read": "This one matters a lot. The posting says engineers are busy and answer when they can. That is not regular access, so you may wait on the people you need."},
    {"id": "tooling_voice", "rating": "unknown", "quote": null,
     "read": "The posting says nothing about who picks the authoring tools."},
    {"id": "style_guide", "rating": "strong", "quote": "We keep a short style guide in our wiki.",
     "read": "A written style guide exists. It is short, but it is there."}
  ],
  "autonomy": {"net": "unknown", "quotes": [], "read": "The posting does not say how much say you would have.
... (2150 more characters)
```

```text
check_findings: ok
{
  "fit": 7,
  "comp": 5,
  "qualifications": 7,
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
      "1 load-bearing gap(s), -1 (cap 4)"
    ],
    "culture": [
      "Perk extra_days_off (big), +2",
      "Perk learning_budget (big), +2"
... (80 more characters)
```

Scoring is done and the verdict is Apply. Next I'll write the note, rename it, and render the summary and email card.

```text
$ cd <work>; N="archive/Ashgrove Example Software - Senior Technical Writer - 2026-10-01.md"
python3 assessment/scripts/render_assessment.py work/findings.json --scores work/scores.json --verdict work/verdict.json --profile career-profile.yaml > work/block.md
cat >> work/block.md <<'EOF'

### 🗒️ Notes on your skills
- OpenAPI / Swagger is a skill you want more of, and the posting asks for it directly.
- Kubernetes is a gap for you. The posting only asks for comfort with the concepts, so it is a small miss.
- The posting also mentions documenting a mobile SDK for iOS and Android, which you have not done. It is worded as something you can do, not a requirement.
- The posting asks for 11 years and you have 9. That kind of number mostly tracks how many people apply.
EOF
python3 assessment/scripts/write_assessment.py "$N" --block work/block.md --verdict apply --date 2026-10-01
python3 assessment/scripts/rename_verdict.py "$N" --verdict apply --profile career-profile.yaml; ls archive
```

```text
Assessment written to archive/Ashgrove Example Software - Senior Technical Writer - 2026-10-01.md (state set to apply_ready).
Renamed: archive/🟢 📋 ✍️ Ashgrove Example Software - Senior Technical Writer - 2026-10-01.md
🟢 📋 ✍️ Ashgrove Example Software - Senior Technical Writer - 2026-10-01.md
```

```text
$ cd <work>; R="archive/🟢 📋 ✍️ Ashgrove Example Software - Senior Technical Writer - 2026-10-01.md"
python3 assessment/scripts/render_assessment.py work/findings.json --scores work/scores.json --verdict work/verdict.json --profile career-profile.yaml --terminal
echo ----
python3 assessment/scripts/render_email.py --note "$R" --findings work/findings.json --scores work/scores.json --verdict work/verdict.json --profile career-profile.yaml --out out --next-prompt "Ashgrove Example Software, Senior Technical Writer: Apply. Fit 7, Comp 5, Qualifications 7, Culture 9. Note: $PWD/$R. Next: ask about pay and engineer access, then decide whether to apply."; pwd
```

```text
ASSESSMENT: archive/Ashgrove Example Software - Senior Technical Writer - 2026-10-01.md

🚦 VERDICT: Apply

🏢 Ashgrove Example Software is a good company, not a dream one. Your reason: Solid product and a fair size, but nothing Robin would move for. This did not change the scores or the verdict.

**Scores:**
Fit 7 🟢🟢🟢🟢🟢🟢🟢⬛⬛⬛  
Comp 5 🟡🟡🟡🟡🟡⬛⬛⬛⬛⬛  
Qualifications 7 🟢🟢🟢🟢🟢🟢🟢⬛⬛⬛  
Culture 9 🟢🟢🟢🟢🟢🟢🟢🟢🟢⬛  

| Check | Rating | Read |
|---|---|---|
| 🧑‍🔬 Regular access to experts | 🟠 Weak | This one matter
... (884 more characters)
```

**ASSESSMENT: Ashgrove Example Software, Senior Technical Writer (tech-writing lane)**

🚦 **VERDICT: Apply**

🏢 Ashgrove is a good company, not a dream one. That read did not change any score or the verdict.

**Scores:**
Fit 7 🟢🟢🟢🟢🟢🟢🟢⬛⬛⬛
Comp 5 🟡🟡🟡🟡🟡⬛⬛⬛⬛⬛
Qualifications 7 🟢🟢🟢🟢🟢🟢🟢⬛⬛⬛
Culture 9 🟢🟢🟢🟢🟢🟢🟢🟢🟢⬛

| Check | Rating | Read |
|---|---|---|
| 🧑‍🔬 Regular access to experts | 🟠 Weak | Engineers are busy and answer when they can. That is not regular access. |
| 🛠️ A say in the authoring tools | ❓ Unknown | The posting says nothing about who picks the tools. |
| 📖 A written style guide | 🟢 Strong | A short style guide exists. |
| How much say you'd have | ❓ Unknown | Only generic "work closely with" language. |

🟢 Strong · 🟡 Fair · 🟠 Weak · 🔴 Poor · ❓ Unknown

Note: `file://<work>/archive/🟢%20📋%20✍️%20Ashgrove%20Example%20Software%20-%20Senior%20Technical%20Writer%20-%202026-10-01.md`

The verdict is Apply because no hard block, job-type override or score floor fired. Pay is not listed, so Comp stays at a neutral 5. Culture is high because the posting lists extra paid days off and a learning budget.

Things to act on:
- **Pay:** ask for the pay range early. The posting only says it is discussed at the second interview.
- **Engineer access:** confirm how much time you would get with the engineers.
- **Gaps:** the posting asks for 11 years and you have 9, which mostly tracks how many people apply. Kubernetes is a small gap, since it only asks for comfort with the concepts. Mobile SDK docs are a duty you have not done, but they are worded as something you "can" do.
- **Outside research:** reviews and funding were not checked.

The email card is at `out/ashgrove-example-software-senior-technical-writer.html`, and its subject is "🟢 Job Assessment: Ashgrove Example Software - Senior Technical Writer - 2026-10-01". It was not sent.

