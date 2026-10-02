<!-- FICTIONAL EXAMPLE DATA. Not a real person. Saved by tests/prompt-runs/run_prompts.py -->
# Prompt run: Understand and teach, on sonnet

- Prompt file: `prompts/01-understand-and-teach.txt`
- Date: 2026-10-01. Model alias `sonnet`, which ran as `claude-sonnet-5-5` (Claude Code can add a small helper model call of its own).
- Turns: 1. Cost: $0.10 (the simulated user's calls are not included).
- Grade: see `GRADES.md`.

## Conversation

### User

[the prompt below, with attached files: README.md, ARCHITECTURE.md, fixtures/robin-sample/career-profile.yaml]

I'm attaching README.md, ARCHITECTURE.md and fixtures/robin-sample/career-profile.yaml from a job assessment tool. Teach me how it works as if I have never seen it. Cover, in this order: what the career-profile file holds and why every claim in it needs a source; how one job posting becomes four scores called Fit, Comp, Qualifications and Culture; the exact order the verdict rules are checked in; and what the tool refuses to do. Use plain words and short sentences. Then ask me three quiz questions, one at a time, and wait for my answer before asking the next. A good answer gives the rule order as hard block, job-type override, Fit and Qualifications floor, reservations band, then Apply, and says unlisted pay scores a neutral 5.

### Model

# How the job assessment tool works

## 1. The career-profile file

This is one YAML file about one person. Here, it is Robin Sample, a made-up technical writer.

It holds:

- **Who they are.** Name, target roles, years of experience, a location label, and a working style.
- **What they refuse.** Hard blocks, such as gambling, weapons, or non-remote work. A named exception can lift a block for one company. Robin's exception is a nearby office.
- **Pay numbers.** Five of them: floor, min, open ask, target, stretch ceiling. They must run low to high.
- **Culture tastes.** Big and nice perks, a time-off threshold, hustle phrases, and phrases that cost nothing.
- **Lanes.** Each lane is a kind of role. Each has its own must-haves, marked strong or soft. Each has autonomy signals and known gaps.
- **History.** Employers and evidence. Evidence is an accomplishment with a date, who did the work, and a proof status.
- **Skills.** A 0 to 5 self-score per skill, tied to evidence ids.

**Why every claim needs a source.** A self-score is only a claim. It is not proof. A qualification counts only if it points to a real evidence entry. The code rejects an id that does not exist. It also rejects entries marked `do_not_use` and work by someone else (`OTHER-AUTHOR`). Robin's wiki entry is one of those.

Evidence from an interview or a reference stays `proof: unchecked`. Nobody read a document to back it up. The validator also refuses a file that marks that kind of evidence as checked.

## 2. One posting becomes four scores

A model reads the posting. It writes a findings file. Each rating (strong, fair, weak, poor, unknown) must quote the posting. Each claimed qualification must cite an evidence id. Scripts then check the quotes and do the math. Each score runs 0 to 10 and is rounded half up.

- **Fit.** Does the job's shape match what you want? Start at 10. A weak strong-must-have costs 1.5. A poor one costs 3. An unknown one costs 1.5. Soft must-haves cost 1 only when weak or poor. Negative autonomy costs 2. Avoided skills that are daily work cost 1 each, up to 2.
- **Comp.** Is the base pay enough? It looks only at base pay. **Unlisted pay scores a neutral 5.** Listed pay uses the top of the range. At or above target is 10. At or above min is 8. At or above floor is 3. Below floor is 1.
- **Qualifications.** Can you do the job, going by your evidence? Start at 10. Too many years asked costs 2, once. Known gaps and low self-scores cost 1 each, capped at 4 together. A working-style mismatch costs 3.
- **Culture.** Start at 5, because silence tells you nothing. A big perk adds 2. A nice perk adds 1. Low time off costs 2. Hustle phrases cost 1 each, up to 3. Soft flags and negative phrases cost 1 each.

## 3. The verdict rules, in order

The first rule that fires decides. The rest are never looked at.

1. **Hard block.** One of your blocks is tripped with no exception. Verdict: Skip.
2. **Job-type override.** A required, central skill has no evidence at all. It is a different job with a familiar title. Verdict: Skip.
3. **Fit and Qualifications floor.** Fit is 5 or lower, or Qualifications is 5 or lower. Verdict: Skip.
4. **Reservations band.** Comp is 3 or lower, Culture is 3 or lower, or the average of Fit and Qualifications is under 7. Verdict: Apply with reservations.
5. **Apply.** Nothing above fired.

The company name is not an input to the verdict. A famous employer cannot talk its way past the rules.

## 4. What the tool refuses to do

- It will not let the model decide. A score or verdict typed by a model is ignored.
- It refuses a quote that is not in the posting.
- It refuses evidence that does not exist, is `do_not_use`, or is someone else's work.
- It refuses "no say" autonomy readings that rest only on generic words like "work closely with".
- It refuses contact details in the profile. There are no email or phone fields.
- It does not guess when the posting is silent. Silence is rated unknown.
- It does not fetch outside facts about the company.
- It does not send email. The summary card is a local file.
- It does not claim to predict hiring.
- It cannot catch a real quote read the wrong way. Every quote can be real and the reading still wrong.

---

## Quiz

**Question 1.** A posting trips one of Robin's hard blocks. Robin has no named exception for that company. The posting also pays well and has great perks. Which rule decides, and what is the verdict?

Take your time. I'll wait for your answer before I ask the next one.
