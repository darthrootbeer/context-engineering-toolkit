<!-- FICTIONAL EXAMPLE DATA. Not a real person. Saved by tests/live/test_live_intake.py -->
# Live run: intake transcript

Date: 2026-10-01. Model: `sonnet`. Commands run by the model: 32. Turns: 33. Cost: $0.81.

A model followed `intake/SKILL.md` and answered from `fixtures/robin-sample/intake-answers.txt`. Tool output is cut to the first 700 characters. Folder names are replaced with `<work>` and `<tmp>`.

## Transcript

*Read* `<work>/intake/SKILL.md`

```text
1	---
2	name: career-intake
3	description: >
4	  Interview the user, one question at a time, to build their career-profile.yaml:
5	  job history, accomplishments with a source for every one, a skills self-score,
6	  what they need from a job, and the kinds of role they are looking at. Every
7	  answer is read back as the exact YAML entry and written only after the user
8	  says yes, and only through scripts/add_entry.py. Never invents, rounds up or
9	  upgrades a claim. Resumes at the next unfinished stage. Use when the user
10	  wants to build or extend the central file for the job assessment, says
11	  "interview me for my career profile", or runs "/career-intake".
12	argument-hint: "[path
... (10255 more characters)
```

```text
$ ls -R . | head -50 && cat intake-answers.txt
```

```text
assessment
intake
intake-answers.txt
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
README.md
scripts
SKILL.md
stage-prompts
stages
templates

./intake/scripts:
merge_survey.py

./intake/stage-prompts:
00-orientation.txt
01-job-history.txt
# FICTIONAL EXAMPLE DATA. Not a real person.
# Scripted answers
... (5827 more characters)
```

```text
$ ls intake/stages intake/templates schema scripts; cat intake/stages/00-orientation.md
```

```text
intake/stages:
00-orientation.md
01-job-history.md
02-accomplishments.md
03-skills.md
04-needs.md
05-lanes.md
06-review.md

intake/templates:
career-profile.template.yaml
skills-catalog.yaml
skills-survey.html

schema:
career-profile.schema.json
findings.schema.json

scripts:
add_entry.py
assess_offline.py
validate_profile.py
# Stage 0: Orientation

**Writes:** a new `career-profile.yaml` copied from the template, then `person`.
**Rules:** every rule in `../SKILL.md` applies. One question at a time.

## Questions, in order

Ask one, wait for the answer, then ask the next.

1. "Where should the file live?"
2. "Do you have a résumé, portfolio or old job descriptions I should read first?"
3. "W
... (2284 more characters)
```

```text
$ ls career-profile.yaml 2>&1; cp intake/templates/career-profile.template.yaml ./career-profile.yaml && cat career-profile.yaml | head -80; cat intake/stages/01-job-history.md
```

```text
ls: career-profile.yaml: No such file or directory
# career-profile.yaml: your job history, your evidence, your skills and what you need
# from a job, in one file. The intake interview fills it in one checked answer at a
# time. Copy this file, then let the interview write to it through
# scripts/add_entry.py. Check it any time with:
#
#     python3 scripts/validate_profile.py career-profile.yaml
#
# Rules that keep the file honest:
#   - Every accomplishment is an evidence entry with a source. Where did the fact
#     come from: the interview, a document, a public link, an artifact, or a
#     reference? Interview and reference facts stay proof: unchecked.
#   - A skill score is your own cl
... (5860 more characters)
```

```text
$ python3 scripts/add_entry.py career-profile.yaml --section person --entry - <<'YAML'
display_name: Robin Sample
target_roles: [Senior Technical Writer, Docs Platform Engineer]
years_experience: 9
YAML
echo "exit $?"
python3 scripts/add_entry.py career-profile.yaml --section meta --entry - <<'YAML'
updated: "2026-10-01"
intake:
  stages_done: [0]
YAML
echo "exit $?"
```

```text
add_entry: updated person display_name, target_roles, years_experience in career-profile.yaml
warning: culture.perks: the perks list is empty, so no perk can raise Culture.
validate_profile: clean, 1 warning(s) in career-profile.yaml
exit 0
add_entry: updated meta updated, intake in career-profile.yaml
warning: culture.perks: the perks list is empty, so no perk can raise Culture.
validate_profile: clean, 1 warning(s) in career-profile.yaml
exit 0
```

```text
$ python3 scripts/add_entry.py career-profile.yaml --section employers --entry - <<'YAML'
id: placeholder_labs
name: Placeholder Labs
title: Senior Technical Writer
start: "2022-01"
YAML
echo "exit $?"
```

```text
add_entry: added employers "placeholder_labs" in career-profile.yaml
warning: culture.perks: the perks list is empty, so no perk can raise Culture.
validate_profile: clean, 1 warning(s) in career-profile.yaml
exit 0
```

```text
$ python3 scripts/add_entry.py career-profile.yaml --section employers --entry - --replace <<'YAML'
id: placeholder_labs
name: Placeholder Labs
title: Senior Technical Writer
start: "2022-01"
end: present
YAML
echo "exit $?"
```

```text
add_entry: replaced employers "placeholder_labs" in career-profile.yaml
warning: culture.perks: the perks list is empty, so no perk can raise Culture.
validate_profile: clean, 1 warning(s) in career-profile.yaml
exit 0
```

```text
$ python3 scripts/add_entry.py career-profile.yaml --section employers --entry - --replace <<'YAML'
id: placeholder_labs
name: Placeholder Labs
title: Senior Technical Writer
start: "2022-01"
end: present
summary: I lead documentation and run the system that builds and checks the docs.
YAML
echo "exit $?"
```

```text
add_entry: replaced employers "placeholder_labs" in career-profile.yaml
warning: culture.perks: the perks list is empty, so no perk can raise Culture.
validate_profile: clean, 1 warning(s) in career-profile.yaml
exit 0
```

