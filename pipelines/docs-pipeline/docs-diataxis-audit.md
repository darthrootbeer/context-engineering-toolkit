---
name: docs-diataxis-audit
description: Audit documentation using Diátaxis framework, generate reports and JSON mapping. Use when user asks to audit docs, analyze documentation structure, or apply Diátaxis framework.
allowed-tools: [Read, Write, Bash]
---

# docs-diataxis-audit

Audit an existing file using the Diataxis framework to identify content types and recommend restructuring. Generates both a markdown audit report and a JSON mapping file.

## Arguments

The user provided: $ARGUMENTS

This should be the path to the markdown file to audit.

## Usage

`/docs-diataxis-audit [file-path]`

**Required:** The `[file-path]` parameter is mandatory. If not provided, stop and ask for the source document to audit.

## Steps

1. **Validate input**

   - Check that `[file-path]` is provided in $ARGUMENTS
   - If not provided, stop: "Please provide the file path to audit: `/docs-diataxis-audit [file-path]`"
   - Determine `INPUT_BASENAME` for output naming:
     - **If running inside a workspace** (directory name starts with `workspace-`): Extract the guide name slug from the workspace folder name. The slug is everything after the ticket number portion. Example: `workspace-doc-1318-intro-to-billing` → `INPUT_BASENAME = "intro-to-billing"`
     - **Otherwise**: Get filename from `basename [file-path]`, remove extension (`.md`, `.markdown`). Example: `docs/source/guide.md` → `INPUT_BASENAME = "guide"`
   - All output files (audit report, mapping JSON, SVGs) are prefixed with `{INPUT_BASENAME}_`. This ensures every artifact is traceable to its guide, even when moved or referenced outside the workspace.

2. **Read the framework**

   - Read and understand: `~/projects/readme-payments-api-docs/_extras/style-guides/diataxis/README.md`
   - Focus on: four types, classification axes, boundary rules
   - Use `Read` tool
   - Note: Multiple files can be read in parallel if needed

3. **Validate file**

   - Check that file exists at provided path using `Read` tool
   - If file doesn't exist, stop: "File not found: [file-path]" (see Error Handling)
   - Read the current file contents using `Read` tool
   - Parse markdown structure to extract all section headings (H1, H2, H3, etc.) and their hierarchy
   - Store section information: heading level, title, approximate line numbers, content between sections

4. **Analyze content using classification procedure**

   Follow this procedure for the document:

   - Examine title and opening lines (strongest signals of intent)
   - Identify primary reader state (studying to gain skill vs. working to apply skill)
   - Identify primary question ("Teach me from zero", "How do I do this now?", "What is this?", "Why is it like this?")
   - Identify dominant value (executable steps vs. propositional understanding)
   - Apply classification decision tree (see below)
   - If multiple intents present, identify dominant intent and note other content types for extraction
   - For each section extracted in step 3, classify it using the decision tree below

5. **Apply classification decision tree**

   For each section of content:

   **Classification Logic:**
   - Step-by-step instructions + learning context → **TUTORIAL**
   - Step-by-step instructions + working context → **HOW-TO GUIDE**
   - Technical facts without narrative → **REFERENCE**
   - Conceptual understanding and "why" → **EXPLANATION**

   **Detailed Decision Path:**

   **Step 1**: Does it contain step-by-step instructions?
   - YES → Continue to step 2
   - NO → Skip to step 4

   **Step 2**: What is the reader's state?
   - Learning/studying (beginner, needs guidance, safe environment) → **TUTORIAL**
   - Working (competent user, real-world task) → **HOW-TO GUIDE**

   **Step 3**: Does it contain factual lists, parameters, commands, or technical specifications?
   - YES → Extract to **REFERENCE** document
   - NO → Continue classification

   **Step 4**: Does it contain conceptual understanding, rationale, or context?
   - YES → **EXPLANATION**
   - NO → **REFERENCE**

   **Step 5**: If multiple kinds detected → Split into separate documents by user need, not by product components

   **Store classification results:**
   - For each section, record:
     - `id`: Stable 6-8 character hex hash (see "ID Generation Algorithm")
     - `slug`: Kebab-case identifier from title (for display)
     - `title`: Section heading as it appears
     - `target_type`: One of tutorial/how-to/reference/explanation/excluded

