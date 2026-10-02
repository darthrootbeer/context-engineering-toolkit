---
name: job-assessment
description: >
  Go/no-go assessment of one job posting (a link or pasted text) against the
  user's own career-profile.yaml. Archives the posting, loads the one lane's
  checklist, reads the posting and writes a findings JSON file in which every
  rating quotes the posting and every claimed qualification cites an evidence
  id. Scripts then check the findings, compute the four scores (Fit, Comp,
  Qualifications, Culture), apply the verdict rules, write the assessment
  into the archived note, rename it with the verdict emoji, print a terminal
  summary and render an email card whose first element is the live job link.
  Ends with Apply, Apply with reservations, or Skip. Use when the user pastes
  a job posting and asks to assess it, "should I apply to this", or
  "/job-assessment".
---

# Assess a job posting

This skill judges an incoming job posting against the user's own written
criteria. It answers one question: is this posting worth the user's time?

**The core rule: you read, the scripts count.** You (the model) do the
reading: what the posting says, which criterion each sentence touches, how
good the posting's answer is. You write that down as a findings file. You
never compute a score, never add up points, and never decide the verdict.
`check_findings.py` checks your quotes and evidence ids, `score_helpers.py`
does the arithmetic, and `verdict.py` applies the verdict rules. A score or
verdict that did not come out of those scripts is wrong, however reasonable
it looks. If a script refuses your findings, fix the findings. Never work
around the script.

All commands below run from `pipelines/job-assessment/` with `python3`
(3.10 or later, with `pip install -r requirements.txt` done once).

## What you need

| Name used below | What it is |
|---|---|
| `PROFILE` | The user's `career-profile.yaml`. Built by the intake skill, checked by `scripts/validate_profile.py`. It is the only source of criteria, lanes, pay numbers, perks and evidence. |
| `ARCHIVE` | The folder where posting notes are kept. Ask once if unknown, then reuse it. |
| `WORK` | A scratch folder for this run's `findings.json`, `scores.json`, `verdict.json` and `block.md`. Use a fresh one per posting. |
| `OUT` | The folder the email card is written to (for example `out/`). |

Run `python3 scripts/validate_profile.py PROFILE` once at the start. If it
exits 1, stop and show the user its problem lines. A broken profile gives
scores that look real and mean nothing.

## Running: never ask, always finish

Asking for an assessment is the permission to archive, write, rename and
render. Never stop to ask "should I go ahead?". Every run ends with all four
outputs, a Skip included: the note with its assessment block, the renamed
file, the terminal summary and the email card. If a script fails, read its
message, fix the cause, and run it again. Several postings: run the whole
skill once per posting, one note and one card each.

## Step 0: check for an existing note

`parse_posting.py` refuses a duplicate for you. It matches on company, role
and lane, compares job ids taken from the link when there is one, and exits
4 with `DUPLICATE:` and the existing note's path. When that happens, do not
archive again. Re-run steps 2 to 9 against the existing note. The new
assessment block replaces the old one, and the block records the new date.
Only pass `--force` when the user says the posting really changed.

**A second lane is not a duplicate.** The same posting may be assessed once
per lane, and both results are kept, because each lane's rules ask a
different question. `parse_posting.py` archives it as a second note and
prints "Also archived for another lane". Keep two files, never two blocks in
one file. In step 7, cross-link the pair (see "Extra lines in the block").

## Step 1: parse and archive the posting

Read enough of the posting to know the company and the role title. Never
guess either. Then archive it:

```text
python3 assessment/scripts/parse_posting.py posting.txt \
  --company "Examplon Co" --role "Docs Platform Engineer" \
  --lane docs-platform --archive-dir ARCHIVE \
  --url "https://example.com/jobs/123" --source board-a
```

- Pasted text: save it to a file, or pipe it on stdin and leave out the file.
  Always pass `--url` with the real job page so the note and the email can
  link to it.