```text
$ python3 scripts/add_entry.py career-profile.yaml --section employers --entry - <<'YAML'
id: northwind
name: Northwind Example Co.
title: Technical Writer
start: "2017-02"
YAML
echo "exit $?"
```

```text
add_entry: added employers "northwind" in career-profile.yaml
warning: culture.perks: the perks list is empty, so no perk can raise Culture.
validate_profile: clean, 1 warning(s) in career-profile.yaml
exit 0
```

ASK: What month and year did you leave, or are you still there?
USER: December 2021.

Read-back (treated as yes): `end: "2021-12"`

```text
$ python3 scripts/add_entry.py career-profile.yaml --section employers --entry - --replace <<'YAML'
id: northwind
name: Northwind Example Co.
title: Technical Writer
start: "2017-02"
end: "2021-12"
YAML
echo "exit $?"
```

```text
add_entry: replaced employers "northwind" in career-profile.yaml
warning: culture.perks: the perks list is empty, so no perk can raise Culture.
validate_profile: clean, 1 warning(s) in career-profile.yaml
exit 0
```

```text
$ python3 scripts/add_entry.py career-profile.yaml --section employers --entry - --replace <<'YAML'
id: northwind
name: Northwind Example Co.
title: Technical Writer
start: "2017-02"
end: "2021-12"
summary: I wrote and maintained the help center and the API reference.
YAML
echo "exit $?"
```

```text
add_entry: replaced employers "northwind" in career-profile.yaml
warning: culture.perks: the perks list is empty, so no perk can raise Culture.
validate_profile: clean, 1 warning(s) in career-profile.yaml
exit 0
```

```text
$ python3 scripts/add_entry.py career-profile.yaml --section meta --entry - <<'YAML'
updated: "2026-10-01"
intake:
  stages_done: [0, 1]
YAML
echo "exit $?"; cat intake/stages/02-accomplishments.md
```

```text
add_entry: updated meta updated, intake in career-profile.yaml
warning: culture.perks: the perks list is empty, so no perk can raise Culture.
validate_profile: clean, 1 warning(s) in career-profile.yaml
exit 0
# Stage 2: Accomplishments

**Writes:** `evidence[]`
**Rules:** every rule in `../SKILL.md` applies. One question at a time.

This is the stage that matters most. The assessment can only claim a
qualification when an evidence entry backs it, so every entry here must be the
user's own account, with an honest label for where it came from.

## Questions, in order

Work one employer at a time, starting with the one the user names first. For
each accomplishment, ask one question, wait, then
... (4893 more characters)
```

```text
$ python3 scripts/add_entry.py career-profile.yaml --section evidence --entry - <<'YAML'
id: ev-northwind-api-reference
employer_id: northwind
claim: Moved the API reference from hand-edited pages to pages generated from the API spec.
details: "Releases stopped breaking the reference pages."
authorship: DIRECTED
proof: unchecked
source: {type: link, ref: "https://example.com/fictional/northwind/api-rebuild", captured_on: "2026-10-01"}
YAML
echo "exit $?"
python3 scripts/add_entry.py career-profile.yaml --section evidence --entry - --replace <<'YAML'
id: ev-northwind-api-reference
employer_id: northwind
claim: Moved the API reference from hand-edited pages to pages generated from the API spec.
details: "Releases stopped breaking the reference pages. I wrote the build step myself and checked it by hand. Skills used (own words): OpenAPI."
authorship: DIRECTED
proof: unchecked
source: {type: link, ref: "https://example.com/fictional/northwind/api-rebuild", captured_on: "2026-10-01"}
YAML
echo "exit $?"
```

```text
add_entry: added evidence "ev-northwind-api-reference" in career-profile.yaml
warning: evidence[0]: "ev-northwind-api-reference" has no dates, so it cannot be judged recent or stale.
warning: culture.perks: the perks list is empty, so no perk can raise Culture.
validate_profile: clean, 2 warning(s) in career-profile.yaml
exit 0
add_entry: replaced evidence "ev-northwind-api-reference" in career-profile.yaml
warning: evidence[0]: "ev-northwind-api-reference" has no dates, so it cannot be judged recent or stale.
warning: culture.perks: the perks list is empty, so no perk can raise Culture.
validate_profile: clean, 2 warning(s) in career-profile.yaml
exit 0
```

```text
$ ls northwind-style-guide.pdf 2>&1 | head -1
python3 scripts/add_entry.py career-profile.yaml --section evidence --entry - <<'YAML'
id: ev-northwind-style-guide
employer_id: northwind
claim: Wrote a 20-page style guide that the whole support team used.
details: "Support answers got more consistent."
authorship: WROTE
proof: unchecked
source: {type: document, ref: "northwind-style-guide.pdf", captured_on: "2026-10-01"}
YAML
echo "exit $?"
python3 scripts/add_entry.py career-profile.yaml --section evidence --entry - --replace <<'YAML'
id: ev-northwind-style-guide
employer_id: northwind
claim: Wrote a 20-page style guide that the whole support team used.
details: "Support answers got more consistent. Skills used (own words): Style guides."
authorship: WROTE
proof: unchecked
source: {type: document, ref: "northwind-style-guide.pdf", captured_on: "2026-10-01"}
YAML
echo "exit $?"
```

```text
ls: northwind-style-guide.pdf: No such file or directory
add_entry: added evidence "ev-northwind-style-guide" in career-profile.yaml
warning: evidence[0]: "ev-northwind-api-reference" has no dates, so it cannot be judged recent or stale.
warning: evidence[1]: "ev-northwind-style-guide" has no dates, so it cannot be judged recent or stale.
warning: culture.perks: the perks list is empty, so no perk can raise Culture.
validate_profile: clean, 3 warning(s) in career-profile.yaml
exit 0
add_entry: replaced evidence "ev-northwind-style-guide" in career-profile.yaml
warning: evidence[0]: "ev-northwind-api-reference" has no dates, so it cannot be judged recent or stale.
warning: evidence[1]: "ev-no
... (221 more characters)
```

