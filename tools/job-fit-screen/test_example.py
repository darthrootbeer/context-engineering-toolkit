#!/usr/bin/env python3
"""
Test fixture for job-fit-screen.
Creates a fake, fully genericized job posting (no real company) and runs the
scorer against criteria.example.yaml, so the tool can be verified without
needing a real criteria file or API costs beyond one test call.
"""

import subprocess
import sys
from pathlib import Path

FAKE_POSTING = """Senior Content Engineer (Remote)

About the role

We're a fictional example company looking for someone to own our documentation
end to end. You'll build our documentation strategy from scratch — we don't
have a dedicated writer today. You'll partner with engineers to gather source
material, and we don't micromanage: we hire people for their judgment.

We use AI tooling throughout our workflow, including for drafting and
refining documentation content.

What we're looking for

5+ years of technical writing or content engineering experience.
Experience with docs-as-code workflows (Git, Markdown).
Comfortable working autonomously with minimal oversight.

Nice to have

Experience with structured content and information architecture.
Familiarity with AI-assisted content workflows.

Location: Fully remote, US time zones.
Pay range: $110,000 - $140,000 USD.
"""


def main():
    fixture_dir = Path(__file__).parent
    posting_path = fixture_dir / "_test_posting.txt"
    posting_path.write_text(FAKE_POSTING, encoding="utf-8")

    criteria_path = fixture_dir / "criteria.example.yaml"
    if not criteria_path.exists():
        print(f"❌ {criteria_path} not found — run this from the job-fit-screen directory.")
        sys.exit(1)

    print("Running job_fit_screen.py against a fake test posting...")
    print("=" * 60)

    result = subprocess.run(
        [sys.executable, str(fixture_dir / "job_fit_screen.py"),
         "--criteria", str(criteria_path),
         "--posting", str(posting_path)],
        cwd=fixture_dir,
    )

    posting_path.unlink(missing_ok=True)

    if result.returncode != 0:
        print("\n❌ Test run failed — see output above.")
        sys.exit(1)

    print("\n✅ Test run completed. Review the report above — it won't score")
    print("   meaningfully well or poorly since criteria.example.yaml is all")
    print("   placeholder text, but it confirms the tool runs end to end.")


if __name__ == "__main__":
    main()
