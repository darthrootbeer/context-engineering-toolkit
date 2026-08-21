---
name: docs-workspace-setup
description: Create or reuse a documentation workspace for a Diataxis guide audit and improvement. Sets up the project directory, TOOLBOX symlinks, CLAUDE.md, directory tree, and Obsidian note.
argument-hint: <ticket-id> <slug>
---

# docs-workspace-setup

Create or reuse a documentation workspace for auditing and improving a guide using the Diataxis framework. If the workspace already exists, validates it and reuses it.

## Arguments

The user provided: $ARGUMENTS

- `$ARGUMENTS[0]` — Ticket ID (e.g., `TICKET-1801`)
- `$ARGUMENTS[1]` — Guide slug (e.g., `webhooks`, `backend-integration`)

**Required:** Both arguments are mandatory. If either is missing, stop:
`"Usage: /docs-workspace-setup TICKET-1801 webhooks"`

## Constants

```
TOOLBOX=~/projects/TOOLBOX
VAULT={YOUR_VAULT_PATH}
```

---

## Step 1 — Parse arguments and derive paths

```
TICKET_ID = $ARGUMENTS[0]              # e.g., TICKET-1801
SLUG = $ARGUMENTS[1]                   # e.g., webhooks
TICKET_NUM = numeric portion of TICKET_ID  # e.g., 1801
PROJECT_NAME = "workspace_doc-{TICKET_NUM}_{SLUG}"
PROJECT_PATH = ~/projects/{PROJECT_NAME}
```

Normalize: lowercase ticket prefix in folder name (`doc-` not `DOC-`), slug in kebab-case. No spaces anywhere in the folder name — use underscores as separators.

**Check if directory already exists:**
- If `PROJECT_PATH` exists:
  1. Print: `"Workspace found at {PROJECT_PATH}, reusing it."`
  2. Verify the directory tree exists (`docs/input/`, `docs/output/`, etc.). Create any missing subdirectories.
  3. Check if a source doc exists in `docs/input/`. If yes, print the filename. If no, print: `"No source doc in docs/input/ yet."`
  4. Check if an audit exists in `docs/output/_process/diataxis-audit/`. If yes, print: `"Audit already completed."` If no, print: `"No audit yet."`
  5. Skip to Step 10 (print summary) — do not recreate files, symlinks, or Obsidian notes.

---

## Step 2 — Confirm before doing anything

Print:

```
Create guide workspace:
  Name:    {PROJECT_NAME}
  Path:    {PROJECT_PATH}
  Ticket:  {TICKET_ID}
  Slug:    {SLUG}

This will:
  - Create project directory with docs tree
  - git init
  - Add 5 TOOLBOX symlinks
  - Create CLAUDE.md, README.md, .gitignore
  - Create Obsidian project note

Proceed? (y/n)
```

Stop if the user says no.

---

## Step 3 — Create directory and git init

```bash
mkdir -p "{PROJECT_PATH}"
git init "{PROJECT_PATH}"
```

---

## Step 4 — Create directory tree

```bash
mkdir -p "{PROJECT_PATH}/docs/input"
mkdir -p "{PROJECT_PATH}/docs/output/_process/diataxis-audit"
mkdir -p "{PROJECT_PATH}/docs/output/_process/link-check"
mkdir -p "{PROJECT_PATH}/docs/output/_process/style-audit"
mkdir -p "{PROJECT_PATH}/docs/output/_process/visual-audit/diagrams"
mkdir -p "{PROJECT_PATH}/docs/output/docs"
```

---

## Step 5 — Create TOOLBOX symlinks (5 symlinks)

For each symlink, skip if it already exists.

| In project | Points to |
|---|---|
| `AGENTS.md` | `{TOOLBOX}/AGENTS.md` |
| `_shared/` | `{TOOLBOX}/_shared` |
| `.cursor/rules/` | `{TOOLBOX}/.cursor/rules` |
| `.cursor/commands/` | `{TOOLBOX}/.cursor/commands` |
| `.cursor/plans/` | `{TOOLBOX}/.cursor/plans` |

Create `.cursor/` directory first: `mkdir -p "{PROJECT_PATH}/.cursor"`

---

## Step 6 — Create files

### CLAUDE.md

Write `{PROJECT_PATH}/CLAUDE.md`:

```markdown
# Guide Workspace — {TICKET_ID}: {SLUG}

Documentation workspace for auditing and restructuring the {SLUG} guide using the Diataxis framework.

## Ticket

[{TICKET_ID}]({YOUR_TICKET_URL}/{TICKET_ID})

## Workflow

**Commit after every step.** Each step produces trackable output; commit it so diffs are reviewable.

**Parallel sessions:** Ben often runs two Claude terminals on the same workspace. Before starting any stage, run `git log --oneline | head -5` to check for commits from the other session. If a stage is already committed, skip it.

1. Place source doc in `docs/input/` → commit
2. Run `/docs-diataxis-audit docs/input/{source-filename}.md` → commit
3. Run `/docs-diataxis-split` to execute the split → commit
4. Run `/docs-style-check-structure docs/output/docs/` for structural style compliance → commit
5. Run `/docs-style-check-voice docs/output/docs/` for voice/tone/formatting → commit
6. Run `/docs-style-check-human docs/output/docs/` for AI pattern cleanup → commit
7. Run `/docs-grammar-spelling docs/output/docs/` for grammar, spelling, and terminology → commit
8. Run `/docs-visuals-review docs/output/docs/` for visual aid recommendations → commit
9. Run `/docs-links-review docs/output/docs/` for cross-link check → commit
10. Run `/docs-sme-review docs/output/docs/` for domain accuracy and reader journey → commit
11. Run `/docs-changes-list` to generate editorial record → commit
12. Run `/docs-decision-checkpoint` to resolve all recommendations → commit
13. Run `/docs-publish docs/output [target-path]` to create branch + PR

## Structure

```text
docs/
  input/                              # Source doc(s) to audit
  output/
    _process/
      diataxis-audit/                 # Audit report, JSON mapping, PDF
      link-check/                     # Cross-link audit results
      style-audit/                    # Style pass audit reports
      visual-audit/diagrams/          # Mermaid diagrams
    docs/                             # Final split output docs