```text
$ python3 scripts/add_entry.py career-profile.yaml --section evidence --entry - <<'YAML'
id: ev-northwind-release-notes
employer_id: northwind
claim: Ran a monthly release-notes process.
details: "Engineers got a regular slot to tell me what changed."
authorship: WROTE
proof: unchecked
source: {type: interview, ref: "interview:2026-10-01:s2.q14", captured_on: "2026-10-01"}
YAML
echo "exit $?"
python3 scripts/add_entry.py career-profile.yaml --section evidence --entry - --replace <<'YAML' | tail -3
id: ev-northwind-release-notes
employer_id: northwind
claim: Ran a monthly release-notes process.
details: "Engineers got a regular slot to tell me what changed. Skills used (own words): Interviewing experts."
authorship: WROTE
proof: unchecked
source: {type: interview, ref: "interview:2026-10-01:s2.q14", captured_on: "2026-10-01"}
YAML
echo "exit $?"
```

```text
add_entry: added evidence "ev-northwind-release-notes" in career-profile.yaml
warning: evidence[0]: "ev-northwind-api-reference" has no dates, so it cannot be judged recent or stale.
warning: evidence[1]: "ev-northwind-style-guide" has no dates, so it cannot be judged recent or stale.
warning: evidence[2]: "ev-northwind-release-notes" has no dates, so it cannot be judged recent or stale.
warning: culture.perks: the perks list is empty, so no perk can raise Culture.
validate_profile: clean, 4 warning(s) in career-profile.yaml
exit 0
warning: evidence[2]: "ev-northwind-release-notes" has no dates, so it cannot be judged recent or stale.
warning: culture.perks: the perks list is empty, so no pe
... (89 more characters)
```

```text
$ python3 scripts/add_entry.py career-profile.yaml --section evidence --entry - <<'YAML' | tail -2
id: ev-placeholder-labs-docs-pipeline
employer_id: placeholder_labs
claim: Built a pipeline that publishes the docs from Markdown files kept in Git.
details: "Docs go live within minutes of an approved change."
authorship: DIRECTED
proof: unchecked
source: {type: artifact, ref: "example.com/fictional/placeholder-labs/docs-pipeline", captured_on: "2026-10-01"}
YAML
echo "exit $?"
python3 scripts/add_entry.py career-profile.yaml --section evidence --entry - --replace <<'YAML' | tail -2
id: ev-placeholder-labs-docs-pipeline
employer_id: placeholder_labs
claim: Built a pipeline that publishes the docs from Markdown files kept in Git.
details: "Docs go live within minutes of an approved change. I directed an AI tool to write most of the build scripts, and I reviewed and tested them. Skills used (own words): Docs as code, static site generators."
authorship: DIRECTED
proof: unchecked
source: {type: artifact, ref: "example.com/fictional/placeholder-labs/docs-pipeline", captured_on: "2026-10-01"}
YAML
echo "exit $?"
```

```text
warning: culture.perks: the perks list is empty, so no perk can raise Culture.
validate_profile: clean, 5 warning(s) in career-profile.yaml
exit 0
warning: culture.perks: the perks list is empty, so no perk can raise Culture.
validate_profile: clean, 5 warning(s) in career-profile.yaml
exit 0
```

```text
$ python3 scripts/add_entry.py career-profile.yaml --section evidence --entry - <<'YAML' | tail -2
id: ev-placeholder-labs-ci-checks
employer_id: placeholder_labs
claim: Added automatic checks for broken links and missing alt text.
details: "Broken links stopped reaching readers."
authorship: CO-WROTE
proof: unchecked
source: {type: link, ref: "https://example.org/fictional/placeholder-labs/ci-checks", captured_on: "2026-10-01"}
YAML
echo "exit $?"
python3 scripts/add_entry.py career-profile.yaml --section evidence --entry - --replace <<'YAML' | tail -2
id: ev-placeholder-labs-ci-checks
employer_id: placeholder_labs
claim: Added automatic checks for broken links and missing alt text.
details: "Broken links stopped reaching readers. I co-wrote it with an engineer. Skills used (own words): Build and check pipelines, Python."
authorship: CO-WROTE
proof: unchecked
source: {type: link, ref: "https://example.org/fictional/placeholder-labs/ci-checks", captured_on: "2026-10-01"}
YAML
echo "exit $?"
```

```text
warning: culture.perks: the perks list is empty, so no perk can raise Culture.
validate_profile: clean, 6 warning(s) in career-profile.yaml
exit 0
warning: culture.perks: the perks list is empty, so no perk can raise Culture.
validate_profile: clean, 6 warning(s) in career-profile.yaml
exit 0
```

```text
$ python3 scripts/add_entry.py career-profile.yaml --section evidence --entry - <<'YAML' | tail -2
id: ev-placeholder-labs-style-prompts
employer_id: placeholder_labs
claim: Wrote the prompts that make an AI assistant draft pages in the team style, with a human review step.
details: "First drafts need fewer rewrites."
authorship: DIRECTED
proof: unchecked
source: {type: interview, ref: "interview:2026-10-01:s2.q34", captured_on: "2026-10-01"}
YAML
echo "exit $?"
python3 scripts/add_entry.py career-profile.yaml --section evidence --entry - --replace <<'YAML' | tail -2
id: ev-placeholder-labs-style-prompts
employer_id: placeholder_labs
claim: Wrote the prompts that make an AI assistant draft pages in the team style, with a human review step.
details: "First drafts need fewer rewrites. I directed the AI tool and wrote the prompts myself. Skills used (own words): Writing prompts for AI tools."
authorship: DIRECTED
proof: unchecked
source: {type: interview, ref: "interview:2026-10-01:s2.q34", captured_on: "2026-10-01"}
YAML
echo "exit $?"
```

