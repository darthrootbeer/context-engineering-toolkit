#!/usr/bin/env python3
"""Parse a job posting, split its requirements, and archive it as a note.

Takes a posting (a file, pasted text on stdin, or an optional URL), lifts
every requirement and responsibility line, and marks each one as "likely
real" or "likely filter". Then it writes the whole posting to an archive
folder as a markdown note with the identity and state fields the rest of the
pipeline reads.

The split follows Modestino, Shoag and Ballance, "Upskilling: Do Employers
Demand Greater Skill When Workers Are Plentiful?", Review of Economics and
Statistics 102(4), 793-805 (2020). They found that employers raise education
and experience requirements when workers are plentiful, so those lines partly
track the labour market, not the job. Credential lines and years-of-experience
lines therefore default to "likely filter". Responsibility lines and lines that
name a tool default to "likely real". The split is a reading aid, not a score.

Nothing here invents a requirement, rewrites the posting's wording, or scores
anyone against it. Requirement text is kept word for word.

Exit codes: 0 done, 1 could not read or write, 4 duplicate (the same posting
is already archived for the same lane; re-run with --force to archive again).

Usage:
    parse_posting.py posting.md --company "Examplon Co" --role "Docs Lead" \\
        --lane docs-platform --archive-dir ./archive
    cat posting.txt | parse_posting.py --company X --role Y --lane L \\
        --archive-dir ./archive --url https://example.com/jobs/123
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from urllib.parse import parse_qs, urlparse

EXIT_OK = 0
EXIT_ERROR = 1
EXIT_DUPLICATE = 4

# ---------------------------------------------------------------------------
# Classification vocabulary
# ---------------------------------------------------------------------------

# A degree, certification, or clearance. This category tracks the labour
# market, so it defaults to a filter.
CREDENTIAL_RE = re.compile(
    r"\b(bachelor'?s?|master'?s?|ph\.?d|b\.?s\.?|b\.?a\.?|m\.?s\.?|mba|degree|"
    r"diploma|certifi(?:ed|cation)|accredit|licen[sc]e[d]?|clearance)\b",
    re.IGNORECASE,
)

# "5+ years", "at least three years", "5-7 years of experience".
YEARS_RE = re.compile(
    r"\b(\d+\s*\+?\s*(?:-|–|to)?\s*\d*\s*years?|"
    r"(?:one|two|three|four|five|six|seven|eight|nine|ten)\s+(?:or more\s+)?years?)\b",
    re.IGNORECASE,
)

# A responsibility describes the work.
RESPONSIBILITY_VERBS = {
    "own", "owns", "lead", "leads", "write", "writes", "build", "builds",
    "design", "designs", "maintain", "maintains", "partner", "partners",
    "collaborate", "collaborates", "drive", "drives", "create", "creates",
    "develop", "develops", "manage", "manages", "support", "supports",
    "review", "reviews", "produce", "produces", "deliver", "delivers",
    "coordinate", "coordinates", "evaluate", "evaluates", "improve",
    "improves", "define", "defines", "document", "documents", "edit",
    "edits", "plan", "plans", "run", "runs", "ship", "ships", "test",
    "tests", "research", "translate", "translates", "contribute",
    "contributes", "establish", "establishes", "pilot", "pilots",
    "publish", "publishes", "audit", "audits", "mentor", "mentors",
}

# Named tools and technologies. A concrete named tool is the clearest sign
# that a line describes the work. A fixed list on purpose: a capitalised word
# is not evidence of a tool, and guessing adds noise.
NAMED_TOOLS = {
    "git", "github", "gitlab", "bitbucket", "markdown", "asciidoc", "rst",
    "restructuredtext", "docusaurus", "mkdocs", "sphinx", "hugo", "jekyll",
    "confluence", "jira", "notion", "zendesk", "intercom", "madcap",
    "flare", "paligo", "document360", "readme", "readthedocs", "gitbook",
    "figma", "sketch", "adobe", "framemaker", "oxygen", "dita", "docbook",
    "swagger", "openapi", "postman", "graphql", "rest", "json", "yaml",
    "xml", "html", "css", "javascript", "typescript", "python", "sql",
    "bash", "shell", "docker", "kubernetes", "terraform", "aws", "azure",
    "gcp", "jenkins", "circleci", "netlify", "vercel", "vale", "algolia",
    "salesforce", "hubspot", "looker", "tableau", "snowflake", "databricks",
    "airflow", "kafka", "postgres", "postgresql", "mysql", "mongodb",
    "elasticsearch", "spark", "llm", "openai", "claude", "anthropic",
    "chatgpt", "copilot", "rag", "miro", "slack", "linear", "asana",
    "trello", "wordpress", "contentful", "sanity", "storyblok",
}

# Section headings that say what kind of list follows. Matched against a
# lowercased, punctuation-stripped line.
REQUIREMENT_HEADINGS = (
    "requirement", "qualification", "what you'll need", "what you need",
    "what we're looking for", "what we are looking for", "who you are",
    "about you", "must have", "must-have", "minimum", "basic qualification",
    "preferred", "nice to have", "nice-to-have", "bonus", "skills",
    "experience", "you have", "you bring", "the right person for this role",
)

RESPONSIBILITY_HEADINGS = (
    "responsibilit", "what you'll do", "what you will do", "what you do",
    "the role", "role overview", "your impact", "day to day", "day-to-day",
    "in this role", "what you'll be doing", "duties", "the job",
    "job description",
)

# Sections that are not requirements: benefits, legal text, pay. Lines under
# them are dropped before classification.
NOISE_HEADINGS = (
    "benefit", "perks", "compensation", "salary", "equal opportunity",
    "eeo", "about us", "about the company", "our values", "why join",
    "how to apply", "application process", "diversity", "accommodation",
    "privacy", "e-verify",
)

BULLET_PREFIX_RE = re.compile(r"^\s*(?:[-*•·‣▪◦]|\d+[.)])\s+")

# A posting's lane and source key are written into the note, so they stay
# plain words.
KEY_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9 _-]*$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------


@dataclass
class Requirement:
    """One line lifted from the posting, word for word, plus its class."""

    text: str  # verbatim, never rewritten
    kind: str  # skill | experience | credential | responsibility
    read_as: str  # "likely real" | "likely filter"
    reason: str  # why it landed on that side of the split


# ---------------------------------------------------------------------------
# Input
# ---------------------------------------------------------------------------


def looks_like_url(value: str) -> bool:
    return value.startswith("http://") or value.startswith("https://")


def fetch_url(url: str) -> str:
    """Fetch a posting URL with a plain GET and reduce it to readable text.

    Optional: needs the `requests` package. There is no fallback. If the page
    cannot be fetched the caller asks for pasted text, because returning a
    navigation menu as if it were the posting would be worse than failing.
    """
    import requests

    response = requests.get(
        url, timeout=30, headers={"User-Agent": "job-assessment-parse/1"}
    )
    response.raise_for_status()
    return clean_posting_text(html_to_text(response.text))


def html_to_text(html: str) -> str:
    """Crude but predictable HTML-to-text, standard library only."""
    text = re.sub(
        r"<(script|style|nav|footer|head)[^>]*>.*?</\1>",
        " ",
        html,
        flags=re.IGNORECASE | re.DOTALL,
    )
    # Keep list and block structure as line breaks before dropping tags.
    text = re.sub(r"<li[^>]*>", "\n- ", text, flags=re.IGNORECASE)
    text = re.sub(
        r"</(p|div|h[1-6]|li|ul|ol|tr|section)>", "\n", text, flags=re.IGNORECASE
    )
    text = re.sub(r"<br\s*/?>", "\n", text, flags=re.IGNORECASE)
    text = re.sub(r"<[^>]+>", " ", text)

    entities = {
        "&nbsp;": " ", "&amp;": "&", "&lt;": "<", "&gt;": ">",
        "&quot;": '"', "&#39;": "'", "&rsquo;": "'", "&lsquo;": "'",
        "&ldquo;": '"', "&rdquo;": '"', "&mdash;": "—", "&ndash;": "–",
    }
    for entity, char in entities.items():
        text = text.replace(entity, char)
    text = re.sub(r"&#x?[0-9a-fA-F]+;", " ", text)

    lines = [re.sub(r"[ \t]+", " ", line).strip() for line in text.splitlines()]
    return "\n".join(line for line in lines if line)


# Short button labels that job boards glue together on one line, such as
# "Save job Hide Report". A line counts as chrome only when EVERY word in it
# belongs to one of these phrases, so a real sentence that happens to contain
# "report" or "apply" is never touched.
_BOARD_CHROME_PHRASES = [
    "save job", "hide", "report", "apply",
    "apply directly on employer s site", "apply directly on employer's site",
    "saved save", "view all open roles", "view all", "job posting view all",
]
# Longest first, so a long phrase is consumed before its shorter pieces.
_BOARD_CHROME_PHRASES.sort(key=len, reverse=True)


def _is_pure_chrome_line(line: str) -> bool:
    remainder = re.sub(r"[^a-z' ]", " ", line.lower())
    remainder = re.sub(r"\s+", " ", remainder).strip()
    if not remainder:
        return False
    for phrase in _BOARD_CHROME_PHRASES:
        remainder = re.sub(rf"\b{re.escape(phrase)}\b", " ", remainder)
    remainder = re.sub(r"\s+", " ", remainder).strip()
    return remainder == ""


# A heading that starts a trailing block of OTHER postings from the same
# page. Everything from this line to the end is dropped. Exact heading match
# only, so a posting that mentions "similar" in its own text is safe.
_TRAILING_NOISE_HEADING_RE = re.compile(
    r"^(similar jobs|related jobs|other jobs you might like|"
    r"more jobs like this|jobs you may be interested in)\b",
    re.IGNORECASE,
)


def clean_posting_text(text: str) -> str:
    """Drop board chrome and trailing "similar jobs" blocks.

    Only structural noise goes: button-label lines and a whole trailing block
    of unrelated postings. No line of the real posting is reworded or trimmed.
    If a board's clutter does not match, it stays rather than risk cutting
    real content on a guess.
    """
    lines = text.splitlines()

    cutoff = len(lines)
    for i, line in enumerate(lines):
        if _TRAILING_NOISE_HEADING_RE.match(line.strip()):
            cutoff = i
            break
    lines = lines[:cutoff]

    return "\n".join(line for line in lines if not _is_pure_chrome_line(line))


# ---------------------------------------------------------------------------
# Classification
# ---------------------------------------------------------------------------


def _normalize_heading(line: str) -> str:
    return re.sub(r"[^a-z' ]", "", line.lower()).strip()


def _is_heading(line: str, needles: tuple[str, ...]) -> bool:
    """A heading is short, unbulleted, and contains one of the needle phrases.

    All three tests matter. Without the bullet test, "- 7+ years of technical
    writing experience" contains the needle "experience", is under the length
    cap, and would be swallowed as a heading, which drops the most important
    filter line in the posting.
    """
    if len(line) > 80:
        return False
    if BULLET_PREFIX_RE.match(line):
        return False
    if line.rstrip().endswith((".", "!", "?", ",", ";")):
        return False
    normalized = _normalize_heading(line)
    return any(needle in normalized for needle in needles)


def _is_unrecognized_subheading(line: str) -> bool:
    """A short, unbulleted line ending in a colon that names no known heading.

    Boards write their own subheadings ("The right person for this role will
    have:"). Without this test they leak into the table as fake requirements.
    Only the colon-ended case is clear enough to catch without a needle list.
    """
    if len(line) > 80:
        return False
    if BULLET_PREFIX_RE.match(line):
        return False
    return line.rstrip().endswith(":")


def _first_word(text: str) -> str:
    match = re.search(r"[A-Za-z']+", text)
    return match.group(0).lower() if match else ""


def _named_tools_in(text: str) -> list[str]:
    words = set(re.findall(r"[A-Za-z][A-Za-z0-9+#.\-]*", text.lower()))
    return sorted(word for word in words if word in NAMED_TOOLS)


def classify(text: str, section: str) -> Requirement:
    """Classify one line. Section context breaks ties; the line wins when it
    is decisive.

    Order matters. Credential and years tests run first because those are the
    two kinds of ask that track the labour market, so a line carrying either
    is a probable filter whatever else it mentions.
    """
    tools = _named_tools_in(text)

    if CREDENTIAL_RE.search(text):
        return Requirement(
            text=text,
            kind="credential",
            read_as="likely filter",
            reason=(
                "Credential line. Employers tend to ask for degrees and "
                "certifications more when applicants are plentiful, so this "
                "ask tracks the market more than the work."
            ),
        )

    years_match = YEARS_RE.search(text)
    if years_match:
        return Requirement(
            text=text,
            kind="experience",
            read_as="likely filter",
            reason=(
                f"Years-of-experience gate ({years_match.group(0).strip()}). "
                "The number is a volume dial, not a description of the work."
            ),
        )

    if section == "responsibility" or _first_word(text) in RESPONSIBILITY_VERBS:
        return Requirement(
            text=text,
            kind="responsibility",
            read_as="likely real",
            reason="Describes the actual work, not a screening filter.",
        )

    if tools:
        return Requirement(
            text=text,
            kind="skill",
            read_as="likely real",
            reason=f"Names concrete tooling ({', '.join(tools)}), specific enough to be real.",
        )

    return Requirement(
        text=text,
        kind="skill",
        read_as="likely real",
        reason=(
            "Skill line with no credential or years gate. Treated as real by "
            "default; nothing in it signals a screening filter."
        ),
    )


def parse_requirements(text: str) -> list[Requirement]:
    """Walk the posting, track the section, and lift every requirement line.

    Only bulleted lines and short lines under a requirement or responsibility
    heading are lifted. Free prose is skipped: splitting a company blurb into
    fake requirements is worse than missing one.
    """
    section = "unknown"
    requirements: list[Requirement] = []
    seen: set[str] = set()

    # Indexed, so an unbulleted line can look at the line after it. That
    # lookahead is the only reliable way to catch the first line of a
    # hard-wrapped paragraph, which looks like a real list item on its own.
    lines = [ln.strip() for ln in text.splitlines()]
    lines = [ln for ln in lines if ln]

    for index, line in enumerate(lines):
        if _is_heading(line, NOISE_HEADINGS):
            section = "noise"
            continue
        if _is_heading(line, RESPONSIBILITY_HEADINGS):
            section = "responsibility"
            continue
        if _is_heading(line, REQUIREMENT_HEADINGS):
            section = "requirement"
            continue
        # A colon-ended subheading in the board's own words. Skip it without
        # changing the section: it opens a subsection of the current one.
        if _is_unrecognized_subheading(line):
            continue

        if section == "noise":
            continue

        is_bullet = bool(BULLET_PREFIX_RE.match(line))
        body = BULLET_PREFIX_RE.sub("", line).strip()

        # A line qualifies if it is bulleted, or sits under a known heading
        # and is short enough to be a list item rather than prose.
        if not is_bullet and section == "unknown":
            continue
        if not is_bullet and len(body) > 200:
            continue
        # An unbulleted line ending in a period is prose, even inside a
        # requirements section. Bulleted lines keep their period; plenty of
        # real requirement bullets are full sentences.
        if not is_bullet and body.rstrip().endswith((".", "!", "?")):
            continue
        # The period test only catches prose that ends on a line boundary. A
        # hard-wrapped paragraph breaks mid-sentence, so every fragment slips
        # through. Three tells mean "sentence fragment":
        if not is_bullet:
            # 1. It starts mid-sentence: a list item starts with a capital,
            #    a digit or a quote, a wrapped continuation starts lowercase.
            if body[:1].islower():
                continue
            # 2. It holds an interior sentence boundary (". Capital").
            if re.search(r"[.!?]\s+[A-Z]", body):
                continue
            # 3. The next line continues this sentence. A real unbulleted
            #    list item is followed by another item, a heading or a
            #    bullet, never by a lowercase continuation.
            following = lines[index + 1] if index + 1 < len(lines) else ""
            if following and not BULLET_PREFIX_RE.match(following):
                continues_sentence = (
                    following[:1].islower()
                    or not body.rstrip().endswith((".", "!", "?", ":", ";"))
                    and not _is_heading(following, NOISE_HEADINGS)
                    and not _is_heading(following, RESPONSIBILITY_HEADINGS)
                    and not _is_heading(following, REQUIREMENT_HEADINGS)
                )
                if continues_sentence:
                    continue

        if len(body) < 12 or len(body) > 400:
            continue

        key = body.lower()
        if key in seen:
            continue
        seen.add(key)

        requirements.append(classify(body, section))

    return requirements


# ---------------------------------------------------------------------------
# Identity: slug, ATS id, duplicate check
# ---------------------------------------------------------------------------


def slugify_for_filename(value: str) -> str:
    """Make a value safe in a filename but still readable.

    A slash becomes a visible dash, so "Writer/Trainer" does not fuse into
    "WriterTrainer".
    """
    cleaned = re.sub(r"[/\\]", "-", value)
    cleaned = re.sub(r"[:*?\"<>|\[\]]", "", cleaned)
    return re.sub(r"\s+", " ", cleaned).strip()


def slug(value: str) -> str:
    """Lowercase, punctuation collapsed to single hyphens."""
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def norm_key(value: str) -> str:
    """Comparison form for company and role names."""
    return re.sub(r"[^a-z0-9]+", "", value.lower())


def ats_id_from_url(url: str) -> str:
    """Return `greenhouse-N`, `lever-ID`, `ashby-ID`, or `none`.

    Only well-known applicant-system URL shapes are read. A bare domain, or
    any other URL, gives `none` rather than a guess.
    """
    if not url:
        return "none"
    parsed = urlparse(url)
    host = (parsed.hostname or "").lower()
    parts = [p for p in parsed.path.split("/") if p]
    query = parse_qs(parsed.query)

    if "greenhouse.io" in host:
        for i, part in enumerate(parts):
            if part == "jobs" and i + 1 < len(parts) and parts[i + 1].isdigit():
                return f"greenhouse-{parts[i + 1]}"
    if "gh_jid" in query and query["gh_jid"][0].isdigit():
        return f"greenhouse-{query['gh_jid'][0]}"
    if host.endswith("lever.co") and len(parts) >= 2:
        return f"lever-{parts[1]}"
    if host.endswith("ashbyhq.com") and len(parts) >= 2:
        return f"ashby-{parts[1]}"
    return "none"


def url_is_bare_domain(url: str) -> bool:
    parsed = urlparse(url)
    return bool(parsed.netloc) and parsed.path in ("", "/") and not parsed.query


def _yaml_str(value: str) -> str:
    """A double-quoted YAML scalar. JSON strings are valid YAML, so any
    colon, quote or backslash in a company name stays safe."""
    return json.dumps(value, ensure_ascii=False)


def split_frontmatter(text: str) -> tuple[str, str] | None:
    """Return (frontmatter body, rest) or None when there is no frontmatter."""
    match = re.match(r"\A---\n(.*?)\n---\n?(.*)\Z", text, flags=re.S)
    if not match:
        return None
    return match.group(1), match.group(2)


def read_meta(path: Path) -> dict | None:
    """Frontmatter of an archived note as a dict, or None when unreadable."""
    try:
        import yaml

        parts = split_frontmatter(path.read_text(encoding="utf-8"))
        if parts is None:
            return None
        data = yaml.safe_load(parts[0])
    except Exception:
        return None
    return data if isinstance(data, dict) else None


def find_duplicates(
    archive_dir: Path, company: str, role: str, lane: str, ats_id: str
) -> tuple[list[Path], list[Path]]:
    """Return (same-lane duplicates, other-lane matches).

    A posting is a duplicate when company + role + lane all match, or when its
    applicant-system id matches in the same lane. The same posting in a
    different lane is not a duplicate: each lane has its own rubric and keeps
    its own note.
    """
    same_lane: list[Path] = []
    other_lane: list[Path] = []
    if not archive_dir.is_dir():
        return same_lane, other_lane
    for path in sorted(archive_dir.glob("*.md")):
        meta = read_meta(path)
        if not meta:
            continue
        same_posting = (
            norm_key(str(meta.get("company", ""))) == norm_key(company)
            and norm_key(str(meta.get("role", ""))) == norm_key(role)
        )
        if not same_posting and ats_id != "none":
            same_posting = str(meta.get("ats_id", "none")) == ats_id
        if not same_posting:
            continue
        if str(meta.get("lane", "")).strip() == lane:
            same_lane.append(path)
        else:
            other_lane.append(path)
    return same_lane, other_lane


# ---------------------------------------------------------------------------
# Archive write
# ---------------------------------------------------------------------------


def archive_path(archive_dir: Path, company: str, role: str, considered: str) -> Path:
    filename = (
        f"{slugify_for_filename(company)} - "
        f"{slugify_for_filename(role)} - {considered}.md"
    )
    return archive_dir / filename


def build_archive_note(
    company: str,
    role: str,
    source_urls: list[str],
    considered: str,
    posting_text: str,
    requirements: list[Requirement],
    lane: str,
    source_key: str | None = None,
) -> str:
    """Render the archive note: frontmatter, status line, requirements table,
    then the full posting text under its own heading."""
    real = [r for r in requirements if r.read_as == "likely real"]
    filters = [r for r in requirements if r.read_as == "likely filter"]

    primary_url = source_urls[0] if source_urls else ""
    ats_id = ats_id_from_url(primary_url)
    for extra in source_urls[1:]:
        if ats_id == "none":
            ats_id = ats_id_from_url(extra)
    opportunity_id = ats_id if ats_id != "none" else f"{slug(company)}-{slug(role)}-{considered}"

    lines = [
        "---",
        "type: reference",
        f"title: {_yaml_str(f'Job Posting - {company}: {role}')}",
        f"company: {_yaml_str(company)}",
        f"role: {_yaml_str(role)}",
        f"lane: {_yaml_str(lane)}",
    ]
    if source_key:
        lines.append(f"source: {_yaml_str(source_key)}")
    # The posting's own page, under both key names the email card reads.
    # Empty when the text was pasted with no URL.
    lines += [
        f"url: {_yaml_str(primary_url)}",
        f"job_url: {_yaml_str(primary_url)}",
    ]
    lines += [
        f"updated: {considered}",
        "status: archived",
        "purpose: >",
        "  Full saved copy of a job posting that was considered.",
        "how_to_use_this_file: >",
        "  Read-only source record. Do not edit the posting text itself; if the",
        "  listing changes or comes down, add a dated note instead.",
        "  The requirements split below is a reading aid, not a fit score.",
        f"  Judge this posting against the {lane} lane rules only.",
        f"opportunity_id: {_yaml_str(opportunity_id)}",
    ]
    if primary_url and url_is_bare_domain(primary_url):
        lines.append(
            "# The URL has no path, so no ATS id could be read. Fill ats_id in by hand."
        )
    if source_urls:
        lines.append("source_urls:")
        lines += [f"  - {_yaml_str(u)}" for u in source_urls]
    else:
        lines.append("source_urls: []")
    lines += [
        f"ats_id: {_yaml_str(ats_id)}",
        "state: needs_review",
        f"state_updated: {considered}",
        'next_action: "Run the assessment"',
        "next_action_due: none",
        "---",
        "",
        f"# Job Posting - {company}: {role}",
        "",
        f"**Source URL:** {primary_url or 'Pasted text, no source URL provided'}",
        f"**Considered:** {considered}",
        "**Application status:** Not yet decided. Update this line when you apply, "
        "or record why you did not.",
        "",
        "---",
        "",
        "## Requirements read",
        "",
        f"{len(real)} read as likely real · {len(filters)} read as likely filters",
        "",
        "The split follows Modestino, Shoag and Ballance (*Review of Economics "
        "and Statistics* 102(4), 2020): stated requirements partly track how "
        "many applicants there are, not only the job. A line marked *likely "
        "filter* is not a reason to skip the role.",
        "",
        "| Requirement | Type | Read as |",
        "|---|---|---|",
    ]

    for req in requirements:
        cell = req.text.replace("|", "\\|")
        lines.append(f"| {cell} | {req.kind} | {req.read_as} |")

    lines += [
        "",
        "---",
        "",
        "## Full posting text",
        "",
        posting_text.strip(),
        "",
    ]

    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------


def render_table(requirements: list[Requirement]) -> str:
    if not requirements:
        return (
            "No requirement or responsibility lines found.\n"
            "The posting may be prose-only, or the fetch may have returned a "
            "navigation page instead of the listing. Paste the posting text "
            "directly and re-run."
        )

    real = [r for r in requirements if r.read_as == "likely real"]
    filters = [r for r in requirements if r.read_as == "likely filter"]

    out = [
        "POSTING READ",
        f"   {len(real)} requirements likely real, {len(filters)} likely filters",
        "",
    ]

    if real:
        out.append("LIKELY REAL: these describe the actual work")
        out.append("")
        for req in real:
            out.append(f"   [{req.kind}] {req.text}")
            out.append(f"      -> {req.reason}")
            out.append("")

    if filters:
        out.append("LIKELY FILTER: read these skeptically")
        out.append("")
        for req in filters:
            out.append(f"   [{req.kind}] {req.text}")
            out.append(f"      -> {req.reason}")
            out.append("")
        out.append(
            "   Source: Modestino, Shoag and Ballance, Review of Economics "
            "and Statistics 102(4), 2020."
        )
        out.append(
            "   A miss in this group is a reason to apply anyway, with a "
            "reason, not a reason to skip the role."
        )
        out.append("")

    return "\n".join(out)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Parse a job posting into a requirements table and "
        "archive it as a markdown note."
    )
    parser.add_argument(
        "source",
        nargs="?",
        help="A file holding the posting text, or a posting URL (needs the "
        "requests package). Omit to read the text from stdin.",
    )
    parser.add_argument("--company", required=True, help="Company name.")
    parser.add_argument("--role", required=True, help="Role title.")
    parser.add_argument(
        "--lane",
        required=True,
        help="Which lane of your search this posting belongs to. Recorded in "
        "the note so the assessment loads the matching rubric.",
    )
    parser.add_argument(
        "--archive-dir",
        help="Folder the note is written to. Required unless --no-archive.",
    )
    parser.add_argument(
        "--url",
        default="",
        help="Source URL to record when the text was pasted, not fetched.",
    )
    parser.add_argument(
        "--date",
        default=date.today().isoformat(),
        help="Date considered (YYYY-MM-DD). Defaults to today.",
    )
    parser.add_argument(
        "--source",
        dest="source_key",
        help="Key of the job source this posting came from, as listed in "
        "your career profile's sources. Recorded in the note.",
    )
    parser.add_argument(
        "--no-archive",
        action="store_true",
        help="Print the table without writing a note (dry run).",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Archive even if the same posting is already archived for this lane.",
    )
    return parser


def fail(message: str) -> None:
    print(message, file=sys.stderr)
    sys.exit(EXIT_ERROR)


def main(argv: list[str] | None = None) -> None:
    args = build_parser().parse_args(argv)

    if not KEY_RE.match(args.lane):
        fail(f"Lane {args.lane!r} must be plain words (letters, digits, spaces, - and _).")
    if args.source_key and not KEY_RE.match(args.source_key):
        fail(f"Source key {args.source_key!r} must be plain words.")
    if not DATE_RE.match(args.date):
        fail(f"Date {args.date!r} must look like YYYY-MM-DD.")
    if not args.archive_dir and not args.no_archive:
        fail("--archive-dir is required unless --no-archive is given.")

    source_urls: list[str] = []
    if args.url:
        source_urls.append(args.url)

    if args.source and looks_like_url(args.source):
        if args.source not in source_urls:
            source_urls.insert(0, args.source)
        try:
            posting_text = fetch_url(args.source)
        except Exception as exc:  # network failure, bad status, missing package
            fail(
                f"Could not fetch {args.source}: {exc}\n"
                "Paste the posting text instead:\n"
                "  cat posting.txt | parse_posting.py --company X --role Y "
                "--lane L --archive-dir DIR --url <url>"
            )
    elif args.source:
        path = Path(args.source)
        if not path.exists():
            fail(f"File not found: {path}")
        posting_text = path.read_text(encoding="utf-8")
    else:
        posting_text = sys.stdin.read()

    if not posting_text.strip():
        fail("No posting text received.")

    ats_id = "none"
    for candidate in source_urls:
        ats_id = ats_id_from_url(candidate)
        if ats_id != "none":
            break

    archive_dir = Path(args.archive_dir) if args.archive_dir else None
    other_lane: list[Path] = []
    if archive_dir is not None:
        same_lane, other_lane = find_duplicates(
            archive_dir, args.company, args.role, args.lane, ats_id
        )
        if same_lane and not args.force:
            print(
                f"DUPLICATE: {args.company} / {args.role} is already archived "
                f"for lane {args.lane}.",
                file=sys.stderr,
            )
            for existing in same_lane:
                print(f"  existing note: {existing}", file=sys.stderr)
            print(
                "Update the assessment in the existing note instead of "
                "archiving again. Use --force to archive anyway.",
                file=sys.stderr,
            )
            sys.exit(EXIT_DUPLICATE)

    requirements = parse_requirements(posting_text)

    print(f"POSTING PARSE: {args.company} / {args.role}")
    print()
    print(render_table(requirements))

    if args.no_archive:
        print("Archive skipped (--no-archive). Nothing was written.")
        return

    assert archive_dir is not None
    archive_dir.mkdir(parents=True, exist_ok=True)
    path = archive_path(archive_dir, args.company, args.role, args.date)
    if path.exists():
        # Same name on the same day can only be another lane (same-lane
        # duplicates were stopped above), so keep both notes apart.
        path = path.with_name(f"{path.stem} - {slugify_for_filename(args.lane)}.md")
        if path.exists() and not args.force:
            fail(f"{path} already exists. Use --force to overwrite it.")
    note = build_archive_note(
        args.company, args.role, source_urls, args.date, posting_text,
        requirements, args.lane, args.source_key,
    )
    path.write_text(note, encoding="utf-8")
    print(f"Archived: {path}")
    if other_lane:
        print("Also archived for another lane (not a duplicate, kept separate):")
        for existing in other_lane:
            print(f"  {existing}")
    print("State is needs_review. Run the assessment next.")


if __name__ == "__main__":
    main()