- A link: pass the URL as the source (needs the `requests` package). If the
  fetch fails, ask the user to paste the text. If the page returns only
  menus or cookie text, look for the company's own job board page, which
  often has the full text. Never assess navigation text.
- `--lane` comes from where the posting came from or what the user said.
  If neither says, read the title and the first responsibilities and pick
  the lane whose `description` fits. If it is still unclear, pick the user's
  main target lane and say in the assessment that the lane was a guess.
- `--source` is a key from the profile's `sources` list, when there is one.

The script prints the requirements split: "likely real" lines describe the
work, "likely filter" lines (degrees, years) mostly track how many people
apply. A miss on a likely-filter line is never a reason to skip on its own.
The note gets the seven identity and state fields (`opportunity_id`,
`source_urls`, `ats_id`, `state`, `state_updated`, `next_action`,
`next_action_due`). Never hand-edit them. A later URL is added to
`source_urls`, never swapped in.

## Step 2: load the one lane's checklist

```text
python3 assessment/scripts/load_criteria.py --profile PROFILE \
  --lane docs-platform --posting "ARCHIVE/<note>.md"
```

Every posting is judged against exactly one lane. A posting judged against
the wrong lane gets a number that looks real and means nothing. The script
is the gate: exit 2 means the lane is not in the profile, exit 3 means the
note's own `lane:` disagrees with `--lane`. Either one prints no checklist.
Do not guess past it. Use the lane the note records.

Read the whole printout every run, never a remembered version. The profile
changes as postings teach the user new things.

**Labels, never ids.** Every place a person reads a criterion (tables, the
terminal, the email) shows its `label` from the profile, never its raw id.
The render scripts do this for you. In your own prose, use the label too.

## Step 3: read the posting against the checklist

Read the archived note's posting text in this order. Write what you find
straight into the findings file (step 4).

### The rating scale (one scale, everywhere)

| Rating | Use when |
|---|---|
| `strong` | The posting's own words clearly confirm this. |
| `fair` | Partly confirmed, or a small miss on a soft item. |
| `weak` | A real concern. The words lean the wrong way. |
| `poor` | The words clearly work against this, or a must-have fails outright. |
| `unknown` | The posting does not say. Not good and not bad. |

