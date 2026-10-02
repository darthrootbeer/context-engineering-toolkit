#!/usr/bin/env python3
"""Run every reader prompt in prompts/ through the claude CLI and save what came back.

    run_prompts.py [--models sonnet haiku] [--only p1 p3 ...] [--out tests/prompt-runs]

Each run is a fresh print-mode session in an empty folder, with no tools, no MCP
servers and no settings files, so the model sees only the prompt and the files
it names. Files are pasted in after the prompt, each between "Attached file"
lines, the way a person would attach them in a chat window.

Three prompts are conversations, not one question: building a profile (02),
the setup walkthrough (s1) and customizing the rubric (r2). For those, a second
model call plays the user from a short written script, and the conversation is
resumed turn by turn.

Two prompts get a check by code on top of the human grading: the findings JSON
from prompt 03 is run through check_findings.py and assess_offline.py, and the
profile printed at the end of prompt 02 is run through validate_profile.py.

This calls a model and costs money. It is never run by the test suite or CI.
Grades are written by a person (or a stronger model) into GRADES.md afterwards.
"""
import argparse
import getpass
import json
import re
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
PY = sys.executable
SIM_MODEL = {"p2": "sonnet", "s1": "haiku", "r2": "haiku"}
BANNER = "<!-- FICTIONAL EXAMPLE DATA. Not a real person. Saved by tests/prompt-runs/run_prompts.py -->"


def section(path, heading):
    """One H2 section of a markdown file, heading included."""
    text = (ROOT / path).read_text(encoding="utf-8")
    start = text.index(f"## {heading}")
    end = text.find("\n## ", start + 3)
    return text[start:end if end != -1 else None].strip()


def validator_output(path):
    proc = subprocess.run([PY, "scripts/validate_profile.py", path], cwd=ROOT,
                          capture_output=True, text=True)
    return (f"$ python3 scripts/validate_profile.py {path}\n{proc.stderr}{proc.stdout}"
            f"(exit code {proc.returncode})")


ROBIN = "fixtures/robin-sample/career-profile.yaml"
POSTINGS = [f"fixtures/postings/{n}.md" for n in ("01-strong-fit", "02-job-type-override", "03-unlisted-pay-perks")]
FINDINGS = [p.replace("postings/", "findings/").replace(".md", ".findings.json") for p in POSTINGS]

CASES = {
    "p1": {"file": "01-understand-and-teach.txt", "title": "Understand and teach",
           "attach": ["README.md", "ARCHITECTURE.md", ROBIN]},
    "p2": {"file": "02-customize.txt", "title": "Customize to my background (build my central file)",
           "attach": ["intake/SKILL.md", "intake/templates/career-profile.template.yaml"],
           "persona": "p2", "turns": 24},
    "p3": {"file": "03-run-first-posting.txt", "title": "Run on my first posting",
           "attach": ["assessment/SKILL.md", "schema/findings.schema.json", ROBIN, POSTINGS[0]]},
    "p4": {"file": "04-test-scoring.txt", "title": "Test the scoring with the fixture",
           "attach": ["ARCHITECTURE.md", ROBIN, *POSTINGS, *FINDINGS, "fixtures/expected.yaml"]},
    "p5": {"file": "05-find-gaps.txt", "title": "Find gaps in my central file",
           "attach": [("ARCHITECTURE.md, section 'What the validator checks'",
                       lambda: section("ARCHITECTURE.md", "What the validator checks")),
                      "fixtures/gappy-profile.yaml"]},
    # The held-out run: the same prompt on a gappy file it was never tuned against.
    "p5h": {"file": "05-find-gaps.txt", "title": "Find gaps in my central file (held-out profile)",
            "attach": [("ARCHITECTURE.md, section 'What the validator checks'",
                        lambda: section("ARCHITECTURE.md", "What the validator checks")),
                       "fixtures/held-out-gappy-profile.yaml"]},
    "p6": {"file": "06-fix-errors.txt", "title": "Fix errors",
           "attach": [("output of the failed command", lambda: validator_output("fixtures/broken-profile.yaml")),
                      "fixtures/broken-profile.yaml"]},
    "r1": {"file": "r1-review-rules.txt", "title": "Review the rules for gaps (ARCHITECTURE.md)",
           "attach": ["ARCHITECTURE.md"]},
    "s1": {"file": "s1-setup-walkthrough.txt", "title": "Walk me through setup (SETUP.md)",
           "attach": ["SETUP.md"], "persona": "s1", "turns": 9},
    "r2": {"file": "r2-customize-rubric.txt", "title": "Customize the rubric (assessment/README.md)",
           "attach": ["assessment/README.md", "ARCHITECTURE.md", ROBIN], "persona": "r2", "turns": 6},
    "h1": {"file": "h1-understand-hook.txt", "title": "Understand the hook (assessment/hooks/README.md)",
           "attach": ["assessment/hooks/README.md", "assessment/hooks/assessment-email-template-guard.sh"]},
}

