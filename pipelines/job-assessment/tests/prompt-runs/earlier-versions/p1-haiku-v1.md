<!-- FICTIONAL EXAMPLE DATA. Not a real person. Saved by tests/prompt-runs/run_prompts.py -->
# Prompt run: Understand and teach, on haiku

- Prompt file: `prompts/01-understand-and-teach.txt`
- Date: 2026-10-01. Model alias `haiku`, which ran as `claude-haiku-4-5-20251001` (Claude Code can add a small helper model call of its own).
- Turns: 1. Cost: $0.05 (the simulated user's calls are not included).
- Grade: see `GRADES.md`.
- Edited after the run: one real company name the model used as an example was replaced with "[a company-review site]".

## Conversation

### User

[the prompt below, with attached files: README.md, ARCHITECTURE.md, fixtures/robin-sample/career-profile.yaml]

I'm attaching README.md, ARCHITECTURE.md and fixtures/robin-sample/career-profile.yaml from a job assessment tool. Teach me how it works as if I have never seen it. Cover, in this order: what the career-profile file holds and why every claim in it needs a source; how one job posting becomes four scores called Fit, Comp, Qualifications and Culture; the exact order the verdict rules are checked in; and what the tool refuses to do. Use plain words and short sentences. Then ask me three quiz questions, one at a time, and wait for my answer before asking the next. A good answer gives the rule order as hard block, job-type override, Fit and Qualifications floor, reservations band, then Apply, and says unlisted pay scores a neutral 5.

### Model

# How This Job Assessment Tool Works

## The Career Profile File

You write one file about yourself: your job history, skills, what you're looking for, and proof of every claim. It's named `career-profile.yaml`.

Here's what goes in it:

**Your basics.** Your name, the types of roles you want, how many years you've worked, and where you live (for picking pay tiers).

**Your limits.** Hard blocks are kinds of employers you'll never work for (example: Robin refuses gambling companies). You can name one exception—a company you'd make an exception for.

**Your pay.** Five numbers: floor (the least you'd accept), min (what you want), open ask, target (your goal), and stretch ceiling.

**What you care about at work.** Perks that matter (unlimited PTO, learning budgets, paid time off). Phrases that matter ("fast-paced" is good, "on-call" is work after hours). Things that worry you (meetings eating your writing time).

**The kinds of roles you want (lanes).** For each lane, you list what must-haves you need in a posting (strong or soft), what autonomy signals you look for, and skills you're missing.

**Your job history and proof.** Every accomplishment comes with a source: a link you can show, a document, an interview, or an artifact. The code refuses to count something if the source is missing or if someone else did the work.

**Your skills.** You score yourself 0 to 5 on each skill. A score only counts if you can point to evidence of doing it. A skill you've never used cannot be scored 4 or 5.

**Why every claim needs a source.** An assessment is only as good as the file behind it. When a posting asks for a skill you claim to have, the code checks: does your file have evidence for it? Is it your work or someone else's? Is it backed by a document or just an interview? The model can then use that evidence to say whether you match.

---

## One Posting Becomes Four Scores

The model reads the job posting and rates how well it matches six things about you:
- Must-haves for the lane
- Autonomy (how much say you have)
- Pay
- Perks and culture signals
- Skills the job wants

The model writes a findings file: one rating per thing, and a quote from the posting to back it up.

Then code takes that findings file and computes four scores, each from 0 to 10:

**Fit**: Does the job's shape match what you want?
- Start with 10 points.
- Each strong must-have the posting doesn't meet costs you 1.5 or 3 points depending on how badly it's missing.
- Soft must-haves cost less.
- Negative autonomy (needing approval for everything) costs 2 points.
- Skills you'd rather avoid cost 1 point if they're core daily work.

**Comp**: Is the base pay enough?
- The code picks your pay tier based on your location, then scores the job's top pay number.
- At or above your target: 10 points.
- At or above your minimum: 8 points.
- At or above your floor: 3 points.
- Below your floor: 1 point.
- **Pay not listed: 5 points. A neutral middle, not zero.**

**Qualifications**: Can you actually do this job?
- Start with 10 points.
- If the job asks for more years than you have, or deep expertise in a narrow thing: minus 2 points (once).
- Each skill gap you know about (you have 0-1 on something required): minus up to 1 point.
- Your working style doesn't match theirs: minus 3 points.

**Culture**: What does the posting say about how people are treated?
- Start with 5 points, because silence tells you nothing.
- Big perks (like unlimited PTO): plus 2 points each.
- Nice perks: plus 1 point each.
- Strong positive phrases: plus 1 point each.
- Few vacation days: minus 2 points.
- Hustle phrases like "rockstar" or "on-call": minus 1 point each (max 3).
- Red flags like "no engineering support": minus 1 point each.
- Negative phrases: minus 1 point each.

All scores are rounded to whole numbers, then clamped to 0–10.

---

## The Verdict Rules (In Order)

The tool checks five rules in this exact order. The first one that fires decides your verdict, and nothing after it matters.

**Rule 1: Hard block.** Does the posting match one of your hard blocks, and no exception covers it? → **Skip**

**Rule 2: Job-type override.** Does the job need a skill that is core daily work, but you have zero evidence of ever doing it? (Example: it's a Go backend role and you've never written Go code.) → **Skip**

**Rule 3: Score floor.** Is Fit at 5 or below, or Qualifications at 5 or below? → **Skip**

**Rule 4: Reservations band.** Is Comp at 3 or below, or Culture at 3 or below, or is the average of Fit and Qualifications below 7? → **Apply with reservations**

**Rule 5: Apply.** Nothing above fired. → **Apply**

The company's name is never an input. A famous employer cannot talk its way past these rules.

---

## What the Tool Refuses to Do

- **Predict whether you'll be hired.** It's not a model of hiring. It only checks whether a job matches your stated needs.
- **Trust the model's tone reading.** If the model misquotes the posting, the code catches it. But if the model quotes real words and reads them the wrong way, code cannot know.
- **Fetch anything from outside the posting.** No web search, no company research, no [a company-review site].
- **Send email.** It writes a summary card to a local HTML file on your machine.
- **Use machine learning or AI to decide.** The model reads and quotes. Scripts do the checking and math. The verdict rules are written code.

---

# Your Turn: Three Questions

I'll ask one at a time. Wait for your answer before I ask the next one.

## Question 1

What does it mean that "unlisted pay scores a neutral 5"? Say what happens when a job posting doesn't say what it pays, and why that's different from other scores.
