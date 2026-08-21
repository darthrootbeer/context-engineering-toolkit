---
name: docs-visuals-review
description: Visual aid audit for docs — reads a file or folder as the target user(s) and recommends where diagrams, flowcharts, or visual aids would most help. Mermaid-first. Use after finishing a new or restructured doc before review/PR.
allowed-tools: [Read, Write, Bash, Glob]
---

# docs-visuals-review

Read one or more markdown docs as their target users and recommend where visual aids would most improve comprehension. Output is a concise, prioritized report: what to add, where exactly, and what problem it solves for the reader. Mermaid diagrams are preferred; graphics are recommended only when no diagram type fits.

## Arguments

The user provided: $ARGUMENTS

This should be a path to a **folder** (all `.md` files inside treated as the doc set) or a single `.md` **file**.

## Usage

`/docs-visuals-review [folder-or-file-path]`

**Required:** The `[folder-or-file-path]` parameter is mandatory. If not provided, stop and ask: "Please provide a folder or file path: `/docs-visuals-review [path]`"

---

## Steps

### 1. Validate input

- Check that `$ARGUMENTS` is provided. If not, stop with usage message.
- Resolve whether the path is a directory or a single file:
  - **Directory**: Glob all `.md` files inside it. Abort if zero `.md` files found.
  - **File**: Use that single file. Abort if it doesn't exist.
- Store the full file list.

### 2. Read each doc in full

Use the `Read` tool to read each doc completely. As you read, note:
- H1, H2, H3 headings and their approximate line numbers
- The presence of an `## Audience` section — extract the named roles if present
- Any existing visuals (Mermaid diagrams, images, ASCII art, ASCII flow diagrams, tables)
- Sections that are already well-served by existing visuals

**Text-diagram scan:** Explicitly flag any of the following found outside a `mermaid` fenced code block:
- ASCII flowcharts using box-drawing characters (`┌`, `└`, `├`, `─`, `┴`) or arrows (`→`, `↓`, `↑`)
- Progress bars or status indicators built from block characters (`█`, `░`)
- Tree structures using `├─`, `└─`, `│`
- Step sequences written inline as `A → B → C`

For each one found, record: file, approximate line number, what it represents, and whether a Mermaid equivalent exists. A suitable Mermaid type exists for flows and trees; it does not exist for progress bars or UI mockups (those stay as ASCII or become screenshots). Add each as a Medium or Strong recommendation accordingly.

### 3. Identify user personas

For each doc (or the doc set as a whole if a folder):

1. **Check for `## Audience` section** — use the named roles directly.
2. **Infer from doc type if no Audience section:**
   - How-to → implementation engineer
   - Explanation → technical PM, architect, or engineer building mental models
   - Reference → engineer in the middle of a task, looking something up
   - Introduction → any first-time reader; both engineers and PMs
   - Tutorial → hands-on learner, following along

Keep personas to 2–3 max. Be specific: "payment engineer" not "developer."

### 4. Assess each section for visual aid candidates

For each non-trivial section in each doc, assess against these patterns. A section qualifies as a candidate if it matches one or more:

**Strong candidates (high signal):**
- **Multi-party flow**: 3+ parties interacting across steps (e.g., app ↔ customer browser ↔ third-party API), especially with redirects or async steps. → Mermaid sequence diagram
- **Decision tree with consequences**: Branching logic where the wrong branch has a real cost (failed transaction, incorrect settlement, data loss). 2+ branches, each with distinct outcomes. → Mermaid flowchart
- **Lifecycle with stages**: A named sequence of phases where each phase feeds the next, especially when a time constraint (expiry, deadline) is attached. → Mermaid flowchart or stateDiagram
- **Error-prone calculation in prose**: A math/proration example described only in words, where the reader must hold intermediate values in their head to follow it. → Annotated table or worked example

**Medium candidates:**
- **Branching logic adequately described in prose**: A decision sequence that's correct as written but would click faster as a visual. No serious penalty for misunderstanding, but a diagram would save re-reads.
- **Comparative data across 3+ options in prose**: Attributes being compared without a table. The reader must reread to compare.
- **Author already tried to visualize**: Section has ASCII art or an inline text diagram — shows the author felt the need but didn't have the tool. Upgrade to Mermaid.

**Low candidates (optional only):**
- Interesting conceptually but prose is adequate and the reader isn't likely to misunderstand.
- Visual would be nice but doesn't clearly outperform the text.

**Skip entirely:**
- Sections already served by an existing Mermaid diagram, image, or well-structured table.
- Reference/lookup sections where the reader is scanning for a specific value — diagrams slow this down.
- Sections with fewer than 3 steps or 2 decision points.
- Short introductory or linking paragraphs.

