# job-fit-screen

A tool for scoring a real job posting against your own personal fit criteria — whether the company would treat you the way you need to be treated, *and* whether you're actually qualified for what's being asked. Both questions matter; a posting that's a perfect culture fit is still a bad target if the required experience doesn't line up with your real skills.

## Status

**Scaffolding stage.** This README, the folder structure, and both example files (`criteria.example.yaml` and `search.example.md`) are in place. The actual scoring logic hasn't been built yet — see [Roadmap](#roadmap) below.

## Why this exists

Most job-search tools tell you whether you match a posting's stated requirements. They don't tell you whether the posting matches *you* — whether the company gives real autonomy, whether the interview process is reasonable, whether a "senior" title secretly means people-management when you don't want to manage people.

This tool separates that judgment into three parts:

1. **Your reasoning** — a plain-language file where you actually think through what you want and why, grounded in your own real work history rather than a generic wishlist. This is the file you write first.
2. **Your criteria** — a structured file distilled from that reasoning, describing what you actually need and want (hard blocks, must-haves, red flags, and softer signals worth noting).
3. **The scorer** — generic code that reads any criteria file in this shape and checks a job posting against it.

Neither your reasoning file nor your criteria file are ever checked into this repo. They belong to you, they're personal, and they usually contain things (salary numbers, work history, hard-won lessons from past jobs) that shouldn't sit in a public tool.

## How to use it

1. **Copy both example files** to your own private location — do not edit `search.example.md` or `criteria.example.yaml` in place, and do not commit your real versions to this repo or any public repo:
   ```bash
   cp search.example.md ~/private/my-job-fit-criteria.md
   cp criteria.example.yaml ~/private/my-job-criteria.yaml
   ```
2. **Write your reasoning first, in `my-job-fit-criteria.md`.** Answer the prompts in each section honestly, grounded in real evidence from your own past jobs — not what you think you're supposed to want. This step matters: distilling straight into structured YAML fields without thinking it through first tends to produce a shallower, less accurate criteria file.
3. **Distill that reasoning into `my-job-criteria.yaml`.** Every field in `criteria.example.yaml` is a placeholder — read the comments, replace each example with something true about you, grounded in what you just wrote in step 2. See the file itself for the expected shape: `hard_blocks`, `requirements`, `autonomy_filter`, `soft_flags`, and `availability`.
4. **Run the tool against a job posting**, pointing it at your private criteria file:
   ```bash
   # Exact command lands here once the scorer is built — see Roadmap
   ```
5. **Read the output.** The tool is meant to flag things for you to weigh, not make the decision for you — a posting that trips a soft flag isn't automatically a reject, it's a "look closer here."

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

- [ ] Define the exact shape a scraped/pasted job posting takes as input
- [ ] Build the scoring logic (hard-block check → requirement scoring → soft-flag surfacing)
- [ ] Decide on output format (terminal report, structured JSON, both)
- [ ] Add a CLI entry point and usage example
- [ ] Add tests against example postings

## License

This project is open source and available under the MIT License.
