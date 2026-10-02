<!-- FICTIONAL EXAMPLE DATA. Not a real person. Saved by tests/prompt-runs/run_prompts.py -->
# Prompt run: Customize to my background (build my central file), on sonnet

- Prompt file: `prompts/02-customize.txt`
- Date: 2026-10-01. Model alias `sonnet`, which ran as `claude-sonnet-5-5` (Claude Code can add a small helper model call of its own).
- Turns: 25. Cost: $3.25 (the simulated user's calls are not included).
- Grade: see `GRADES.md`.
- Paths and addresses were shortened to labels such as <home>, <tmp> and <repo-url> before saving.

## Checks run by code on the reply

```text
$ python3 scripts/validate_profile.py <tmp>/career-profile.yaml
validate_profile: 9 problem(s), 0 warning(s) in career-profile.yaml
(top level): missing required field "schema_version".
(top level): missing required field "hard_blocks".
(top level): missing required field "comp".
(top level): missing required field "culture".
(top level): missing required field "lanes".
(top level): missing required field "employers".
(top level): missing required field "evidence".
(top level): missing required field "skills".
(top level): missing required field "meta".
(exit code 1)
```

## Conversation

### User

[the prompt below, with attached files: intake/SKILL.md, intake/templates/career-profile.template.yaml]

I'm attaching intake/SKILL.md and intake/templates/career-profile.template.yaml. Interview me to build my own career-profile.yaml. Ask exactly one question at a time and wait for my answer. If a question has two parts, ask them separately. Never suggest an answer and never invent a fact, date, number or skill. After each answer, show the exact YAML entry you would add, with its source label, and ask me to confirm it. Anything I cannot point to a document, link or artifact for gets proof: unchecked. Start with stage 0, orientation. A good session ends with a file that passes scripts/validate_profile.py.

### Model

I'll start by finding the stage 0 file and the scripts the skill refers to.


<invoke name="Glob">
<parameter name="pattern">**/{00-orientation.md,add_entry.py,validate_profile.py,career-profile*.yaml}</parameter>
</invoke>
<invoke name="Glob">
<parameter name="pattern">**/SKILL.md</parameter>
</invoke>
.


<invoke name="Bash">
<parameter name="command">pwd; ls -la</parameter>
</invoke>

### User

Do you have a resume or portfolio you'd like me to review, or should we start from scratch?

### Model

I don't have a résumé or portfolio of yours. Only the two attached files have come through, and the searches I just ran for `stages/00-orientation.md`, `scripts/add_entry.py` and `scripts/validate_profile.py` returned nothing I can see. I'll need to confirm where those live before I can write anything, but that doesn't block the interview.

So the question comes back to you: do you have a résumé, portfolio or any other document you'd like me to read first, or should we start from scratch? If you do, give me the file path or link. Anything I take from a résumé will be stored as `proof: unchecked`, since it only shows what the résumé says.

### User

No resume or portfolio to read. Start from scratch.

### Model

Starting from scratch. First I'll check the working folder for the stage 0 file and the scripts.


<invoke name="Bash">
<parameter name="command">pwd; ls -la; find . -maxdepth 4 \( -name '00-orientation.md' -o -name 'add_entry.py' -o -name 'validate_profile.py' -o -name 'career-profile*.yaml' \) 2>/dev/null</parameter>
</invoke>

### User

What's your name?

### Model

I'm Claude, an AI agent built on Anthropic's Claude Agent SDK. I'm the interviewer here, so I have no name to record. That question is the one for you.

What name do you want in the file as `display_name`? A first name or a nickname is fine.

I haven't seen the result of my last check for the stage 0 file and scripts. I'll sort that out before anything is written, and nothing will be saved until you've confirmed the entry.

### User

Robin Sample.

### Model

Here is the entry I would add. The `person` section has no `source` field, so the source label is shown on its own line.

```yaml
display_name: Robin Sample
```

Source: `interview:2026-10-01:s0.q1`, said in the interview, so `proof: unchecked` applies.

"Robin Sample" is also the example name in the template's comment. I'm not assuming anything from that, but the entry should be exactly what you want stored.

Is this right?

Nothing is written yet. Once you confirm, the file still has to be created from the template first, and `add_entry.py` does the write.

### User

Yes, that's right.

### Model

Confirmed. Before I write it, I need to find the template and `add_entry.py` on disk.


<invoke name="Bash">
<parameter name="command">pwd; ls -la; find . -maxdepth 5 \( -name '00-orientation.md' -o -name 'add_entry.py' -o -name 'validate_profile.py' -o -name 'career-profile*.yaml' \) 2>/dev/null</parameter>
</invoke>

### User

Senior Technical Writer and Docs Platform Engineer.

### Model

I haven't asked about target roles yet, but I'll take that as your answer to `target_roles`. Two things first.

- **Nothing is saved yet.** `display_name: Robin Sample` is confirmed but not written. My file checks have returned no output I can see, so I don't know where the template and `add_entry.py` are. I won't write by any other route. If you know the path to `pipelines/job-assessment/`, tell me when we get to a convenient point.
- **Your sentence could mean two things.** It could be two roles joined by "and", or one combined title.

This is how I would store it if they are two roles:

```yaml
target_roles:
  - Senior Technical Writer
  - Docs Platform Engineer
```

Source: `interview:2026-10-01:s0.q2`, `proof: unchecked`.

Is this right, with those as two separate roles?

### User

Yes, that's right.

### Model

Confirmed. I'll look for the files again, this time more widely.


<invoke name="Bash">
<parameter name="command">pwd; ls -la; find "$PWD" "$HOME" -maxdepth 6 \( -name 'add_entry.py' -o -name 'validate_profile.py' -o -name 'career-profile.template.yaml' -o -name '00-orientation.md' \) -not -path '*/node_modules/*' 2>/dev/null | head -20</parameter>
</invoke>

### User

9 years.

### Model

I'll take that as your answer to `years_experience`.

```yaml
years_experience: 9
```

Source: `interview:2026-10-01:s0.q3`, `proof: unchecked`.

I'm storing 9 as you said it, with nothing added or rounded.

Is this right?

Three confirmed items are still unsaved: `display_name`, `target_roles` and this one. My last file search again returned nothing I can see, so I haven't been able to run `add_entry.py`. I'll keep trying to find it, and I'll write all of them through it once it's located.

### User

What's your current employer?

### Model

I don't have an employer. I'm an AI agent built by Anthropic. Your employers are covered in stage 1, so I'm not asking about them yet.

Still open from my last message: is this entry right?

```yaml
years_experience: 9
```

### User

Placeholder Labs, an invented developer tool company.

### Model

Noted for stage 1, where I'll read it back as an `employers[]` entry before anything is stored. I'm not recording it now, because we're still in stage 0 and one confirmation is still open.

Is this entry right?

```yaml
years_experience: 9
```

### User

Yes, that's right.

### Model

All three stage 0 answers are confirmed. I'll try once more to locate the template and `add_entry.py` so I can write them.


<invoke name="Bash">
<parameter name="command">pwd; ls -la; find / -maxdepth 8 \( -name 'add_entry.py' -o -name 'validate_profile.py' -o -name 'career-profile.template.yaml' \) 2>/dev/null | head -20</parameter>
</invoke>

### User

Senior Technical Writer.

### Model

I can't tell which question that answers, and I won't guess. "Senior Technical Writer" is already stored as a target role, and it could also be your title at Placeholder Labs, which belongs to stage 1.

Which question is that an answer to?

Nothing is saved yet. None of my commands have returned any output, so I can't confirm the template or `add_entry.py` exist anywhere I can reach. Your three confirmed stage 0 answers are held in this conversation only. If you have the path to `pipelines/job-assessment/`, send it when convenient and I'll write them through `add_entry.py`.

### User

I don't know.

### Model

That's fine. I won't store that line, since I can't tie it to a question. If it's your Placeholder Labs title, I'll ask for it properly in stage 1.

Next I'll test whether the shell returns anything at all.


<invoke name="Bash">
<parameter name="command">echo shell-ok; pwd; ls -la</parameter>
</invoke>

### User

Senior Technical Writer.

### Model

I've heard "Senior Technical Writer" twice now, but I still can't tie it to a question. I'm leaving it unattached and unstored rather than guessing. In stage 1 I'll ask for your title at each employer, and you can give it there.

The shell test I just ran also returned no output. I can't see `echo shell-ok`, a directory listing, or any file. Without that I can't create the file or run `add_entry.py`, and I won't write by another route.

Where is the `pipelines/job-assessment/` folder on your machine, as a full path?

### User

I don't know.

### Model

"I don't know" is fine. The path stays unknown, and I won't guess one.

The files didn't come through to me as a folder. Only their text was attached, so `scripts/add_entry.py` and `scripts/validate_profile.py` may not be on this machine at all. Without them, no entry can be written and the validator can't run, and the session can't end with a passing file.

Run this in your own terminal and paste me what it prints:

```bash
find ~ -name add_entry.py -o -name validate_profile.py 2>/dev/null
```

If it prints nothing, the scripts aren't installed, and the interview can't produce a validated file until they are. I'd rather say that now than collect a long interview I can't save.

Will you run that and paste the output?

### User

I don't know.

### Model

I'll stop asking about the path.

**State of the session**
- **Confirmed but not saved:** `display_name: Robin Sample`, `target_roles: [Senior Technical Writer, Docs Platform Engineer]`, `years_experience: 9`. All three are from the interview with `proof: unchecked`.
- **Held, not stored:** Placeholder Labs as an employer, for stage 1, and the stray "Senior Technical Writer".
- **Gap:** I don't know where the scripts are, and none of my commands have returned output.

**My recommendation:** pause the interview here. Continuing would pile up confirmed answers that exist only in this chat. Once `add_entry.py` and `validate_profile.py` are reachable, there are two ways to resume:
1. Start me from the `pipelines/job-assessment/` folder, so the commands work.
2. Run the `find` command above yourself and paste the result.

Either way, the first thing I'll do is write the three stage 0 entries, then record stage 0 in `meta.intake.stages_done` and move on to stage 1.

### User

Ok.

### Model

We're paused. When you're ready to continue, start me from the `pipelines/job-assessment/` folder or paste the `find` output. I'll write the three confirmed stage 0 entries first and then move on to stage 1.

### User

Ready to continue whenever you are.

### Model

Let me check whether the shell works from here now.


<invoke name="Bash">
<parameter name="command">pwd; ls -la; find "$PWD" "$HOME" -maxdepth 6 \( -name 'add_entry.py' -o -name 'validate_profile.py' -o -name 'career-profile.template.yaml' \) 2>/dev/null | head</parameter>
</invoke>

### User

I'm ready to continue.

### Model

My last shell command returned nothing again, so I still can't write anything myself. The skill has a fallback for this: I show the exact command, you run it, and you paste back the output. The file is still written only by `add_entry.py`.

Run these from inside your `pipelines/job-assessment/` folder. They copy the empty template into place and write the three entries you confirmed:

```bash
cp intake/templates/career-profile.template.yaml career-profile.yaml

python3 scripts/add_entry.py career-profile.yaml --section person --entry - <<'YAML'
display_name: Robin Sample
target_roles: [Senior Technical Writer, Docs Platform Engineer]
years_experience: 9
YAML
```

If `cp` says the template isn't found, adjust the source path to wherever `career-profile.template.yaml` is. If `add_entry.py` isn't found, the scripts aren't in that folder.

Paste whatever the second command prints, including any error. Once it exits 0, I'll record stage 0 as done and start stage 1.

### User

Senior Technical Writer.

### Model

That's the third time I've received "Senior Technical Writer", and I still have no question it answers. It stays unattached and unstored. I'll ask for your title at each employer in stage 1, and it will be recorded properly then.

I'm still waiting on the output of the two commands from my last message. Nothing is saved until `add_entry.py` exits 0, and stage 1 starts after that.

### User

I don't know.

### Model

That's fine. Nothing is lost: your three confirmed answers are in this conversation, and "I don't know" is recorded as a gap, not a guess.

The next step is the two commands from my earlier message, run in your terminal, with the output pasted back. Until then I'll hold, and I won't ask anything else.

### User

I don't know.

### Model

Understood. I'm holding here, and nothing has been saved or invented. When you have the command output, or can start me from the `pipelines/job-assessment/` folder, paste it or say so and I'll pick up with the stage 0 write.

### User

Placeholder Labs, an invented developer tool company.

### Model

I have that one already. It's held for stage 1, where I'll read it back as an `employers[]` entry for you to confirm before it's stored. Stage 1 can't start until the stage 0 write has gone through `add_entry.py`, so I'm still waiting on the output of those two commands.

### User

Let's stop here for today. Print the whole career-profile.yaml as it stands now, with only what I confirmed, as one yaml code block and nothing else.

### Model

```yaml
# NOT WRITTEN TO DISK. add_entry.py has not run, so no career-profile.yaml exists yet.
# This is only what Robin confirmed in the stage 0 interview (2026-10-01).
# Source for every value: interview, proof: unchecked.
person:
  display_name: Robin Sample                # interview:2026-10-01:s0.q1
  target_roles:                             # interview:2026-10-01:s0.q2
    - Senior Technical Writer
    - Docs Platform Engineer
  years_experience: 9                       # interview:2026-10-01:s0.q3
```