### 5. Build recommendations list

For each candidate:
- Record: doc filename, section heading, approximate line range, candidate strength (Strong / Medium / Low), recommended visual type, and the one-sentence problem statement (what the reader can't easily do without a visual).
- Discard any Low candidate if there are already 3+ Strong or Medium recommendations for the same doc — keep the report focused.

### 6. Validate output directory

- Check whether `docs/output/_process/visual-audit/` exists relative to the current working directory.
- If not, create it: `mkdir -p docs/output/_process/visual-audit/`

### 7. Write report

Write the report to: `docs/output/_process/visual-audit/visual-audit-[slug].md`

Where `[slug]` is:
- The folder name (last path component) if the input was a directory.
- The filename stem (no extension) if the input was a single file.

See **Report Format** below.

### 8. Display summary

After writing, output:

```
Visual audit complete.

Docs reviewed: [N]
Recommendations: [N Strong] strong, [N Medium] medium, [N Low] low

Report: docs/output/_process/visual-audit/visual-audit-[slug].md
```

---

## When Implementing Diagrams

This section applies whenever Mermaid diagrams or visual aids are implemented as part of a ticket — whether as a follow-up to this skill's recommendations or as standalone work.

**Trigger:** Any time a Mermaid diagram or markdown visual is embedded into a doc as part of a tracked ticket.

### Step A — Save each diagram as a standalone file

For every diagram implemented:

1. **Mermaid diagrams** → save as `.md` file with a fenced ```` ```mermaid ```` code block
2. **Non-Mermaid visuals** (tables, worked examples) → save as `.md` file

Using `.md` (not `.mermaid` or `.mmd`) ensures the file can be previewed in Cursor with Command+Shift+V via the `bierner.markdown-mermaid` extension.

**File location:** `docs/output/_process/visual-audit/diagrams/`
- Create if missing: `mkdir -p docs/output/_process/visual-audit/diagrams/`

**File naming:** Descriptive kebab-case slug matching the diagram's content, not the ticket:
- ✅ `balance-session-capture-flow.md`
- ✅ `straddle-rules.md`
- ✅ `discount-proration-mixed-cart.md`
- ❌ `doc-1204-diagram-1.md`

**File content for all `.md` diagram files** — include a plain markdown header, then wrap Mermaid in a fenced code block. Do NOT include the ticket ID — this is redundant when the file is posted as a comment on that same ticket:
```markdown
### [Short title]

Used in: `[filename]`, §[Section heading]

```mermaid
[Mermaid diagram code here]
```
```

**Dollar signs in prose:** Escape with `\$` in all inline prose text (e.g., `\$10 off a \$100 cart`). Dollar signs inside table cells render correctly and do not need escaping. Unescaped `$...$` pairs in prose are parsed as LaTeX math delimiters by VS Code preview and other renderers.

**Line breaks in Mermaid nodes:** Use `<br />` for line breaks inside Mermaid diagram node labels. `\n` and `<br>` do not work in Mermaid syntax.

### Step B — Post diagrams to the ticket as a threaded comment

Post one **parent comment** summarising what's attached, then one **sub-comment per diagram** nested under it — **all in the same script, in the same response.** Never post the parent without immediately posting the sub-comments. If you can't post them all at once, don't post the parent yet. Use the Linear GraphQL API directly — `linearis` doesn't support replies.

```python
import json, urllib.request, os

TOKEN = open(os.path.expanduser("~/.linear_api_token")).read().strip()
HEADERS = {"Authorization": TOKEN, "Content-Type": "application/json"}

def gql(query, variables=None):
    payload = {"query": query, "variables": variables or {}}
    req = urllib.request.Request("https://api.linear.app/graphql",
        data=json.dumps(payload).encode(), headers=HEADERS)
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read())

ISSUE_ID = "<TICKET-ID>"  # e.g. "DOC-102"

# 1. Create parent comment
parent = gql(
    "mutation($input:CommentCreateInput!){commentCreate(input:$input){success comment{id}}}",
    {"input": {"issueId": ISSUE_ID, "body": "Here are the diagrams created as part of this ticket — one comment per diagram below."}}
)
parent_id = parent["data"]["commentCreate"]["comment"]["id"]

# 2. One sub-comment per diagram (paste full .md file content as body)
diagrams = [
    open("docs/output/_process/visual-audit/diagrams/diagram-one.md").read(),
    open("docs/output/_process/visual-audit/diagrams/diagram-two.md").read(),
]
for body in diagrams:
    gql(
        "mutation($input:CommentCreateInput!){commentCreate(input:$input){success}}",
        {"input": {"issueId": ISSUE_ID, "body": body, "parentId": parent_id}}
    )
