"""Shared helpers for the live runs: a clean work folder, one claude call, a readable record."""
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
TESTS = ROOT / "tests"
MODEL = os.environ.get("JA_LIVE_MODEL", "sonnet")
TIMEOUT = int(os.environ.get("JA_LIVE_TIMEOUT", "3000"))
IGNORE = shutil.ignore_patterns("tests", "fixtures", "__pycache__", ".pytest_cache", ".venv", "*.pyc")


def make_workdir(base: Path) -> Path:
    """Copy the pipeline without its tests and fixtures, so the model cannot read the answer key.

    A `python3` that is the interpreter running this test goes first on PATH, so the skills'
    `python3 ...` commands find pyyaml.
    """
    work = base / "pipeline"
    shutil.copytree(ROOT, work, ignore=IGNORE)
    bin_dir = base / "bin"
    bin_dir.mkdir()
    (bin_dir / "python3").symlink_to(sys.executable)
    return work


def run_claude(prompt: str, cwd: Path, bin_dir: Path):
    """One print-mode run with full tool use inside cwd. Returns (events, final_result_dict)."""
    env = dict(os.environ)
    env["PATH"] = f"{bin_dir}{os.pathsep}{env.get('PATH', '')}"
    cmd = [
        "claude", "-p", prompt,
        "--model", MODEL,
        "--output-format", "stream-json", "--verbose",
        "--setting-sources", "project",       # no personal settings, hooks or memory files
        "--disable-slash-commands", "--strict-mcp-config", "--no-session-persistence",
        "--permission-mode", "acceptEdits",
        "--allowedTools", "Read", "Write", "Edit", "Bash",
    ]
    proc = subprocess.run(cmd, cwd=cwd, env=env, capture_output=True, text=True, timeout=TIMEOUT)
    events = []
    for line in proc.stdout.splitlines():
        try:
            events.append(json.loads(line))
        except ValueError:
            continue
    final = next((e for e in reversed(events) if e.get("type") == "result"), {})
    return proc, events, final


def _clip(text, n):
    text = text.strip()
    return text if len(text) <= n else text[:n] + f"\n... ({len(text) - n} more characters)"


def render_record(events, scrub, clip=700):
    """Turn the event stream into markdown: what the model said, the commands it ran, what came back."""
    out = []
    for e in events:
        msg = e.get("message") or {}
        content = msg.get("content")
        if e.get("type") == "assistant" and isinstance(content, list):
            for part in content:
                if part.get("type") == "text" and part["text"].strip():
                    out.append(scrub(part["text"].strip()) + "\n")
                elif part.get("type") == "tool_use":
                    inp = part.get("input", {})
                    if part["name"] == "Bash":
                        out.append("```text\n$ " + scrub(_clip(inp.get("command", ""), 1200)) + "\n```\n")
                    else:
                        target = inp.get("file_path") or inp.get("path") or ""
                        out.append(f"*{part['name']}* `{scrub(str(target))}`\n")
        elif e.get("type") == "user" and isinstance(content, list):
            for part in content:
                if part.get("type") == "tool_result":
                    body = part.get("content")
                    if isinstance(body, list):
                        body = "\n".join(b.get("text", "") for b in body if isinstance(b, dict))
                    out.append("```text\n" + scrub(_clip(str(body or ""), clip)) + "\n```\n")
    return "\n".join(out)


def make_scrub(work: Path):
    """Replace this machine's paths so a saved record names no one's folders."""
    pairs = [(str(work.resolve()), "<work>"), (str(work), "<work>"), (str(work.parent.resolve()), "<tmp>"),
             (str(work.parent), "<tmp>"), (str(Path.home()), "<home>")]

    def scrub(text):
        for old, new in pairs:
            text = text.replace(old, new)
        text = re.sub(r"/(?:private/)?(?:var/folders|tmp)/\S+", "<tmp>", text)
        text = re.sub(r"/Users/[^/\s]+", "<home>", text)
        return re.sub(r"<home>/\S*", "<home>", text)
    return scrub


def assert_ran(proc, events, final):
    """A print-mode run can fail silently. Prove it did real work before trusting anything."""
    assert events, f"claude printed no events. stderr: {proc.stderr[:500]}"
    assert final, "the run never reported a result"
    assert not final.get("is_error"), f"claude reported an error: {str(final.get('result'))[:500]}"
    assert (final.get("result") or "").strip(), "claude finished with an empty reply"
    tool_calls = sum(1 for e in events if e.get("type") == "assistant"
                     for p in (e.get("message", {}).get("content") or []) if p.get("type") == "tool_use")
    assert tool_calls > 0, "claude ran no commands, so nothing was produced"
    return tool_calls
