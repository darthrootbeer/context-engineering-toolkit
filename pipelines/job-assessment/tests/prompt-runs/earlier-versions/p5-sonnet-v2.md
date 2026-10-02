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

I found the three planted gaps, plus a few smaller ones. I changed nothing in the file.

## 1. Skills scored 3+ on thin evidence

**`skills[1]` (`docs_ci`), `self_score: 5`, `evidence_ids: [ev-placeholder-docs-ci]`**
- **Why it matters:** The top score rests on one item. That item is `unchecked`, comes from an interview (`evidence[1].source`), and spans one month (`evidence[1].dates`: 2023-05 to 2023-06). `how` is `[self]` only, so nobody else vouches for it. A posting that leans on CI and build skill would get a 5 that nothing backs up.
- **Question:** "Besides the broken-link check, what else have you built or maintained in the docs pipeline, and is there a commit, config file or teammate who could confirm it?"

**`skills[0]` (`openapi`), `self_score: 4`**
- **Why it matters:** The only evidence is `evidence[0]`, which is dated 2021 and marked `authorship: DIRECTED`. That shows you led the change, not that you hands-on wrote OpenAPI specs. `last: 2y` also doesn't match evidence that ends in 2021-09.
- **Question:** "Have you written or edited OpenAPI specs yourself, and when did you last do it?"

**`skills[2]` (`style_guides`), `last: 2y`** (minor)
- **Why it matters:** The evidence is one document from 2022 (`evidence[2].dates`), and `last: 2y` is a stretch from there. The 4 itself is reasonably supported.
- **Question:** "Have you updated or applied the style guide since 2022, and is there anything newer to point to?"

## 2. Unchecked evidence a posting would lean on

**`evidence[1].proof: unchecked`** (`ev-placeholder-docs-ci`)
- **Why it matters:** This is the only evidence behind the skill scored 5, and it supports the "owns the docs build" requirement in `lanes[0].requirements[1]`. It is the most likely thing for a posting to test, and it is the least verified.
- **Question:** "Is there a link, a repo file, a PR, or a reference who can confirm the link-check work so it can move to `checked`?"

**`writing_samples[0].evidence_id`**
- **Why it matters:** The sample is a getting-started guide, but it points at `ev-northwind-api-rebuild`, which is about generating the API reference. The sample doesn't clearly prove that claim, and the evidence is `DIRECTED`, not `WROTE`.
- **Question:** "Did you write the getting-started guide yourself, and does it belong with a different piece of evidence?"

## 3. Evidence with no dates

None here. Every evidence item and employer has dates, which is why the validator is silent. Two things to check anyway:
- `evidence[1].dates` is a one-month window. Was the work really that short, or is the range just when it shipped?
- Several skills claim `last: 2y`, but the dated evidence for them is older than that. See section 1.

## 4. Must-haves or hard blocks with no reason

**`hard_blocks[1]` (`weapons`) has no `why`**
- **Why it matters:** The validator only warns about strong must-haves, not hard blocks. A hard block removes a posting outright, so an unexplained one can't be judged on borderline cases such as defense-adjacent software or dual-use tools.
- **Question:** "What is the line for you: only makers of weapons, or also companies that sell software or services to them?"

**`hard_blocks[2].match_hints` includes `hybrid`** (`non_remote`)
- **Why it matters:** The `why` says you won't relocate and work from home, but the hint blocks hybrid roles too. Whether hybrid is acceptable changes which postings get screened out.
- **Question:** "Is a hybrid role with a few office days within walking or commuting range ever acceptable?"

**`lanes[0].requirements[2]` and `lanes[1].requirements[2]` (`small_team`), `severity: soft`, no `why`**
- **Why it matters:** It's soft, so the validator won't flag it. It still sways scoring, and without a reason it can't be weighed against other signals.
- **Question:** "What does 'small' mean to you in headcount, and what goes wrong for you on a larger team?"

## 5. Lanes whose requirements look copied

**`lanes[1]` (`tech-writing`) duplicates `lanes[0]` (`docs-platform`) in:**
- `lanes[1].requirements`: same three ids, severities and reasons.
- `lanes[1].autonomy`: same positive and negative signals.
- `lanes[1].keyword_signals`: same `docs as code` phrase.

- **Why it matters:** The validator only checks that each lane has some must-haves, not that they differ. With identical rules, both lanes score every posting the same, so the lane choice tells you nothing. `owns_pipeline` as a strong must-have also contradicts `lanes[1].description` ("writing and editing"): a writing-focused role would normally not own the build. That makes the `tech-writing` lane unlikely to match the roles it is meant to find.
- **Question:** "For a role that is mostly writing, which of these must-haves would you actually insist on, and what would you want to see that the docs-platform lane doesn't ask for?"

Related: `lanes[1].known_gaps` is empty while `lanes[0].known_gaps` names Kubernetes. Is Kubernetes really irrelevant to the writing lane, or did that lane just never get the same review?
