# FICTIONAL EXAMPLE DATA. Not a real person.

# Fixtures

These files were written by directing Claude Code: the author set the rules and the expected results, reviewed the output, and checked the scores against the written rules.

Everything in this folder is invented. Robin Sample is not a real person, the companies do not exist, and every link points at an example domain. The numbers were chosen for the tests and match no real pay, years or thresholds.

## Fictional names used

| Name | Where it appears | What it is |
|---|---|---|
| Robin Sample | `robin-sample/` | The invented job seeker |
| Northwind Example Co. | Robin's first employer | Invented software company |
| Placeholder Labs | Robin's current employer | Invented developer tool company |
| Lanternfield Example Co. | Robin's named exception | Invented company with a nearby office |
| Copperline Example Co. | Posting 01 | Invented hiring company |
| Driftmark Example Media | Posting 02 | Invented hiring company |
| Ashgrove Example Software | Posting 03 | Invented hiring company |

## What each posting is for

| Posting | Lane | Fit | Comp | Qualifications | Culture | Verdict | Rule that decides | What it proves |
|---|---|---|---|---|---|---|---|---|
| `postings/01-strong-fit.md` | docs-platform | 9 | 10 | 9 | 10 | Apply | 4d | Perks beyond the cap still give Culture 10 (5+2+2+1+1 = 11) |
| `postings/02-job-type-override.md` | tech-writing | 7 | 3 | 6 | 5 | Skip | 4a | The job-type rule wins even though the low pay alone would say "reservations". Silence keeps Culture at 5 |
| `postings/03-unlisted-pay-perks.md` | tech-writing | 7 | 5 | 6 | 9 | Apply with reservations | 4c, average | Unlisted pay scores 5, not 0. Culture is 5+2+2 = 9. The Fit and Qualifications average of 6.5 is below 7 |

The same numbers are in machine-readable form in `expected.yaml`.

## Other files

- `robin-sample/career-profile.yaml`: Robin's central file, two lanes, seven evidence entries, fourteen skills.
- `robin-sample/intake-answers.txt`: scripted answers for the intake interview test.
- `gappy-profile.yaml` and `held-out-gappy-profile.yaml`: two profiles that pass the validator with no warnings but have judgment gaps it cannot see. The "find gaps" prompt was tuned on the first. The second is held out: nothing in the prompt describes its gaps. The planted gaps are listed in `tests/test_validate_profile.py`, not here.
- `findings/*.findings.json`: hand-written model output for each posting. Every quote is copied from the posting text.
- Each posting file starts with `company`, `role`, `lane`, `url` and `source` lines, then a divider, then the posting text.

## Planted details worth knowing

- Robin's evidence includes one entry marked `do_not_use` (work a teammate did), which no finding may cite.
- Posting 03 is the only one with a Culture-neutral phrase ("fast-paced") that costs nothing, and the only one with generic collaboration words that must not count as autonomy.
- Posting 01 names the one company in `company_criteria.high_interest`. The company read is shown but never changes the verdict.

---

### Prompt for your AI model

Paste this into any AI model, together with `../ARCHITECTURE.md`, Robin's profile, the three postings and their findings files.

**Test the scoring with the fixture**

<!-- prompt: prompts/04-test-scoring.txt -->
```text
I'm attaching ARCHITECTURE.md, fixtures/robin-sample/career-profile.yaml, the three postings in fixtures/postings/ and their files in fixtures/findings/. For each posting, apply the scoring rules by hand to its findings file. Show the arithmetic for Fit, Comp, Qualifications and Culture, round each the way ARCHITECTURE.md says, then apply the verdict rules in order and name the rule that decided it. Only after all three answers are written, open fixtures/expected.yaml, compare, and list every mismatch with the step where your arithmetic and the file disagree. A good answer matches all three verdicts and all twelve scores.
```

**Tested on:** Claude Sonnet and Claude Haiku through the Claude Code command line, 2026-10-01. Both models passed. Every run, every rewrite and every grade is in `../tests/prompt-runs/GRADES.md`.