6. **Recognize content patterns**

   Use these patterns to identify content types:

   **Tutorial patterns:**

   - "In this tutorial, we'll..."
   - Step-by-step with expected outputs
   - Beginner-friendly language
   - Single path, no alternatives
   - Safety checks and recovery steps
   - First-person plural ("we", "our")

   **How-to Guide patterns:**

   - "How to [achieve goal]"
   - Conditional statements ("if you want X, do Y")
   - Real-world scenarios
   - Decision points and variations
   - Assumes competence
   - Focus on outcome, not process

   **Reference patterns:**

   - Lists of parameters, options, commands
   - Tables of facts
   - Technical specifications
   - API documentation structure
   - Neutral, factual tone
   - Organized by system architecture

   **Explanation patterns:**

   - "Why" questions
   - Historical context
   - Design decisions and tradeoffs
   - Conceptual relationships
   - Analogies and comparisons
   - Readable away from the interface

7. **Identify boundary violations**

   Check for these anti-patterns:

   - Tutorial with options/choices
   - How-to with teaching/background
   - Reference with narrative/story
   - Explanation with step-by-step procedures
   - Mixed-type pages

   Common boundary violations:

   - Tutorial → How-to: Skipping explanations, assuming knowledge, prioritizing efficiency over learning
   - How-to → Explanation: Adding conceptual explanations beyond task context
   - How-to → Tutorial: Teaching basics instead of assuming competence
   - Reference → How-to: Including procedural steps or setup instructions
   - Reference → Explanation: Explaining design decisions or reasoning
   - Explanation → How-to: Prescribing specific actions
   - Explanation → Reference: Listing technical specifications without context

8. **Apply content migration rules**

   Identify what should be extracted:

   - **Step sequences** → How-to Guide (unless beginner learning journey → Tutorial)
   - **Lists of options, parameters, commands, tables, constraints, error messages** → Reference
   - **History, rationale, tradeoffs, alternatives, conceptual framing, reasons-why** → Explanation
   - **Teaching content in how-to/reference** → Extract to Tutorial or Explanation, link back

   **Group sections into target documents:**
   - Group sections by their `target_type`
   - For each group, determine appropriate target document title
   - For each target section, determine mapping type:
     - **1:1 mapping** (section moves intact): Use the SAME hash `id` from source section (retain ID as section moves)
     - **Split mapping** (one source → multiple targets): Generate new hash `id` for each target section
     - **Combined mapping** (multiple sources → one target): Generate new hash `id` for target section
     - **New content** (no source): Generate new hash `id` for target section
   - For each target section, generate:
     - `id`: Hash ID (reuse source ID for 1:1, generate new for split/combined/new)
     - `slug`: New kebab-case identifier from title (unique within document)
     - `source_sections`: Array of source hash IDs that map to this section
   - Store this mapping for JSON generation

9. **Generate audit report (in-memory)**

   Create a comprehensive markdown report. Open with a header block and intro section, then the content sections.

   **Header and intro (write first, before any sections):**

   ```markdown
   # Diátaxis Audit Report: [Document Title]

   **Input file**: `[ORIGINAL_PATH]`
   **Date**: [today's date]
   **Framework**: Diátaxis (diataxis.fr)

   This report was produced as part of the product documentation team's structured conversion process for `[original-filename.md]`. It applies the Diataxis framework to classify every section of the source document by reader intent, surface structural problems that affect how readers use the doc, and recommend how to split it into a set of focused, purpose-built documents.

   Below you'll find a content type breakdown across all [N] sections, a list of boundary violations with their reader impact, and section-level restructuring recommendations for [N] output documents.

   **Companion outputs from this audit:**

   | File | What it is |
   |------|------------|
   | `{INPUT_BASENAME}_audit-report.md` | This document — the full analysis, violations, and restructuring recommendations |
   | `{INPUT_BASENAME}_mapping.json` | Machine-readable mapping of every source section to its target document and section; used to track the split programmatically |
   | `00-overview.svg`, `01-*.svg`, ... | Visual mapping diagrams — overview shows all source → target flows; per-target-doc pages show the full source with relevant sections highlighted |
   ```

   Do not mention AI or automation tools. "The Product documentation team's structured conversion process" is the right framing.

   Fill in `[N] sections` and `[N] output documents` with the actual numbers from your analysis before writing the file.

   **Content Analysis:**

   - Percentage breakdown of content types found
   - List of sections by content type with specific line/section references
   - Identification of mixed or unclear content
   - Dominant content type classification

   **Boundary Violations:**

   - List specific violations with line/section references
   - For each violation, use this structure:
     - `**Where:**` — section name and line range
     - `**What's happening:**` — what the content is doing and why it's in the wrong place. For low-severity violations (no heading, minor misplacement), fold the "why" into this block rather than adding a separate sub-header.
     - `**Why it matters:**` (medium/high severity only) — explain the reader impact in plain English. Do NOT lecture about the framework ("Reference documents answer X, not Y"). Say what the mix does to the reader: makes the section harder to scan, buries guidance where they won't look, etc.
     - `**Fix:**` — concrete action
   - Severity labels: High / Medium / Low — include in the section header: `### Violation N — [plain English label] (High/Medium/Low)`

   **Restructuring Recommendations:**

   - Open with: "Suggested structure: **[type] → [type] → ...** — each doc below maps to one of these." (caption format, not instruction)
   - Suggest how to split content into separate documents
   - Recommend titles for each new document (use appropriate naming: "tutorial-", "how-to-", "reference-", "explanation-")
   - Propose content organization strategy
   - Identify cross-references needed between documents
   - Apply content migration rules to each section
   - Ensure each document stands alone for its kind
   - Replace removed material with signposts and links

   **Priority Actions:**

   - Most critical changes to improve documentation quality
   - Quick wins that provide immediate value
   - Long-term structural improvements
   - Specific steps from rewrite protocol to follow