PERSONAS = {
    "p2": lambda: (
        "You are role-playing Robin Sample, an invented person, who is being interviewed to build a career file. "
        "You are the one answering, never the interviewer: never ask the interviewer a question, and never "
        "answer a question that was not asked. Your scripted answers are below. "
        "Reply to the interviewer's latest message with only Robin's next reply. "
        "If the interviewer gives you a command to run, reply 'Done, it printed no errors.' "
        "Answer only the question actually asked, using the matching scripted answer, in the script's order. "
        "If the interviewer shows a YAML entry and asks you to confirm it, reply 'Yes, that's right.' unless it "
        "contains a fact, date, number or skill you never said, in which case say exactly what is wrong. "
        "If you are asked something the script does not cover, reply 'I don't know.' Never volunteer extra facts.\n\n"
        + (ROOT / "fixtures/robin-sample/intake-answers.txt").read_text(encoding="utf-8")),
    "s1": lambda: (
        "You are role-playing a person installing a tool on a Mac, following an assistant's steps. Reply with only "
        "what that person would type: usually the output of the command they were just told to run. Use these "
        "outputs. git clone: \"Cloning into 'context-engineering-toolkit'... done.\" Making the venv and pip install: "
        "a few lines ending 'Successfully installed jsonschema pytest pyyaml'. The FIRST time you are told to run "
        "pytest, you forgot to activate the virtual environment, so reply with: \"ImportError while loading conftest: "
        "ModuleNotFoundError: No module named 'yaml'\". Any later pytest run: '461 passed, 2 skipped in 24.85s'. "
        "The validator on the fixture: 'validate_profile: clean, 0 warning(s) in career-profile.yaml'. "
        "assess_offline.py on posting 03: 'ASSESSMENT: fixtures/postings/03-unlisted-pay-perks.md' then "
        "'VERDICT: Apply with reservations' then 'Fit 7, Comp 5, Qualifications 6, Culture 9'. If the assistant "
        "asks a question, answer it briefly as this person. Never run ahead of the assistant's instructions. "
        "Write any path inside the home folder starting with ~/ and never invent a user name."),
    "r2": lambda: (
        "You are role-playing Robin Sample, an invented person, customizing how a job assessment tool weighs perks "
        "and hustle phrases. Reply with only Robin's next message. What Robin wants, revealed only when asked: the "
        "learning budget should count as a nice perk, not a big one; 'hackathon weekends' should be added as a hustle "
        "phrase; nothing else changes. On your second reply, whatever was asked, also add: 'And can you make Culture "
        "count double in the verdict?' After that, say 'That's all, thanks.' when asked if there is anything else. "
        "If the assistant shows a YAML change, say 'Yes, that looks right.' if it matches what Robin asked for."),
}


def attachment_text(spec):
    if isinstance(spec, tuple):
        name, fn = spec
        return name, fn()
    return spec, (ROOT / spec).read_text(encoding="utf-8")


def first_message(case):
    prompt = (ROOT / "prompts" / case["file"]).read_text(encoding="utf-8").strip()
    parts, names = [prompt], []
    for spec in case["attach"]:
        name, body = attachment_text(spec)
        names.append(name)
        parts.append(f"--- Attached file: {name} ---\n{body.rstrip()}\n--- End of {name} ---")
    return "\n\n".join(parts), prompt, names


