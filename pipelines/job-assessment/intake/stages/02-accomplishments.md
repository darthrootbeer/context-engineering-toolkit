# Stage 2: Accomplishments

**Writes:** `evidence[]`
**Rules:** every rule in `../SKILL.md` applies. One question at a time.

This is the stage that matters most. The assessment can only claim a
qualification when an evidence entry backs it, so every entry here must be the
user's own account, with an honest label for where it came from.

## Questions, in order

Work one employer at a time, starting with the one the user names first. For
each accomplishment, ask one question, wait, then ask the next.

1. "At [employer], what is one thing you made or changed that you would want a
   hiring manager to know?"
2. "What changed because of it?"
3. "Did you write it yourself, direct a person or an AI tool to make it,
   co-write it, design it for someone else to build, or review someone else's
   work?"
4. "Is there anything that shows it happened: a document, link, repo or page?"
5. "Which skills did it use?"

Loop: aim for 2 to 5 accomplishments per employer. After each one, ask "Is
there another one at [employer]?" When the user says no (or after five), move
to the next employer. After the last employer, ask once: "Is there anything
from outside a job, like a personal project, that you want in the file?"

If stage 0 read a résumé, confirm its accomplishments one at a time instead
of asking question 1 cold: "Your résumé says you wrote a style guide at
Northwind Example Co. Do you want that in the file?" Then ask questions 2 to 5
for it.

## Follow-ups, only when an answer leaves a gap

- A result with no size, when a size would matter: "Roughly how many or how
  big?" Accept "I don't know" or no number. Never suggest one.
- A link, page or repo in the answer to question 4: "Can I read that link now?"
  If yes, read it. If you cannot open it, say so and keep the entry unchecked.

## Turning answers into an entry

| Field | From | Notes |
|---|---|---|
| `id` | the claim | `ev-<employer id>-<two or three words>`, for example `ev-northwind-style-guide` |
| `employer_id` | the employer being asked about | `null` for a personal project |
| `claim` | question 1 | the user's sentence, trimmed of filler only. No added results, adjectives or scope. |
| `details` | questions 2 and 5, and any extra detail from question 3 | the user's words. Put the question 5 answer last, as "Skills used (own words): ...", so stage 3 can read it back. |
| `dates` | only if the user gave them | stage 2 does not ask for dates. Leave the field out; stage 6 lists it as a gap. |
| `authorship` | question 3 | see the table below |
| `proof` and `source` | question 4 | see the table below |

**Authorship, from the user's answer to question 3:**

| The user said | `authorship` |
|---|---|
| wrote it, built it, did it myself | `WROTE` |
| directed a person or an AI tool, had it made, wrote the prompts and checked the result | `DIRECTED` |
| wrote it with someone, co-wrote, paired | `CO-WROTE` |
| designed it, someone else built it | `DESIGNED` |
| reviewed, edited or approved someone else's work | `REVIEWED` |
| was on the team, but someone else did it | `OTHER-AUTHOR`, with `proof: do_not_use` |

If the answer names two modes for the work as a whole ("I directed it and
wrote some of it"), ask: "Which one describes the work as a whole?" Store that
one, and put the user's full answer in `details`. If the user gives a plain
answer like "I directed the work. I wrote the build step myself", the first
sentence is about the work as a whole: store `DIRECTED` and keep the second
sentence in `details`. Never pick the mode that gives more credit.

**Source, from the user's answer to question 4:**

| The user said | `source` | `proof` |
|---|---|---|
| nothing to show | `{type: interview, ref: "interview:<date>:s2.q<n>"}`, where `<n>` is the number of the question 1 that opened this accomplishment | `unchecked` |
| a file they have (PDF, doc) | `{type: document, ref: "<file name>"}` | `unchecked` until you read it, then `ref: "<file name>#<section>"` and `checked` |
| a public page | `{type: link, ref: "<the full https URL as given>"}` | `unchecked` until you read it, then `checked` |
| a repo, file path or published artifact | `{type: artifact, ref: "<as given>"}` | `unchecked` until you read it, then `checked` |
| a colleague who could vouch | `{type: reference, ref: "<their role only>"}` | `unchecked`. Never store the colleague's name or contact. |

Copy a URL or path exactly as the user gave it. Do not add `https://` or fix
it. If it looks wrong, ask.

Every evidence entry has a source. No exceptions. Add `captured_on` with
today's date.

**When to write.** The entry is complete once questions 1, 3 and 4 are
answered. Write it then. Question 5 (and any follow-up) updates it with
`--replace`.

```bash
python3 scripts/add_entry.py PROFILE --section evidence --entry - <<'YAML'
id: ev-northwind-style-guide
employer_id: northwind
claim: Wrote a 20-page style guide that the whole support team used.
details: "Support answers got more consistent."
authorship: WROTE
proof: unchecked
source: {type: document, ref: "northwind-style-guide.pdf", captured_on: "2026-10-01"}
YAML
```

## End of stage

Read back the list of claims, one line each with its authorship and source
type. Ask whether any of them overstates what happened. If the user corrects
one, fix it with `--replace`. Then record stage 2 in `meta.intake.stages_done`
and move to stage 3.
