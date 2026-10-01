---
name: docs-changes-list
description: Generate a completed editorial-changes.md after a Diataxis split. Reads the original doc, output docs, audit report, and visual audit to auto-fill all sections. Use after the split, style pass, and visual aids are done — before review/PR.
argument-hint: [original-doc-path] [output-dir] [optional: TICKET-ID]
allowed-tools: [Read, Write, Glob, Bash]
---

# docs-changes-list

Generate a completed `editorial-changes.md` for a guide conversion project. This document records all significant changes made during a Diataxis split — written for original authors and SMEs, not engineers.

Reads all available evidence and writes the full document with real content. No `[FILL IN]` placeholders.

## Arguments

The user provided: $ARGUMENTS

- `$ARGUMENTS[0]` — Path to the original source document (e.g., `docs/input/configure-webhooks.md`)
- `$ARGUMENTS[1]` — Output directory where new docs live (e.g., `docs/output/`)
- `$ARGUMENTS[2]` — Optional ticket ID (e.g., `DOC-101`) — used to pull style change comments

## Usage

`/editorial-changes [original-doc-path] [output-dir] [ticket-id]`

**Required:** First two arguments are mandatory. If either is missing, stop and ask:
`"Please provide both paths: /editorial-changes [original-doc-path] [output-dir]"`

---

## Steps

### 1. Validate input

- Parse `ORIGINAL_PATH = $ARGUMENTS[0]`
- Parse `OUTPUT_DIR = $ARGUMENTS[1]` (strip trailing slash)
- Parse `TICKET_ID = $ARGUMENTS[2]` (optional — may be empty)
- Derive `OUTPUT_FILE = {OUTPUT_DIR}/_process/editorial-changes.md`
- If `ORIGINAL_PATH` or `OUTPUT_DIR` missing: stop with usage message
- If `OUTPUT_FILE` already exists: stop with "File already exists: {OUTPUT_FILE} — delete it first."

### 2. Read the original document

- Read `ORIGINAL_PATH` in full
- Extract H1 title (first `# ` heading). If no H1, use the frontmatter `title:` field. If neither, use filename stem.
- Note: total line count (for the header)

### 3. Discover and read output docs

Glob all `.md` files in `{OUTPUT_DIR}/docs/` (the deliverables subfolder). No exclusions needed — everything in `docs/` is a Diataxis output doc.

Read all files in full. Call this set `OUTPUT_DOCS`.

If zero output docs found: stop with "No output docs found in {OUTPUT_DIR}. Run the split first."

### 4. Read supporting files (if they exist)

Check for and read each of these if present — they are the primary evidence sources:

**Audit report:**
Derive the basename in a separate Bash call:
```bash
basename "ORIGINAL_PATH" .md
```
Store the output as `BASENAME`. Then construct the path:
```
AUDIT_REPORT="{OUTPUT_DIR}/_process/diataxis-audit/BASENAME_audit-report.md"
```
Read if exists. Key sections to extract:
- Content Analysis (percentage breakdown, section classification)
- Boundary Violations (what was in the wrong place and why)
- Restructuring Recommendations

**Visual audit:**
```bash
VISUAL_AUDIT="{OUTPUT_DIR}/_process/visual-audit/visual-audit-output.md"
```
Read if exists. Key sections to extract:
- Recommendations (diagram type, location, problem it solves, priority rating)
- Not recommended (what was explicitly skipped)

**Ticket comments and sub-issues (if TICKET_ID provided):**
```bash
linearis issues read $TICKET_ID 2>/dev/null
```
Read if TICKET_ID is set. Extract comment bodies — they often document style changes, decisions made, and rationale that isn't captured in the audit report.

Also fetch the ticket's sub-issues (child issues linked to it):
```bash
linearis issues list --parent $TICKET_ID 2>/dev/null
```
Read each sub-issue's title and description. Build a `TICKET_MAP` — a mapping from category of work to the sub-issue that covered it. Use the sub-issue titles as signals:
- "split" / "diataxis" / "separate" → split ticket
- "style" / "formatting" / "style guide" → style ticket
- "visual" / "diagram" / "flowchart" → visual aids ticket
- "terminology" / "align" / "structure" → terminology/structure ticket
- "cross-link" / "link audit" / "overlap" → link-check ticket
- "feedback" / "reviewer" / "suggested changes" → feedback ticket