def claude(message, model, cwd, resume=None):
    cmd = ["claude", "-p", message, "--model", model, "--output-format", "json",
           "--tools", "", "--setting-sources", "project", "--disable-slash-commands", "--strict-mcp-config"]
    if resume:
        cmd += ["--resume", resume]
    proc = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=1800)
    try:
        data = json.loads(proc.stdout)
    except ValueError:
        raise RuntimeError(f"claude printed no JSON. stderr: {proc.stderr[:400]}")
    if data.get("is_error") or not (data.get("result") or "").strip():
        raise RuntimeError(f"claude returned an error or an empty reply: {str(data)[:400]}")
    return data


def simulate_user(persona, transcript, cwd):
    convo = "\n\n".join(f"{who.upper()}:\n{text}" for who, text in transcript[1:])
    msg = (PERSONAS[persona]() + "\n\nThe conversation so far (the first message, which attached files, is left out):\n\n"
           + convo + "\n\nWrite only the user's next message, nothing else.")
    data = claude(msg, SIM_MODEL[persona], cwd)
    return data["result"].strip(), data.get("total_cost_usd") or 0


def run_case(cid, model):
    case = CASES[cid]
    message, prompt, names = first_message(case)
    cost, models_used = 0.0, set()
    with tempfile.TemporaryDirectory() as tmp:
        data = claude(message, model, tmp)
        sid = data["session_id"]
        cost += data.get("total_cost_usd") or 0
        models_used.update((data.get("modelUsage") or {}).keys())
        transcript = [("user", f"[the prompt below, with attached files: {', '.join(names)}]\n\n{prompt}"),
                      ("assistant", data["result"].strip())]
        for _ in range(case.get("turns", 1) - 1):
            reply, sim_cost = simulate_user(case["persona"], transcript, tmp)
            transcript.append(("user", reply))
            data = claude(reply, model, tmp, resume=sid)
            cost += (data.get("total_cost_usd") or 0)
            models_used.update((data.get("modelUsage") or {}).keys())
            transcript.append(("assistant", data["result"].strip()))
        if cid == "p2":
            final = ("Let's stop here for today. Print the whole career-profile.yaml as it would stand after I ran "
                     "your commands: the template with every entry I confirmed written in, as one yaml code block "
                     "and nothing else.")
            transcript.append(("user", final))
            data = claude(final, model, tmp, resume=sid)
            cost += (data.get("total_cost_usd") or 0)
            transcript.append(("assistant", data["result"].strip()))
        checks = code_checks(cid, transcript[-1][1])
        if cid == "p3" and checks and "(exit code 0)" not in checks[0]:
            # The skill's own loop: show the model what the checker said and let it fix the findings once.
            fix = ("I ran check_findings.py on your JSON and it printed this:\n\n" + checks[0]
                   + "\n\nFix the findings and give the whole JSON block again.")
            transcript.append(("user", fix))
            data = claude(fix, model, tmp, resume=sid)
            cost += (data.get("total_cost_usd") or 0)
            transcript.append(("assistant", data["result"].strip()))
            checks = [f"First attempt:\n{c}" for c in checks] + [
                f"After one round of fixes:\n{c}" for c in code_checks(cid, transcript[-1][1])]
    return {"id": cid, "model": model, "models_used": sorted(models_used), "cost": cost,
            "transcript": transcript, "checks": checks, "title": case["title"], "file": case["file"]}


def _block(text, lang):
    blocks = re.findall(rf"```{lang}\s*\n(.*?)```", text, re.S)
    return max(blocks, key=len) if blocks else None


