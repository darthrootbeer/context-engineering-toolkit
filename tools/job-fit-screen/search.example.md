# Example: Fit Criteria (search.md)

This is a PLACEHOLDER with fake example values, showing the human-readable half of job-fit-screen. Pair it with `criteria.example.yaml` — that file is the structured version a script reads; this one is the reasoning behind it, written for you to actually think through and read back later.

Copy this file to your own private location, rename it whatever makes sense to you, and replace every example with something true about your own situation. Nothing in this file is read by the tool automatically — it exists so the structured criteria file isn't the only place your preferences live, and so you have somewhere to write out *why* each rule exists, not just *what* it checks.

---

## Why two files, not one

A screening tool needs machine-checkable fields (`criteria.example.yaml`). A person trying to figure out their own preferences needs to actually reason through them in plain language first — what happened at past jobs, what patterns repeated, what tradeoffs are real versus assumed. Writing the reasoning down here, then distilling it into the YAML's structured fields, produces a better criteria file than jumping straight to YAML ever would. Keep both in sync: if a rule changes here, update the matching entry in your criteria YAML, and vice versa.

---

## Fit criteria

Use this section as your own checklist for judging any posting — a place to write down what actually matters to you, grounded in real evidence from your own work history rather than guessed preferences.

### Availability and process

Example prompts to answer for yourself:
- How soon could you actually start if offered a job today? (Notice period, if any.)
- What's your work authorization status, and how should postings from employers outside your country be handled?
- What's your real tolerance for interview process length — number of rounds, take-home assignments, timeline expectations? Has a past experience (good or bad) taught you something specific about this?

**Example:** *Available immediately — no current employer, no notice to serve. Up to 5 interview rounds is fine; 6+ gets flagged. Take-home assignments are okay if reasonably scoped (a couple hours) — a past employer's scoped take-home actually helped land the job, so this isn't a flat rule against them, it's about total process length stacking up.*

### Location

Example prompts:
- Remote, hybrid, onsite, or some mix — and how firm is that requirement?
- Any exceptions (occasional travel, specific regions)?
- Time zone expectations, and how flexible you actually are.

**Example:** *Remote only — hard requirement. Up to 1-2 trips a year for training or off-sites is fine. Works Eastern time by default, some flexibility. Open to employers outside my home country as long as pay/benefits are competitive and there's no legal complication to working for them from here.*

### Company size and stage

Example prompts:
- Does company size actually predict whether you've been happy somewhere, based on your real history — or is something else the real filter (autonomy, culture, team structure)?
- What's the strongest evidence from your own past roles, not a guess about what *should* matter?

**Example:** *No fixed headcount preference — history spans a 60-person startup to an 800-person enterprise product, and size itself never predicted whether the job was good. The real filter is autonomy: does this company need someone to own this function and hand over real decision-making power, or is it a seat on an existing team. The two strongest "liked" data points in my whole work history are both a version of building something from nothing with real ownership.*

### Industries

Example prompts:
- Any hard blocks — industries you refuse to work in, and why (values-based, knowledge-gap-based, something else)?
- Any industries you used to avoid out of a real gap that's since closed? Worth naming so an old instinct doesn't auto-reject a posting that's actually fine now.

**Example:** *No hard preference by industry — judged on autonomy and treatment, not what the company sells. Hard blocks: [industry you refuse], [industry you refuse] — not preferences, real lines. One industry [name] used to be avoided out of a real knowledge gap; a past role proved that gap closable, so don't auto-reject a posting there on the old instinct.*

### The pitch you're chasing

A short paragraph naming, in your own words, what the ideal posting actually looks like — not a job title, but the shape of the opportunity you're actually hoping to find.

**Example:** *The ideal posting isn't a job description — it's a company that needs [the thing you do] fixed and doesn't yet have anyone dedicated to it. The pitch: "Here's my system. I'll plug it in, tune it to your situation, and make this genuinely great." A role with real ownership over that outcome is the target.*

### Culture red flags

List the specific things that predict a bad fit, each backed by a real pattern from your own history — not a generic "good culture" wishlist.

**Example:**
- **[Specific dealbreaker].** A dealbreaker, not a minor downside.
- **[Specific pattern you've lived through].** Lived directly at [company] ([what happened]) and [company] ([what happened]). Tolerated every time, never enjoyed.
- **Low employee satisfaction on Glassdoor** (or your local equivalent) — a signal worth checking every time, not noise.
- **[Anything else specific to you].**

---

## Notes on writing your own version

- **Ground every rule in real evidence.** "I don't want a bureaucratic company" is vague. "I lived through 9 reorgs in 7 years at one job and it wore me down every time" is a real, checkable pattern.
- **Separate hard blocks from soft preferences.** Some things are non-negotiable; most things are worth weighing case by case. Say which is which, in both this file and your structured criteria YAML.
- **Keep this file and your criteria YAML in sync.** When you learn something new about your own preferences, update both — the prose explains why, the YAML is what the tool actually checks.
- **This file is never read automatically by any script.** It's for you. Keep it wherever makes sense — a private notes app, a personal vault, a plain text file. It does not need to live inside this repo, and if you fork this tool publicly, keep your real version private the same way the real criteria YAML stays private.