The rating answers one question: how good is this posting's answer to this
criterion? It never says how important the criterion is. A soft item that
clearly passes is `strong`. A must-have that clearly passes is also `strong`.
Severity lives in the profile and in your plain-words read ("a miss here is
close to a dealbreaker"), never in the rating.

**Silence is `unknown`.** Any rating other than `unknown` needs a quote, and
the quote must be about the criterion itself. A generic project verb is not
evidence about autonomy: "partner with", "work closely", "collaborate",
"stakeholder", "set deadlines", "escalate" and the like show up in almost
every senior posting. If the only words you can find are generic, the
rating is `unknown`. `check_findings.py` enforces this for autonomy and
micromanagement reads.

### 3a. Hard blocks first

Check every hard block in the printout against what the company builds and
what the job is. A hard block is absolute, but only a real match counts, not
a stretch (a company that merely sells to a sector is not that sector).

Before declaring one, check the profile's `named_exceptions` for this
company and this block. If one exists, it is not a block. Record the
exception's company in `hard_block.named_exception` and assess normally.

If a block trips, record its id and the exact quote. Do not soften it with
"but otherwise strong". Stop the deep checklist. Still fill enough for
context: pay, the autonomy read, and any requirement the posting clearly
answers. A Skip with one row tells the user nothing.

### 3b. Requirements

Rate each lane requirement, one at a time, with a quote and a plain-words
read. A `bonus: true` requirement is a plus when present, never a minus. A
requirement with no words about it stays in the list as `unknown`, with
`quote: null`.

### 3c. Autonomy

Read the posting against the lane's positive and negative autonomy signals.
This is a judgment of tone across the whole posting, not a phrase count.
Set `autonomy.net` (`positive`, `neutral`, `negative` or `unknown`), quote
the words behind it, and write the read as "how much say you would have".

### 3d. Keyword signals

Read each keyword hit in its sentence. "We don't micromanage" and "close
daily oversight" both touch oversight. The sentence decides the meaning.
Record hits in `keyword_signals_found`. Strong positive phrases also go in
`culture.strong_positive_phrases`, negative ones in
`culture.negative_phrases`. A new phrase worth adding to the profile goes
in `new_signals_to_consider` and in your reply. Never add it yourself.

### 3e. Qualifications (can the user do this job?)

Eligibility, judged apart from fit, from the profile's `evidence` only. A
`self_score` is the user's claim, never evidence. Never write a
qualification, number or accomplishment that no evidence entry holds.

1. **Years.** Put the posting's stated minimum in `years_required`. Set
   `narrow_subdomain: true` only when it asks for years in a narrow area the
   user's total does not cover. You do not compare numbers. The script does.
2. **Known gaps.** List each lane `known_gaps` id that a load-bearing
   required line leans on in `known_gaps_hit`. A nice-to-have line does not
   count.
3. **Skills.** Run the matcher:
   ```text
   python3 assessment/scripts/match_skills.py "ARCHIVE/<note>.md" --profile PROFILE
   ```
   It prints every skill the posting mentions, grouped by self-score, with
   the sentence that matched and `BACKED` or `UNPROVEN`. The patterns are
   broad on purpose, so read each hit in its sentence and drop false ones
   (a "vision" pattern hits "dental and vision insurance"). A mention in the
   benefits or the company blurb is not a requirement. Then:
   - Self-score 0 or 1 on a load-bearing required line: add the skill id to
     `self_score_gaps`. If it is already a known gap, list it once only.
   - Self-score 2 (a stretch): mention it in your skill notes. No deduction.
   - A required or standout line matched by a backed skill: add a `matches`
     entry with the posting's line and the evidence ids. Evidence marked
     `proof: unchecked` may be cited. The note will say it is the user's
     own account.
   - A skill scored 3 or higher with no usable evidence: add an `unproven`
     entry. It is never written as a match.
   - `next: avoid` on a skill that is core daily work in this job (not a
     passing mention): add its id to `avoid_core_skills`. Being skilled at
     something is not the same as wanting to do it all day.
   - `next: more` on core daily work: a plus, named in your skill notes.
   - Scored 3 or higher but only ever done by directing AI (`how: [ai]`):
     note that interviews may probe hands-on depth.
   - Last used 5 or more years ago (`last: 5plus`) on a required line: note
     that it is dated.
4. **Working style.** Set `working_style_mismatch: true` when the posting
   expects the user to become the subject expert and the profile says
   `working_style: gather_from_experts`, or the reverse.
5. **Job-type override.** A required skill that has no evidence entry
   behind it at all (checked strictly, no credit for something close) and
   is central to the daily work (among the first two or three
   responsibilities, or named more than once) means this is a different job
   with a familiar title. Set `job_type_override.fired: true` with the skill,
   the quotes, and the evidence ids you checked. Subject knowledge counts as
   a skill: a required "strong understanding of finance" (or law, health
   care and so on) with no evidence fires the override when that subject is
   in the title or most of the duties. Duties about working with experts do
   not rescue it. A skill named once in a list and never in the duties is
   not an override. It belongs in `known_gaps_hit` or `self_score_gaps`.

### 3f. Pay, culture, soft flags

- **Pay is base pay only.** Bonus, commission and stock go in
  `other_pay_noted`, never in the numbers. If no base pay is stated, set
  `stated: false`. That is a neutral unknown, never a bad sign. If pay is
  stated, list every tier the posting gives as
  `{"label": ..., "min": ..., "max": ..., "quote": ...}` using the
  posting's own tier name. Do not pick the tier yourself. The script picks
  it from the profile's location. With a single range and no tiers, list
  that range as one tier.
- **Perks:** only perks in the profile's `culture.perks` list, by
  `perk_id`, each with its quote. Never infer a perk from a company being
  well funded or well known.
- **Time off:** if the posting states yearly paid days, or says time off
  accrues as you earn it, fill `low_time_off` with `days` and/or
  `accrual_only` and the quote. The script decides whether it is low.
- **Hustle language** ("rockstar", on-call, weekend work and the profile's
  `hustle_phrases`): each with its quote. Phrases in `free_phrases` (mild
  ones like "fast-paced") are never listed.
- **Soft flags and benefits terms:** list a soft flag only when the
  posting's own words trip it, with the quote. Unlisted pay is never a soft
  flag. It is already counted once, in Comp. Anything that needs outside
  research (reviews, funding, layoffs) is not fetched. Say the user would
  have to check it, unless the user supplies it.

### 3g. The company itself

Look the hiring company up in `company_criteria`. Set `company_read.status`
to `high_interest`, `good_not_dream` or `none`, and copy the stored reason
word for word. For a high-interest company, tell the user to move fast,
check for a warm introduction, and check the qualifications honestly. For
`none`, record no reaction. Never invent or infer one from fame or funding.

**The company read never changes a score or the verdict.** `verdict.py`
takes no company input at all. Wanting to work somewhere must never lower
the "can I do this job" bar. A company the user loves can still get Skip.
That is the system working.

## Step 4: write the findings file

Write `WORK/findings.json`. It must match `schema/findings.schema.json`:
every top-level key present, nothing extra.

```json
{
  "posting_file": "ARCHIVE/<note>.md",
  "lane": "docs-platform",
  "hard_block": {"tripped": false, "id": null, "quote": null, "named_exception": null},
  "job_type_override": {"fired": false, "skill": null, "quotes": [], "evidence_checked": []},
  "requirements": [{"id": "ai_forward", "rating": "strong", "quote": "Use AI tools every day",
                    "read": "The team uses AI tools every day, which is what you want."}],
  "autonomy": {"net": "positive", "quotes": ["You own the docs platform end to end"],
               "read": "You would decide how the platform works."},
  "pay": {"stated": true, "tier_used": null, "top": null, "other_pay_noted": [],
          "tiers": [{"label": "all other US locations", "min": 98000, "max": 104000,
                     "quote": "Base pay range: $98,000 - $104,000 (all other US locations)"}]},
  "culture": {"perks": [{"perk_id": "learning_budget", "quote": "Annual learning budget"}],
              "strong_positive_phrases": [], "low_time_off": null, "hustle": [],
              "soft_flags_tripped": [], "negative_phrases": []},
  "qualifications": {"years_required": 5, "narrow_subdomain": false, "known_gaps_hit": [],
                     "self_score_gaps": [], "working_style_mismatch": false, "unproven": [],
                     "matches": [{"requirement_quote": "Experience with OpenAPI.",
                                  "evidence_ids": ["ev-northwind-api-rebuild"]}]},
  "avoid_core_skills": [],
  "company_read": {"status": "none", "name": "Examplon Co", "stored_reason": null},
  "verdict_reason": "This looks like a great fit. You would build the docs platform yourself, with AI tools every day.",
  "keyword_signals_found": [],
  "new_signals_to_consider": []
}
```

Rules for the file:

- **Quotes are copied, never paraphrased.** Copy the exact words from the
  posting text below the note's "Full posting text" heading. Case, spacing
  and curly quotes do not matter. Words do. A quote from your own reads or
  the requirements table does not count.
- **Ids come from the profile:** requirement ids from this lane, perk ids,
  hard block ids, skill ids and evidence ids. Never make one up.
- **Leave `tier_used` and `top` as null** when you list tiers. The script
  picks the tier.
- **`verdict_reason` is written before you know the verdict**, from what
  you read. Write it as you would tell a friend about a job you found for
  them: one or two short sentences, warm, plain. Say what matched in real
  terms ("you would own the docs platform") and what still needs
  confirming in real terms ("how good the health plan is"). Never use rubric
  words: no "4a" to "4d", no "job-type override", no "score floor", no
  field names. `check_findings.py` rejects them. If the verdict that comes
  back from step 6 contradicts your sentence (you wrote "great fit" and the
  verdict is Skip), rewrite the sentence to match and re-run steps 5 and 6.
  Never change a rating to change the verdict.

## Step 5: check the findings

```text
python3 assessment/scripts/check_findings.py WORK/findings.json \
  --posting "ARCHIVE/<note>.md" --profile PROFILE
```

Exit 0 prints `check_findings: ok`. Exit 1 prints one problem per line. Fix
the findings and re-run until it passes. Never go on with a failing file.

| The script says | What to do |
|---|---|
| a quote was not found in the posting text | Copy the real words. If no words exist, the rating is `unknown`. |
| a rating has no quote | Add the quote, or make it `unknown`. |
| an autonomy read rests only on generic phrases | Make it `unknown`. The posting is silent. |
| an evidence id is not in the profile, is `do_not_use`, or is someone else's work | Remove the claim, or move the skill to `unproven`. Never point at other evidence just to pass. |
| a perk, hard block, skill or requirement id is unknown | Use the profile's id, or drop the item. |
| the lanes disagree | The note's `lane:` wins. Go back to step 2. |
| `verdict_reason` uses a rubric term | Rewrite it in plain words. |

## Step 6: scores and verdict, from the scripts

```text
python3 assessment/scripts/score_helpers.py WORK/findings.json \
  --profile PROFILE --json > WORK/scores.json
```

This prints the four whole-number scores and a `why` list for each. Then
build the verdict from those scores and the findings, with no numbers typed
by you:

```text
python3 -c "import json,sys; sys.path.insert(0,'assessment/scripts'); import verdict as v; \
s=json.load(open('WORK/scores.json')); f=json.load(open('WORK/findings.json')); \
print(json.dumps(v.decide(s['fit'],s['qualifications'],s['comp'],s['culture'], \
override=v.override_skill(f),hard_block=v.hard_block_id(f))))" > WORK/verdict.json
```

`verdict.json` holds `label`, `trigger` and `rule`. The first rule that
fires wins: hard block, job-type override, the Fit and Qualifications floor,
the reservations band, then Apply (full rules in `ARCHITECTURE.md`). You
report them, never apply them. If `score_helpers.py` exits 1, fix the field
it names (often a pay tier with no number) and go back to step 5. The next
scripts take `apply`, `reservations` or `skip` for the three labels.

## Step 7: write the assessment into the note and rename it

```text
python3 assessment/scripts/render_assessment.py WORK/findings.json \
  --scores WORK/scores.json --verdict WORK/verdict.json --profile PROFILE \
  > WORK/block.md
```

Verdict first, then the reason and the four ten-segment score bars, in the
order Fit, Comp, Qualifications, Culture. Then the tables and reads.

**Extra lines in the block.** Append these at the end of `WORK/block.md`,
only when they apply. Plain prose, no numbers of your own:

- `### 🗒️ Notes on your skills`: the stretch, want-more, directed-AI-only
  and dated notes from step 3e, one short sentence each, naming the skill.
- For a second-lane note: `> **Also assessed in the <lane> lane:** <the other
  note's file name>, verdict <its label>.` Add the matching line to the other
  note's block the next time that note is assessed.
- If the lane was a guess (step 1), one sentence saying so.

Then write it and rename the file:

```text
python3 assessment/scripts/write_assessment.py "ARCHIVE/<note>.md" \
  --block WORK/block.md --verdict apply --date YYYY-MM-DD
python3 assessment/scripts/rename_verdict.py "ARCHIVE/<note>.md" \
  --verdict apply --profile PROFILE
```

`write_assessment.py` puts the block under the `**Application status:**`
line, leaves everything below the divider alone, and replaces an earlier
block on a re-run. Skip sets state `closed`. Apply and Apply with
reservations set `apply_ready` and "Decide: apply, hold, or skip". It never
moves a note past `apply_ready`: applying is the user's decision.

`rename_verdict.py` puts the verdict emoji (🟢 Apply, 🟡 reservations,
🔴 Skip), then source, then lane emoji at the far left of the file name and
`title:`. Re-running swaps old emoji, never stacks them. Never rename by
hand. Use the path printed after `Renamed:` from here on.

## Step 8: print the terminal summary

```text
python3 assessment/scripts/render_assessment.py WORK/findings.json \
  --scores WORK/scores.json --verdict WORK/verdict.json --profile PROFILE --terminal
```

Show its output as-is, not inside a code block, so the table renders. It
ends with the rating legend. Then add one line linking the renamed note (a
`file://` link, or the link the user's notes app uses). Every run ends with
that link, a Skip included. Then two to four plain sentences: the verdict,
the rule that decided it (`verdict.json`'s `rule`, in plain words), and
anything for the user to act on (new signals, outside research, a
high-interest company). Never state a finding that is not in the note.

## Step 9: render the email card

```text
python3 assessment/scripts/render_email.py --note "ARCHIVE/<renamed note>.md" \
  --findings WORK/findings.json --scores WORK/scores.json \
  --verdict WORK/verdict.json --profile PROFILE --out OUT
```

Every verdict gets a card, Skip included. The first thing on the card is a
**View the job posting** button that links to the live job page, above the
verdict. The script takes that link from the note's `url` or `job_url`. If
that is a job-board link and the company's own job page is known, pass the
company page with `--job-url`. It must be a full `https://` link. Never a
link to the note, never a bare domain. With no real link the script stops
with exit 1: find the job page first.

The script runs `check_email.py` on the card, writes nothing if it fails
(exit 2), and prints the file path and a subject that starts with the
verdict dot. It never sends anything. The optional hook in
`assessment/hooks/` blocks a plain-text body if the user mails it with their
own command. For the footer, pass `--next-prompt` with one line built from
this assessment: company, role, verdict, the four scores, the note's path,
and a suggested next step.

## Pending: a posting you could not read

If the posting text could not be fetched and the user is not around to
paste it, do not assess a fragment. If a note exists, mark it with
`rename_verdict.py NOTE --verdict pending --profile PROFILE`. Pending is not
a verdict. There is nothing to score, so there is no card. Tell the user
what is missing and re-run the whole skill once the text is in hand.

## Writing every read in plain words

These rules cover every read you write: requirement reads, the autonomy
read, keyword reads, skill notes and the verdict reason.

- Open with the real thing the posting says, never "this reads as".
- Turn every rule word into its real effect: "a miss here is close to a
  dealbreaker", not "strong-tier". "How much say you would have", not
  "autonomy".
- Short sentences, everyday words, each one making sense on its own.
- Quote the posting when its words matter, then say what they mean.
- Name real things ("the pay range"), never "stuff". One to three
  sentences per read.
- A must-have miss is named outright, never folded into "some tradeoffs".

Not "Strong-tier, soft pass, coordination over ownership." Instead: "This
one matters a lot, and the posting does not say it outright. It talks about
setting deadlines for other people. That sounds more like a coordinator."

## What this skill never does

- Never computes a score, adds points, or picks the verdict.
- Never claims a qualification without an evidence id.
- Never rates silence as anything but `unknown`.
- Never lets the company read touch a score or the verdict.
- Never treats a likely-filter line as a reason to skip by itself.
- Never mixes two lanes in one note.
- Never edits the profile. New signals are suggestions for the user.
- Never sends email, and never fetches outside reviews or funding news.
