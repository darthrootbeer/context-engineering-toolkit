<!-- FICTIONAL EXAMPLE DATA. Not a real person. Saved by tests/prompt-runs/run_prompts.py -->
# Prompt run: Find gaps in my central file, on sonnet

- Prompt file: `prompts/05-find-gaps.txt`
- Date: 2026-10-01. Model alias `sonnet`, which ran as `claude-sonnet-5-5` (Claude Code can add a small helper model call of its own).
- Turns: 1. Cost: $0.09 (the simulated user's calls are not included).
- Grade: see `GRADES.md`.

## Conversation

### User

[the prompt below, with attached files: ARCHITECTURE.md, section 'What the validator checks', fixtures/gappy-profile.yaml]

I'm attaching the 'What the validator checks' section of ARCHITECTURE.md and my career-profile.yaml. The validator checks shape and consistency, not truth, so find what it cannot catch. Read my whole file the way a skeptical hiring manager and a careful editor would: look for places where the file claims more than its own evidence shows, says something that conflicts with another part of the file, or would make a posting score in a misleading way. Check every section, not only skills. For each weak spot, give the exact YAML path, quote the part that worries you, say why it matters for scoring, and give one question you would ask me to fix it. Do not fill any gap yourself, and do not report a problem you cannot point to in the file. A good answer names only things that are really in the file and gives a YAML path for each one.

### Model

I found 13 weak spots, ordered roughly by how much they would distort scoring. Each one gives the path, the quoted text, why it matters, and one question for you. I haven't filled in any answers.

## Skills and evidence

**1. `skills[1].self_score` (docs_ci)**
- Quote: `self_score: 5`, `how: [self]`, `evidence_ids: [ev-placeholder-docs-ci]`
- Why it matters: The top score rests on one item, `evidence[1]`, which is `proof: unchecked`, comes from an interview, and has `dates: {start: 2023-05, end: 2023-06}`. That is one month. A posting that asks for CI skill gets maximum credit for a claim nothing in the file backs up, and it is the same skill your strong `owns_pipeline` requirement leans on.
- Question: Beyond that one month in 2023, what else shows you have worked on docs builds and CI checks, and what would a reviewer be able to open to see it?

**2. `skills[0].last`, `skills[2].last`, `skills[1].last` (all `2y`) against the evidence dates**
- Quote: openapi `last: 2y`, style_guides `last: 2y`, docs_ci `last: 2y`
- Why it matters: Today is 2026-10-01. The newest evidence for openapi ends 2021-09, for style_guides 2022-08, and for docs_ci 2023-06. That is about 5, 4 and 3 years ago. If recency is used in scoring, all three are overstated, and the file itself shows no more recent use.
- Question: For each of these three skills, what is the most recent piece of work you did with it, and where is it recorded?

**3. `skills[0].how` (openapi)**
- Quote: `how: [self, ai]`
- Why it matters: It claims AI-assisted learning or use for OpenAPI. No evidence item mentions AI and no skill covers AI tools. This is also the only support in the file for your strong `ai_forward` requirement.
- Question: What did you actually do with AI tools on OpenAPI work, and when?

**4. `evidence[2].source` and `evidence[2].proof` (style guide)**
- Quote: claim: "Wrote the team style guide **and the review checklist that goes with it**"; `proof: checked`; `ref: "style-guide.pdf#introduction"`
- Why it matters: The claim has two parts, but the checked source points at the introduction. The checklist half is marked verified without any pointer to it, so `skills[2]` (score 4) gets credit for both.
- Question: Which part of the document did you check, and does it show the checklist as well as the guide?

**5. `evidence[0]` (Northwind API rebuild)**
- Quote: `authorship: DIRECTED`, `proof: checked`, details: "Robin's own words: the reference stopped drifting from the real API."
- Why it matters: Two things sit under one `checked` mark. The link may verify that the work existed, but the outcome is described as your own words. `DIRECTED` also sits oddly with `employers[0].title: Technical Writer`, and the file never says what you directed, who you directed, or what generated the pages. This item is the only evidence behind `skills[0]` (score 4).
- Question: What exactly did the checked link show, and who or what did you direct in this project?

**6. `writing_samples[0].evidence_id`**
- Quote: title "API getting-started guide", `evidence_id: ev-northwind-api-rebuild`
- Why it matters: The linked evidence is about generating the API reference from the spec. A getting-started guide is a different artifact, so the sample may not show the work it is attached to. The file also has no sample from Placeholder Labs.
- Question: Is the getting-started guide part of the API rebuild, and which sample best shows your current work?

## Lanes

**7. `lanes[0]` and `lanes[1]` are identical below the description**
- Quote: both lanes have the same `requirements` (`ai_forward`, `owns_pipeline`, `small_team`), `autonomy`, and `keyword_signals`.
- Why it matters: The two lanes cannot score a posting differently, since only the name, emoji and description differ. The validator's "lane with no must-haves of its own" warning doesn't fire because each lane has some.
- Question: What is the one thing that would make you rank a posting higher in tech-writing than in docs-platform, or the other way round?

**8. `lanes[1].requirements[1]` (owns_pipeline in tech-writing)**
- Quote: lane description "Roles writing and editing technical content"; requirement `owns_pipeline`, `severity: strong`, why "The point of the role is building, not only writing."
- Why it matters: This contradicts the lane's own description. A pure writing or editing role would take a strong miss in the lane meant for it.
- Question: Is owning the docs build a must-have for the writing lane, or only for docs-platform?

**9. `lanes[0].requirements[0]` and `lanes[1].requirements[0]` (ai_forward, strong)**
- Quote: `why: Robin wants to keep working with AI tools daily.`
- Why it matters: "Keep working" says this is current practice, yet the skills and evidence contain no AI-tool work apart from the `ai` tag in item 3. A strong requirement therefore penalizes postings on a preference the file doesn't back.
- Question: Which AI tools do you use daily now, and for what?

**10. `lanes[*].keyword_signals`**
- Quote: `strong_positive: [{phrase: docs as code, why: Matches how Robin works.}]`, with `positive: []`, `negative: []`, `strong_negative: []`
- Why it matters: Nothing in either lane lowers a score through keywords, so postings can only go up. "Docs as code" is also called how you work, but no skill or evidence names git, static site generators or Markdown tooling.
- Question: Which phrases in a posting would make you want to skip it, and which evidence shows you work docs-as-code?

## Hard blocks and culture

**11. `hard_blocks[2].match_hints`**
- Quote: `match_hints: [on-site, in-office, hybrid]`
- Why it matters: These are broad. "Hybrid" appears in many developer-platform postings that are about hybrid cloud, and "in-office" can appear in a remote posting's perks text. Either could trigger a hard block on a remote-friendly role. Separately, `hard_blocks[1]` (weapons) has no `why`, unlike the other two blocks.
- Question: Which of these hints do you want to block a posting on its own, and why do you rule out weapons makers?

**12. `culture.perks[0]` against `culture.low_time_off_days`**
- Quote: `{id: unlimited_pto, ..., kind: big}` and `low_time_off_days: 15`
- Why it matters: You treat 15 days as too few, but you also reward unlimited PTO as a big perk. A posting that says "unlimited PTO" with no stated days gets full credit and can't be checked against your own threshold.
- Question: If a posting says unlimited PTO and gives no number of days, should it count as a big perk, as unknown, or as a flag?

## Pay and completeness

**13. `comp.stretch_ceiling` and `meta.intake.stages_done`**
- Quote: `target: 100000`, `stretch_ceiling: 175000`; `stages_done: [1, 2, 3, 4, 5, 6]`
- Why it matters: The ceiling is 75% above target and far above `open_ask: 85000`, so a mid-range posting could score as either a good or a poor match. The file also doesn't say whether the numbers mean base or total pay, or per year. Meanwhile `stages_done` claims every intake stage is finished, yet `company_criteria.good_not_dream` is `[]`, three keyword lists are empty, and `evidence` has only three items.
- Question: What do these pay numbers cover, and which intake stage did you actually finish for the empty sections?
