<!-- FICTIONAL EXAMPLE DATA. Not a real person. Saved by tests/prompt-runs/run_prompts.py -->
# Prompt run: Understand and teach, on sonnet

- Prompt file: `prompts/01-understand-and-teach.txt`
- Date: 2026-10-01. Model alias `sonnet`, which ran as `claude-sonnet-5-5` (Claude Code can add a small helper model call of its own).
- Turns: 1. Cost: $0.11 (the simulated user's calls are not included).
- Grade: see `GRADES.md`.

## Conversation

### User

[the prompt below, with attached files: README.md, ARCHITECTURE.md, fixtures/robin-sample/career-profile.yaml]

I'm attaching README.md, ARCHITECTURE.md and fixtures/robin-sample/career-profile.yaml from a job assessment tool. Teach me how it works as if I have never seen it. Cover, in this order: what the career-profile file holds and why every claim in it needs a source; how one job posting becomes four scores called Fit, Comp, Qualifications and Culture; the exact order the verdict rules are checked in; and what the tool refuses to do. Use plain words and short sentences. Then ask me three quiz questions, one at a time, and wait for my answer before asking the next. A good answer gives the rule order as hard block, job-type override, Fit and Qualifications floor, reservations band, then Apply, and says unlisted pay scores a neutral 5.

### Model

# How the job assessment tool works

## 1. The career-profile file

This file is everything the tool knows about you. It is one YAML file. In the sample, the person is Robin Sample, an invented writer.

It holds:

- **Who you are:** target roles, years of experience, a location label, and a working style.
- **What you refuse:** hard blocks, such as gambling or weapons. A named exception can allow one company despite a block.
- **What you need:** five pay numbers (floor, min, open ask, target, stretch ceiling) and your culture tastes. Culture tastes are perks you like, hustle phrases you dislike, and the minimum time off you want.
- **What roles you want:** each "lane" has its own must-haves. Each must-have is strong or soft.
- **Your history:** employers, and evidence entries (the accomplishments).
- **Your skills:** a 0 to 5 self-score for each.

**Why every claim needs a source.** The tool is only as honest as this file. So the file separates what you say from what you can show.

- A self-score is your own opinion. It is never evidence.
- Each evidence entry says who did the work: wrote it, co-wrote it, directed it, or someone else did.
- Each entry says whether a document backs it. `proof: checked` means someone read a link or document. Claims from an interview or a reference stay `unchecked`.
- A qualification only counts if it points at a real evidence entry.
- The code rejects entries marked `do_not_use` or written by another author. Robin's wiki entry is one example.
- The validator also refuses a file that marks interview-only claims as checked.

## 2. One posting becomes four scores

The flow is simple. A model reads the posting and writes a **findings file**. Scripts check it, then count.

**The model's job.** It rates each of your criteria as strong, fair, weak, poor, or unknown. It must quote the posting for every rating except unknown. If the posting is silent, the rating is unknown. It does not guess.

**The checker's job.** It confirms every quote is really in the posting. It confirms every evidence id is real and is yours.

**The scoring.** Each score runs 0 to 10. Each is rounded half up (8.5 becomes 9).

| Score | Question it answers | Start | How it moves |
|---|---|---|---|
| **Fit** | Does the job's shape match what you want? | 10 | Each strong must-have rated weak costs 1.5, poor costs 3, and unknown costs 1.5. A soft must-have rated weak or poor costs 1. Bad autonomy costs 2. Core daily work in a skill you want to avoid costs 1 each, up to 2. |
| **Comp** | Is the base pay enough? | n/a | Only the top of the listed base range counts. At or above target is 10. At or above min is 8. At or above floor is 3. Below floor is 1. **Unlisted pay scores a neutral 5, not 0.** |
| **Qualifications** | Can you do this job, going by your evidence? | 10 | Too many years or too narrow a sub-domain costs 2, once. Known gaps and weak self-scores on load-bearing lines cost 1 each, up to a combined cap of 4. A working-style mismatch costs 3. |
| **Culture** | How does the posting say people are treated? | 5 | A big perk adds 2. A nice perk adds 1. A strong positive phrase adds 1. Low time off costs 2. Hustle phrases cost 1 each, up to 3. Each soft flag costs 1. Each negative phrase costs 1. |

Culture starts at 5 for the same reason Comp does: silence tells you nothing.

Take posting 03 as an example. Fit comes to 7, Comp to 5, Qualifications to 6, and Culture to 9.

## 3. The verdict rules, in exact order

`verdict.py` checks these top to bottom. The first rule that fires decides. Nothing after it is looked at.

1. **Hard block.** The posting trips one of your hard blocks and no named exception covers the company. Verdict: **Skip**.
2. **Job-type override.** A required skill central to the daily work has no evidence at all. It is a different job with a familiar title. Verdict: **Skip**.
3. **Fit and Qualifications floor.** Fit is 5 or lower, or Qualifications is 5 or lower. Verdict: **Skip**.
4. **Reservations band.** Comp is 3 or lower, or Culture is 3 or lower, or the average of Fit and Qualifications is under 7. Verdict: **Apply with reservations**.
5. **Apply.** Nothing above fired. Verdict: **Apply**.

Posting 03 reaches rule 4. Its average is (7 + 6) / 2 = 6.5, which is under 7. So the verdict is Apply with reservations.

## 4. What the tool refuses to do

- **It refuses a model's verdict.** A score or verdict typed by the model is ignored. Only the findings count.
- **It refuses made-up quotes.** A quote not found in the posting text fails the check. Case, spacing, and curly quotes are ignored. Words are not.
- **It refuses fake or borrowed evidence.** The evidence id must exist, must not be `do_not_use`, and must not be someone else's work.
- **It refuses generic "no say" readings.** Phrases like "work closely with" appear in almost every senior posting. They alone cannot prove poor autonomy.
- **It refuses to look at the company's name.** `verdict.py` takes four numbers and two flags. A famous or favorite employer cannot change the outcome.
- **It refuses contact details.** The profile has no field for them, and the validator rejects anything shaped like an email or phone number.
- **It refuses to guess.** Silence becomes unknown, not a guess.
- **It refuses to send email.** The summary card is a local HTML file.
- **It refuses to research the company.** It uses only the posting.
- **It refuses to promise results.** It does not predict hiring. It cannot catch a real quote read too kindly. The live run on the "You can document our mobile SDK" line shows this. The mistake sat in one visible field, so a person can fix it.

---

## Quiz

I'll ask three questions, one at a time. Here is the first.

**Question 1:** A posting never mentions pay at all. What does Comp score, and why is it that number and not 0?