```text
warning: culture.perks: the perks list is empty, so no perk can raise Culture.
validate_profile: clean, 7 warning(s) in career-profile.yaml
exit 0
warning: culture.perks: the perks list is empty, so no perk can raise Culture.
validate_profile: clean, 7 warning(s) in career-profile.yaml
exit 0
```

```text
$ python3 scripts/add_entry.py career-profile.yaml --section meta --entry - <<'YAML' | tail -2
updated: "2026-10-01"
intake:
  stages_done: [0, 1, 2]
YAML
cat intake/stages/03-skills.md; head -60 intake/templates/skills-catalog.yaml; python3 intake/scripts/merge_survey.py -h
```

```text
warning: culture.perks: the perks list is empty, so no perk can raise Culture.
validate_profile: clean, 7 warning(s) in career-profile.yaml
# Stage 3: Skills survey

**Writes:** `skills[]`
**Rules:** every rule in `../SKILL.md` applies. One question at a time.

A skill score is the user's own claim. It is never proof. The assessment
counts a skill as proven only when it points at an evidence entry, and reports
the rest as "unproven". That is not a failure; it is the file being honest.

The list of skills comes from `intake/templates/skills-catalog.yaml`: about 60
items in ten groups. Each group has a 0 anchor and a 5 anchor in plain words.

## Choose a way to do it

Ask: "There are about 60 
... (7558 more characters)
```

```text
$ python3 - <<'E'
import json
s=json.load(open('schema/career-profile.schema.json'))
print(json.dumps(s['properties']['skills'],indent=1)[:2500])
E
grep -n "id:" intake/templates/skills-catalog.yaml | head -80
```

```text
{
 "type": "array",
 "items": {
  "$ref": "#/$defs/skill"
 }
}
34:  - id: communication
40:      - id: plain-language
44:      - id: editing-others
48:      - id: instructions
52:      - id: explain-hard-topics
56:      - id: expert-interviews
60:      - id: style-guides
65:  - id: research
71:      - id: desk-research
75:      - id: comparison-studies
79:      - id: user-interviews
83:      - id: source-checking
87:      - id: recommendations
91:      - id: notes-system
96:  - id: data
102:      - id: spreadsheets
106:      - id: sql
110:      - id: data-cleaning
114:      - id: dashboards
118:      - id: statistics
122:      - id: data-formats
127:  - id: code
133:      - id: python
137:  
... (1257 more characters)
```

Still on stage 3. I'm checking what a skill entry requires before I write any.

```text
$ python3 - <<'E'
import json
s=json.load(open('schema/career-profile.schema.json'))
print(json.dumps(s['$defs']['skill'],indent=1))
E
```

```text
{
 "type": "object",
 "additionalProperties": false,
 "required": [
  "id",
  "label",
  "self_score"
 ],
 "properties": {
  "id": {
   "$ref": "#/$defs/id"
  },
  "label": {
   "$ref": "#/$defs/text"
  },
  "group": {
   "$ref": "#/$defs/id"
  },
  "match": {
   "$ref": "#/$defs/text_list",
   "description": "Regex patterns used to find this skill in a posting."
  },
  "self_score": {
   "type": "integer",
   "minimum": 0,
   "maximum": 5,
   "description": "The person's own claim, 0 to 5. Never evidence on its own."
  },
  "next": {
   "enum": [
    "more",
    "neutral",
    "avoid"
   ]
  },
  "last": {
   "enum": [
    "2y",
    "5y",
    "5plus",
    "never"
   ]
  },
  "how": {
   "ty
... (234 more characters)
```

```text
$ add(){ python3 scripts/add_entry.py career-profile.yaml --section skills --entry - | grep -v "no dates\|perks list"; echo "exit ${PIPESTATUS[0]}"; }
echo "--- openapi"; add <<'YAML'
id: openapi
label: OpenAPI
self_score: 4
next: more
last: 2y
how: [self, ai]
evidence_ids: [ev-northwind-api-reference]
YAML
echo "--- docs_as_code"; add <<'YAML'
id: docs_as_code
label: Docs as code
self_score: 5
next: more
last: 2y
how: [self, ai, team]
evidence_ids: [ev-placeholder-labs-docs-pipeline, ev-placeholder-labs-ci-checks]
YAML
echo "--- static_sites"; add <<'YAML'
id: static_sites
label: Static sites
self_score: 4
next: neutral
last: 2y
how: [self, ai]
evidence_ids: [ev-placeholder-labs-docs-pipeline]
YAML
echo "--- ci_pipelines"; add <<'YAML'
id: ci_pipelines
label: CI pipelines
self_score: 3
next: neutral
last: 2y
how: [self, ai]
evidence_ids: [ev-placeholder-labs-ci-checks]
YAML
echo "--- python_scripting"; add <<'YAML'
id: python_scripting
label: Python scripting
self_score: 3
next: more
last: 2y
how: [self, ai]
evidence_ids: [ev-placeholder-labs-ci-checks]
YAML
echo "--- prompt_writing"; add <<'YAML'
id: prompt_writing
label: Prompt writing
self_score: 4
next: more
last: 2y
how: [self]
... (1207 more characters)
```

