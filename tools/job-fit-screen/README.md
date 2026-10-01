# job-fit-screen

> **Early version (August 2026), being replaced soon.** This is the first, simple scorer. The job assessment system I use today is far larger and has been updated almost daily since. A cleaned-up public version of it is being added to this repo.

A tool for scoring a real job posting against your own personal fit criteria — whether the company would treat you the way you need to be treated, *and* whether you're actually qualified for what's being asked. Both questions matter; a posting that's a perfect culture fit is still a bad target if the required experience doesn't line up with your real skills.

## Status

**Working.** The scorer (`job_fit_screen.py`) reads your criteria file and a job posting, sends both to Claude via the local `claude` CLI (no API key needed), and prints a scorecard. See [Setup](#setup) and [How to use it](#how-to-use-it) below.

## Why this exists

Most job-search tools tell you whether you match a posting's stated requirements. They don't tell you whether the posting matches *you* — whether the company gives real autonomy, whether the interview process is reasonable, whether a "senior" title secretly means people-management when you don't want to manage people.

This tool separates that judgment into three parts:

1. **Your reasoning** — a plain-language file where you actually think through what you want and why, grounded in your own real work history rather than a generic wishlist. This is the file you write first.
2. **Your criteria** — a structured file distilled from that reasoning, describing what you actually need and want (hard blocks, must-haves, red flags, and softer signals worth noting).
3. **The scorer** — generic code that reads any criteria file in this shape and checks a job posting against it.

Neither your reasoning file nor your criteria file are ever checked into this repo. They belong to you, they're personal, and they usually contain things (salary numbers, work history, hard-won lessons from past jobs) that shouldn't sit in a public tool.

## Setup

This tool scores postings by shelling out to the local `claude` CLI (Claude Code) — it does **not** use a raw Anthropic API key.

1. **Install [Claude Code](https://docs.claude.com/claude-code)** if you don't already have it, and log in once by running `claude` interactively.
2. **Install this tool's dependencies:**
   ```bash
   ./install.sh
   ```
   This checks for Python 3.9+, installs the required packages, and confirms the `claude` CLI is on your PATH.

## How to use it

1. **Copy both example files** to your own private location — do not edit `search.example.md` or `criteria.example.yaml` in place, and do not commit your real versions to this repo or any public repo:
   ```bash
   cp search.example.md ~/private/my-job-fit-criteria.md
   cp criteria.example.yaml ~/private/my-job-criteria.yaml
   ```
2. **Write your reasoning first, in `my-job-fit-criteria.md`.** Answer the prompts in each section honestly, grounded in real evidence from your own past jobs — not what you think you're supposed to want. This step matters: distilling straight into structured YAML fields without thinking it through first tends to produce a shallower, less accurate criteria file.
3. **Distill that reasoning into `my-job-criteria.yaml`.** Every field in `criteria.example.yaml` is a placeholder — read the comments, replace each example with something true about you, grounded in what you just wrote in step 2. See the file itself for the expected shape: `hard_blocks`, `requirements`, `autonomy_filter`, `keyword_signals`, `qualifications_match`, `soft_flags`, and `availability`.
4. **Save a job posting to a text file**, or grab its URL directly. (A URL works for plain server-rendered pages; a JavaScript-heavy job board — Greenhouse, Ashby, Lever — usually won't extract cleanly from a URL fetch. Save the posting text to a `.txt` file in that case instead.)
5. **Run the tool:**
   ```bash
   ./run_screen.sh --criteria ~/private/my-job-criteria.yaml --posting ~/Downloads/posting.txt
   # or, with a URL:
   ./run_screen.sh --criteria ~/private/my-job-criteria.yaml --posting "https://example.com/job/123"
   # optionally save the full structured result too:
   ./run_screen.sh --criteria ~/private/my-job-criteria.yaml --posting posting.txt --json-out result.json
   ```
6. **Read the output.** The tool is meant to flag things for you to weigh, not make the decision for you — a posting that trips a soft flag isn't automatically a reject, it's a "look closer here." A tripped `hard_blocks` entry is the one case the tool treats as a real reject, and the report says so plainly.

Every verdict in the report is grounded in a quote or close paraphrase from the actual posting — if the tool can't point to specific language backing a claim, it's instructed to say so rather than guess.

### Try it without a real criteria file first

```bash
python3 test_example.py
```

Runs the scorer against a fake, fully generic test posting and `criteria.example.yaml` as-is. Confirms the tool works end to end (and that `claude` is logged in and responding) before you've written anything real.

## Reasoning file shape

See `search.example.md` for the full annotated template. It walks through the same sections as the criteria YAML — availability/process, location, company size/stage, industries, the pitch you're chasing, and culture red flags — but as prompts to answer in your own words, with space to write out *why*, not just *what*.

## Criteria file shape

See `criteria.example.yaml` for the full annotated template. In short:

| Section | What it's for | Effect |
|---|---|---|
| `hard_blocks` | Instant disqualifiers | Posting is dropped entirely, no scoring |
| `requirements` | Must-haves | Strong reject on miss, but scored/flagged, not silently dropped — a human can still override |
| `autonomy_filter` | A judgment call too nuanced for yes/no | Scored on positive/negative signal matches |
| `keyword_signals` | Weighted language patterns to scan for in a posting's own text | Fast first pass — `strong_positive` / `positive` / `negative` / `strong_negative` phrase lists, each with a `why` |
| `qualifications_match` | Whether you're actually eligible, separate from fit | Checks a posting's required/standout experience against your real `core_skills_and_evidence` and `known_gaps` |
| `soft_flags` | Worth noting, not disqualifying | Surfaced alongside the posting for you to weigh |
| `availability` | Notice period, work authorization | Used to flag postings that need special handling (e.g. non-local employer) |

`keyword_signals` is different in kind from the other sections — those are *criteria* (facts to check, sometimes needing outside research). `keyword_signals` is *language patterns* worth scanning for directly in the posting text itself, weighted by how strong a signal each phrase is. It grows over time: every real posting you screen either confirms an existing phrase's weight or teaches you a new one — add it to the list rather than losing the pattern in a one-off read.

`qualifications_match` is different again — every other section answers "would this company treat me right," this one answers "am I actually qualified." A posting can pass every fit check above and still be a poor target if its required experience leans hard into skills you don't have.

This shape is deliberately generic — it's built from one person's real job search, but nothing in the structure assumes any specific industry, role, or set of values. Your criteria file is what makes it yours.

## Roadmap

- [x] Define the exact shape a scraped/pasted job posting takes as input — local text file or URL
- [x] Build the scoring logic — Claude reads the criteria and posting together and returns a structured verdict, since the criteria file's own checks (negation, working-philosophy fit, qualifications judgment) need real reading comprehension, not keyword matching
- [x] Decide on output format — terminal scorecard by default, optional `--json-out` for the full structured result
- [x] Add a CLI entry point and usage example — `job_fit_screen.py` via `click`, wrapped by `run_screen.sh`
- [x] Add a test fixture — `test_example.py` runs a fake generic posting through the real tool end to end
- [ ] Auto-fetch from JS-rendered job boards (Greenhouse, Ashby, Lever) — currently these need the posting text saved to a file first, since a plain URL fetch only sees the unrendered page shell
- [ ] Persistent history across scored postings — right now each run is a one-off report, no log of what's been screened before

## License

This project is open source and available under the MIT License.