10. **Validate output directory**

    - Check if `docs/output/_process/diataxis-audit/` exists
    - If not, create using `Bash` tool: `mkdir -p docs/output/_process/diataxis-audit/`
    - Verify creation succeeded (no error from mkdir)
    - If creation fails:
      - Stop with error: "Cannot create output directory: docs/output/_process/diataxis-audit/"
      - Include error details from Bash command (see Error Handling)

    This ensures subsequent steps can write files successfully.

11. **Write audit report to file**

    - Generate output filename: `docs/output/_process/diataxis-audit/{INPUT_BASENAME}_audit-report.md`
    - Write the complete audit report using `Write` tool
    - If write fails: Stop with error message including file path (see Error Handling)
    - Report: "Audit report written to: docs/output/_process/diataxis-audit/{INPUT_BASENAME}_audit-report.md"

12. **Generate and write JSON mapping**

    Create JSON mapping following schema: `_shared/schemas/diataxis-audit-mapping/schema.json`

    a. **Read schema files**
       - Read: `_shared/schemas/diataxis-audit-mapping/schema.json`
       - Read: `_shared/schemas/diataxis-audit-mapping/README.md`
       - Use `Read` tool (can read both in parallel)
       - Understand structure, validation rules, dual-ID system

    b. **Generate section IDs**
       - For original sections: Generate hash `id` and `slug` (see "ID Generation Algorithm")
       - For target sections:
         - 1:1 mapping: Reuse source hash `id` (section retains ID as it moves)
         - Split/combined/new: Generate new hash `id`
       - Generate `slug` for all sections from titles

    c. **Build JSON structure**
       - Create `original_document` object:
         - `name`: Document title (from H1) or filename
         - `sections[]`: Array with `id`, `slug`, `title`, `target_type`
       - Create `target_documents[]` array:
         - Each document: `type`, `title`, `sections[]`
         - Each section: `id`, `slug`, `title`, `source_sections[]`
       - Map sources to targets via `source_sections[]` (use hash IDs, not slugs)

    d. **Validate JSON structure**

       Run validation checks before writing (see Error Handling for failure handling):

       - **ID Format**: All hash `id` match `^[a-f0-9]{6,8}$`, all `slug` match `^[a-z0-9-]+$`
       - **Uniqueness**: Hash IDs unique in `original_document.sections[]` and within each `target_documents[].sections[]`
       - **Mapping Integrity**:
         - For 1:1: If `source_sections.length === 1`, target `id` must equal `source_sections[0]`
         - All IDs in `source_sections[]` exist in `original_document.sections[].id`
         - All source sections appear in at least one `source_sections[]` (unless `target_type` is null/"excluded")
       - **Structure**: Required fields present (name, sections, type, title, etc.)

       If validation fails:
       - Report specific errors with section IDs and field names
       - Do NOT write invalid JSON to file
       - Stop and prompt review

    e. **Write to file**
       - Filename: `docs/output/_process/diataxis-audit/{INPUT_BASENAME}_mapping.json`
       - Format: 2-space indentation, proper JSON syntax
       - Use `Write` tool
       - If write fails: Stop with error message (see Error Handling)
       - Report: "JSON mapping written to: docs/output/_process/diataxis-audit/{INPUT_BASENAME}_mapping.json"