```text
--- openapi
add_entry: added skills "openapi" in career-profile.yaml
validate_profile: clean, 7 warning(s) in career-profile.yaml
exit 
--- docs_as_code
add_entry: added skills "docs_as_code" in career-profile.yaml
validate_profile: clean, 7 warning(s) in career-profile.yaml
exit 
--- static_sites
add_entry: added skills "static_sites" in career-profile.yaml
validate_profile: clean, 7 warning(s) in career-profile.yaml
exit 
--- ci_pipelines
add_entry: added skills "ci_pipelines" in career-profile.yaml
validate_profile: clean, 7 warning(s) in career-profile.yaml
exit 
--- python_scripting
add_entry: added skills "python_scripting" in career-profile.yaml
validate_profile: clean, 7 warning(s) i
... (6938 more characters)
```

Stage 3 is saved. All 14 skills are written. The 8 scored 3 or higher each point at evidence the user named.

```text
$ python3 - <<'E'
import json
s=json.load(open('schema/career-profile.schema.json'))
for k in ['hard_blocks','named_exceptions','company_criteria','culture','comp']:
    p=s['properties'][k]
    print(k,json.dumps(p)[:900]); print()
d=s['$defs']
for k,v in d.items():
    if k in('hard_block','named_exception','company','perk','criterion'): print(k,json.dumps(v)[:600])
print(list(d))
E
```

```text
hard_blocks {"type": "array", "items": {"$ref": "#/$defs/hard_block"}}

named_exceptions {"type": "array", "items": {"$ref": "#/$defs/named_exception"}}

company_criteria {"$ref": "#/$defs/company_criteria"}

culture {"$ref": "#/$defs/culture"}

comp {"$ref": "#/$defs/comp"}

hard_block {"type": "object", "additionalProperties": false, "required": ["id", "label"], "properties": {"id": {"$ref": "#/$defs/id"}, "label": {"$ref": "#/$defs/text"}, "why": {"type": "string"}, "match_hints": {"$ref": "#/$defs/text_list"}}}
named_exception {"type": "object", "additionalProperties": false, "required": ["company", "block_id"], "properties": {"company": {"$ref": "#/$defs/text"}, "block_id": {"$ref": "#/
... (618 more characters)
```

```text
$ add(){ python3 scripts/add_entry.py career-profile.yaml "$@" | grep -v "no dates\|perks list"; }
add --section hard_blocks --entry - <<'YAML'
id: gambling
label: Gambling and betting
YAML
add --section hard_blocks --entry - <<'YAML'
id: weapons
label: Weapons makers
YAML
add --section hard_blocks --entry - <<'YAML'
id: non_remote
label: Any job that is not remote
YAML
```

```text
add_entry: added hard_blocks "gambling" in career-profile.yaml
validate_profile: clean, 7 warning(s) in career-profile.yaml
add_entry: added hard_blocks "weapons" in career-profile.yaml
validate_profile: clean, 7 warning(s) in career-profile.yaml
add_entry: added hard_blocks "non_remote" in career-profile.yaml
validate_profile: clean, 7 warning(s) in career-profile.yaml
```

```text
$ add(){ python3 scripts/add_entry.py career-profile.yaml "$@" | grep -v "no dates\|perks list"; }
add --section comp --entry - <<'YAML'
currency: USD
floor: 90000
min: 110000
open_ask: 125000
target: 140000
stretch_ceiling: 170000
YAML
python3 - <<'E'
import yaml;d=yaml.safe_load(open('career-profile.yaml'));print(d['person'],d['culture'])
E
```

```text
add_entry: updated comp currency, floor, min, open_ask, target, stretch_ceiling in career-profile.yaml
validate_profile: clean, 7 warning(s) in career-profile.yaml
{'display_name': 'Robin Sample', 'target_roles': ['Senior Technical Writer', 'Docs Platform Engineer'], 'years_experience': 9, 'location_label': None, 'working_style': None} {'perks': [], 'low_time_off_days': None, 'hustle_phrases': [], 'free_phrases': []}
```

```text
$ add(){ python3 scripts/add_entry.py career-profile.yaml "$@" | grep -v "no dates\|perks list"; }
add --section person --entry - <<'YAML'
location_label: Region B
YAML
add --section culture --entry - <<'YAML'
perks:
  - {id: unlimited_time_off, label: Unlimited time off, kind: big}
  - {id: learning_budget, label: A learning budget, kind: big}
  - {id: extra_paid_days_off, label: Extra paid days off, kind: big}
  - {id: meetups, label: Meetups, kind: nice}
  - {id: home_office_stipend, label: A home-office stipend, kind: nice}
  - {id: paid_parental_leave, label: Paid parental leave, kind: nice}
YAML
add --section culture --entry - <<'YAML'
low_time_off_days: 15
YAML
add --section culture --entry - <<'YAML'
hustle_phrases: [Rockstar, work hard play hard, on-call, weekend work]
free_phrases: [fast-paced]
YAML
python3 - <<'E'
import yaml;d=yaml.safe_load(open('career-profile.yaml'));print(d['person'],d['culture'])
E
```

```text
add_entry: updated person location_label in career-profile.yaml
validate_profile: clean, 7 warning(s) in career-profile.yaml
add_entry: updated culture perks in career-profile.yaml
validate_profile: clean, 6 warning(s) in career-profile.yaml
add_entry: updated culture low_time_off_days in career-profile.yaml
validate_profile: clean, 6 warning(s) in career-profile.yaml
add_entry: updated culture hustle_phrases, free_phrases in career-profile.yaml
validate_profile: clean, 6 warning(s) in career-profile.yaml
{'display_name': 'Robin Sample', 'target_roles': ['Senior Technical Writer', 'Docs Platform Engineer'], 'years_experience': 9, 'location_label': 'Region B', 'working_style': None} {'perks':
... (582 more characters)
```

