<!-- FICTIONAL EXAMPLE DATA. Not a real person. Saved by tests/prompt-runs/run_prompts.py -->
# Prompt run: Find gaps in my central file, on sonnet

- Prompt file: `prompts/05-find-gaps.txt`
- Date: 2026-10-01. Model alias `sonnet`, which ran as `claude-sonnet-5-5` (Claude Code can add a small helper model call of its own).
- Turns: 1. Cost: $0.05 (the simulated user's calls are not included).
- Grade: see `GRADES.md`.

## Conversation

### User

[the prompt below, with attached files: ARCHITECTURE.md, section 'What the validator checks', fixtures/gappy-profile.yaml]

I'm attaching the 'What the validator checks' section of ARCHITECTURE.md and my career-profile.yaml. Find the weak spots the validator cannot catch: skills scored 3 or higher that rest on thin evidence, unchecked evidence a posting would lean on, evidence with no dates, must-haves or hard blocks with no reason, and lanes whose requirements look copied from each other. For each, give the exact YAML path, why it matters for scoring, and one question you would ask me to fix it. Do not fill any gap yourself. A good answer on fixtures/gappy-profile.yaml finds all three planted gaps.

### Model

I found three high-confidence gaps, matching the three the validator's docs say are planted, plus a few lower-priority ones. I changed nothing. The paths are YAML paths, with list indexes counted from 0.

## High confidence

**1. Skill scored 5 on thin evidence: `skills[1]` (docs_ci)**
- **What's there:** `self_score: 5`, one evidence id, `how: [self]`. That evidence is `evidence[1]` (`ev-placeholder-docs-ci`), which is `proof: unchecked`, comes from an interview answer (`source.type: interview`), and covers `dates` 2023-05 to 2023-06, a single month.
- **Why it matters for scoring:** This is the top score on the weakest evidence in the file. It also backs the strong `owns_pipeline` requirement in the docs-platform lane, so postings that stress CI or build ownership will lean on it. The validator only blocks `checked` on interview evidence. It doesn't object to a 5 resting on one unchecked answer.
- **Question:** Is there anything that shows the build check existed and ran, such as a repo link, a config file, a PR, or a colleague who could confirm it? Or is the 5 really about something broader than this one month?

**2. Hard block with no reason: `hard_blocks[1]` (weapons)**
- **What's there:** `gambling` and `non_remote` have `why`. `weapons` has only `label` and `match_hints`.
- **Why it matters for scoring:** A hard block removes a posting outright. Without a reason, nothing separates a firm moral line from a passing preference. The hints `munitions` and `weapons systems` could also catch defense-adjacent or dual-use companies, and nothing says whether that's intended. The validator warns only on strong must-haves with no reason, not on hard blocks.
- **Question:** Why is this a hard block, and does it cover companies that only partly work in defense, such as a cloud vendor with a defense contract, or only makers of weapons?

**3. Lane requirements copied: `lanes[1]` (tech-writing) mirrors `lanes[0]` (docs-platform)**
- **What's there:** In these paths, `lanes[1]` is identical to `lanes[0]`:
  - `lanes[1].requirements` (all three entries, same ids, labels, severities and reasons)
  - `lanes[1].autonomy`
  - `lanes[1].keyword_signals.strong_positive`
- **Why it matters for scoring:** Both lanes will score any posting the same way, so lane choice stops mattering. `owns_pipeline` ("building, not only writing") also contradicts the tech-writing description ("writing and editing"). A pure writing role would be marked down for something this lane shouldn't need. The validator only warns on a lane with no must-haves, and this one has three.
- **Question:** What does a great tech-writing posting have that a docs-platform posting doesn't, and which of these three requirements would you actually drop or downgrade for this lane?

## Lower priority

**4. Requirement with no supporting evidence: `lanes[0].requirements[0]` (ai_forward, strong)**
- **Why it matters:** It's a strong must-have, but no evidence describes AI tool use. Only `skills[0].how` includes `ai`.
- **Question:** What have you done with AI tools in your work that I could record as evidence?

**5. Skill dates that don't match their evidence**
- `skills[0].last: 2y` (openapi) rests on `evidence[0]`, which ended 2021-09, about five years ago.
- `skills[2].last: 2y` (style_guides) rests on `evidence[2]`, which ended 2022-08, about four years ago.
- **Why it matters:** If recency feeds scoring, `last` is either wrong or backed by work that isn't recorded.
- **Question:** For each of these, when did you last use the skill, and is there newer work to record?

**6. Soft requirement with no reason: `lanes[0].requirements[2]` and `lanes[1].requirements[2]` (small_team)**
- **Why it matters:** It's only soft, so the validator ignores it. But the reason determines how much a posting for a large team should be penalized.
- **Question:** Is a small team a real preference or a nice-to-have, and what goes wrong for you on a big one?

**7. Single-source evidence for skills scored 4**
- `skills[0]` (openapi) and `skills[2]` (style_guides) each have one evidence item. Both are checked, so they are sound but narrow.
- `evidence[0].authorship` is `DIRECTED`, not `WROTE`. A posting that wants hands-on spec work may read that as weaker.

## Evidence with no dates

I found none. All three evidence items have `dates`, so the validator's warning has nothing to catch here. The only date weakness is the one-month window on `evidence[1]`, covered in item 1.
