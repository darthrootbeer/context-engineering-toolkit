---
name: docs-diataxis-split
description: Execute a Diataxis split — reads the audit report and JSON mapping from a completed /docs-diataxis-audit run, extracts content from the source doc into typed output files (explanation, how-to, reference, tutorial), and always creates an overview doc. Auto-detects all inputs from project structure. Use when user asks to split a doc, execute the split, or run the Diataxis split.
allowed-tools: [Read, Write, Edit, Glob, Bash]
---

# docs-diataxis-split

Execute a Diataxis split. Reads the audit report and JSON mapping produced by `/docs-diataxis-audit`, extracts content from the source document into purpose-built typed docs, and always produces an overview doc that acts as the guide's entry point. All output goes to `docs/output/docs/`.

No arguments required — all inputs are inferred from project structure.

## Steps

### 1. Auto-detect inputs

**Find the source doc:**
```bash
ls docs/input/*.md 2>/dev/null
```
Expect exactly one `.md` file. If zero: stop — `"No source doc found in docs/input/. Add the original document there first."` If multiple: list them and prompt — `"Multiple docs found in docs/input/ — which one is the source? Enter the filename:"`

Store as `SOURCE_PATH` and extract `INPUT_BASENAME` (filename without extension).

**Find audit artifacts:**
```bash
ls docs/output/_process/diataxis-audit/ 2>/dev/null
```
Look for:
- `*_audit-report.md` → store as `AUDIT_REPORT_PATH`
- `*_mapping.json` → store as `MAPPING_PATH`

If either is missing: stop — `"Audit artifacts not found in docs/output/_process/diataxis-audit/. Run /docs-diataxis-audit [source-doc] first."`

**Confirm what was found:**
```
Inputs detected:
  Source:       {SOURCE_PATH}
  Audit report: {AUDIT_REPORT_PATH}
  JSON mapping: {MAPPING_PATH}

Proceed? (y/n)
```

---

### 2. Read all inputs

Read these files in parallel using the `Read` tool:
- The source document (`SOURCE_PATH`)
- The audit report (`AUDIT_REPORT_PATH`)
- The JSON mapping (`MAPPING_PATH`)

From the JSON mapping, extract:
- `original_document.name` → guide title
- `original_document.sections[]` → source sections (id, slug, title, target_type)
- `target_documents[]` → target docs (type, title, sections[])

From the audit report, read:
- Restructuring Recommendations (what each output doc should contain)
- Boundary violations (which content needs to be split away from adjacent content)
- Cross-reference strategy (signpost wording and link strategy)

---

### 3. Parse source document into sections

Parse `SOURCE_PATH` into a section map:
- Split on H1 (`# `) and H2 (`## `) headings
- For each section, store: heading level, heading text, content body (everything until the next heading of equal or higher level)
- Build a lookup: `{normalized_title → content_block}` and `{slug → content_block}`

Normalization: lowercase, strip non-alphanumeric, collapse spaces → kebab-case.

**Resolve section ID → source content:**
For each entry in `original_document.sections[]`:
- Match by normalized title/slug against the parsed section map
- Store resolved content alongside each section record
- If a section can't be matched: note it as `UNRESOLVED` — do not stop, continue with remaining sections

---

### 4. Determine filenames and create output folder

#### 4a. Determine all filenames first

**Guide name prefix:** If running inside a workspace (directory name starts with `workspace-`), extract the guide name slug from the workspace folder name. The slug is everything after the ticket number portion. Example: `workspace-doc-1318-intro-to-the product` → `GUIDE_PREFIX = "intro-to-the product"`. All output files are prefixed with `{GUIDE_PREFIX}_`.

For each entry in `target_documents[]` from the JSON mapping, convert the target document `title` to a kebab-case slug. Do not add a Diataxis type prefix — the type is recorded in the `diataxis_type` frontmatter field instead. Prepend the guide name prefix.

**Examples** (guide prefix `intro-to-the product`):
- type `explanation`, title `"benefits-card Payments and the The Product Ecosystem"` → `intro-to-the product_ebt-payments.md`
- type `reference`, title `"Integration Options"` → `intro-to-the product_integration-options.md`

**Examples** (guide prefix `benefitspay`):
- type `explanation`, title `"Understanding BenefitsPay Payments"` → `wic_understanding-payments.md`
- type `how-to`, title `"How to Integrate BenefitsPay with The Product"` → `wic_integrate-with-the product.md`
- type `reference`, title `"BenefitsPay API Reference"` → `wic_api-reference.md`

Store each filename as you go — you'll need these for the overview doc.

**Validate filename before accepting it:**

Run these checks on the proposed filename (stem only, no `.md`):

| Check | Rule | Example fail |
|---|---|---|
| Lowercase + dashes only | No uppercase, underscores, or spaces | `BenefitsPay-Payments`, `wic_payments` |
| Area prefix present | At least one segment before the first dash | `payments.md` (no prefix) |
| Length | 2–4 dash-separated segments total | `benefitspay-a.md`, `benefitspay-payment-api-endpoint-list.md` |
| No gerunds | No word ending in `-ing` in any segment | `benefitspay-understanding-payments.md` |
| No bare type words | Descriptor is not solely `introduction` or `explanation` | `benefitspay-introduction.md`, `benefitspay-explanation.md` |

