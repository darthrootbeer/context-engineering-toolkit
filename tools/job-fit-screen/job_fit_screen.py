#!/usr/bin/env python3
"""
job-fit-screen
Scores a real job posting against a personal fit-criteria YAML file, using
Claude to make the judgment calls the criteria file itself requires (context,
negation, working-philosophy fit) rather than naive keyword matching.
"""

import json
import os
import sys
from pathlib import Path
from typing import Optional

import click
import yaml
import httpx
from anthropic import Anthropic
from rich.console import Console
from rich.panel import Panel

console = Console()

ANTHROPIC_MODEL = "claude-sonnet-5"

SEVERITY_ICON = {
    "strong": "🔴",
    "soft": "🟡",
}
STATUS_ICON = {
    "pass": "🟢",
    "fail": "🔴",
    "unclear": "🔵",
}


class JobFitScreener:
    def __init__(self, criteria_path: Path):
        self.criteria_path = criteria_path
        self.criteria = self.load_criteria(criteria_path)
        self.client = Anthropic()  # reads ANTHROPIC_API_KEY from env

    def load_criteria(self, path: Path) -> dict:
        """Load and parse the criteria YAML file."""
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
        except yaml.YAMLError as e:
            raise click.ClickException(f"Criteria file is not valid YAML: {e}")
        except FileNotFoundError:
            raise click.ClickException(f"Criteria file not found: {path}")

        if not isinstance(data, dict):
            raise click.ClickException("Criteria file did not parse to a mapping — check its structure.")
        return data

    def load_posting(self, source: str) -> str:
        """Load posting text from a local file path or a URL."""
        if source.startswith("http://") or source.startswith("https://"):
            try:
                resp = httpx.get(source, timeout=30, follow_redirects=True)
                resp.raise_for_status()
            except httpx.HTTPError as e:
                raise click.ClickException(f"Failed to fetch posting URL: {e}")
            # Best-effort plain text — strips HTML tags crudely. Postings
            # rendered client-side (JS-heavy job boards) may come back thin;
            # if so, save the posting to a text file and pass that instead.
            import re
            text = re.sub(r"<script.*?</script>", "", resp.text, flags=re.DOTALL | re.IGNORECASE)
            text = re.sub(r"<style.*?</style>", "", text, flags=re.DOTALL | re.IGNORECASE)
            text = re.sub(r"<[^>]+>", " ", text)
            text = re.sub(r"\s+", " ", text).strip()
            if len(text) < 200:
                console.print(
                    "[yellow]⚠️  Fetched content looks thin — this posting may render via "
                    "JavaScript. Save the posting text to a .txt file and pass that instead.[/yellow]"
                )
            return text

        path = Path(source)
        if not path.exists():
            raise click.ClickException(f"Posting file not found: {source}")
        return path.read_text(encoding="utf-8")

    def build_prompt(self, posting_text: str) -> str:
        criteria_yaml = yaml.safe_dump(self.criteria, sort_keys=False, allow_unicode=True)
        return f"""You are screening a job posting against a candidate's personal fit criteria.
The criteria file below explicitly requires real reading comprehension, not keyword
matching — handle negation ("no relocation required" is NOT a relocation requirement),
euphemisms, and implied meaning the way a careful human reader would.

For every verdict, quote or closely paraphrase the SPECIFIC posting language behind
it. A verdict with no evidence is not usable — never state a conclusion without
citing the words in the posting that led to it. If the posting doesn't address
something, say so plainly rather than guessing.

<criteria_yaml>
{criteria_yaml}
</criteria_yaml>

<job_posting>
{posting_text}
</job_posting>

Respond with ONLY a JSON object (no markdown fences, no commentary before or after)
in exactly this shape:

{{
  "hard_blocks": [
    {{"id": "<id from criteria>", "tripped": true/false, "evidence": "<quote or 'not mentioned'>"}}
  ],
  "requirements": [
    {{"id": "<id>", "severity": "<from criteria>", "status": "pass|fail|unclear", "evidence": "<quote>"}}
  ],
  "autonomy_filter": {{"assessment": "<1-3 sentences, citing specific posting language>"}},
  "keyword_signals": {{
    "strong_positive": [{{"phrase": "<matched phrase or close paraphrase>", "context": "<surrounding quote>"}}],
    "positive": [...],
    "negative": [...],
    "strong_negative": [...]
  }},
  "qualifications_match": {{
    "years_requirement_met": "yes|no|unclear|not_stated",
    "years_evidence": "<quote of the posting's stated requirement, if any>",
    "core_skills_alignment": "<1-3 sentences on how well required/standout language matches core_skills_and_evidence>",
    "known_gaps_present": "<1-3 sentences on whether required experience leans on known_gaps>",
    "working_philosophy_fit": "<1-3 sentences on whether the role expects the working_philosophy stance or its opposite>"
  }},
  "soft_flags": [
    {{"id": "<id>", "present": true/false, "evidence": "<quote or 'not mentioned'>"}}
  ],
  "bottom_line": "<2-4 sentence plain-language summary of whether this is worth applying to, and why>"
}}

Only include ids that actually exist in the criteria file above — do not invent ids."""

    def score(self, posting_text: str) -> dict:
        """Send criteria + posting to Claude, return the parsed verdict."""
        prompt = self.build_prompt(posting_text)
        try:
            response = self.client.messages.create(
                model=ANTHROPIC_MODEL,
                max_tokens=4096,
                messages=[{"role": "user", "content": prompt}],
            )
        except Exception as e:
            raise click.ClickException(f"Claude API call failed: {e}")

        raw_text = "".join(block.text for block in response.content if hasattr(block, "text"))
        raw_text = raw_text.strip()
        if raw_text.startswith("```"):
            raw_text = raw_text.split("```")[1]
            if raw_text.startswith("json"):
                raw_text = raw_text[4:]
            raw_text = raw_text.strip()

        try:
            return json.loads(raw_text)
        except json.JSONDecodeError as e:
            raise click.ClickException(
                f"Could not parse Claude's response as JSON: {e}\n\nRaw response:\n{raw_text[:1000]}"
            )

    def render_report(self, result: dict):
        """Print a readable terminal scorecard."""
        console.print()
        console.rule("[bold]job-fit-screen report[/bold]")

        hard_blocks = result.get("hard_blocks", [])
        tripped = [h for h in hard_blocks if h.get("tripped")]
        console.print("\n[bold]Hard blocks[/bold]")
        if not hard_blocks:
            console.print("  [dim]none defined in criteria[/dim]")
        for h in hard_blocks:
            icon = "🔴" if h.get("tripped") else "🟢"
            console.print(f"  {icon} {h.get('id')} — {h.get('evidence', '')}")

        console.print("\n[bold]Requirements[/bold]")
        for r in result.get("requirements", []):
            sev = SEVERITY_ICON.get(r.get("severity"), "⚪")
            status = STATUS_ICON.get(r.get("status"), "🔵")
            console.print(f"  {status} {sev} {r.get('id')} — {r.get('evidence', '')}")

        af = result.get("autonomy_filter", {})
        if af.get("assessment"):
            console.print("\n[bold]Autonomy filter[/bold]")
            console.print(f"  {af['assessment']}")

        ks = result.get("keyword_signals", {})
        console.print("\n[bold]Keyword signals[/bold]")
        for tier, icon in [("strong_positive", "🟢🟢"), ("positive", "🟢"), ("negative", "🟠"), ("strong_negative", "🔴")]:
            for k in ks.get(tier, []):
                console.print(f"  {icon} \"{k.get('phrase')}\" — {k.get('context', '')}")

        qm = result.get("qualifications_match", {})
        if qm:
            console.print("\n[bold]Qualifications match[/bold]")
            console.print(f"  Years requirement met: {qm.get('years_requirement_met', 'unclear')}")
            if qm.get("years_evidence"):
                console.print(f"    {qm['years_evidence']}")
            if qm.get("core_skills_alignment"):
                console.print(f"  Core skills alignment: {qm['core_skills_alignment']}")
            if qm.get("known_gaps_present"):
                console.print(f"  Known gaps: {qm['known_gaps_present']}")
            if qm.get("working_philosophy_fit"):
                console.print(f"  Working philosophy fit: {qm['working_philosophy_fit']}")

        console.print("\n[bold]Soft flags[/bold]")
        for s in result.get("soft_flags", []):
            icon = "🟠" if s.get("present") else "⚪"
            console.print(f"  {icon} {s.get('id')} — {s.get('evidence', '')}")

        if tripped:
            console.print()
            console.print(Panel(
                f"[bold red]Hard block(s) tripped: {', '.join(h['id'] for h in tripped)}[/bold red]\n"
                f"This posting is disqualified regardless of anything else below.",
                title="⛔ Disqualified",
            ))
        elif result.get("bottom_line"):
            console.print()
            console.print(Panel(result["bottom_line"], title="👉 Bottom line"))

    def save_json(self, result: dict, path: Path):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2)
        console.print(f"\n[dim]Full result saved to {path}[/dim]")


@click.command()
@click.option("--criteria", required=True, type=click.Path(exists=True), help="Path to your criteria YAML file.")
@click.option("--posting", required=True, help="Path to a posting text file, or a URL to fetch.")
@click.option("--json-out", type=click.Path(), default=None, help="Optional path to also save the full result as JSON.")
def main(criteria: str, posting: str, json_out: Optional[str]):
    """Score a job posting against your personal fit criteria."""
    if not os.environ.get("ANTHROPIC_API_KEY"):
        raise click.ClickException(
            "ANTHROPIC_API_KEY is not set. Get a key from console.anthropic.com and "
            "export it: export ANTHROPIC_API_KEY=sk-ant-..."
        )

    screener = JobFitScreener(Path(criteria))
    console.print(f"[dim]Loading posting from {posting}...[/dim]")
    posting_text = screener.load_posting(posting)

    console.print("[dim]Scoring against criteria...[/dim]")
    result = screener.score(posting_text)

    screener.render_report(result)

    if json_out:
        screener.save_json(result, Path(json_out))


if __name__ == "__main__":
    main()
