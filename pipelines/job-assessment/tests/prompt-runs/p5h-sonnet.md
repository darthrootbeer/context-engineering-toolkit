<!-- FICTIONAL EXAMPLE DATA. Not a real person. Saved by tests/prompt-runs/run_prompts.py -->
# Prompt run: Find gaps in my central file (held-out profile), on sonnet

- Prompt file: `prompts/05-find-gaps.txt`
- Date: 2026-10-01. Model alias `sonnet`, which ran as `claude-sonnet-5-5` (Claude Code can add a small helper model call of its own).
- Turns: 1. Cost: $0.07 (the simulated user's calls are not included).
- Grade: see `GRADES.md`.

## Conversation

### User

[the prompt below, with attached files: ARCHITECTURE.md, section 'What the validator checks', fixtures/held-out-gappy-profile.yaml]

I'm attaching the 'What the validator checks' section of ARCHITECTURE.md and my career-profile.yaml. The validator checks shape and consistency, not truth, so find what it cannot catch. Read my whole file the way a skeptical hiring manager and a careful editor would: look for places where the file claims more than its own evidence shows, says something that conflicts with another part of the file, or would make a posting score in a misleading way. Check every section, not only skills. For each weak spot, give the exact YAML path, quote the part that worries you, say why it matters for scoring, and give one question you would ask me to fix it. Do not fill any gap yourself, and do not report a problem you cannot point to in the file. A good answer names only things that are really in the file and gives a YAML path for each one.

### Model

I found 10 weak spots. Each one is in the file, and none of them is something the validator checks.

**1. `hard_blocks[0].match_hints`**
- Quote: `match_hints: [remote, work from home, distributed team]`, under the label "Must be in an office".
- Why it matters: the block is meant to catch office-only postings, but the hints are the words remote postings use. A remote posting would be blocked, and an on-site one would pass.
- Question: Which words in a posting show that a role is office-only, as opposed to remote?

**2. `evidence[0].dates` (`ev-harbor-onboarding`)**
- Quote: `dates: {start: 2018-01, end: 2018-06}`. The linked employer `harbor` runs `start: 2021-03` to `end: 2023-06`.
- Why it matters: the dates fall three years before you worked there, so either the dates or the employer link is wrong. This is the only evidence for `user_guides` (scored 4), so a recency or proof check on that skill would rest on a wrong date.
- Question: When did you write the onboarding guide, and was it at Harbor?

**3. `skills[1].last` (`user_guides`)**
- Quote: `last: 2y`. The evidence ends 2023-06 at the latest, or 2018 as written, and today is 2026-10.
- Why it matters: "2y" is shorter than either date supports, so the skill looks fresher than the file shows. Recency scoring would favor it.
- Question: When did you last write user guides or onboarding material?

**4. `evidence[1].authorship` (`ev-tidewater-migration`)**
- Quote: `claim: Wrote every page of the help center again...` next to `authorship: REVIEWED`.
- Why it matters: the claim says you wrote it and the tag says you reviewed it. This is the only evidence for `docs_as_code` (self_score 4), and it is marked `proof: checked`, so a reader would trust the stronger claim.
- Question: Did you write the pages, review someone else's rewrite, or both, and which pages were yours?

**5. `writing_samples[0]`**
- Quote: `title: Help center home page`, with `evidence_id: ev-tidewater-migration`.
- Why it matters: the sample is one page, but the evidence claims "every page". Because the evidence is tagged `REVIEWED`, a hiring manager opening the link cannot tell whether the sample is your writing.
- Question: Is the home page text yours, and is there a page you wrote that shows the work better?

**6. `skills[0].last` (`docs_as_code`)**
- Quote: `last: 2y`. `employers[1].summary` says "Runs the help center and its build" and `end: present`.
- Why it matters: the employer summary describes current, ongoing use of docs-as-code, but the skill says two years ago. That understates the skill and could cost it points on recency.
- Question: Are you still working in the docs-as-code build today, and if so, is `2y` meant to be something else?

**7. `person.years_experience`**
- Quote: `years_experience: 14`. The `employers` list covers 2021-03 to present, about five and a half years.
- Why it matters: nothing in the file backs the other eight or so years. A posting with a years-required threshold would score on a number the file can't support.
- Question: Where did you work before 2021, and should those jobs be in `employers`?

**8. API work: `person.target_roles`, `lanes[0]`, `skills`**
- Quote: `target_roles: [API Technical Writer]` and the lane `api-docs`. No skill or evidence item mentions an API. The only trace is `employers[0].summary`: "Wrote the admin and API guides".
- Why it matters: the whole target rests on API documentation, yet no skill or evidence covers it. The lane's strong requirement `api_owner` ("Owns the API docs") can't be matched to anything you have shown.
- Question: What API reference or guide work have you done, and where is it shown?

**9. `skills[2]` (`glossaries`)**
- Quote: `self_score: 3`, backed only by `ev-tidewater-glossary` with `proof: unchecked` and `type: interview`, and dates of `2024-02` to `2024-03`.
- Why it matters: the score is the same as a verified skill's, but it rests on one two-month item from an interview. The validator only warns when a skill has no evidence at all, so this passes.
- Question: Is there a document, a link or a person who can confirm the glossary and its term rule?

**10. Culture and keywords**
- `culture.hustle_phrases[1]` and `culture.free_phrases[0]`: `fast-paced` appears in both lists. A posting with that phrase would be flagged as a hustle sign and as a free-time sign at once. Question: Is "fast-paced" a warning or acceptable to you?
- `lanes[0].keyword_signals`: `positive`, `negative` and `strong_negative` are all `[]`, so nothing can lower a posting's score by keyword. The one `strong_positive` phrase (`docs as code`) is literal, while the skill's `match` also accepts `docs-as-code`. Question: Which words in a posting should count against it, and should the hyphenated form count as a positive too?
- `hard_blocks[1].match_hints`: `crypto` would also match "cryptography", which could block security-tool API roles you might want. Question: Do you want postings about encryption or cryptography blocked?
- `culture.perks[0]` (`unlimited_pto`, `kind: big`) next to `low_time_off_days: 15`: a posting that offers unlimited PTO gets a big perk with no days stated, while you track a 15-day floor. Question: Should unlimited PTO count as a big perk, or only when the posting states a number of days?
