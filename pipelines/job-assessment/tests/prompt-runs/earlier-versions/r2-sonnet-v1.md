<!-- FICTIONAL EXAMPLE DATA. Not a real person. Saved by tests/prompt-runs/run_prompts.py -->
# Prompt run: Customize the rubric (assessment/README.md), on sonnet

- Prompt file: `prompts/r2-customize-rubric.txt`
- Date: 2026-10-01. Model alias `sonnet`, which ran as `claude-sonnet-5-5` (Claude Code can add a small helper model call of its own).
- Turns: 6. Cost: $0.67 (the simulated user's calls are not included).
- Grade: see `GRADES.md`.

## Conversation

### User

[the prompt below, with attached files: assessment/README.md, ARCHITECTURE.md, fixtures/robin-sample/career-profile.yaml]

I'm attaching assessment/README.md, ARCHITECTURE.md and my career-profile.yaml. Help me change which perks count as big or nice and which phrases count as hustle, one question at a time, and show the YAML change for each. Do not change the verdict rules.

### Model

The file you attached is the Robin Sample fixture (`fixtures/robin-sample/career-profile.yaml`), which is fictional data. I'll use it as the starting point. If you have your own `career-profile.yaml`, paste it and I'll work from that instead.

The changes only touch `culture.perks` and `culture.hustle_phrases` (plus `free_phrases` if relevant). The verdict rules stay as they are.

**Question 1 of a few: perks you'd call "big"**

A big perk adds 2 to Culture and a nice perk adds 1, so the big list is where a perk moves your score most. Right now you have three:

```yaml
culture:
  perks:
    - {id: unlimited_pto, label: Unlimited PTO, kind: big}
    - {id: learning_budget, label: Learning budget, kind: big}
    - {id: extra_days_off, label: Extra paid days off, kind: big}
```

Which of these should stay big, and should any drop to nice or be removed? Unlimited PTO is the one people most often reconsider, because it can mean less time off in practice.

Tell me your pick, and I'll show the exact YAML change before moving on to the next question (perks you'd add as big or nice, then hustle phrases).

### User

I'd keep Unlimited PTO and Extra paid days off as big—those are both meaningful to me. But learning budget should really be a nice perk instead, not a big one. That feels more accurate.

### Model

Here's the change. Only the `kind` on `learning_budget` moves:

```yaml
culture:
  perks:
    - {id: unlimited_pto, label: Unlimited PTO, kind: big}
-   - {id: learning_budget, label: Learning budget, kind: big}
+   - {id: learning_budget, label: Learning budget, kind: nice}
    - {id: extra_days_off, label: Extra paid days off, kind: big}
    - {id: offsites, label: Regular meetups or offsites, kind: nice}
    - {id: home_office, label: Home-office or wellness stipend, kind: nice}
    - {id: parental_leave, label: Paid parental leave, kind: nice}
```

A posting that mentions a learning budget now adds 1 to Culture instead of 2. In the worked example for posting 03, Culture would go from 9 to 8 (5 + 2 + 1). The verdict there doesn't change. If you run the fixture tests against this edited profile, though, the Culture score in `fixtures/expected.yaml` will no longer match, so keep this edit in your own copy rather than the fixture.

**Question 2: perks to add**

Is there a perk that isn't on your list but would matter to you? Examples:

- Four-day week or Friday-off schedule
- Fully paid health coverage
- Retirement match
- Sabbatical
- Equipment budget
- Flexible hours

Name any you'd add and say whether each is big (+2) or nice (+1). If none, say so and I'll move on to hustle phrases.

### User

None of those really stand out to me—I think the perks I have are already covering what matters. Let me skip ahead though: I do want to add 'hackathon weekends' as a hustle phrase, since that's something I'd actually enjoy and find energizing. And can you make Culture count double in the verdict?

### Model

**Hackathon weekends**

You said you'd enjoy it, so I think it belongs in `free_phrases`, not `hustle_phrases`. A hustle phrase costs 1 Culture point each (up to 3), while a free phrase costs nothing. Putting it under hustle would penalize postings for something you like. Here's the change I'd make:

```yaml
culture:
  hustle_phrases: [rockstar, work hard play hard, on-call, weekend work]
- free_phrases: [fast-paced]
+ free_phrases: [fast-paced, hackathon weekends]
```

One caveat: `weekend work` stays on your hustle list. A posting that says "hackathon weekends" will contain the word "weekends", but the check matches whole quoted phrases, so the two shouldn't collide. Per interpretation 9, a phrase on `free_phrases` costs nothing even if the model also flags it.

If you did want it to cost points, say so and I'll put it in `hustle_phrases` instead.

**Culture counting double in the verdict**

I'll leave that one out. It changes the verdict rules in `verdict.py`, and you asked me not to touch those. It's also not a YAML change: `verdict.py` takes four fixed scores and applies the rules in order, so nothing in `career-profile.yaml` can change how Culture is weighed there.

What your profile can do is change how much Culture moves. You've already adjusted the perks, and the hustle list is the other lever.

**Question 3: other hustle phrases**

Your current hustle list is `rockstar`, `work hard play hard`, `on-call` and `weekend work`. Are there phrases you'd add that signal a culture you'd avoid, such as "ninja", "wear many hats", "thrive under pressure", "other duties as assigned", or "self-starter who needs no hand-holding"? Or is there one on the current list you'd drop or move to free?

### User

That makes sense actually—if I enjoy hackathon weekends, putting them in free_phrases means they don't count against me, which is better. So yes, go ahead with that.

For the hustle phrases, I think the current list is fine. `Rockstar`, `work hard play hard`, `on-call`, and `weekend work` are all phrases I want to avoid, so I'll keep those. I don't have anything else to add or remove.

### Model

Both changes are settled, and the hustle list stays as it is. Here is the full `culture` block with everything combined:

```yaml
culture:
  perks:
    - {id: unlimited_pto, label: Unlimited PTO, kind: big}
    - {id: learning_budget, label: Learning budget, kind: nice}
    - {id: extra_days_off, label: Extra paid days off, kind: big}
    - {id: offsites, label: Regular meetups or offsites, kind: nice}
    - {id: home_office, label: Home-office or wellness stipend, kind: nice}
    - {id: parental_leave, label: Paid parental leave, kind: nice}
  low_time_off_days: 15
  hustle_phrases: [rockstar, work hard play hard, on-call, weekend work]
  free_phrases: [fast-paced, hackathon weekends]
```

Two things changed from what you attached:

- `learning_budget` moved from big to nice, so it adds 1 to Culture instead of 2.
- `hackathon weekends` joined `free_phrases`, so it costs nothing.

I haven't edited any file. I only have the text you pasted, and I don't know where your own `career-profile.yaml` lives. Paste the edits into your copy, then run this from `pipelines/job-assessment/` to confirm it's still valid:

```
python3 scripts/validate_profile.py career-profile.yaml
```

The verdict rules are untouched. If you want Culture weighted more heavily, that would be a change to `verdict.py` rather than your profile, and I can look at it separately if you decide you want that.

### User

Yes, that looks right.

### Model

Good. That finishes the rubric changes:

- `learning_budget` is now a nice perk (+1 instead of +2).
- `hackathon weekends` is now a free phrase, so it costs nothing.
- Your other perks and the hustle list stay as they were, and the verdict rules are untouched.

Next step is to paste the `culture` block into your own `career-profile.yaml` and run `python3 scripts/validate_profile.py career-profile.yaml`. If it prints problems, paste the output here and I'll walk through them.

### User

That's all, thanks.

### Model

You're welcome. Good luck with the job search.