```text
$ add(){ python3 scripts/add_entry.py career-profile.yaml "$@" | grep -v "no dates"; }
add --section person --entry - <<'YAML'
working_style: gather_from_experts
YAML
add --section company_criteria --entry - <<'YAML'
high_interest:
  - {name: Copperline Example Co., why: Makes tools for writers.}
good_not_dream:
  - {name: Ashgrove Example Software, why: Good but not a dream.}
YAML
add --section meta --entry - <<'YAML'
updated: "2026-10-01"
intake:
  stages_done: [0, 1, 2, 3, 4]
YAML
cat intake/stages/05-lanes.md
```

```text
add_entry: updated person working_style in career-profile.yaml
validate_profile: clean, 6 warning(s) in career-profile.yaml
add_entry: updated company_criteria high_interest, good_not_dream in career-profile.yaml
validate_profile: clean, 6 warning(s) in career-profile.yaml
add_entry: updated meta updated, intake in career-profile.yaml
validate_profile: clean, 6 warning(s) in career-profile.yaml
# Stage 5: Lanes

**Writes:** `lanes[]`
**Rules:** every rule in `../SKILL.md` applies. One question at a time.

A lane is one kind of role, with its own must-haves. Every posting is read
against exactly one lane, and lanes are never mixed. A user looking at one kind
of role still has one lane.

## Qu
... (2825 more characters)
```

Stage 4 is saved. Before stage 5, I'm checking the lane schema.

```text
$ python3 - <<'E'
import json
s=json.load(open('schema/career-profile.schema.json'))['$defs']
for k in ['lane','requirement','signal','labelled_item']: print(k,json.dumps(s[k]));print()
E
```

```text
lane {"type": "object", "additionalProperties": false, "required": ["name", "description", "requirements"], "properties": {"name": {"$ref": "#/$defs/id"}, "emoji": {"type": "string"}, "description": {"$ref": "#/$defs/text"}, "requirements": {"type": "array", "items": {"$ref": "#/$defs/requirement"}}, "autonomy": {"type": "object", "additionalProperties": false, "properties": {"positive_signals": {"$ref": "#/$defs/text_list"}, "negative_signals": {"$ref": "#/$defs/text_list"}}}, "keyword_signals": {"type": "object", "additionalProperties": false, "properties": {"strong_positive": {"type": "array", "items": {"$ref": "#/$defs/signal"}}, "positive": {"type": "array", "items": {"$ref": "#/$defs/s
... (1096 more characters)
```

ASK: Are you looking at more than one kind of role?
USER: Yes, two kinds of role.

ASK: What short name should this kind of role have?
USER: docs-platform

ASK: Which emoji should mark it?
USER: 🔧

ASK: In one sentence, what is the work?
USER: Roles building the systems that produce documentation.

Read-back (treated as yes), written first with empty requirements:
```yaml
name: docs-platform
emoji: "🔧"
description: Roles building the systems that produce documentation.
requirements: []
```

ASK: Which must-haves are different for this kind of role?
USER: AI-forward team, docs live in version control, docs are built and checked automatically, owns the docs system.

ASK: How much does each one matter: a must-have that counts hard, a softer one, or a bonus that never counts against a posting?
USER: AI-forward team (strong), docs live in version control (strong), docs are built and checked automatically (soft), owns the docs system (soft, bonus only).

ASK: What skills does this kind of role want that you don't have yet?
USER: Reading Go code.

ASK: What language in a posting makes you trust it?
USER: "definition of done" and "single source of truth".

ASK: What language in a posting makes you distrust it?
USER: "wiki cleanup" and "no engineering support".

Read-back (treated as yes). "Reading Go code" is linked to your stored skill `go_lang` (Go lang, scored 1). The phrases are `positive` and `negative`, and none are promoted:
```yaml
name: docs-platform
emoji: "🔧"
description: Roles building the systems that produce documentation.
requirements:
  - {id: ai_forward_team, label: AI-forward team, severity: strong}
  - {id: docs_in_version_control, label: Docs live in version control, severity: strong}
  - {id: docs_built_and_checked, label: Docs are built and checked automatically, severity: soft}
  - {id: owns_docs_system, label: Owns the docs system, severity: soft, bonus: true}
known_gaps:
  - {id: reading_go_code, label: Reading Go code, skill_id: go_lang}
keyword_signals:
  positive: [{phrase: definition of done}, {phrase: single source of truth}]
  negative: [{phrase: wiki cleanup}, {phrase: no engineering support}]
```

```text
$ add(){ python3 scripts/add_entry.py career-profile.yaml "$@" | grep -v "no dates"; }
add --section lanes --entry - <<'YAML'
name: docs-platform
emoji: "🔧"
description: Roles building the systems that produce documentation.
requirements: []
YAML
add --section lanes --entry - --replace <<'YAML'
name: docs-platform
emoji: "🔧"
description: Roles building the systems that produce documentation.
requirements:
  - {id: ai_forward_team, label: AI-forward team, severity: strong}
  - {id: docs_in_version_control, label: Docs live in version control, severity: strong}
  - {id: docs_built_and_checked, label: Docs are built and checked automatically, severity: soft}
  - {id: owns_docs_system, label: Owns the docs system, severity: soft, bonus: true}
known_gaps:
  - {id: reading_go_code, label: Reading Go code, skill_id: go_lang}
keyword_signals:
  positive: [{phrase: definition of done}, {phrase: single source of truth}]
  negative: [{phrase: wiki cleanup}, {phrase: no engineering support}]
YAML
```

```text
add_entry: added lanes "docs-platform" in career-profile.yaml
warning: lanes[0].requirements: lane "docs-platform" has no requirements of its own.
validate_profile: clean, 7 warning(s) in career-profile.yaml
add_entry: replaced lanes "docs-platform" in career-profile.yaml
warning: lanes[0].requirements[0]: strong requirement "ai_forward_team" has no why.
warning: lanes[0].requirements[1]: strong requirement "docs_in_version_control" has no why.
validate_profile: clean, 8 warning(s) in career-profile.yaml
```

