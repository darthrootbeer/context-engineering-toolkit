#!/usr/bin/env python3
"""Run the three "Prompt for your AI model" prompts of each pattern doc on Sonnet and Haiku.

Same method as pipelines/docs-pipeline/tests/prompt-runs: `claude -p` with no tools, no
project instructions and no automatic memory, the doc pasted where the prompt says [PASTE FILE], the other bracketed
inputs replaced with made-up samples. Writes one record per doc, prompt and model into
prompt-runs/. Needs the `claude` command line tool; the normal test suite does not run this.

Usage: python3 run_prompts.py [doc-stem ...]
"""
import os, re, subprocess, sys, tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
PATTERNS = HERE.parent
OUT = HERE / "prompt-runs"
MODELS = ["sonnet", "haiku"]

SAMPLES = {
    "block-and-tell-hooks": {
        2: {"[DESCRIBE YOUR SETUP]": "I use Claude Code. Hooks are enabled in ~/.claude/settings.json. Today my rules are prose in a CLAUDE.md file: always run the tests before a merge, never edit files under migrations/ without reading docs/MIGRATIONS.md, and keep commit messages short."},
        3: {"[YOUR \"ALWAYS DO X FIRST\" RULE]": "Before editing any file under migrations/, read docs/MIGRATIONS.md in the same session.", "[YOUR AGENT TOOL]": "Claude Code"},
    },
    "rules-index-architecture": {
        2: {"[PASTE LISTING AND TOOL NAME]": "Tool: Claude Code.\nCLAUDE.md 410 lines\nrules/git.md 90 lines\nrules/testing.md 60 lines\nrules/deploy.md 120 lines\nrules/old-notes.md 300 lines (rarely needed)"},
        3: {"[YOUR AGENT TOOL]": "Claude Code", "[PASTE YOUR INSTRUCTIONS FILE]": "# Project rules\n\n## Git\nUse short commit messages. Never push to main.\n\n## Testing\nRun pytest before every merge. Add a test for every bug fix.\n\n## Deploys\nDeploys go through make deploy. Check the changelog first. Never deploy on Fridays.\n\n## Style\nUse type hints. Keep functions under 40 lines.\n\n## Old migration notes\nThe 2023 migration moved the billing tables. See docs/billing-2023.md for the details."},
    },
    "typed-memory-system": {
        2: {"[PASTE LISTING AND TOOL NAME]": "Tool: Claude Code.\nMEMORY.md 182 lines, 21,400 bytes\nuser_role.md 12 lines\nfeedback_testing.md 20 lines\nfeedback_commits.md 15 lines\nproject_billing_rewrite.md 40 lines\nreference_dashboards.md 8 lines"},
        3: {"[YOUR AGENT TOOL]": "Claude Code", "[LIST FIVE FACTS, PREFERENCES AND CORRECTIONS]": "1. I am a backend engineer who knows Go but not React. 2. Do not mock the database in integration tests; we got burned when mocks passed and the real migration failed. 3. Yes, the single bundled PR was the right call for the refactor. 4. The billing rewrite must finish before 2026-12-01 because of an audit. 5. Pipeline bugs are tracked in the Ops board in the issue tracker."},
    },
}


def extract_prompts(text):
    sec = text.split("## Prompt for your AI model", 1)[1]
    blocks = re.findall(r"\*\*(\d)\. ([^\n]*)\*\*\n\n```\n(.*?)\n```", sec, re.S)
    return {int(n): (title, body) for n, title, body in blocks}


def run(stem, n, title, body, doc_text, model):
    shown = body
    for k, v in SAMPLES[stem].get(n, {}).items():
        shown = shown.replace(k, v)
    sent = shown.replace("[PASTE FILE]", doc_text)
    with tempfile.TemporaryDirectory() as scratch:
        p = subprocess.run(
            ["claude", "-p", "--model", model, "--tools", "", "--setting-sources", "project"],
            input=sent, capture_output=True, text=True, cwd=scratch, timeout=600,
            env={**os.environ, "CLAUDE_CODE_DISABLE_AUTO_MEMORY": "1"})
    ans = p.stdout.strip() if p.returncode == 0 else f"RUN FAILED (exit {p.returncode}): {p.stderr.strip()}"
    kind = ["", "teach", "review", "adapt"][n]
    rec = (f"# {stem} prompt {n} ({title}) on {model}\n\n"
           "Prompt (the document's full text was pasted where it says [PASTE FILE]; other inputs filled with made-up samples):\n\n"
           f"```text\n{shown}\n```\n\nAnswer:\n\n{ans}\n")
    (OUT / f"{stem}-{kind}-{model}.md").write_text(rec)
    return stem, kind, model, p.returncode


def main():
    OUT.mkdir(exist_ok=True)
    stems = sys.argv[1:] or list(SAMPLES)
    jobs = []
    with ThreadPoolExecutor(max_workers=6) as ex:
        for stem in stems:
            doc = (PATTERNS / f"{stem}.md").read_text()
            for n, (title, body) in extract_prompts(doc).items():
                for m in MODELS:
                    jobs.append(ex.submit(run, stem, n, title, body, doc, m))
        for j in jobs:
            print(*j.result())


if __name__ == "__main__":
    main()
