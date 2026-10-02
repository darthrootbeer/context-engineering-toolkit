---
name: docs-workspace-setup
description: Create or reuse a documentation workspace for a Diataxis guide audit and improvement. Sets up the project directory, a copy of the knowledge files, CLAUDE.md, the directory tree, and an optional project note.
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
WORKSPACE_ROOT=~/projects
PIPELINE_DIR={YOUR_PIPELINE_DIR}
SHARED_CONFIG_DIR={SHARED_CONFIG_DIR}
NOTES_DIR={NOTES_DIR}
```

- `WORKSPACE_ROOT` is the folder where workspaces are created. Change it if you want them somewhere else.
- `PIPELINE_DIR` is the absolute path of the `docs-pipeline` folder that holds `_knowledge/` and `workspace-gitignore.template`. The install steps in `SETUP.md` fill it in for you.
- `SHARED_CONFIG_DIR` and `NOTES_DIR` are optional. `SHARED_CONFIG_DIR` can point at a folder of your own shared tools and agent instructions. `NOTES_DIR` can point at a notes folder (for example an Obsidian vault) where a project note is written. If a value is empty or still reads `{SHARED_CONFIG_DIR}` or `{NOTES_DIR}`, treat it as unset and skip every step that needs it.
- If `PIPELINE_DIR` still reads `{YOUR_PIPELINE_DIR}`, or `{PIPELINE_DIR}/_knowledge/` does not exist, stop: `"PIPELINE_DIR is not set. Set it to the docs-pipeline folder (see SETUP.md, Install)."`

---

## Step 1 — Parse arguments and derive paths

```
TICKET_ID = $ARGUMENTS[0]              # e.g., TICKET-1801
SLUG = $ARGUMENTS[1]                   # e.g., webhooks
TICKET_NUM = numeric portion of TICKET_ID  # e.g., 1801
PROJECT_NAME = "workspace_doc-{TICKET_NUM}_{SLUG}"
PROJECT_PATH = {WORKSPACE_ROOT}/{PROJECT_NAME}
```

Normalize: lowercase ticket prefix in folder name (`doc-` not `DOC-`), slug in kebab-case. No spaces anywhere in the folder name — use underscores as separators.

**Check if directory already exists:**
- If `PROJECT_PATH` exists:
  1. Print: `"Workspace found at {PROJECT_PATH}, reusing it."`
  2. Verify the directory tree exists (`docs/input/`, `docs/output/`, etc.). Create any missing subdirectories.
  3. Check if a source doc exists in `docs/input/`. If yes, print the filename. If no, print: `"No source doc in docs/input/ yet."`
  4. Check if an audit exists in `docs/output/_process/diataxis-audit/`. If yes, print: `"Audit already completed."` If no, print: `"No audit yet."`
  5. Skip to Step 10 (print summary) — do not recreate files, links, or project notes.

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
  - Copy the _knowledge/ folder from PIPELINE_DIR
  - Link SHARED_CONFIG_DIR as _shared (only if it is set)
  - Create CLAUDE.md, README.md, .gitignore
  - Create a project note (only if NOTES_DIR is set)

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

## Step 5 — Copy the knowledge files and link the optional shared folder

The skills read `./_knowledge/` relative to the workspace, so the workspace needs its own copy.

```bash
cp -R "{PIPELINE_DIR}/_knowledge" "{PROJECT_PATH}/_knowledge"
```

Skip if `{PROJECT_PATH}/_knowledge` already exists. Never overwrite it.

**Optional shared folder.** Only if `SHARED_CONFIG_DIR` is set and the folder exists:

```bash
ln -s "{SHARED_CONFIG_DIR}" "{PROJECT_PATH}/_shared"
```

Skip if `{PROJECT_PATH}/_shared` already exists. If `SHARED_CONFIG_DIR` is unset, skip this whole link and print: `"No shared config folder set, skipping _shared link."`

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

**Parallel sessions:** If you run two sessions on the same workspace, check what the other one has done first. Before starting any stage, run `git log --oneline | head -5` to check for commits from the other session. If a stage is already committed, skip it.

1. Place source doc in `docs/input/` → commit
2. Run `/docs-diataxis-audit docs/input/{source-filename}.md` → commit
3. Run `/docs-diataxis-split` to execute the split → commit
4. Run `/docs-style-check-structure docs/output/docs/` for structural style compliance → commit
5. Run `/docs-style-check-voice docs/output/docs/` for voice/tone/formatting → commit
6. Run `/docs-style-check-human docs/output/docs/` for AI pattern cleanup → commit
7. Run `/docs-readability-check docs/output/docs/` for reading level and dense sentences → commit
8. Run `/docs-grammar-spelling docs/output/docs/` for grammar, spelling, and terminology → commit
9. Run `/docs-visuals-review docs/output/docs/` for visual aid recommendations → commit
10. Run `/docs-links-review docs/output/docs/` for cross-link check → commit
11. Run `/docs-sme-review docs/output/docs/` for domain accuracy and reader journey → commit
12. Run `/docs-changes-list` to generate editorial record → commit
13. Run `/docs-decision-checkpoint` to resolve all recommendations → commit
14. Run `/docs-publish docs/output [target-path]` to create branch + PR

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

## Knowledge files

Copied into this workspace from the pipeline folder:

- Style guides: `_knowledge/style-guides/`
- Glossary: `_knowledge/glossary.yaml`
- Product knowledge base: `_knowledge/product-kb/`

If a shared config folder was set, it is linked as `_shared/`.
```

