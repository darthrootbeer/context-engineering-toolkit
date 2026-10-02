# Smoke test run, saved output

This is the real output of following the Install and Smoke test sections of [SETUP.md](../SETUP.md) literally, from a fresh clone, on 2026-10-01 (Claude Code 2.1.287, `sonnet` for the stages).

**What was run, and what was changed to keep it away from my own setup.** I cloned the pushed branch of this repo from GitHub into an empty temp folder, ran the check script, ran the install loop exactly as written but with `SKILLS_DIR` pointed at a scratch project folder instead of `~/.claude/skills`, and ran each stage with `claude -p`. Because the skills sit in a scratch folder and not in the user folder, each stage run adds `--add-dir <scratch project>` so Claude Code can see them from inside the workspace, and `--setting-sources project` keeps my own user settings out. The install-count check uses the same flags. Before the run I also changed the `WORKSPACE_ROOT` line in the two installed copies that use it from `~/projects` to a scratch folder, which the guide says you can do. Nothing else was edited.

## Part 1: the fresh clone, install, stage 0, stage 3b, stage 4c

Commit under test: `e035975`.

```text
$ git clone -b fix/docs-pipeline-runnable https://github.com/darthrootbeer/context-engineering-toolkit.git repo
commit e035975 docs(docs-pipeline): add saved prompt runs, offline check and readability skill readme

$ python3 pipelines/docs-pipeline/tests/check_pipeline.py
check_pipeline: clean (17 skill files, 50 files scanned)
exit=0

$ install loop (SETUP.md section 3; SKILLS_DIR pointed at a scratch folder)
skill folders created:       17

$ claude -p "hi" --model haiku --output-format stream-json --verbose | grep -o "\"docs-[a-z-]*\"" | sort -u | wc -l
      17

$ claude -p "/docs-workspace-setup TICKET-1 smoke-test"   (answering y)
The workspace is set up and the initial commit is made.

```
Done.

  /tmp/dpfix-proof3/proj/workspaces/workspace_doc-1_smoke-test/

  Files:
    - CLAUDE.md
    - README.md
    - .gitignore

  Knowledge files:
    - _knowledge/      (copied from /tmp/dpfix-proof3/repo/pipelines/docs-pipeline)

  Directories:
    - docs/input/
    - docs/output/_process/diataxis-audit/
    - docs/output/_process/link-check/
    - docs/output/_process/style-audit/
    - docs/output/_process/visual-audit/diagrams/
    - docs/output/docs/
