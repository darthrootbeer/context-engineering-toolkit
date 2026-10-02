<!-- FICTIONAL EXAMPLE DATA. Not a real person. Saved by tests/prompt-runs/run_prompts.py -->
# Prompt run: Understand and teach, on haiku

- Prompt file: `prompts/01-understand-and-teach.txt`
- Date: 2026-10-01. Model alias `haiku`, which ran as `claude-haiku-4-5-20251001` (Claude Code can add a small helper model call of its own).
- Turns: 1. Cost: $0.05 (the simulated user's calls are not included).
- Grade: see `GRADES.md`.

## Conversation

### User

[the prompt below, with attached files: README.md, ARCHITECTURE.md, fixtures/robin-sample/career-profile.yaml]

I'm attaching README.md, ARCHITECTURE.md and fixtures/robin-sample/career-profile.yaml from a job assessment tool. Teach me how it works as if I have never seen it. Cover, in this order: what the career-profile file holds and why every claim in it needs a source; how one job posting becomes four scores called Fit, Comp, Qualifications and Culture; the exact order the verdict rules are checked in; and what the tool refuses to do. Use plain words and short sentences. Then ask me three quiz questions, one at a time, and wait for my answer before asking the next. A good answer gives the rule order as hard block, job-type override, Fit and Qualifications floor, reservations band, then Apply, and says unlisted pay scores a neutral 5.

### Model

# How the job assessment tool works

## 1. The career-profile file and why everything needs a source

Your `career-profile.yaml` is the single source of truth about you. It holds:

- **Job history and dates.** Where you worked, what title you had, when.
- **Evidence: things you did that prove a skill.** Each entry says what you accomplished, dates it happened, links to proof (a document, a live artifact, or an interview), and whether the proof was actually checked by someone.
- **Skills: a 0 to 5 self-score per skill.** You pick the number. The tool trusts you, but only when you can point to evidence.
- **What you need from a job.** Pay floor and ceiling, perks that matter, time off, how much meeting load you can handle.
- **Lanes: kinds of roles you're looking at.** Each lane has its own must-haves (strong or soft), keywords that signal good or bad, and gaps you know about.
- **Hard blocks: employers you will never work for.** And one-off exceptions (a company you said no to, but you'd make an exception for).

**Every claim needs a source because the assessment is only as honest as the file behind it.** A self-score is just your opinion. To count a skill when the job posting wants it, the posting must quote a requirement the model finds, and then you must point to evidence in your file that proves you have it. The code refuses to let the tool cite evidence that does not exist, that you marked `do_not_use`, or that was someone else's work.

---

## 2. How four scores come from one posting

The model reads the posting and writes down what it found, quoting the text for every claim. Then code computes four scores, each 0 to 10:

**Fit** (does the job's shape match what you want?)
- Start at 10. Lose points for each must-have the posting does not meet or meets poorly. A strong must-have the posting does not mention at all costs 1.5. A soft must-have costs less. Lose 2 if the autonomy sounds bad. Lose 1 per skill you'd rather avoid if it is core daily work.

**Comp** (is the base pay enough?)
- If pay is not listed: score **5**, a neutral middle. Not 0, and not high.
- If pay is listed: find the pay tier that matches your location, then score the top of that range: 10 if at or above your target, 8 if at or above your minimum, 3 if at or above your floor, 1 if below your floor.

**Qualifications** (can you do this job, by your own evidence?)
- Start at 10. Lose 2 if the posting asks for more years than you have, or years in a narrow sub-domain. Lose 1 for each known gap the posting lists. Lose up to 4 total for low self-scores (0 or 1) on things the job needs. Lose 3 if your working style does not match.

**Culture** (what does the posting say about how people are treated?)
- Start at **5** (silence tells you nothing). Add 2 per big perk named, 1 per nice perk. Add 1 per positive phrase the posting mentions. Lose 2 if time off is low. Lose 1 per hustle phrase (like "rockstar"), up to 3 total. Lose 1 per soft flag that trips (heavy meetings, etc.). Phrases on your "free list" cost nothing.

Each score is clamped to its floor and cap, then rounded (8.5 becomes 9, not 8).

---

## 3. The exact order verdict rules are checked

`verdict.py` checks these in order. The first one that fires decides. Nothing after it is looked at.

1. **Hard block.** Does the posting trip one of your hard blocks, and is there no named exception for this company? → **Skip**
2. **Job-type override (4a).** A required skill central to the daily work has no evidence behind it at all. Different job, familiar title. → **Skip**
3. **Score floor (4b).** Fit is 5 or lower? Or Qualifications is 5 or lower? → **Skip**
4. **Reservations band (4c).** Comp is 3 or lower? Or Culture is 3 or lower? Or the average of Fit and Qualifications is under 7? → **Apply with reservations**
5. **Apply (4d).** Nothing above fired. → **Apply**

---

## 4. What the tool refuses to do

- It does not predict whether you will be hired.
- It does not fetch information about the company from outside the posting.
- It does not send email. The card is written to your computer.
- It does not let a famous company's name change the verdict. The rules take four numbers and nothing else.
- It does not check whether the model read tone correctly. It only checks that every quote is real and every evidence id exists.
- It is not machine learning or retrieval. It is prompts, a schema, and code that always gives the same answer for the same input.

---

Now, three quiz questions. I'll ask one at a time and wait for your answer.

**Question 1 of 3:** In what order are the five verdict rules checked, and what is the name of each rule?
