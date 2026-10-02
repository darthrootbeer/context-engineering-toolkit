"""The prompt blocks in the docs are the prompts that were tested, word for word.

Every doc ends with a "Prompt for your AI model" section. Each block in it is
preceded by a marker naming its file in prompts/, and the block text must equal
that file. The tested prompt and the published prompt can therefore never drift
apart. Every prompt file must also have a saved run on both tested models and a
grade in tests/prompt-runs/GRADES.md.
"""
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
PROMPTS = ROOT / "prompts"
RUNS = ROOT / "tests" / "prompt-runs"
DOCS = [
    "README.md",
    "ARCHITECTURE.md",
    "SETUP.md",
    "intake/README.md",
    "assessment/README.md",
    "assessment/hooks/README.md",
    "fixtures/README.md",
]
MODELS = ("sonnet", "haiku")
HEADING = "### Prompt for your AI model"
MARKER = re.compile(r"<!-- prompt: (prompts/[^ ]+\.txt) -->\n```text\n(.*?)```", re.S)
FENCE = re.compile(r"^```text\n(.*?)^```", re.S | re.M)
MAJOR_SECTION_LINES = 60


def read(rel):
    return (ROOT / rel).read_text(encoding="utf-8")


def prompt_files():
    return sorted(p.name for p in PROMPTS.glob("*.txt"))


def run_id(name):
    """prompts/03-run-first-posting.txt -> p3, prompts/r1-review-rules.txt -> r1."""
    head = name.split("-", 1)[0]
    return f"p{int(head)}" if head.isdigit() else head


def h2_sections(text):
    """(heading, body) for each H2 section, ignoring headings inside code fences."""
    sections, current, body, in_fence = [], None, [], False
    for line in text.splitlines():
        if line.startswith("```"):
            in_fence = not in_fence
        if not in_fence and line.startswith("## "):
            if current is not None:
                sections.append((current, body))
            current, body = line, []
        elif current is not None:
            body.append(line)
    if current is not None:
        sections.append((current, body))
    return sections


def test_there_are_ten_prompt_files():
    assert len(prompt_files()) == 10, prompt_files()


@pytest.mark.parametrize("doc", DOCS)
def test_doc_ends_with_a_prompt_section(doc):
    text = read(doc)
    assert HEADING in text, f"{doc} has no '{HEADING}' section"
    tail = text[text.rindex(HEADING):]
    assert MARKER.search(tail), f"{doc}: its last prompt section has no marked prompt block"
    assert not re.search(r"^#{1,3} ", tail[len(HEADING):], re.M), f"{doc}: a heading follows its last prompt section"


@pytest.mark.parametrize("doc", DOCS)
def test_every_block_equals_its_prompt_file(doc):
    text = read(doc)
    found = MARKER.findall(text)
    assert found, f"{doc} has no marked prompt blocks"
    for rel, body in found:
        path = ROOT / rel
        assert path.exists(), f"{doc} names {rel}, which does not exist"
        assert body.strip() == path.read_text(encoding="utf-8").strip(), f"{doc}: block for {rel} differs from the file"


@pytest.mark.parametrize("doc", DOCS)
def test_no_unmarked_text_blocks_in_prompt_sections(doc):
    text = read(doc)
    for part in text.split(HEADING)[1:]:
        part = re.split(r"^#{1,2} ", part, maxsplit=1, flags=re.M)[0]
        marked = len(MARKER.findall(part))
        fences = len(FENCE.findall(part))
        assert fences == marked, f"{doc}: a prompt section holds a text block with no prompt marker"


@pytest.mark.parametrize("doc", DOCS)
def test_no_untested_markers_remain(doc):
    text = read(doc).lower()
    assert "<!-- untested" not in text
    assert "not yet tested" not in text


@pytest.mark.parametrize("doc", DOCS)
def test_doc_names_the_tested_models_and_date(doc):
    tail = read(doc)[read(doc).rindex(HEADING):]
    line = next((l for l in tail.splitlines() if l.startswith("**Tested on:**")), None)
    assert line, f"{doc}: no 'Tested on' line after its prompts"
    assert "Sonnet" in line and "Haiku" in line, line
    assert re.search(r"\b20\d\d-\d\d-\d\d\b", line), line


@pytest.mark.parametrize("doc", DOCS)
def test_long_sections_carry_a_prompt_block(doc):
    for heading, body in h2_sections(read(doc)):
        if len(body) > MAJOR_SECTION_LINES:
            assert HEADING in "\n".join(body), f"{doc}: '{heading}' is {len(body)} lines with no prompt block"


def test_every_prompt_file_is_published_in_a_doc():
    used = {rel for doc in DOCS for rel, _ in MARKER.findall(read(doc))}
    missing = {f"prompts/{name}" for name in prompt_files()} - used
    assert not missing, f"prompt files not shown in any doc: {sorted(missing)}"


def test_readme_carries_the_six_core_prompts():
    used = {rel for rel, _ in MARKER.findall(read("README.md"))}
    core = {f"prompts/{name}" for name in prompt_files() if name[0].isdigit()}
    assert len(core) == 6 and core <= used, sorted(core - used)


@pytest.mark.parametrize("name", prompt_files())
def test_every_prompt_has_a_saved_run_on_each_model(name):
    for model in MODELS:
        record = RUNS / f"{run_id(name)}-{model}.md"
        assert record.exists(), f"no saved run {record.name} for {name}"
        text = record.read_text(encoding="utf-8")
        assert "### Model" in text and len(text) > 500, f"{record.name} looks empty"


@pytest.mark.parametrize("name", prompt_files())
def test_every_prompt_is_graded_on_each_model(name):
    grades = (RUNS / "GRADES.md").read_text(encoding="utf-8")
    row = next((l for l in grades.splitlines() if f"`{name}`" in l and l.startswith("|")), None)
    assert row, f"GRADES.md has no row for {name}"
    cells = [c.strip() for c in row.strip("|").split("|")]
    verdicts = [c for c in cells if re.match(r"^(PASS|FAIL|PARTIAL)\b", c)]
    assert len(verdicts) == len(MODELS), f"{name}: expected one grade per model, got {verdicts}"


def test_readme_opens_with_what_it_is_and_a_quickstart():
    text = read("README.md")
    first_screen = "\n".join(text.splitlines()[:12])
    assert "**What it is.**" in first_screen
    assert "../docs-pipeline/" in first_screen
    headings = re.findall(r"^## (.+)$", text, re.M)
    assert headings[0].startswith("Quickstart"), headings[:3]