If a sub-issue matches a category, use its identifier in that section's `**Related:**` line. If no sub-issue matches, fall back to the parent TICKET_ID. If TICKET_ID was not provided, omit `**Related:**` lines entirely.

### 5. Analyze the evidence

Using the material gathered, identify what changed across these categories. For each category, note what to include and what to skip if not applicable.

#### A. Diataxis split

From the audit report:
- What type mix was in the original (percentages) and why that's a problem
- What each output doc contains and its Diataxis type
- Whether a doc type was recommended in the audit but deferred (e.g., Introduction doc)

Determine Diataxis type for each output doc. Read `diataxis_type` from the file's frontmatter first. If absent, fall back to filename prefix for legacy docs:
- `explanation-*` → Explanation
- `how-to-*` → How-to
- `reference-*` → Reference
- `overview-*` or `introduction-*` → Overview

#### B. Content moved between documents

From the audit report's Boundary Violations and Restructuring Recommendations:
- Which sections were extracted from the original and placed in a different new doc
- The source location in the original (section name + approximate line range)
- The destination (new doc + new section heading)
- The reason (one sentence: why it belongs in the new location)

**What counts as "moved":** Content that existed in the original and appears in a new doc under a different section or with a different heading. If it's 1:1 verbatim in the same section, it's not "moved" — it's just carried over.

#### C. Content removed

From the audit report's Boundary Violations and Restructuring Recommendations:
- Prescriptive or recommendation language stripped from Reference sections
- Navigation-only sections removed (e.g., "Next steps" with only links)
- Any other content present in the original that does not appear in any output doc

**Skip this section if nothing was removed.**

#### D. Style and formatting changes

Look for style patterns by comparing the original and output docs:

1. **Callout types** — Scan original for 🚧 emoji in callouts. Scan output docs for the same. If 🚧 was replaced with ⚠️ or 📘, note it.
2. **Navigation callouts** — Look for callout blocks at the top of the original that link to other sections ("See also:", "Next:", etc.). If absent from output docs, note removal.
3. **List lead-ins** — Check whether numbered lists in how-to output docs have a lead-in sentence before the list and an outcome sentence after. If the original lacked these, note it was added.
4. **Link-only sections** — Check if "Next steps" or similar link-only sections from the original were removed.
5. **Ticket comments** — If ticket comments were read, extract any explicitly documented style changes.

Include only style changes that actually happened. If none of the above patterns are present, omit this section.

#### E. Visual aids added