```text
$ add(){ python3 scripts/add_entry.py career-profile.yaml "$@" | grep -v "no dates"; }
add --section lanes --entry - <<'YAML'
name: tech-writing
emoji: "✍️"
description: Roles writing guides, references and help content for a product.
requirements: []
YAML
add --section lanes --entry - --replace <<'YAML'
name: tech-writing
emoji: "✍️"
description: Roles writing guides, references and help content for a product.
requirements:
  - {id: expert_access, label: Regular access to experts, severity: strong}
  - {id: authoring_tools_say, label: A say in the authoring tools, severity: strong}
  - {id: written_style_guide, label: A written style guide, severity: soft}
known_gaps:
  - {id: dita_xml, label: DITA XML, skill_id: dita_xml}
  - {id: mobile_sdk_docs, label: Mobile SDK documentation, skill_id: mobile_sdk}
keyword_signals:
  positive: [{phrase: writers sit with the engineers}]
  negative: [{phrase: content mill}]
YAML
add --section meta --entry - <<'YAML'
updated: "2026-10-01"
intake:
  stages_done: [0, 1, 2, 3, 4, 5]
YAML
cat intake/stages/06-review.md
```

```text
add_entry: added lanes "tech-writing" in career-profile.yaml
warning: lanes[0].requirements[0]: strong requirement "ai_forward_team" has no why.
warning: lanes[0].requirements[1]: strong requirement "docs_in_version_control" has no why.
warning: lanes[1].requirements: lane "tech-writing" has no requirements of its own.
validate_profile: clean, 9 warning(s) in career-profile.yaml
add_entry: replaced lanes "tech-writing" in career-profile.yaml
warning: lanes[0].requirements[0]: strong requirement "ai_forward_team" has no why.
warning: lanes[0].requirements[1]: strong requirement "docs_in_version_control" has no why.
warning: lanes[1].requirements[0]: strong requirement "expert_access" has no w
... (4351 more characters)
```

Stage 5 is saved. Stage 6 starts with the validator.

```text
$ python3 scripts/validate_profile.py career-profile.yaml
```

```text
validate_profile: clean, 10 warning(s) in career-profile.yaml
warning: evidence[0]: "ev-northwind-api-reference" has no dates, so it cannot be judged recent or stale.
warning: evidence[1]: "ev-northwind-style-guide" has no dates, so it cannot be judged recent or stale.
warning: evidence[2]: "ev-northwind-release-notes" has no dates, so it cannot be judged recent or stale.
warning: evidence[3]: "ev-placeholder-labs-docs-pipeline" has no dates, so it cannot be judged recent or stale.
warning: evidence[4]: "ev-placeholder-labs-ci-checks" has no dates, so it cannot be judged recent or stale.
warning: evidence[5]: "ev-placeholder-labs-style-prompts" has no dates, so it cannot be judged recent or 
... (352 more characters)
```

The validator reports no problems, only warnings. These labels describe the file, not you.

**Gap list by label**
- **confirmed:** nothing. No evidence entry is `checked`, because every link or file was unread or missing.
- **overclaimed** (skill at 4 or 5, all linked evidence unchecked): OpenAPI, Docs as code, Static sites, Prompt writing, Style guides, SME interviews.
- **no record** (skill at 3, only unchecked or interview evidence): CI pipelines, Python scripting.
- **stale:** nothing.
- **underclaimed:** nothing.

**Other gaps**
- All 6 evidence entries have no dates.
- The 4 strong lane requirements have no `why`.
- The 3 hard blocks have no `why`.
- The Lanternfield exception is not written, because the block it overrides is unknown.
- The two lanes' requirements differ, so none look copied.

Each gap gets one question, and the script has no answers for any of them. I'll print them in order. Each one is treated as "leave it", so the gap stays.

ASK: Your file scores OpenAPI at 4, and the only thing behind it is a public page I haven't read. Is there something I can read?
USER: (no scripted answer). Left as is.

ASK: Docs as code is scored 5 and rests on unchecked entries. Is there a page or file I can read?
USER: (no scripted answer). Left as is.

ASK: Static sites is scored 4 and rests on the unchecked docs pipeline entry. Is there a page or file I can read?
USER: (no scripted answer). Left as is.

ASK: Prompt writing is scored 4 and rests on your own account of the style prompts. Is there a page or file I can read?
USER: (no scripted answer). Left as is.

ASK: Style guides is scored 5 and rests on a PDF that isn't in this folder. Is there a copy I can read?
USER: (no scripted answer). Left as is.

ASK: SME interviews is scored 4 and rests only on your account of the release-notes process. Is there anything I can read?
USER: (no scripted answer). Left as is.

ASK: Roughly when did you do the API reference rebuild?
USER: (no scripted answer). Left as is.

ASK: Roughly when did you write the style guide?
USER: (no scripted answer). Left as is.

ASK: Roughly when did you run the release-notes process?
USER: (no scripted answer). Left as is.

ASK: Roughly when did you build the docs pipeline?
USER: (no scripted answer). Left as is.

ASK: Roughly when did you add the link and alt-text checks?
USER: (no scripted answer). Left as is.

ASK: Roughly when did you write the style prompts?
USER: (no scripted answer). Left as is.

ASK: Why does an AI-forward team matter to you?
USER: (no scripted answer). Left as is.

ASK: Why does docs living in version control matter to you?
USER: (no scripted answer). Left as is.

ASK: Why does regular access to experts matter to you?
USER: (no scripted answer). Left as is.

ASK: Why does a say in the authoring tools matter to you?
USER: (no scripted answer). Left as is.

