# Stage 6: Review

**Writes:** `meta` (and fixes to any section, through `add_entry.py --replace`)
**Rules:** every rule in `../SKILL.md` applies. One question at a time.

This stage checks the file, lists what it can and cannot back up, and asks the
user about each gap once. It does not grade the user and does not fill any gap
itself.

## Step 1: run the validator

```bash
python3 scripts/validate_profile.py PROFILE
```

- **Problems** (lines without `warning:`) must be fixed before the interview
  ends. Each one names a YAML path. Explain it to the user in one plain
  sentence, ask the one question that fixes it, read the fix back, and write
  it with `add_entry.py`. Run the validator again until it prints no problems.
- **Warnings** are kept as a list for step 2. They are allowed in a finished
  file.

## Step 2: the gap check

Look for the weak spots the validator cannot judge:

- skills scored 3 or higher with no `evidence_ids`;
- `proof: unchecked` evidence that a posting would lean on (a skill at 4 or 5
  that rests only on it);
- evidence with no `dates`;
- must-haves (lane requirements) and hard blocks with no `why`;
- lanes whose requirements look copied from each other.

Then label every claim in the file with one of five words. Show the list to
the user, grouped by label:

| Label | Means |
|---|---|
| **confirmed** | backed by at least one `proof: checked` evidence entry |
| **no record** | a skill at 3 or higher, or a claim, with no evidence entry, or only an interview answer behind it |
| **stale** | a skill at 3 or higher whose `last` is `5plus`, or whose only evidence ended more than five years ago |
| **overclaimed** | a skill at 4 or 5 where every linked entry is `unchecked`, or is `REVIEWED` work while the skill is about doing it |
| **underclaimed** | checked evidence shows a skill the user scored 0 to 2, or did not score |

These labels describe the file, not the person. Say that once.

## Step 3: one question per gap

Ask about each gap, one question at a time, in the order of the list. Examples:

- "Your file scores writing prompts at 4, and the only thing behind it is your
  own account of the style prompts. Is there a page or file I can read?"
- "The style guide entry has no dates. Roughly when did you write it?"
- "Your file scores OpenAPI at 1, but the API reference rebuild used it. Do you
  want to change the score?"

What the user says decides it:

- New proof, a date, or a reason: read back the corrected entry and write it
  with `--replace`.
- "Leave it": leave it. The gap stays, and the assessment will report it as
  unproven or unknown.
- A lower score or a correction: write it. Never argue for a higher one.

Never change a score, an authorship mode or a proof value without the user's
answer. A lower `proof` is never upgraded because you think the work is real.

## Step 4: the closing question

Ask exactly this, and wait:

**"Does this file feel like a fair picture of you?"**

Store the answer in the user's own words, unedited, in
`meta.intake.closing_answer`, together with the full `stages_done` list:

```bash
python3 scripts/add_entry.py PROFILE --section meta --entry - <<'YAML'
updated: "2026-10-01"
intake:
  stages_done: [0, 1, 2, 3, 4, 5, 6]
  closing_answer: "Yes, that is a fair picture of me."
YAML
```

If the answer is "no" or "not quite", ask what feels wrong, one question at a
time, and fix those entries before storing the closing answer. Never override
the user's own read of the file with your own.

## End of interview

Run the validator one last time and show its output. Tell the user, in two or
three sentences, what the file now holds, how many claims are confirmed, and
that the assessment can be run against it.