```

I skipped three optional steps because their settings are still placeholders:
- **Shared config link:** `SHARED_CONFIG_DIR` is unset, so there is no `_shared` link.
- **Project note:** `NOTES_DIR` is unset, so I wrote no project note.
- **Source doc fetch:** no docs repo is configured, so I didn't copy a source doc. Copy it into `docs/input/` manually.

The ticket line in `CLAUDE.md` is the plain ID `TICKET-1`, with no link, because the ticket URL is also a placeholder.

The first commit is `84c483e` on `master`.

Next, copy the source doc into `docs/input/` and run `/docs-pipeline` or `/docs-diataxis-audit`.

$ ls -A workspace; git log --oneline
_knowledge
.git
.gitignore
CLAUDE.md
docs
README.md
84c483e docs: scaffold guide workspace for TICKET-1

$ claude -p "/docs-style-check-voice docs/output/docs/"
General style audit complete.

Docs audited: 1
Fixes applied: 6
Flags for review: 6

I fixed these in `acme-orders-cancellations.md`:
- I replaced the chatty, marketing intro with a direct opening.
- I split the long paragraph in "What a cancellation is" in two.
- I renamed the heading "How to cancel an order" to "Cancel an order".
- I added the `**To cancel an order:**` lead-in and an outcome sentence to the numbered list.
- I changed "order id" to the exact field name `order_id`.

These are flagged for you to review:
- "Paid orders are refunded automatically" and "The API is rate limited" are passive. Check both claims against the product KB.
- "Hosted order form" and "integration type" are undefined at first use.
- "Things to know" mixes rate limits with the `reason` field.
- The doc has no closing "Prompt for your AI model" block. That belongs to the structural pass, so check it was handled there.

Audit report: `docs/output/_process/style-audit/style-audit-general-docs.md`

Committed as `1417607`.

What's next: `/docs-style-check-human docs/output/docs/` for the AI pattern cleanup pass.

$ claude -p "/docs-sme-review docs/output/docs/"
SME review complete. I committed the reports as `28d39b2`.

- **Draft files analyzed:** 1 (`acme-orders-cancellations.md`)
- **Corpus titles indexed:** skipped, because no docs repo is configured, so the naming-collision check didn't run
- **Product KB extracted:** 2026-10-01. The KB is still the fictional starter data, so these findings only mean something once you've replaced it with your real product facts.

**Reports** are in `docs/output/_process/sme-review/`. I put them there instead of a top-level `_process/` to match the other audit folders:
- `acme-orders-cancellations-sme-review.md`
- `sme-review-summary.md`

**Findings (11 total):**
- **Domain accuracy:** 3 HIGH, 1 MEDIUM
  - HIGH, line 13: the draft says paid orders can be canceled and are refunded automatically. The KB says a paid order can't be canceled (`order_not_cancelable`, 409).
  - HIGH, line 37: the draft says every integration type gets `order.canceled`. Only Server API does, and the hosted order form gets no webhooks.
  - HIGH, line 41: the draft gives a rate limit of about 1,000 requests a minute. The KB says 100 per API key.
  - MEDIUM, line 20: the cancel endpoint is Server API only, and the page never says so.
- **Reader journey:** 3 MEDIUM
  - There is no "who this is for" line or prerequisites.
  - Only the 404 error is documented; the 409 and 429 errors are missing.
  - The page doesn't say where to find `order_id`.
- **Naming collisions:** skipped
- **Technical clarity:** 1 MEDIUM, 3 LOW
  - The MEDIUM is that the curl example sends JSON without a `Content-Type` header.
  - The LOWs are an odd rationale sentence, a repeated outcome line and the word "Utilize".
- **Proofreading:** 0

Next is `/docs-changes-list`. I'd fix the three HIGH items first; the decision checkpoint at step 13 is where the apply/skip/defer choices get made.

$ git log --oneline; find . -name "*.md" -path "*_process*"
28d39b2 docs: SME review pass for TICKET-1
1417607 docs: general style voice pass for TICKET-1
84c483e docs: scaffold guide workspace for TICKET-1
./docs/output/_process/style-audit/style-audit-general-docs.md
./docs/output/_process/sme-review/sme-review-summary.md
./docs/output/_process/sme-review/acme-orders-cancellations-sme-review.md
```

**What this shows.** Stage 0 built a workspace with a copy of `_knowledge/`. Stage 3b loaded the style guide and wrote its report. Stage 4c loaded the product knowledge base and found the three HIGH domain errors the sample doc plants: a paid order cannot be canceled, the hosted order form gets no webhooks, and the rate limit is 100 a minute. Neither stage stopped on a missing file. The naming-collision check was skipped with a note, because no docs repo is configured.

## Part 2: the other stages that need no docs repo

These ran in the same kind of scratch workspace, one commit earlier (`6864bf7`, before the saved-run records and this file were added; no skill file, knowledge file or sample changed in between; only the README, SETUP, ARCHITECTURE and the readability README did). Stage 1 needed the sample copied into `docs/input/` first.

**Stage 3a stopped on purpose.** `/docs-style-check-structure` needs a `diataxis_type` in the doc's frontmatter, and the split stage (not run here) is what adds it. Its message is a design rule, not a missing file.