### README.md

Write `{PROJECT_PATH}/README.md`:

```markdown
# {PROJECT_NAME}

> Diataxis guide workspace for {TICKET_ID}.
```

### .gitignore

Copy `{PIPELINE_DIR}/workspace-gitignore.template` to `{PROJECT_PATH}/.gitignore`. Skip if `.gitignore` already exists.

### .git/info/exclude

Write `{PROJECT_PATH}/.git/info/exclude`:

```
# Optional shared config link
_shared
```

---

## Step 7 — Create the project note (optional)

Skip this whole step if `NOTES_DIR` is unset, and print: `"No notes folder set, skipping project note."`

Check if `{NOTES_DIR}/{PROJECT_NAME}.md` exists. If it does, skip.

If it doesn't, write:

```markdown
---
created: {today YYYY-MM-DD}
updated: {today YYYY-MM-DD}
ticket: {TICKET_ID}
---

# {PROJECT_NAME}

> Diataxis guide workspace for {TICKET_ID}.

## Links

- **README:** {PROJECT_PATH}/README.md
- **Ticket:** [{TICKET_ID}]({YOUR_TICKET_URL}/{TICKET_ID})

## Changelog

- {today YYYY-MM-DD}: Created via /docs-workspace-setup.
```

---

## Step 8 — Copy source doc (optional auto-fetch)

If `{YOUR_DOCS_REPO_PATH}` still reads as a placeholder (it starts with `{`), skip this step and print: `"No docs repo configured. Copy the source doc into docs/input/ manually."` Otherwise search `{YOUR_DOCS_REPO_PATH}` for a file matching the slug:

```bash
find {YOUR_DOCS_REPO_PATH} -name "{SLUG}.md" -type f
```

If found, copy it to `{PROJECT_PATH}/docs/input/`. If not found, print:
`"Source doc not found in {YOUR_DOCS_REPO_PATH}. Copy it manually into docs/input/."`

---

## Step 9 — Initial git commit

**Important:** Do not use `cd && git`. Use `git -C` with absolute paths. Each command is a separate tool call.

```bash
git -C "{PROJECT_PATH}" add CLAUDE.md README.md .gitignore _knowledge
```

```bash
git -C "{PROJECT_PATH}" commit -m "docs: scaffold guide workspace for {TICKET_ID}"
```

If the commit fails because git does not know who you are, stop and print: `"Set your git identity first: git config --global user.name and user.email. Then re-run."`

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

  Knowledge files:
    - _knowledge/      (copied from {PIPELINE_DIR})

  Links:
    - _shared/         → {SHARED_CONFIG_DIR} (only if set)

  Directories:
    - docs/input/
    - docs/output/_process/diataxis-audit/
    - docs/output/_process/link-check/
    - docs/output/_process/style-audit/
    - docs/output/_process/visual-audit/diagrams/
    - docs/output/docs/

  Project note: {NOTES_DIR}/{PROJECT_NAME}.md (only if NOTES_DIR is set)

Next step: copy the source doc into docs/input/ and run `/docs-pipeline` or `/docs-diataxis-audit`.
```

---

## Notes

- All operations are idempotent — safe to re-run
- Never overwrite existing files
- **Bash safety:** Never use `cd &&` or compound commands. Use absolute paths and `git -C`. One command per Bash tool call.