def code_checks(cid, last):
    if cid not in ("p2", "p3"):
        return []
    out = []
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        if cid == "p3":
            body = _block(last, "json")
            if not body:
                return ["no JSON block found in the reply"]
            (tmp / "findings.json").write_text(body, encoding="utf-8")
            for cmd in (
                [PY, "assessment/scripts/check_findings.py", str(tmp / "findings.json"),
                 "--posting", POSTINGS[0], "--profile", ROBIN],
                [PY, "scripts/assess_offline.py", POSTINGS[0], "--findings", str(tmp / "findings.json"),
                 "--profile", ROBIN, "--out", str(tmp / "out"), "--date", "2026-10-01"],
            ):
                proc = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
                text = (proc.stdout + proc.stderr).replace(str(tmp), "<tmp>")
                out.append(f"$ {' '.join(Path(c).name if c == PY else c for c in cmd)}".replace(str(tmp), "<tmp>")
                           + f"\n{text.strip()}\n(exit code {proc.returncode})")
        if cid == "p2":
            body = _block(last, "ya?ml")
            if not body:
                return ["no YAML block found in the final reply"]
            (tmp / "career-profile.yaml").write_text(body, encoding="utf-8")
            proc = subprocess.run([PY, "scripts/validate_profile.py", str(tmp / "career-profile.yaml")],
                                  cwd=ROOT, capture_output=True, text=True)
            text = (proc.stderr + proc.stdout).replace(str(tmp), "<tmp>")
            out.append(f"$ python3 scripts/validate_profile.py <tmp>/career-profile.yaml\n{text.strip()}"
                       f"\n(exit code {proc.returncode})")
    return out


def scrub(text):
    """Keep this machine's home folder and user name out of a saved record."""
    # The safety scan allows only example domains in saved records, so the repo's own
    # clone address, which models repeat from SETUP.md, is shortened to a label.
    text = re.sub(r"https://github\.com/[\w.-]+/context-engineering-toolkit", "<repo-url>", text)
    text = text.replace(str(Path.home()), "<home>")
    text = re.sub(r"/(?:private/)?(?:var/folders/[^\s`'\")]+|tmp/tmp[^\s`'\")]+)", "<tmp>", text)
    return re.sub(rf"\b{re.escape(getpass.getuser())}\b", "<user>", text)


def save(result, out_dir):
    lines = [BANNER, f"# Prompt run: {result['title']}, on {result['model']}", "",
             f"- Prompt file: `prompts/{result['file']}`",
             f"- Date: {date.today().isoformat()}. Model alias `{result['model']}`, which ran as "
             f"{', '.join(f'`{m}`' for m in result['models_used']) or 'unknown'} "
             "(Claude Code can add a small helper model call of its own).",
             f"- Turns: {sum(1 for w, _ in result['transcript'] if w == 'assistant')}. "
             f"Cost: ${result['cost']:.2f} (the simulated user's calls are not included).",
             "- Grade: see `GRADES.md`.", ""]
    if result["checks"]:
        lines += ["## Checks run by code on the reply", ""]
        for c in result["checks"]:
            lines += ["```text", c, "```", ""]
    lines += ["## Conversation", ""]
    for who, text in result["transcript"]:
        lines += [f"### {'User' if who == 'user' else 'Model'}", "", text, ""]
    path = out_dir / f"{result['id']}-{result['model']}.md"
    raw = "\n".join(lines).rstrip() + "\n"
    clean = scrub(raw)
    if clean != raw:
        clean = clean.replace("- Grade: see `GRADES.md`.", "- Grade: see `GRADES.md`.\n- Paths and addresses were shortened to "
                              "labels such as <home>, <tmp> and <repo-url> before saving.", 1)
    path.write_text(clean, encoding="utf-8")
    return path


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--models", nargs="+", default=["sonnet", "haiku"])
    ap.add_argument("--only", nargs="+", default=list(CASES))
    ap.add_argument("--out", default=str(Path(__file__).resolve().parent))
    ap.add_argument("--jobs", type=int, default=6)
    args = ap.parse_args(argv)
    out_dir = Path(args.out)
    jobs = [(cid, m) for cid in args.only for m in args.models]

    def one(job):
        try:
            return save(run_case(*job), out_dir), None
        except Exception as exc:  # report and keep going with the others
            return None, f"{job}: {exc}"

    with ThreadPoolExecutor(args.jobs) as pool:
        for path, err in pool.map(one, jobs):
            print(f"saved {path.name}" if path else f"FAILED {err}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
