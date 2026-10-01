# Stage 5: Lanes

**Writes:** `lanes[]`
**Rules:** every rule in `../SKILL.md` applies. One question at a time.

A lane is one kind of role, with its own must-haves. Every posting is read
against exactly one lane, and lanes are never mixed. A user looking at one kind
of role still has one lane.

## Questions, in order

Ask one, wait for the answer, then ask the next.

1. "Are you looking at more than one kind of role?"

Then for each kind of role, one at a time:

2. "What short name should this kind of role have?" (lowercase, a word or two,
   for example `tech-writing`)
3. "Which emoji should mark it?"
4. "In one sentence, what is the work?"
5. "Which must-haves are different for this kind of role?"
6. For each must-have named: "How much does [must-have] matter: is it a
   must-have that counts hard, a softer one, or a bonus that never counts
   against a posting?"
7. "What skills does this kind of role want that you don't have yet?"
8. "What language in a posting makes you trust it?"
9. "What language in a posting makes you distrust it?"

The design lists questions 8 and 9 as one question ("trust it, or distrust
it"). It has two asks, so it is asked as two.

## Follow-ups

None in this stage. A must-have with no reason is left without `why`; stage 6
lists it.

## Turning answers into an entry

| Field | From | Notes |
|---|---|---|
| `name` | question 2 | lowercase, `-` or `_` between words |
| `emoji` | question 3 | as given |
| `description` | question 4 | the user's sentence |
| `requirements` | questions 5 and 6 | `{id, label, severity}`. Counts hard → `severity: strong`. Softer → `severity: soft`. Bonus → `severity: soft, bonus: true`. Never raise a severity the user gave. |
| `known_gaps` | question 7 | `{id, label, skill_id}`. Set `skill_id` only when a stored skill matches; otherwise leave it out. |
| `keyword_signals.positive` | question 8 | `{phrase}` per phrase, the user's exact words |
| `keyword_signals.negative` | question 9 | `{phrase}` per phrase, the user's exact words |

Store trust and distrust phrases as `positive` and `negative`. Use
`strong_positive` or `strong_negative` only when the user says a phrase
counts extra. Never promote a phrase on your own.

**When to write.** A lane is complete once `name`, `emoji` and `description`
are confirmed. Write it then with `requirements: []`. Each later answer is
read back and written with `--replace`, sending the whole lane.

```bash
python3 scripts/add_entry.py PROFILE --section lanes --entry - --replace <<'YAML'
name: tech-writing
emoji: "✍️"
description: Roles writing guides, references and help content for a product.
requirements:
  - {id: expert_access, label: Regular access to experts, severity: strong}
YAML
```

The `autonomy` signals of a lane are not asked in this stage. They can be
added later in the same way if the user wants them.

## End of stage

Read back each lane in one short block. If two lanes have the same must-haves,
say so in one sentence and ask whether that is right; copied requirements are
the most common lane mistake. Record stage 5 in `meta.intake.stages_done` and
move to stage 6.
