# Stage 4: Needs

**Writes:** `hard_blocks`, `named_exceptions`, `comp`, `culture`, `soft_flags`,
`benefits_and_terms`, `company_criteria`, `person.location_label`,
`person.working_style`
**Rules:** every rule in `../SKILL.md` applies. One question at a time.

This stage records what the user needs from a job. These answers decide hard
blocks, the Comp score and the Culture score, so the read-back must say which
list each answer lands in and what that list does.

## Questions, in order

Ask one, wait for the answer, then ask the next.

1. "Which kinds of company would you never work for?"
   This is the one question with a starter menu. Offer it as options, never as
   a default: gambling or betting, weapons, tobacco, payday lending, adult
   content, jobs that are not remote, jobs with heavy travel. The user can pick
   none, some, or name their own.
2. "Is there any one-off exception: one company you would work for even though
   it trips one of those?"
3. "What is the lowest base pay you would take if everything else were
   perfect?"
4. "What base pay would you normally accept?"
5. "What would you ask for?"
6. "What would feel like a great offer?"
7. "What is the most you could see a role like this paying?"
8. "Where are you, for picking a pay tier when a posting lists pay by
   location?" (a region label is enough; no address)
9. "Which perks would really change your mind about a job?"
10. "How much yearly paid time off is too little?"
11. "Which phrases in a job ad make you wary?"
12. "What work would you rather avoid, even if you are good at it?"
13. "Do you prefer gathering knowledge from experts, or becoming the expert
    yourself?"
14. "Which companies do you actually want to work for, and why?"

## Follow-ups, only when an answer leaves a gap

- A must-have or a hard block with no reason: "Why does this matter to you?"
  Store the answer as `why`, in the user's words. If the user would rather not
  say, leave `why` out.
- A perk with no weight given: "Is [perk] a big one, or a nice one?" (big adds
  2 to Culture, nice adds 1).
- A pay answer in another currency, or per hour: "Which currency, and is that
  per year?" Store yearly numbers in one currency. Do not convert currencies
  yourself.

No other follow-ups in this stage.

## Turning answers into entries

**Question 1, `hard_blocks`.** One entry per kind of company:
`{id, label, why}`. The label is the user's words. Add `match_hints` only from
words the user said; never add your own list of related terms.

**Question 2, `named_exceptions`.** `{company, block_id, why, added}`, where
`block_id` is the id of the hard block it overrides and `added` is today's
date. If the user names a company but not which block it overrides, ask.

**Questions 3 to 7, `comp`.** One number per answer:
`floor` (3), `min` (4), `open_ask` (5), `target` (6), `stretch_ceiling` (7),
plus `currency` (a three-letter code such as `USD`). Store the number as given,
never rounded. "I don't know" leaves that key `null`. The door refuses numbers
out of order (floor ≤ min ≤ open_ask ≤ target ≤ stretch_ceiling); if it
does, read the two numbers back and ask which one is right.

**Question 8, `person.location_label`.** The user's words, as short as they
gave them.

**Question 9, `culture.perks`.** `{id, label, kind}` per perk, `kind: big` or
`kind: nice`. The `culture` section is a mapping, so send the whole `perks`
list each time.

**Question 10, `culture.low_time_off_days`.** A whole number of days. "Fewer
than 15 days" is stored as `15`.

**Question 11.** Phrases that make the user wary go in `culture.hustle_phrases`
(each found in a posting costs 1 Culture point, at most 3). Phrases the user
names but says do not bother them go in `culture.free_phrases` (they cost
nothing). A worry that is a condition rather than a phrase, such as "lots of
meetings", is a `soft_flags` entry `{id, label, why}` (costs 1 point). A
benefit or term the user wants to see, such as "pay listed in the ad", is a
`benefits_and_terms` entry `{id, label, why}`. Say which list each lands in
during the read-back.

**Question 12, avoided work.** This updates `skills[]`, not a stage 4 section.
For each kind of work named:
- If a stored skill matches it, read back that skill with `next: avoid` and,
  on a yes, write it with `--replace`. If the stored skill already says
  `avoid`, say so and write nothing.
- If no stored skill matches, ask the stage 3 score question for it ("From 0
  to 5, ..."), then write a new skill with `next: avoid`.

Avoiding work you are good at is allowed. Never argue the user out of it.

**Question 13, `person.working_style`.** `gather_from_experts` or
`become_expert`.

**Question 14, `company_criteria`.** Ask, for each company named, whether it
is a high-interest company or a good one that is not a dream, unless the user
already said. `high_interest` or `good_not_dream`, each `{name, why}`. This
list is shown in an assessment, and never changes a score or a verdict. Say so
in the read-back.

## Example writes

```bash
python3 scripts/add_entry.py PROFILE --section hard_blocks --entry - <<'YAML'
id: gambling
label: Gambling and betting
YAML
```

```bash
python3 scripts/add_entry.py PROFILE --section comp --entry - <<'YAML'
currency: USD
floor: 75000
YAML
```

## End of stage

Read back the whole needs picture in one short block: hard blocks, the five pay
numbers in order, perks by weight, time off, wary phrases, avoided work,
working style, companies. Record stage 4 in `meta.intake.stages_done` and move
to stage 5.
