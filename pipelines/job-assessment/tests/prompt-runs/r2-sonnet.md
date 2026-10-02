<!-- FICTIONAL EXAMPLE DATA. Not a real person. Saved by tests/prompt-runs/run_prompts.py -->
# Prompt run: Customize the rubric (assessment/README.md), on sonnet

- Prompt file: `prompts/r2-customize-rubric.txt`
- Date: 2026-10-01. Model alias `sonnet`, which ran as `claude-sonnet-5-5` (Claude Code can add a small helper model call of its own).
- Turns: 6. Cost: $0.72 (the simulated user's calls are not included).
- Grade: see `GRADES.md`.

## Conversation

### User

[the prompt below, with attached files: assessment/README.md, ARCHITECTURE.md, fixtures/robin-sample/career-profile.yaml]

I'm attaching assessment/README.md, ARCHITECTURE.md and my career-profile.yaml. Help me change which perks count as big or nice and which phrases count as hustle, one question at a time, and show the YAML change for each. Do not change the verdict rules.

### Model

Here's your current setup, so we start from the same place.

**Perks now (in `culture.perks`)**
- Big (+2 each): Unlimited PTO, Learning budget, Extra paid days off
- Nice (+1 each): Regular meetups or offsites, Home-office or wellness stipend, Paid parental leave

**Hustle phrases now (`culture.hustle_phrases`):** rockstar, work hard play hard, on-call, weekend work
**Free phrases now (`culture.free_phrases`):** fast-paced

Two things to know before you decide:
- Culture starts at 5 and is capped at 10, so three big perks already reach the cap with nothing else going on. Adding more big perks makes each one worth less.
- Changing `kind` only changes the +2 or +1. The verdict rules stay as they are.

**Question 1 of several: which perks, if any, should move between big and nice?**

Unlimited PTO is the one I'd look at first. Many postings advertise it, and it often means people take less time off. Your low-time-off check (`low_time_off_days: 15`) can't catch that. Moving it to nice would look like this:

```yaml
# before
- {id: unlimited_pto, label: Unlimited PTO, kind: big}
# after
- {id: unlimited_pto, label: Unlimited PTO, kind: nice}
```

Tell me which of these you want:
1. Move Unlimited PTO to nice, as shown above.
2. Keep it big.
3. Move a different perk, or more than one. Tell me which and which direction.

Once you answer, I'll show the exact YAML for your choice and then ask about adding new perks, then the hustle phrases.

### User

I want to move Learning budget to nice. It seems like the kind of thing companies add to look good, but actual support varies a lot from place to place.

### Model

Here's the change for Learning budget:

```yaml
# culture.perks
# before
- {id: learning_budget, label: Learning budget, kind: big}
# after
- {id: learning_budget, label: Learning budget, kind: nice}
```

I left the `id` unchanged because the checker matches perks by id. A posting that mentions a learning budget still gets credit, now +1 instead of +2.

Your perks now stand like this:
- **Big (+2):** Unlimited PTO, Extra paid days off
- **Nice (+1):** Learning budget, Regular meetups or offsites, Home-office or wellness stipend, Paid parental leave

I kept Unlimited PTO as big, since you only asked to move Learning budget. Tell me if you want to revisit it.

If you ever score the Robin sample fixture with this change, its posting 03 Culture score would drop from 9 to 8, because the Learning budget perk there would be worth 1 instead of 2. Make these edits in your own `career-profile.yaml`, not in the fixture, or the fixture tests will fail against `expected.yaml`.

**Question 2: is there a perk missing from your list that you'd count as big or nice?**

A perk can only add to Culture if it's in `culture.perks`, so anything not listed is ignored. Candidates people often add:
- Four-day week or summer Fridays (big)
- Equity or profit sharing (nice)
- Sabbatical (big)
- Conference travel paid (nice)
- Flexible hours (nice)

If you pick one, the YAML would look like this, using a new unique id:

```yaml
- {id: four_day_week, label: Four-day week, kind: big}
```

Tell me which of these you want, give me your own perks with big or nice for each, or say none and we'll move on to hustle phrases.

### User

None of those—I think the ones we have are solid. Let's move on to the hustle phrases.

### Model

Here's how hustle phrases work now:

- Each hustle phrase the model quotes from a posting costs 1 Culture point, up to 3 in total.
- A phrase on `free_phrases` costs nothing, and "fast-paced" is on yours.
- Per Interpretation 9, the model can quote a hustle phrase that isn't on your list and it still costs 1. The `hustle_phrases` list mostly tells the model what to look for, so a listed phrase is more likely to get caught.

Your current `hustle_phrases` are: rockstar, work hard play hard, on-call, weekend work.

**Question 3: which phrases should be added to the hustle list?**

These are common ones that signal overwork or unclear boundaries and aren't on your list yet:
- wear many hats
- we're like a family
- scrappy
- ninja
- thrive in ambiguity
- flexible hours when needed (often means "available whenever")

Adding the first three would look like this:

```yaml
# culture.hustle_phrases
# before
hustle_phrases: [rockstar, work hard play hard, on-call, weekend work]
# after
hustle_phrases: [rockstar, work hard play hard, on-call, weekend work, wear many hats, we're like a family, scrappy]
```

Pick any from the list, give me your own phrases, or say none. Keep in mind that each phrase you add can cost a point on a posting, so only add ones you'd really hold against a job. After this I'll ask whether anything on your list should move to `free_phrases`, or whether "fast-paced" should stay free.

### User

I want to add 'hackathon weekends' to the hustle phrases. That's the one that bugs me—it sounds like fun but it's really just unpaid work on top of your regular job. And can you make Culture count double in the verdict?

### Model

Here's the hustle phrase change:

```yaml
# culture.hustle_phrases
# before
hustle_phrases: [rockstar, work hard play hard, on-call, weekend work]
# after
hustle_phrases: [rockstar, work hard play hard, on-call, weekend work, hackathon weekends]
```

A posting that says "hackathon weekends" now costs 1 Culture point, and the cap of 3 across all hustle phrases still applies.

On making Culture count double, I haven't done that. You asked me not to change the verdict rules at the start, and this is a verdict rule. Culture only enters the verdict through rule 4c (Culture of 3 or lower puts a job in Apply with reservations), and that lives in `verdict.py`, not in `career-profile.yaml`, so no YAML edit can do it. The closest thing the YAML can do is make Culture lower more often. More hustle phrases and fewer big perks both push scores down, which makes the 4c trigger fire sooner.

If you do want Culture weighted more in the verdict, that's a separate change to `verdict.py`, its tests and ARCHITECTURE.md. Tell me explicitly that you want to lift the "no verdict changes" restriction, and I'll treat it as its own task.

**Question 4: should anything move onto your `free_phrases` list, or should "fast-paced" come off it?**

"Fast-paced" is free now, so a posting using it costs nothing. If a fast pace bothers you, you can remove it:

```yaml
# before
free_phrases: [fast-paced]
# after
free_phrases: []
```

Note that removing it won't make it cost anything by default. It only costs a point if the model quotes it as a hustle phrase, so you'd also need to add it to `hustle_phrases` for it to be reliably caught.

You can keep it free, remove it, or tell me about other phrases you want to treat as harmless, such as "startup environment" or "small team".

### User

Keep fast-paced free. I think we're all set with these changes.

### Model

Here's the full set of changes, all in the `culture` section of your `career-profile.yaml`:

```yaml
culture:
  perks:
    - {id: unlimited_pto, label: Unlimited PTO, kind: big}
    - {id: learning_budget, label: Learning budget, kind: nice}   # was big
    - {id: extra_days_off, label: Extra paid days off, kind: big}
    - {id: offsites, label: Regular meetups or offsites, kind: nice}
    - {id: home_office, label: Home-office or wellness stipend, kind: nice}
    - {id: parental_leave, label: Paid parental leave, kind: nice}
  low_time_off_days: 15
  hustle_phrases: [rockstar, work hard play hard, on-call, weekend work, hackathon weekends]   # added hackathon weekends
  free_phrases: [fast-paced]
```

Nothing else changed. The verdict rules, scoring rules and `low_time_off_days` are as before.

I haven't written anything to a file. These YAML snippets are shown for you to apply. The attached file was the Robin Sample fixture, which should stay as is because its tests expect the current values. Make these edits in your own profile, then run `python3 scripts/validate_profile.py career-profile.yaml` to confirm it still passes.

Culture will now come out a point lower on postings with a learning budget and a point lower on postings with "hackathon weekends".

### User

Yes, that looks right.

### Model

Good. The changes are the Learning budget moving to nice and "hackathon weekends" added to your hustle phrases. Nothing has been written to disk yet.

If you'd like me to apply them, give me the path to your own `career-profile.yaml` and I'll make the two edits and run the validator. Otherwise you can paste the block above into the `culture` section yourself and run `python3 scripts/validate_profile.py career-profile.yaml`.