```text
$ claude -p "/docs-diataxis-audit docs/input/acme-orders-cancellations.md"
The audit is written and committed. I made no changes to the source file.

- **Input:** `docs/input/acme-orders-cancellations.md`
- **Audit report:** `docs/output/_process/diataxis-audit/smoke-test_audit-report.md`
- **JSON mapping:** `docs/output/_process/diataxis-audit/smoke-test_mapping.json`. It passed the built-in ID, uniqueness and mapping checks before I wrote it.
- **SVG diagrams:** skipped, because no shared diagram tool is configured.
- **Sections analyzed:** 5.
- **Content type:** mixed, with no type above roughly 40%. Reference is the largest share (~40%), and how-to is the only step-by-step content.
- **Recommended split:** 3 typed documents, plus an overview that the split step creates.
  - Explanation: how order cancellation works.
  - How-to: cancel an order, with the `reason` tip moved in.
  - Reference: webhooks, errors and rate limits.

The main problems it flags:
- The "Things to know" section mixes a rate limit with a task tip.
- The 404 error sits inside the how-to steps.
- The promotional intro should be dropped.

Three things to know:
- **Commits:** I committed the untracked source doc first (`444bce3`), then the audit (`2a9847a`). Your workflow says to commit after every step.
- **Earlier stages:** git history already shows voice-style and SME-review commits, and `docs/output/docs/acme-orders-cancellations.md` exists. That is later-stage work with no audit or split behind it. You may want to check whether it should be redone after the split.
- **SME check:** the audit flags two claims for review. One is that every integration type gets the webhook. The other is that paid orders are refunded automatically.

Next is `/docs-diataxis-split`.


$ claude -p "/docs-style-check-structure docs/output/docs/"
I stopped before making any edits, because `docs/output/docs/acme-orders-cancellations.md` has no resolvable `diataxis_type`.

- **Frontmatter:** the file has none. It starts with an HTML comment and then the `#` heading.
- **Filename:** `acme-orders-cancellations.md` matches none of the patterns (`index.md`, `*-overview.md`, `*-reference.md`, `how-to-*`, `tutorial-*`).

```
Cannot determine diataxis_type for:
  - acme-orders-cancellations.md (no frontmatter type, no recognizable filename pattern)
```

**The split looks like it hasn't run.** The git log has the audit commit (`2a9847a`) as the latest. It has no split commit, and `docs/output/docs/` holds one file. That file reads like the original source: it mixes explanation ("What a cancellation is"), how-to steps, and webhook facts. There is also no `index.md` overview. Step 3 (`/docs-diataxis-split`) normally produces typed files with frontmatter, and running the structure check on the unsplit doc would give misleading results.

Which would you like?

1. **Run `/docs-diataxis-split` first (recommended).** That produces typed docs, and I then re-run this check.
2. **Let me assess and propose a type for this file now.** From the content I'd suggest `explanation`, but it's mixed content. You'd confirm before I add `diataxis_type` to the frontmatter and continue.

I haven't written an audit report or made a commit.


$ claude -p "/docs-style-check-human docs/output/docs/"
Human style audit complete.

Docs audited: 1
Fixes applied: 4
Flags for review: 1

Most common fixes:
  - Passive voice: 2
  - Redundant sentence: 1
  - Short-sentence stacking: 1

The doc had almost no AI patterns. It has no em dashes, banned words, filler openers, or bold-label lists.

The flag: "This helps with reporting" in "Things to know" doesn't say how it helps. Someone who knows the product should supply the specific benefit.

Audit report: `docs/output/_process/style-audit/style-audit-human-docs.md`

The changes are committed as `734ddc5`.


$ claude -p "/docs-readability-check docs/output/docs/"
Readability audit complete.

- **Docs audited:** 1 (`acme-orders-cancellations.md`)
- **Docs improved:** 0
- **Docs within target:** 1
- **Docs still below target:** 0
- **Wall paragraphs flagged for manual review:** 0

The doc reads at an easy level, about 8th–9th grade or below. That estimate is a rough hand calculation of the Flesch-Kincaid grade level (about 6–7). The doc has no `diataxis_type`, so the target is 11th–12th grade. Being easier than the target is fine for a short task guide. None of the seven dense-sentence patterns appeared, so I made no edits.

The audit report is at `docs/output/_process/style-audit/readability-audit-docs.md`. I committed it as 48e8406.


$ claude -p "/docs-grammar-spelling docs/output/docs/"
Proofread audit complete.

- **Docs audited:** 1
- **Fixes applied:** 2, both punctuation. In `acme-orders-cancellations.md` I changed "order id" to `order_id` and "a 404 error" to a `404 Not Found` error.
- **Flags for review:** 1. Line 39 says "a thousand cancellation requests". That's a technical value, so it could be "1,000". I'd also confirm the limit against the rate-limit docs.
- **Terminology and spelling:** no issues. All glossary terms were in canonical form, and the spelling is American English.

The audit report is at `docs/output/_process/style-audit/style-audit-proofread-docs.md`. I committed the changes as `f5c1678`.

Next: review the flag, then run `/docs-visuals-review docs/output/docs/`. The workflow puts visuals review next, so I didn't suggest `/docs-links-review` yet.
```