13. **Generate SVG visualizations**

    - Command: `node _shared/tools/diataxis-mapper/generate-svg.js --multi --prefix {INPUT_BASENAME} docs/output/_process/diataxis-audit/{INPUT_BASENAME}_mapping.json docs/output/_process/diataxis-audit/`
    - Use `Bash` tool to execute the command
    - Output files (all prefixed with `{INPUT_BASENAME}_`):
      - `{INPUT_BASENAME}_00-overview.svg` — Complete overview showing all source → target mappings
      - `{INPUT_BASENAME}_01-{type}.svg`, `{INPUT_BASENAME}_02-{type}.svg`, ... — One per target document, showing full source with relevant sections highlighted and non-relevant sections muted
    - Sections with `target_type: "ignored"` are omitted from all diagrams
    - Sections with `target_type: "excluded"` appear greyed out on detail pages
    - If command fails:
      - Catch error and continue (SVGs are optional output)
      - Report: "SVG generation failed: [error message]"
    - If successful:
      - Report: "SVG visualizations written to: docs/output/_process/diataxis-audit/"

14. **Display summary**

    - Present a brief summary:
      - Input file: `[file-path]`
      - Audit report: `docs/output/_process/diataxis-audit/{INPUT_BASENAME}_audit-report.md`
      - JSON mapping: `docs/output/_process/diataxis-audit/{INPUT_BASENAME}_mapping.json`
      - SVG visualizations: `docs/output/_process/diataxis-audit/00-overview.svg`, etc. (if generated)
      - Number of sections analyzed
      - Number of target documents recommended
      - Dominant content type found
    - Note: No changes were made to the source file
    - **Next step prompt**: If the audit recommends splitting into multiple documents, end with:
      "Ready to scaffold the editorial record? Run `/editorial-changes [file-path] docs/output/` to create the `editorial-changes.md` for this split."

## ID Generation Algorithm

### Hash ID Generation

Generate stable 6-8 character hexadecimal hash for each section.

**Input Components**:
1. Section title (normalized: lowercase, trimmed, alphanumeric only)
2. Section position/hierarchy (e.g., "2.3.1" or line number "45")
3. First 50 characters of section content (normalized)

**Pseudo-code**:
```javascript
function generateHashId(section) {
  const titleNorm = section.title.toLowerCase().replace(/[^a-z0-9]/g, '').trim();
  const position = section.position;  // "2.1" or "45"
  const contentNorm = section.content.substring(0, 50)
    .toLowerCase()
    .replace(/[^a-z0-9]/g, '')
    .trim();

  const input = titleNorm + position + contentNorm;
  const hash = sha256(input);  // Full SHA-256 hash
  return hash.substring(0, 8);  // First 8 characters
}
```

**Example**:
- Title: "Get Started"
- Position: "2.1"
- Content: "This section explains how to begin using..."
- Normalized: `"getstarted2.1thissectionexplainshowtobegin"`
- SHA-256: `a3f9b2c1d4e7f8g9...` (full hash)
- **Hash ID**: `a3f9b2c1` (first 8 chars)

**ID Reuse Policy**:
- **1:1 mapping**: Target section MUST use SAME hash ID as source
- **Split mapping**: Each target gets NEW hash ID
- **Combined mapping**: Target gets NEW hash ID
- **New content**: Target gets NEW hash ID

### Slug Generation

Generate human-readable kebab-case identifier from title.

**Pseudo-code**:
```javascript
function generateSlug(title) {
  return title
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')  // Non-alphanumeric → hyphens
    .replace(/^-+|-+$/g, '')       // Remove leading/trailing
    .replace(/-{2,}/g, '-');       // Collapse consecutive hyphens
}
```

**Examples**:
- "Get Started" → `"get-started"`
- "API Reference: Authentication" → `"api-reference-authentication"`
- "How to Deploy (Production)" → `"how-to-deploy-production"`

**Note**: Slugs are for display only. Use hash IDs for all mapping connections.

## Error Handling

Handle these error conditions gracefully:

### Input File Errors (Step 3)
- **File not found**: Stop with "File not found: [file-path]"
- **File read failure**: Stop with "Cannot read file: [file-path]" + error details

### Output Directory Errors (Step 10)
- **Directory creation fails**: Stop with "Cannot create output directory: docs/output/_process/diataxis-audit/" + error details

### File Write Errors (Steps 11, 12)
- **Audit report write fails**: Stop with "Cannot write audit report: [file-path]" + error details
- **JSON write fails**: Stop with "Cannot write JSON mapping: [file-path]" + error details

### JSON Validation Errors (Step 12d)
- Report specific errors with section IDs and field references
- Example: "Validation error: Section 'abc123' has invalid ID format (must match ^[a-f0-9]{6,8}$)"
- Do NOT write invalid JSON to file
- Stop and prompt review

