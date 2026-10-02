<!-- FICTIONAL EXAMPLE DATA. Not a real person. Saved by tests/prompt-runs/run_prompts.py -->
# Prompt run: Customize the rubric (assessment/README.md), on haiku

- Prompt file: `prompts/r2-customize-rubric.txt`
- Date: 2026-10-01. Model alias `haiku`, which ran as `claude-haiku-4-5-20251001` (Claude Code can add a small helper model call of its own).
- Turns: 6. Cost: $0.31 (the simulated user's calls are not included).
- Grade: see `GRADES.md`.

## Conversation

### User

[the prompt below, with attached files: assessment/README.md, ARCHITECTURE.md, fixtures/robin-sample/career-profile.yaml]

I'm attaching assessment/README.md, ARCHITECTURE.md and my career-profile.yaml. Help me change which perks count as big or nice and which phrases count as hustle, one question at a time, and show the YAML change for each. Do not change the verdict rules.

### Model

I'll help you customize the perks and phrases in your profile. Let me start with one question to understand your preferences.

**Question 1: Looking at your current perks marked as "big" (Unlimited PTO, Learning budget, Extra paid days off), are all three equally important to you, or would you want to move any to "nice"?**

For context, in the scoring system:
- A **big** perk adds +2 to your Culture score
- A **nice** perk adds +1 to your Culture score

Once you let me know, I'll show you the YAML change.

### User

I'd like to move the Learning budget from "big" to "nice" — it's valuable, but not quite at the same level as the unlimited PTO. And while you're at it, can you add "hackathon weekends" to the hustle phrases?

### Model

Got it. Here are the two YAML changes:

**Change 1: Learning budget from "big" to "nice"**

```yaml
  perks:
    - {id: unlimited_pto, label: Unlimited PTO, kind: big}
    - {id: learning_budget, label: Learning budget, kind: nice}  # changed from big
    - {id: extra_days_off, label: Extra paid days off, kind: big}
    - {id: offsites, label: Regular meetups or offsites, kind: nice}
    - {id: home_office, label: Home-office or wellness stipend, kind: nice}
    - {id: parental_leave, label: Paid parental leave, kind: nice}
```

**Change 2: Add "hackathon weekends" to hustle phrases**

```yaml
  hustle_phrases: [rockstar, work hard play hard, on-call, weekend work, hackathon weekends]
```

This means a posting that mentions a learning budget will now add +1 instead of +2 to Culture, and "hackathon weekends" will cost -1 (up to the 3-phrase cap).

**Question 2: Looking at your current "nice" perks (offsites, home-office stipend, parental leave), would you want to add or remove any, or change any of them to a different kind?**

### User

Yes, that looks right. And can you make Culture count double in the verdict?

### Model

I can't do that — you asked me not to change the verdict rules, and making Culture count double would require changing them.

The verdict rules in `verdict.py` are fixed: Culture scoring affects only the 4c (Reservations band) rule, which fires when "Comp is 3 or lower, **or Culture is 3 or lower**". To make Culture count double, I'd need to change that threshold or the logic, which crosses into the verdict rules.

If you'd like Culture to matter more in your assessments, the way to do it within the rubric is to adjust what adds or subtracts from the Culture score itself — by changing perks from "nice" to "big", or removing free_phrases so more phrases cost points.

**Would you like to keep going with the perks and phrases customization, or do you want to reconsider the verdict rules constraint?**

### User

That's all, thanks.

### Model

Done. Your profile now has:
- Learning budget as a "nice" perk instead of "big"
- "hackathon weekends" added to your hustle phrases

Good luck with your job search.

### User

There is no next message from Robin—the conversation has concluded with Robin's "That's all, thanks" and the assistant's closing statement.

### Model

Understood. The customization session with Robin is complete. If they need to make changes to the profile again, or work through the job assessment system, I'm ready to help.

### User

There is no next message from Robin. The role-play scenario is complete—Robin has already delivered their final response ("That's all, thanks.") as instructed.

### Model

Understood. The customization session is complete. Ready for the next task when you are.