From the visual audit (if it exists):
- For each "Recommendations" entry in the visual audit: check whether the diagram it recommended appears in the corresponding output doc (look for a `mermaid` code block near the described location)
- If the diagram is present: include it in this section
- If recommended but not present: skip it (it wasn't done)
- For each included diagram: use the visual audit's "Problem it solves" field as the basis for the prose description

Use the priority rating (Critical / High / Medium / Low) to inform the prose. Higher-priority diagrams solved a more critical gap than lower-priority ones.

**Skip this section if no visual audit exists or no diagrams were added.**

### 6. Write the document

Write `OUTPUT_FILE` using the structure below. Omit any section where nothing applies — don't include empty sections or placeholder text.

**Voice and tone:**
- State the fact, then the one-line consequence. Don't separate them.
- Drop framework terminology from prose (`Diataxis boundary violation`, `pattern violation`). Use plain English: "that's not what Reference is for", "the split separates those by reader intent".
- Lead with the concrete example (`"succeeded is a terminal state"`) rather than the category it violates.
- Cut meta-framing: don't explain the audit's priority system in the output — just describe what was done and why.
- Shortest path to the point. "The flowchart fixes that." is better than a three-sentence explanation of the fix.

---

## Document structure

```markdown
# Editorial Changes: [Guide Title]

This document records all significant changes made during the conversion of `[original-filename.md]` into a Diataxis-structured multi-document guide set. It is written for original authors and SMEs so they can understand what changed, where, and why.

**Original source:** `[original-doc-path]` ([N] lines)
**Output:** `[output-dir]` — [N] documents

---

## Diataxis split

[One paragraph: what the original mixed together (type percentages and the reader problem that caused), and that the split solves it by giving each reader need its own doc.]

[If a doc type was recommended but deferred, note it here: "The audit also recommended a [type] doc; that is deferred to [ticket or phase]."]

| New document | What it contains | Diataxis type |
| --- | --- | --- |
| `[filename.md]` | [one-line description] | [type] |
| ... | ... | ... |

**Related:** [SPLIT-TICKET-ID]({YOUR_ISSUE_TRACKER}/SPLIT-TICKET-ID)  ← use the sub-issue whose title matches "split" / "diataxis"; fall back to TICKET_ID

---

## Content moved between documents

The following sections were extracted from the original doc and placed in a different document. The underlying content was not rewritten — only its location changed.

| Content | Source (original doc) | Destination | Why |
| --- | --- | --- | --- |
| [section name (lines N–N)] | [original doc section/context] | [new doc → new section heading] | [one sentence] |
| ... | ... | ... | ... |

**Related:** [SPLIT-TICKET-ID]({YOUR_ISSUE_TRACKER}/SPLIT-TICKET-ID)  ← same as Diataxis split section

---

## Content removed

[Intro sentence: brief framing of what was removed and the general reason.]

| Content | Where it was | Why removed |
| --- | --- | --- |
| [description] | [section in original] | [one sentence] |
| ... | ... | ... |

**Related:** [SPLIT-TICKET-ID]({YOUR_ISSUE_TRACKER}/SPLIT-TICKET-ID)  ← same as Diataxis split section

---

## Style and formatting changes

These changes do not affect meaning. They bring the documents into compliance with your team's style guide and your docs platform's markdown rendering requirements.

- [change 1]
- [change 2]
- [change 3]

*All style and formatting changes: [STYLE-TICKET-ID]({YOUR_ISSUE_TRACKER}/STYLE-TICKET-ID)*  ← use the sub-issue whose title matches "style" / "formatting"; fall back to TICKET_ID

---

## Visual aids added

[One sentence framing: N diagrams added, sourced from the visual audit, each solving a specific reading gap.]

### [Diagram name]
**Doc:** `[filename.md]` — "[Section heading]"
**Priority:** [Critical / High / Medium / Low]

[2–3 sentences: the problem the prose had without this diagram, and how the diagram solves it. Use the visual audit's "Problem it solves" as the basis.]

[Repeat for each diagram added.]

*All visual aid additions: [VISUAL-TICKET-ID]({YOUR_ISSUE_TRACKER}/VISUAL-TICKET-ID)*  ← use the sub-issue whose title matches "visual" / "diagram"; fall back to TICKET_ID
```

---

### 7. Display summary

After writing the file:

```
Created: {OUTPUT_FILE}

Sections written:
  ✓ Diataxis split ([N] docs)
  ✓ Content moved ([N] sections)
  [✓ Content removed ([N] items) — if applicable]
  [✓ Style and formatting changes ([N] items) — if applicable]
  [✓ Visual aids added ([N] diagrams) — if applicable]

Evidence used:
  - Original doc: [ORIGINAL_PATH]
  - Output docs: [list]
  - Audit report: [found / not found]
  - Visual audit: [found / not found]
  - Ticket: [TICKET_ID / not provided]
```

---

## Error Handling

| Situation | Behavior |
|-----------|----------|
| Missing required argument | Stop, show usage |
| Original doc not found | Stop: "File not found: [path]" |
| Output dir not found | Stop: "Directory not found: [path]" |
| Zero output docs found | Stop: "No output docs found in [path]. Run the split first." |
| OUTPUT_FILE already exists | Stop: "File already exists — delete it first." |
| Audit report not found | Continue without it; note in summary |
| Visual audit not found | Skip visual aids section; note in summary |
| Ticket read fails | Continue without ticket context; note in summary |

---

## Notes

- Omit any section where nothing applies. A shorter, accurate document beats a longer one with empty sections.
- The "Content moved" section only covers intentional relocations — not 1:1 content carried from original to new doc under the same heading.
- Style changes that are trivial or obvious (e.g., whitespace, minor punctuation) don't need to be listed. Focus on changes an SME would notice or care about.
- Gold standard output: `docs/output/_process/editorial-changes.md` in a completed guide-conversion workspace.
- Trigger: after the split is complete, style pass done, visual aids added — before review/PR
- Do NOT run for minor edits or partial rewrites — only for structural splits producing multiple output files