### SVG Generation Errors (Step 13)
- **Script not found**: Continue without SVGs, report: "SVG generation skipped (generate-svg.js not found)"
- **Other failures**: Continue without SVGs, report: "SVG generation failed: [error message]"

**Philosophy**: Stop on critical errors (input, validation, write). Continue on optional failures (SVG).

## Example JSON Output

### Minimal Example (1:1 mapping)

```json
{
  "original_document": {
    "name": "Getting Started Guide",
    "sections": [
      {
        "id": "a3f9b2c1",
        "slug": "installation",
        "title": "Installation",
        "target_type": "tutorial"
      },
      {
        "id": "b7e4d9f2",
        "slug": "configuration",
        "title": "Configuration",
        "target_type": "reference"
      }
    ]
  },
  "target_documents": [
    {
      "type": "tutorial",
      "title": "Tutorial: Install and Setup",
      "sections": [
        {
          "id": "a3f9b2c1",
          "slug": "install-setup",
          "title": "Install and Setup",
          "source_sections": ["a3f9b2c1"]
        }
      ]
    },
    {
      "type": "reference",
      "title": "Reference: Configuration Options",
      "sections": [
        {
          "id": "b7e4d9f2",
          "slug": "config-options",
          "title": "Configuration Options",
          "source_sections": ["b7e4d9f2"]
        }
      ]
    }
  ]
}
```

**Note**: In 1:1 mappings, target section IDs match source section IDs.

### Complex Example (split mapping)

```json
{
  "original_document": {
    "name": "Complete Guide",
    "sections": [
      {
        "id": "c8a5f3d1",
        "slug": "getting-started",
        "title": "Getting Started",
        "target_type": "tutorial"
      }
    ]
  },
  "target_documents": [
    {
      "type": "tutorial",
      "title": "Tutorial: Basic Setup",
      "sections": [
        {
          "id": "1a2b3c4d",
          "slug": "basic-install",
          "title": "Basic Installation",
          "source_sections": ["c8a5f3d1"]
        },
        {
          "id": "5e6f7g8h",
          "slug": "first-project",
          "title": "Create First Project",
          "source_sections": ["c8a5f3d1"]
        }
      ]
    }
  ]
}
```

**Note**: In split mappings, same source ID appears in multiple target sections, but each target gets a new unique ID.

## Diataxis Framework Reference

**Full framework**: `~/projects/readme-payments-api-docs/_extras/style-guides/diataxis/README.md`

### Quick Reference

**Classification Axes**:
- **Acquisition vs. Application**: Learning the product vs. accomplishing work
- **Practice vs. Cognition**: Hands-on doing vs. thinking/understanding

**Four Documentation Types**:

| Type | Axes | Purpose | Tone |
|------|------|---------|------|
| **Tutorial** | Acquisition + Practice | Teach skills through guided practice | Supportive, teaching |
| **How-to Guide** | Application + Practice | Solve specific real-world problems | Direct, task-focused |
| **Reference** | Application + Cognition | Provide technical facts for lookup | Factual, neutral |
| **Explanation** | Acquisition + Cognition | Deepen conceptual understanding | Informative, contextual |

**Critical Rule**: Maintain strict separation. One type per document. Split mixed content and cross-link.

**Common Boundary Violations**:
- Tutorial with options/choices → Split alternatives into how-tos
- How-to with teaching/background → Move concepts to explanation
- Reference with narrative/story → Extract narrative to explanation
- Explanation with step-by-step → Move procedures to how-to

**For complete details** (type definitions, classification decision tree, content patterns, anti-patterns, language requirements, content migration rules):

Read: `~/projects/readme-payments-api-docs/_extras/style-guides/diataxis/README.md`

## Reference

- Framework source: `~/projects/readme-payments-api-docs/_extras/style-guides/diataxis/README.md`
- Schema directory: `_shared/schemas/diataxis-audit-mapping/`
  - JSON schema: `_shared/schemas/diataxis-audit-mapping/schema.json`
  - Schema documentation: `_shared/schemas/diataxis-audit-mapping/README.md`

## Sources

- https://diataxis.fr/tutorials/
- https://diataxis.fr/how-to-guides/
- https://diataxis.fr/reference/
- https://diataxis.fr/explanation/

## Notes

- This command is read-only for the source file (no changes to input)
- Output files are written to `docs/output/_process/diataxis-audit/`
- The audit identifies what content types exist and how they should be separated
- Follow the classification axes: Acquisition vs. Application, Practice vs. Cognition
- Maintain strict separation between documentation types
- The goal is to help improve documentation quality by applying Diataxis principles
- Split by user need, not by product components
- JSON mapping enables programmatic processing of restructuring recommendations