If any check fails, propose a corrected filename and confirm with the user before writing. Do not write the file with an invalid name.

#### 4b. Infer AREA_PREFIX and create output folder

Once all filenames are determined, infer `AREA_PREFIX` from the output filenames. Extract the leading segment (everything before the first `-`) from each filename; if all share the same prefix, use it. If ambiguous, prompt the user.

Examples:
- Output files `webhooks-concepts.md`, `webhooks-configure.md`, `webhooks-event-reference.md` → `AREA_PREFIX = webhooks`
- Output files `caper-refunds-customer-initiated.md`, `caper-refunds-staff-initiated.md` → `AREA_PREFIX = caper-refunds`

**Create the guide subfolder:**

```bash
mkdir -p docs/output/docs/{AREA_PREFIX}
```

This matches the ReadMe convention where each guide set lives in its own folder with `index.md` as the parent page and child docs alongside it. At publish time, `/docs-publish` copies this folder into the target category path.

---

### 5. Produce each typed output document

For each entry in `target_documents[]` from the JSON mapping (filenames already determined in step 4a):

#### 5b. Extract and assemble content

For each `sections[]` entry in this target document:
1. Look up `source_sections[]` IDs in `original_document.sections[]`
2. Retrieve the resolved source content for each
3. If a source section maps to **this target only** (1:1 or fully merged here): include the full content block
4. If a source section maps to **multiple targets** (split — same source ID appears in both how-to and reference targets): apply Diataxis extraction rules:
   - **How-to target**: Keep numbered procedure steps, decision points, outcomes. Strip field tables, JSON request/response examples, and parameter descriptions — replace with a signpost: `See [Guide Title API Reference — {section name}] for the full endpoint spec.`
   - **Reference target**: Keep field tables, JSON examples, parameter descriptions, and technical constraints. Strip narrative prose, "why this step exists" context, and procedural steps — replace with a signpost: `See [How to Integrate — {section name}] for the step this endpoint belongs to.`
   - **Explanation target**: Keep conceptual prose, system behavior descriptions, "why" context, analogies, and historical background. Strip numbered action steps and field tables.

5. Assemble target doc: ordered list of section content blocks, with a document H1 equal to `target_documents[].title`

#### 5c. Add cross-reference header (non-reference docs)

At the top of each typed doc, below the H1 but before the first section heading, add a one-line reader signpost appropriate to the doc type:

- **Explanation**: `> New to BenefitsPay? This doc explains the concepts. Ready to implement? See [How to Integrate — title](./how-to-filename).`
- **How-to**: `> New to BenefitsPay? Read [Understanding BenefitsPay — title](./explanation-filename) first. For endpoint specs, see [API Reference — title](./reference-filename).`
- **Reference**: `> For step-by-step instructions, see [How to Integrate — title](./how-to-filename).`
- **Tutorial**: `> When you're ready to go beyond the tutorial, see [How to Integrate — title](./how-to-filename).`

#### 5d. Write to file

Prepend a stub frontmatter block before the document H1, then write to `docs/output/docs/{AREA_PREFIX}/{filename}`:

```yaml
---
diataxis_type: {type}
hidden: true
---
```

Report each file written: `✓ {filename} ({section_count} sections)`

---

### 6. Produce the overview document

The overview doc is always produced regardless of what types exist in the mapping. It is the entry point and navigation hub for the split — it does not contain conceptual explanation, steps, or API specs.

#### 6a. Extract content from source

Locate these in the source document:
- **Guide title**: H1 of the source doc (or `original_document.name` from JSON mapping)
- **Opening orientation paragraph**: First substantive prose paragraph after the H1 (the "what this guide covers" framing). If none exists, synthesize one: `"This guide covers everything you need to [action] using the The Product API."`
- **Audience section**: Content of any section titled "Audience", "Who this is for", or similar. Use verbatim if clean; trim to 1–2 sentences if long.
- **Prerequisites section**: Content of any section titled "Prerequisites", "Before you start", or similar. If none exists, synthesize from context: what the source doc assumes the reader already has in place.

#### 6b. Build "What's in this guide" list

For each entry in `target_documents[]`, generate a bullet in this format:

```markdown
- **[{target title}](./{filename})**. {One sentence describing what this doc contains and when to use it.}
```

**Order:** Explanation → How-to → Reference → Tutorial (Diataxis reading order)

The one-sentence description is drawn from the audit report's description of each target doc's purpose. If not explicit in the audit report, infer from the target doc's type:
- Explanation: "Conceptual overview of how [topic] works. Read this before implementing."
- How-to: "Step-by-step instructions for each phase of the integration."
- Reference: "Complete endpoint specifications, error codes, and technical constraints."
- Tutorial: "Beginner walkthrough. Build a working [topic] integration from scratch."

#### 6c. Overview doc filename