ASK: Why do gambling and betting, weapons makers, and non-remote jobs matter to you as hard blocks?
USER: (no scripted answer). Left as is.

ASK: Does this file feel like a fair picture of you?
USER: Yes, that is a fair picture of me.

```text
$ python3 scripts/add_entry.py career-profile.yaml --section meta --entry - <<'YAML' | tail -1
updated: "2026-10-01"
intake:
  stages_done: [0, 1, 2, 3, 4, 5, 6]
  closing_answer: "Yes, that is a fair picture of me."
YAML
echo ----; python3 scripts/validate_profile.py career-profile.yaml
```

```text
validate_profile: clean, 10 warning(s) in career-profile.yaml
----
validate_profile: clean, 10 warning(s) in career-profile.yaml
warning: evidence[0]: "ev-northwind-api-reference" has no dates, so it cannot be judged recent or stale.
warning: evidence[1]: "ev-northwind-style-guide" has no dates, so it cannot be judged recent or stale.
warning: evidence[2]: "ev-northwind-release-notes" has no dates, so it cannot be judged recent or stale.
warning: evidence[3]: "ev-placeholder-labs-docs-pipeline" has no dates, so it cannot be judged recent or stale.
warning: evidence[4]: "ev-placeholder-labs-ci-checks" has no dates, so it cannot be judged recent or stale.
warning: evidence[5]: "ev-placeholder-
... (419 more characters)
```

All seven stages are done, and `./career-profile.yaml` passes validation with 0 problems and 10 warnings. The final output of `python3 scripts/validate_profile.py career-profile.yaml`:

```
validate_profile: clean, 10 warning(s) in career-profile.yaml
warning: evidence[0]: "ev-northwind-api-reference" has no dates, so it cannot be judged recent or stale.
warning: evidence[1]: "ev-northwind-style-guide" has no dates, so it cannot be judged recent or stale.
warning: evidence[2]: "ev-northwind-release-notes" has no dates, so it cannot be judged recent or stale.
warning: evidence[3]: "ev-placeholder-labs-docs-pipeline" has no dates, so it cannot be judged recent or stale.
warning: evidence[4]: "ev-placeholder-labs-ci-checks" has no dates, so it cannot be judged recent or stale.
warning: evidence[5]: "ev-placeholder-labs-style-prompts" has no dates, so it cannot be judged recent or stale.
warning: lanes[0].requirements[0]: strong requirement "ai_forward_team" has no why.
warning: lanes[0].requirements[1]: strong requirement "docs_in_version_control" has no why.
warning: lanes[1].requirements[0]: strong requirement "expert_access" has no why.
warning: lanes[1].requirements[1]: strong requirement "authoring_tools_say" has no why.
```

The file holds:
- 2 employers
- 6 evidence entries
- 14 skills
- 3 hard blocks
- the pay numbers
- 6 perks
- 2 lanes
- the closing answer, in Robin's words

**Judgment calls to check**
- **Confirmations:** the answers file has no "yes" lines for the read-backs. I treated each scripted answer as the confirmation and wrote it through `scripts/add_entry.py` only.
- **Other unscripted questions:** "Is there another one?" followed whether the file listed more accomplishments. Every other question the file had no answer for was treated as "I don't know", and the field was left out.
- **Nothing is `checked`:** no link or file was read, and `northwind-style-guide.pdf` isn't in the folder. Every evidence entry is `proof: unchecked`.
- **Lanternfield exception not stored:** the answer named the company but not which hard block it overrides. I asked, got no scripted answer, and wrote nothing rather than guess.
- **Inferred links:** I read "managing translation vendors" as the stored `localization_pm` skill, which is already `avoid`, so nothing was written for it. I linked "Reading Go code" to `go_lang`, and the DITA XML and mobile SDK gaps to `dita_xml` and `mobile_sdk`. These were my matches, not the user's.
- **Gaps left open:** the stage 6 gap questions got no scripted answers, so the 6 overclaimed skills stay overclaimed. The only scripted stage 6 answer was the closing one.


## Checks

- Validator exit code: 0 (pass)
```text
warning: evidence[0]: "ev-northwind-api-reference" has no dates, so it cannot be judged recent or stale.
warning: evidence[1]: "ev-northwind-style-guide" has no dates, so it cannot be judged recent or stale.
warning: evidence[2]: "ev-northwind-release-notes" has no dates, so it cannot be judged recent or stale.
warning: evidence[3]: "ev-placeholder-labs-docs-pipeline" has no dates, so it cannot be judged recent or stale.
warning: evidence[4]: "ev-placeholder-labs-ci-checks" has no dates, so it cannot be judged recent or stale.
warning: evidence[5]: "ev-placeholder-labs-style-prompts" has no dates, so it cannot be judged recent or stale.
warning: lanes[0].requirements[0]: strong requirement "ai_forward_team" has no why.
warning: lanes[0].requirements[1]: strong requirement "docs_in_version_control" has no why.
warning: lanes[1].requirements[0]: strong requirement "expert_access" has no why.
warning: lanes[1].requirements[1]: strong requirement "authoring_tools_say" has no why.
validate_profile: clean, 10 warning(s) in career-profile.yaml
```
- employer ids: pass (['northwind', 'placeholder_labs'] vs ['northwind', 'placeholder_labs'])
- lane names: pass (['docs-platform', 'tech-writing'] vs ['docs-platform', 'tech-writing'])
- evidence count within 2: pass (6 vs 7)
- skills count: pass (14 vs 14)
- person: Robin Sample, 9 years
- Skill ids are Robin's own words, not catalog ids: ci_pipelines, dita_xml, docs_as_code, go_lang, kubernetes, localization_pm, mobile_sdk, openapi, ...

Result: PASS