```

Do not use `linearis embeds upload` or `### Attachments` sections for diagram files.

---

## Report Format

```markdown
# Visual Aid Audit: [input name]

This report was produced as part of the product documentation team's structured conversion process for [brief description of the doc or doc set]. It reviews each document as its target reader would and identifies where visual aids would most improve comprehension.

Below you'll find prioritized recommendations sorted by impact — Strong where a visual clearly outperforms prose, Medium where it helps but prose is adequate — followed by a "Not recommended" section logging what was deliberately skipped.

## Who reads these docs

[2–4 sentences. Name the personas (by role), what they're trying to do, and where they typically enter the doc set. Be specific — "payment engineer building their first AcmePay integration" not "developers."]

---

## Recommendations (sorted by strength)

---

### [N]. [Short label for the recommendation]
**Strength:** Strong / Medium / Low
**Doc:** `[filename]`
**Location:** [Section heading]
**Visual type:** [Mermaid sequence diagram / Mermaid flowchart / Mermaid stateDiagram / annotated table / screenshot / graphic image]
**Problem it solves:** [One sentence. What the reader can't easily do with the text alone — don't describe the diagram, describe the gap.]

---

[Repeat for each recommendation]

---

## Not recommended

| Doc | Section | Why skipped |
| --- | ------- | ----------- |
| `[filename]` | [Section or "(whole doc)"] | [1 sentence] |

[Include only notable skips — things where a visual might seem obvious but isn't warranted. Omit trivially short or lookup-only sections.]
```

**Voice:** Do not mention AI or automation tools. "The Product documentation team's structured conversion process" is the right framing for the intro sentence.

**Ordering within the report:**
1. Strong recommendations first, in doc order (top of doc → bottom)
2. Medium recommendations next, in doc order
3. Low recommendations last

---

## Visual Type Reference

Use these Mermaid diagram types as defaults. Recommend a graphic image only when none of these fit.

| Situation | Diagram type |
| --------- | ------------ |
| Multiple parties exchanging messages across time | `sequenceDiagram` |
| Branching decisions and outcomes | `flowchart TD` or `flowchart LR` |
| Lifecycle stages / states and transitions | `stateDiagram-v2` |
| Entity relationships or data structure | `erDiagram` |
| Gantt / timeline | `gantt` |
| Already present as ASCII art | Upgrade to equivalent Mermaid type |
| UI screenshot / customer-facing flow | Graphic image (note: requires actual screenshots) |
| Abstract concept requiring custom illustration | Graphic image (note: requires design work) |

---

## Scoring Criteria (reference)

**Strong** — meets one or more:
- Flow involves 3+ parties or 5+ steps, especially with redirects, async callbacks, or time constraints
- Decision tree where misunderstanding a branch causes a real failure (wrong API call, incorrect settlement, data loss)
- Math or proration in prose where the reader must hold multiple intermediate values in their head

**Medium** — meets one or more:
- Branching logic that's correct as text but would click faster visually
- Comparison of 3+ options across multiple attributes, currently prose
- Section has existing ASCII art (author already tried to visualize)

**Low:**
- Visual is nice but prose is sufficient; low cost of misunderstanding

**Skip:**
- Section is already served by an existing visual
- Reference/lookup sections (tables already the right format)
- Fewer than 3 steps or 2 decision points
- Short transition or linking paragraphs

---

## Error Handling

| Situation | Behavior |
| --------- | --------- |
| No `$ARGUMENTS` | Stop: show usage message |
| Path doesn't exist | Stop: "File not found: [path]" or "Directory not found: [path]" |
| Directory has no `.md` files | Stop: "No markdown files found in: [path]" |
| File >1500 lines | Note in report header: "⚠️ Large file — deep sections may be partially analyzed." Continue. |
| Output directory creation fails | Stop: "Cannot create output directory: docs/output/_process/visual-audit/" |

---

## Notes

- This skill is **read-only**. Nothing in the source docs is modified.
- Run this **after** `/docs-diataxis-audit` (structure) and `/docs-links-review` (cross-links), before submitting for review.
- Mermaid is always preferred over graphic images. Only recommend a graphic image when the content is inherently visual (UI screenshots, product illustrations) or no Mermaid diagram type fits.
- The report is a recommendation, not a spec. The author decides what to implement. "Not recommended" sections give the reader confidence that skips were deliberate.
- If the input is a folder, assess the doc set as a unit — some recommendations may span docs (e.g., a sequence diagram that would live in the how-to but references concepts from the explanation doc).