`index.md` — always. Written to `docs/output/docs/{AREA_PREFIX}/index.md` (the same subfolder as the typed docs from step 5). `AREA_PREFIX` was already determined in step 4b.

#### 6d. Introduction doc format

Prepend a stub frontmatter block before the H1:

```yaml
---
diataxis_type: overview
hidden: true
---
```

Then the doc body:

```markdown
# {Guide Title}

{Opening orientation paragraph — 1–3 sentences. What this guide covers and what capability it enables.}

## Audience

{1–2 sentences. Who this is for. Assumed background.}

## Prerequisites

{2–4 sentences. What must already be in place before starting. Include links to upstream docs (get-started, prior integration guide, etc.) where appropriate.}

## What's in this guide

- **[{Explanation title}](./{explanation-filename})**. {One sentence.}
- **[{How-to title}](./{how-to-filename})**. {One sentence.}
- **[{Reference title}](./{reference-filename})**. {One sentence.}
{tutorial entry if present}
```

**What NOT to include in the overview doc:**
- Conceptual explanation of how the technology works (that's the explanation doc)
- Numbered steps or procedures (that's the how-to doc)
- Field tables, API specs, or error codes (that's the reference doc)
- Any content that duplicates what's already in one of the typed docs

#### 6e. Write to file

Write to `docs/output/docs/{AREA_PREFIX}/index.md`.

Report: `✓ {AREA_PREFIX}/index.md (overview — entry point)`

---

### 7. Handle unresolved sections

If any source sections were marked `UNRESOLVED` in step 3:

For each unresolved section:
- Report: `⚠  Could not auto-extract "{section title}" — check docs/output/docs/{AREA_PREFIX}/{target-filename}.md and add it manually`
- Insert a placeholder comment in the relevant output file at the location where the section should appear:
  ```
  <!-- TODO: Add content from source section "{section title}" here -->
  ```

---

### 8. Display summary

```
Split complete.

Output folder: docs/output/docs/{AREA_PREFIX}/

  ✓ index.md                             [overview — guide entry point]
  ✓ {slug}.md                            [explanation]
  ✓ {slug}.md                            [how-to]
  ✓ {slug}.md                            [reference]
  {tutorial if present}

All files include stub frontmatter with diataxis_type and hidden: true.

{If unresolved sections:}
⚠  {N} section(s) need manual review — placeholders added in the relevant files.

Source doc was not modified.

What's next:
  /docs-links-review docs/output/docs/{AREA_PREFIX}/  → cross-link check against The Product corpus
  /docs-visuals-review docs/output/docs/{AREA_PREFIX}/ → diagram recommendations
```

---

## Overview Doc Reference

The overview doc follows the same pattern as `benefitspay-overview.md`. Refer to it as a style reference:

```
docs/output/docs/{AREA_PREFIX}/index.md
```

Key characteristics of a good overview doc:
- Short (15–25 lines). Its job is to route, not inform.
- Opening paragraph orients the reader to the product capability, not to the docs themselves.
- Audience and Prerequisites are factual and direct — no marketing language.
- "What's in this guide" bullets are linked and describe the reader's *purpose* in going to that doc (e.g., "when to read this"), not just what the doc contains.
- Nothing in the overview doc is original content — it draws from the source doc's existing orientation language and from the typed docs' titles/purposes.

---

## Diataxis Extraction Quick Reference

When splitting a source section that maps to multiple targets:

| Content type | Goes to how-to | Goes to reference | Goes to explanation |
|---|---|---|---|
| Numbered steps | ✓ | | |
| "Why this step exists" prose | | | ✓ |
| Decision points and conditionals | ✓ | | |
| Field tables (request/response) | | ✓ | |
| JSON examples | | ✓ | |
| Parameter descriptions | | ✓ | |
| System behavior descriptions (no action required) | | | ✓ |
| Error codes and remediation steps | split | ✓ (codes) | |
| Conceptual analogies and comparisons | | | ✓ |
| Constraints and limits (static facts) | | ✓ | |

When in doubt: if the reader can act on it → how-to. If the reader looks it up → reference. If the reader reads it to understand → explanation.

---

## Error Handling

| Situation | Behavior |
|---|---|
| No source doc in `docs/input/` | Stop: "No source doc found in docs/input/" |
| Multiple source docs in `docs/input/` | Prompt: "Multiple docs found — which one?" |
| Audit artifacts missing | Stop: "Run /docs-diataxis-audit first" |
| Source section not matched in parse | Note as UNRESOLVED, insert placeholder, continue |
| Output file already exists | Stop per file: "File already exists: {path}. Delete it first or confirm overwrite." |
| `docs/output/docs/{AREA_PREFIX}/` can't be created | Stop with mkdir error |

---

## Notes

- Source doc is never modified. All output goes to `docs/output/docs/{AREA_PREFIX}/`.
- The overview doc is always produced — even if the audit doesn't mention it explicitly.
- Signpost cross-references are added to each typed doc automatically; do not omit them.
- For split sections, apply Diataxis extraction judgment — don't just copy the full section into both targets.
- Run `/docs-links-review` and `/docs-visuals-review` after the split before marking the work done.
