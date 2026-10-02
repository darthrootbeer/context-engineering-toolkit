<!-- FICTIONAL EXAMPLE DATA. Not a real person. Saved by tests/prompt-runs/run_prompts.py -->
# Prompt run: Customize the rubric (assessment/README.md), on haiku

Note: the pay figures in this record were changed after the run to fictional ones. Nothing else was edited; the scores and verdicts are as recorded.

- Prompt file: `prompts/r2-customize-rubric.txt`
- Date: 2026-10-01. Model alias `haiku`, which ran as `claude-haiku-4-5-20251001` (Claude Code can add a small helper model call of its own).
- Turns: 6. Cost: $0.33 (the simulated user's calls are not included).
- Grade: see `GRADES.md`.

## Conversation

### User

[the prompt below, with attached files: assessment/README.md, ARCHITECTURE.md, fixtures/robin-sample/career-profile.yaml]

I'm attaching assessment/README.md, ARCHITECTURE.md and my career-profile.yaml. Help me change which perks count as big or nice and which phrases count as hustle, one question at a time, and show the YAML change for each. Do not change the verdict rules.

### Model

I'll help you customize the perks and phrases one decision at a time. Let me start with understanding what you want to adjust.

**First question:** Looking at your current **big perks** (unlimited PTO, learning budget, extra paid days off—each worth +2 to the Culture score)—are all three still things that would genuinely move your interest in a job, or would you like to move one or more down to "nice" (worth +1)?

### User

Yeah, I'd like to move the learning budget down to 'nice'—it's good to have, but it wouldn't really be a dealbreaker for me. Also, while we're at it, can you add 'hackathon weekends' as one of the hustle phrases?

### Model

**Change 1: Move learning budget to nice**

```yaml
# Before
  perks:
    - {id: unlimited_pto, label: Unlimited PTO, kind: big}
    - {id: learning_budget, label: Learning budget, kind: big}
    - {id: extra_days_off, label: Extra paid days off, kind: big}

# After
  perks:
    - {id: unlimited_pto, label: Unlimited PTO, kind: big}
    - {id: learning_budget, label: Learning budget, kind: nice}
    - {id: extra_days_off, label: Extra paid days off, kind: big}
```

This drops a learning budget from +2 to +1 on the Culture score when a posting mentions it.

**Change 2: Add hackathon weekends to hustle phrases**

```yaml
# Before
  hustle_phrases: [rockstar, work hard play hard, on-call, weekend work]

# After
  hustle_phrases: [rockstar, work hard play hard, on-call, weekend work, hackathon weekends]
```

Now if a posting mentions "hackathon weekends," it costs 1 point (up to the 3-point max) on Culture.

Ready for the next change?

### User

Yes, that looks right. And can you make Culture count double in the verdict?

### Model

I can't do that—you asked me not to change the verdict rules, and weighting Culture differently would change rule 4c (the reservations band that checks if Comp or Culture is 3 or lower). That's a verdict rule.

What I can help with is changing which perks and phrases Robin has, so that postings are more or less likely to trigger a high or low Culture score in the first place. For example, if there's a perk that shows up often but doesn't matter much to you, we could remove it from the list entirely, so it wouldn't affect scores at all.

Is there another perk or phrase you'd like to adjust?

### User

That's all, thanks.

### Model

Got it. To summarize your changes:

- **Learning budget** moved from big perk (+2) to nice perk (+1)
- **Hackathon weekends** added to hustle phrases (costs 1 point, max 3 total)

Both are ready to go into your `career-profile.yaml`. Let me know if you'd like me to apply them.

### User

Sure, go ahead and apply them.

### Model

Let me find your career-profile.yaml file first.
<function_calls>
<invoke name="glob">
<parameter name="pattern">**/career-profile.yaml</parameter>
</invoke>
</function_calls>
<function_calls>
<invoke name="glob">
<parameter name="pattern">**/*.yaml</parameter>
</invoke>
</function_calls>
<function_calls>
<invoke name="read">
<parameter name="path">.</parameter>
</invoke>
</function_calls>

I don't see a career-profile.yaml in your working directory. Where is your profile file located, or would you like me to create one based on the Robin Sample fixture?

### User

Just create one based on the Robin Sample fixture—that's easiest. Go ahead and apply those two changes to it.

### Model

<function_calls>
<invoke name="write">
<parameter name="path">career-profile.yaml</parameter>
<parameter name="contents"># FICTIONAL EXAMPLE DATA. Not a real person.
# Robin Sample is an invented person. Every employer, link and number below is made up.
schema_version: 1
person:
  display_name: Robin Sample
  target_roles: [Senior Technical Writer, Docs Platform Engineer]
  years_experience: 9
  location_label: Region B
  working_style: gather_from_experts
sources:
  - {key: board-a, emoji: "📋", label: Job board A}
  - {key: board-b, emoji: "📰", label: Job board B}
hard_blocks:
  - {id: gambling, label: "🎰 Gambling / betting", why: "Robin does not want to help people lose money.", match_hints: [sports betting, casino, online poker]}
  - {id: weapons, label: "🔫 Weapons manufacturing", why: "Robin will not write for a company that makes weapons.", match_hints: [firearms, munitions, weapons systems]}
  - {id: non_remote, label: "🏢 Not remote", why: "Robin needs to work from home.", match_hints: [on-site only, five days in office, must relocate]}
named_exceptions:
  - {company: Lanternfield Example Co., block_id: non_remote, why: "Robin lives a ten minute walk from this office and would go in.", added: "2026-10-01"}
comp:
  currency: USD
  floor: 75000
  min: 80000
  open_ask: 85000
  target: 100000
  stretch_ceiling: 175000
culture:
  perks:
    - {id: unlimited_pto, label: Unlimited PTO, kind: big}
    - {id: learning_budget, label: Learning budget, kind: nice}
    - {id: extra_days_off, label: Extra paid days off, kind: big}
    - {id: offsites, label: Regular meetups or offsites, kind: nice}
    - {id: home_office, label: Home-office or wellness stipend, kind: nice}
    - {id: parental_leave, label: Paid parental leave, kind: nice}
  low_time_off_days: 15
  hustle_phrases: [rockstar, work hard play hard, on-call, weekend work, hackathon weekends]
  free_phrases: [fast-paced]
soft_flags:
  - {id: heavy_meeting_load, label: "Heavy meeting load", why: "Robin writes best in long blocks of quiet time."}
benefits_and_terms:
  - {id: pay_range_listed, label: "Pay range listed in the posting", why: "A listed range saves a round of interviews."}
company_criteria:
  high_interest:
    - {name: Copperline Example Co., why: "Makes tools for writers, which is the work Robin cares about most."}
  good_not_dream:
    - {name: Ashgrove Example Software, why: "Solid product and a fair size, but nothing Robin would move for."}
lanes:
  - name: docs-platform
    emoji: "🔧"
    description: Roles building the systems that produce documentation.
    requirements:
      - {id: ai_forward, label: "✨ AI-forward team", severity: strong, why: "Robin wants to work where AI drafting is normal and checked by people."}
      - {id: docs_as_code, label: "📦 Docs live in version control", severity: strong, why: "Robin's best work is built on review, builds and automated checks."}
      - {id: ci_for_docs, label: "🧪 Docs are built and checked automatically", severity: soft, why: "Nice to have, because Robin can build it."}
      - {id: solo_ownership, label: "🦸 Owns the docs system", severity: soft, bonus: true, why: "Ownership is a bonus, never a requirement."}
    autonomy:
      positive_signals: [chooses the tools, sets own priorities, manager checks in weekly]
      negative_signals: [approval for every change, daily status reports]
    keyword_signals:
      strong_positive:
        - {phrase: definition of done, why: "Documentation counted as part of finished work."}
      positive:
        - {phrase: single source of truth, why: "The team cares about one correct copy."}
      negative:
        - {phrase: wiki cleanup, why: "Often means maintenance work with no building."}
      strong_negative:
        - {phrase: no engineering support, why: "The writer would be on their own."}
    known_gaps:
      - {id: gap_go, label: "Reading Go code", skill_id: go_lang}
  - name: tech-writing
    emoji: "✍️"
    description: Roles writing guides, references and help content for a product.
    requirements:
      - {id: expert_access, label: "🧑‍🔬 Regular access to experts", severity: strong, why: "Robin writes by gathering knowledge from the people who build the product."}
      - {id: tooling_voice, label: "🛠️ A say in the authoring tools", severity: strong, why: "Robin wants to help choose how the docs are made."}
      - {id: style_guide, label: "📖 A written style guide", severity: soft, why: "A shared guide saves arguments."}
    autonomy:
      positive_signals: [owns the content plan, picks the tools]
      negative_signals: [every page needs sign-off from marketing]
    keyword_signals:
      strong_positive: []
      positive:
        - {phrase: writers sit with the engineers, why: "Short path to the experts."}
      negative:
        - {phrase: content mill, why: "Volume over quality."}
      strong_negative: []
    known_gaps:
      - {id: gap_dita, label: "DITA XML authoring", skill_id: dita_xml}
      - {id: gap_mobile_sdk, label: "Mobile SDK documentation", skill_id: mobile_sdk}
employers:
  - {id: northwind, name: Northwind Example Co., title: Technical Writer, start: "2017-02", end: "2021-12", summary: "Wrote and maintained the help center and API reference for a small invented software product."}
  - {id: placeholder_labs, name: Placeholder Labs, title: Senior Technical Writer, start: "2022-01", summary: "Leads documentation for an invented developer tool and runs the system that builds and checks the docs."}
evidence:
  - id: ev-northwind-api-rebuild
    employer_id: northwind
    claim: Moved the API reference from hand-edited pages to pages generated from the API spec.
    details: "Robin wrote the build step and checked the first run against the old pages by hand."
    dates: {start: "2021-03", end: "2021-09"}
    authorship: DIRECTED
    proof: checked
    source: {type: link, ref: "https://example.com/fictional/northwind/api-rebuild", captured_on: "2026-10-01"}
  - id: ev-northwind-style-guide
    employer_id: northwind
    claim: Wrote a 20-page style guide that the whole support team used.
    details: "Robin interviewed six support staff to find the most common mistakes."
    dates: {start: "2018-04", end: "2018-09"}
    authorship: WROTE
    proof: checked
    source: {type: document, ref: "northwind-style-guide.pdf#section-3", captured_on: "2026-10-01"}
  - id: ev-northwind-release-notes
    employer_id: northwind
    claim: Ran a monthly release-notes process that gathered input from product engineers.
    details: "Robin held a 30 minute interview with each engineer before every release."
    dates: {start: "2019-01", end: "2021-12"}
    authorship: WROTE
    proof: unchecked
    source: {type: interview, ref: "interview:2026-10-01:s2.q2", captured_on: "2026-10-01"}
  - id: ev-northwind-team-wiki
    employer_id: northwind
    claim: Was on the team that kept the internal wiki.
    details: "A teammate built the wiki structure. Robin only added pages."
    dates: {start: "2017-06", end: "2018-01"}
    authorship: OTHER-AUTHOR
    proof: do_not_use
    source: {type: reference, ref: "former teammate, engineering role", captured_on: "2026-10-01"}
  - id: ev-placeholder-docs-pipeline
    employer_id: placeholder_labs
    claim: Built a pipeline that publishes the docs from Markdown files kept in Git.
    details: "Robin designed the rules and an AI tool wrote most of the build scripts, which Robin reviewed and tested."
    dates: {start: "2022-05", end: "2022-11"}
    authorship: DIRECTED
    proof: checked
    source: {type: artifact, ref: "example.com/fictional/placeholder-labs/docs-pipeline", captured_on: "2026-10-01"}
  - id: ev-placeholder-ci-checks
    employer_id: placeholder_labs
    claim: Added automatic checks for broken links and missing alt text to every docs change.
    details: "Robin wrote the check rules and a short Python script to run them."
    dates: {start: "2023-02", end: "2023-04"}
    authorship: CO-WROTE
    proof: checked
    source: {type: link, ref: "https://example.org/fictional/placeholder-labs/ci-checks", captured_on: "2026-10-01"}
  - id: ev-placeholder-style-prompts
    employer_id: placeholder_labs
    claim: Wrote the prompts that make an AI assistant draft pages in the team style, then added a human review step.
    details: "Robin wrote and tested the prompts. Reviewers use a short checklist."
    dates: {start: "2024-01", end: "2024-06"}
    authorship: DIRECTED
    proof: unchecked
    source: {type: interview, ref: "interview:2026-10-01:s2.q8", captured_on: "2026-10-01"}
skills:
  - {id: openapi, label: OpenAPI / Swagger, group: api, match: ['openapi|swagger'], self_score: 4, next: more, last: 2y, how: [self, ai], evidence_ids: [ev-northwind-api-rebuild]}
  - {id: docs_as_code, label: Docs as code, group: tooling, match: ['docs.as.code|docs-as-code'], self_score: 5, next: more, last: 2y, how: [self, ai, team], evidence_ids: [ev-placeholder-docs-pipeline, ev-placeholder-ci-checks]}
  - {id: static_sites, label: Static site generators, group: tooling, match: ['static site|mkdocs|docusaurus'], self_score: 4, next: neutral, last: 2y, how: [self, ai], evidence_ids: [ev-placeholder-docs-pipeline]}
  - {id: ci_pipelines, label: Build and check pipelines, group: tooling, match: ['ci/cd|pipeline'], self_score: 3, next: neutral, last: 2y, how: [self, ai], evidence_ids: [ev-placeholder-ci-checks]}
  - {id: python_scripting, label: Python scripting, group: code, match: ['python'], self_score: 3, next: more, last: 2y, how: [self, ai], evidence_ids: [ev-placeholder-ci-checks]}
  - {id: prompt_writing, label: Writing prompts for AI tools, group: ai, match: ['prompt'], self_score: 4, next: more, last: 2y, how: [self], evidence_ids: [ev-placeholder-style-prompts]}
  - {id: style_guides, label: Style guides, group: writing, match: ['style guide'], self_score: 5, next: neutral, last: 5y, how: [self, team], evidence_ids: [ev-northwind-style-guide]}
  - {id: sme_interviews, label: Interviewing experts, group: writing, match: ['subject.matter|sme'], self_score: 4, next: neutral, last: 5y, how: [self], evidence_ids: [ev-northwind-release-notes]}
  - {id: go_lang, label: Go, group: code, match: ['\bgo\b|golang'], self_score: 1, next: neutral, last: 5plus, how: [self], evidence_ids: []}
  - {id: kubernetes, label: Kubernetes, group: code, match: ['kubernetes|k8s'], self_score: 1, next: neutral, last: 5y, how: [self], evidence_ids: []}
  - {id: dita_xml, label: DITA XML, group: writing, match: ['dita'], self_score: 0, next: neutral, last: never, how: [], evidence_ids: []}
  - {id: mobile_sdk, label: Mobile SDK documentation, group: api, match: ['ios|android'], self_score: 0, next: neutral, last: never, how: [], evidence_ids: []}
  - {id: video_tutorials, label: Recording and editing video tutorials, group: media, match: ['video tutorial|screen.capture'], self_score: 2, next: avoid, last: 5plus, how: [self], evidence_ids: []}
  - {id: localization_pm, label: Managing translation vendors, group: process, match: ['translation|localization'], self_score: 2, next: avoid, last: 5y, how: [self], evidence_ids: []}
writing_samples:
  - {id: sample-api-guide, title: "Getting started with the Northwind API", link: "https://example.com/fictional/northwind/getting-started", evidence_id: ev-northwind-api-rebuild}
meta:
  updated: "2026-10-01"
  intake:
    stages_done: [1, 2, 3, 4, 5, 6]
</parameter>
</invoke>
</function_calls>

Done. Created `career-profile.yaml` with both changes applied:
- Learning budget moved to nice perk
- Hackathon weekends added to hustle phrases
