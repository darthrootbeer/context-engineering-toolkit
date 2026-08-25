# job-fit-screen

A tool for scoring a real job posting against your own personal fit criteria — the things that actually predict whether a job will make you happy, not just whether you're qualified for it.

## Status

**Scaffolding stage.** This README, the folder structure, and the example criteria file are in place. The actual scoring logic hasn't been built yet — see [Roadmap](#roadmap) below.

## Why this exists

Most job-search tools tell you whether you match a posting's stated requirements. They don't tell you whether the posting matches *you* — whether the company gives real autonomy, whether the interview process is reasonable, whether a "senior" title secretly means people-management when you don't want to manage people.

This tool separates that judgment into two parts:

1. **Your criteria** — a structured file only you write, describing what you actually need and want (hard blocks, must-haves, red flags, and softer signals worth noting).
2. **The scorer** — generic code that reads any criteria file in this shape and checks a job posting against it.

Your criteria are never checked into this repo. They belong to you, they're personal, and they usually contain things (salary numbers, work history, hard-won lessons from past jobs) that shouldn't sit in a public tool.

## How to use it

1. **Copy the example criteria file** to your own private location — do not edit `criteria.example.yaml` in place, and do not commit your real criteria file to this repo or any public repo:
   ```bash
   cp criteria.example.yaml ~/private/my-job-criteria.yaml
   ```
2. **Fill in your own values.** Every field in `criteria.example.yaml` is a placeholder — read the comments, replace each example with something true about you. See the file itself for the expected shape: `hard_blocks`, `requirements`, `autonomy_filter`, `soft_flags`, and `availability`.
3. **Run the tool against a job posting**, pointing it at your private criteria file:
   ```bash
   # Exact command lands here once the scorer is built — see Roadmap
   ```
4. **Read the output.** The tool is meant to flag things for you to weigh, not make the decision for you — a posting that trips a soft flag isn't automatically a reject, it's a "look closer here."

## Criteria file shape

See `criteria.example.yaml` for the full annotated template. In short:

| Section | What it's for | Effect |
|---|---|---|
| `hard_blocks` | Instant disqualifiers | Posting is dropped entirely, no scoring |
| `requirements` | Must-haves | Strong reject on miss, but scored/flagged, not silently dropped — a human can still override |
| `autonomy_filter` | A judgment call too nuanced for yes/no | Scored on positive/negative signal matches |
| `soft_flags` | Worth noting, not disqualifying | Surfaced alongside the posting for you to weigh |
| `availability` | Notice period, work authorization | Used to flag postings that need special handling (e.g. non-local employer) |

This shape is deliberately generic — it's built from one person's real job search, but nothing in the structure assumes any specific industry, role, or set of values. Your criteria file is what makes it yours.

## Roadmap

- [ ] Define the exact shape a scraped/pasted job posting takes as input
- [ ] Build the scoring logic (hard-block check → requirement scoring → soft-flag surfacing)
- [ ] Decide on output format (terminal report, structured JSON, both)
- [ ] Add a CLI entry point and usage example
- [ ] Add tests against example postings

## License

This project is open source and available under the MIT License.