```

## Shared Resources

Access via `_shared/` symlink (points to `TOOLBOX/_shared/`):

- Style guides: `_knowledge/style-guides/`
- Glossary: `_knowledge/glossary.yaml`
- Tools: `_shared/tools/`
- Audit log: `_shared/log/audit.log`
```

### README.md

Write `{PROJECT_PATH}/README.md`:

```markdown
# {PROJECT_NAME}

> Diataxis guide workspace for {TICKET_ID}.
```

### .gitignore

Copy from `{TOOLBOX}/_shared/templates/.gitignore`.

### .git/info/exclude

Write `{PROJECT_PATH}/.git/info/exclude`:

```
# TOOLBOX symlinks
.cursor/
_shared
AGENTS.md
```

---

## Step 7 — Create Obsidian project note

Check if `{VAULT}/projects/{PROJECT_NAME}.md` exists. If it does, skip.

If it doesn't, write:

```markdown
---
tags:
  - project
  - active
created: {today YYYY-MM-DD}
updated: {today YYYY-MM-DD}
github: ""
readme: "{PROJECT_PATH}/README.md"
related: []
proj-ids: []
ticket: {TICKET_ID}
---

# {PROJECT_NAME}

> Diataxis guide workspace for {TICKET_ID}.

## Links

- **README:** `= this.readme`
- **Ticket:** [{TICKET_ID}]({YOUR_TICKET_URL}/{TICKET_ID})
- **Related:** `= this.related`

## Changelog

- {today YYYY-MM-DD} — Created via /docs-workspace-setup.

---

#### Board Tasks

```dataviewjs
const ids = dv.current().file.frontmatter["proj-ids"] || [];
if (!ids.length) { dv.paragraph("*No linked tasks.*"); return; }

const board = await dv.io.load("_tracking/project-board.md");
const lines = board.split("\n");
const open = [], done = [];

for (const id of ids) {
    const line = lines.find(l => l.includes(`] ${id}:`));
    if (!line) continue;
    const isDone = /^\s*- \[x\]/i.test(line);
    const title = line
        .replace(/^\s*-\s*\[.\]\s*/, "")
        .replace(/\s*→\s*\[\[.*?\]\].*$/, "")
        .trim();
    (isDone ? done : open).push(`${id} — ${title}`);
}

if (open.length) { dv.paragraph("**Open**"); dv.list(open); }
if (done.length) { dv.paragraph("**Closed**"); dv.list(done.map(t => `~~${t}~~`)); }
if (!open.length && !done.length) { dv.paragraph("*No tasks found for: " + ids.join(", ") + "*"); }
` `` `
```

---

## Step 8 — Copy source doc (optional auto-fetch)

Search `{YOUR_DOCS_REPO_PATH}` for a file matching the slug:

```bash
find {YOUR_DOCS_REPO_PATH} -name "{SLUG}.md" -type f
```

If found, copy it to `{PROJECT_PATH}/docs/input/`. If not found, print:
`"Source doc not found in {YOUR_DOCS_REPO_PATH}. Copy it manually into docs/input/."`

---

## Step 9 — Initial git commit

**Important:** Do not use `cd && git`. Use `git -C` with absolute paths. Each command is a separate tool call.

```bash
git -C "{PROJECT_PATH}" add CLAUDE.md README.md .gitignore
```

```bash
git -C "{PROJECT_PATH}" commit -m "docs: scaffold guide workspace for {TICKET_ID}"
```

---

## Step 10 — Print summary

```
Done.

  {PROJECT_PATH}/

  Files:
    - CLAUDE.md
    - README.md
    - .gitignore
    - .git/info/exclude

  Symlinks:
    - AGENTS.md        → TOOLBOX
    - _shared/         → TOOLBOX
    - .cursor/rules/   → TOOLBOX
    - .cursor/commands/ → TOOLBOX
    - .cursor/plans/   → TOOLBOX

  Directories:
    - docs/input/
    - docs/output/_process/diataxis-audit/
    - docs/output/_process/link-check/
    - docs/output/_process/style-audit/
    - docs/output/_process/visual-audit/diagrams/
    - docs/output/docs/

  Obsidian: {VAULT}/projects/{PROJECT_NAME}.md

Next step: copy the source doc into docs/input/ and run `/docs-pipeline` or `/docs-diataxis-audit`.
```

---

## Notes

- All operations are idempotent — safe to re-run
- TOOLBOX path: `~/projects/TOOLBOX`
- Obsidian vault: set `VAULT` constant at the top to your vault path
- Never overwrite existing files
- No MISTAKES_TO_AVOID.md symlink (retired)
- **Bash safety:** Never use `cd &&` or compound commands. Use absolute paths and `git -C`. One command per Bash tool call.
