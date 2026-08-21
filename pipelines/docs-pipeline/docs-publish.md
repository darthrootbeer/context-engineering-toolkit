---
name: docs-publish
description: Publish finished Diataxis output docs from a workspace project into {YOUR_DOCS_REPO} — copies files, adds docs platform frontmatter, creates _order.yaml, archives process artifacts, then creates a branch and opens a PR.
argument-hint: [source-dir] [target-path]
allowed-tools: [Read, Write, Edit, Glob, Bash]
---

# docs-publish

Copy finished Diataxis output docs into `{YOUR_DOCS_REPO}`, add docs platform frontmatter, create the folder structure and `_order.yaml`, archive process artifacts, then branch + commit + PR.

All pages are published `hidden: true`. Confirmations at each step before anything is written or pushed.

## Arguments

The user provided: $ARGUMENTS

- `$ARGUMENTS[0]` — Source directory containing the workspace output (e.g., `docs/output`)
- `$ARGUMENTS[1]` — Target path inside `{YOUR_DOCS_REPO}` (e.g., `docs/YOUR-SECTION/your-guide`). Category folder names should be Title Case (e.g., `Backend-to-Backend`, not `BACKEND-TO-BACKEND`).

**Required:** Both arguments are mandatory. If either is missing, stop:
`"Please provide both paths: /docs-publish [source-dir] [target-path]"`

## Constants

```
DOCS_REPO=~/projects/{YOUR_DOCS_REPO}
```

---

## Steps

### 1. Validate input and confirm identifiers

**Parse arguments:**
- `SOURCE_DIR = $ARGUMENTS[0]` (strip trailing slash)
- `TARGET_PATH = $ARGUMENTS[1]` (path relative to `DOCS_REPO`, strip leading/trailing slashes)
- `DOCS_BASE = {SOURCE_DIR}/docs` — base docs directory
- `PROCESS_DIR = {SOURCE_DIR}/_process` — where process artifacts live

**Find output docs (handles both flat and subfolder structures):**

The split skill outputs docs to a subfolder (`docs/output/docs/{area}/`), but older splits may have flat files in `docs/output/docs/`. Check both patterns:

1. Glob `{DOCS_BASE}/*.md` — if `.md` files found directly, set `DOCS_DIR = {DOCS_BASE}` (flat structure)
2. If no `.md` files found directly, look one level deeper: find the single subfolder in `{DOCS_BASE}` that contains `.md` files. Set `DOCS_DIR = {DOCS_BASE}/{subfolder}`.
3. If multiple subfolders contain `.md` files, stop: `"Multiple doc subfolders found in {DOCS_BASE}/. Pass the specific subfolder as the source directory."`
4. If zero `.md` files found at either level: stop — `"No output docs found in {DOCS_BASE}. Run the split first."`

**Validate filenames (hard gate — runs before anything else):**

For each `.md` in `DOCS_DIR`, check the filename stem against these rules:

| Check | Rule | Example fail |
|---|---|---|
| Lowercase + dashes only | No uppercase, underscores, or spaces | `BenefitsPay-Payments`, `wic_payments` |
| Area prefix present | At least one segment before the first dash | `payments.md` |
| Length | 2–4 dash-separated segments total | `benefitspay-a.md`, `benefitspay-payment-api-endpoint-list.md` |
| No gerunds | No segment ending in `-ing` | `benefitspay-understanding-payments.md` |
| No bare type words | Stem is not solely `{area}-introduction` or `{area}-explanation` | `benefitspay-introduction.md` |

If any file fails, stop and list all offenders:
```
❌ Filename convention failed — fix before publishing:

  benefitspay-understanding-payments.md  → gerund ("understanding") in descriptor
  benefitspay-introduction.md            → bare type word as descriptor

Rename and re-run.
```

Do not proceed until all filenames pass.

**Infer guide slug:**
- For each filename stem in `DOCS_DIR`, strip known Diataxis prefixes: `explanation-`, `how-to-`, `reference-`, `tutorial-`, `overview-`, `introduction-`
- Preferred source: the how-to doc (strip `how-to-` → e.g., `configure-webhooks`)
- Fallback: extract from workspace folder name — pattern `workspace - doc-NNNN - SLUG` or `workspace - DOC-NNNN - SLUG` → use `SLUG` portion
- Fallback 2: most common word fragment across all stripped stems

**Check for existing guide at same slug:**
```bash
ls {DOCS_REPO}/{TARGET_PATH}/{SLUG}.md 2>/dev/null
```
If a file with that name exists → set `REPLACE_EXISTING=true`. The old file will be deleted in the same commit so the new folder takes over the slug. Set `FOLDER_NAME={SLUG}`.
Otherwise → `REPLACE_EXISTING=false`, `FOLDER_NAME={SLUG}`.

The folder name always matches the original slug. This preserves URL continuity — anyone with the old URL finds the new guide in its place. Tested and confirmed that ReadMe handles file-to-folder slug handoff in a single push.

**Infer ticket ID:**
Extract from the workspace folder name. Pattern: `workspace - doc-NNNN -` or `workspace - DOC-NNNN -` → `DOC-NNNN` (uppercase).
If no match: prompt — `"Could not infer ticket ID from workspace folder name. Enter ticket ID (e.g., TICKET-1801):"`.

**Confirm with user:**

```
Inferred:
  Guide slug:    {SLUG}
  Folder name:   {FOLDER_NAME}
  Ticket:        {TICKET_ID}
  Target:        {DOCS_REPO}/{TARGET_PATH}/{FOLDER_NAME}/

{If REPLACE_EXISTING: ⚠️  "{SLUG}.md" exists and will be deleted in this commit. The new folder takes over the same URL.}

Correct? (y/n/edit)
```

If `n`: prompt for corrected slug and ticket ID.
If `edit`: prompt for each value 1:1.
Continue when confirmed.

---

### 2. Frontmatter staging

For each doc in `DOCS_DIR` (and the new `index.md`), propose ReadMe frontmatter.

**For each output doc:**
- Read the file
- Extract H1 title (first `# ` heading)
- Extract first non-blank paragraph after the H1 (the intro)
- Generate frontmatter:

**Read `diataxis_type` from the file's existing frontmatter** (set by the split). If the field is present, use it as-is. If it's absent, fall back to inferring from the filename prefix (for older docs produced before this convention):
- `overview-*` → `overview`
- `introduction-*` → `overview` (legacy alias)
- `explanation-*` → `explanation`
- `how-to-*` → `how-to`
- `reference-*` → `reference`
- `tutorial-*` → `tutorial`
- Neither present nor inferrable → omit the field and warn: `"Could not read diataxis_type for {filename} — add manually."`

```yaml
---
title: {H1 title}
excerpt: {first sentence of intro paragraph — truncate at first period, ≤120 chars}
deprecated: false
hidden: true
diataxis_type: {inferred type}
metadata:
  title: {H1 title}
  description: {first 155 chars of intro paragraph, ending at word boundary}
  image: {YOUR_DEFAULT_OG_IMAGE_URL}
  robots: index
next:
  description: ''
---
```

**For the new `index.md` (nav page for the folder):**
- Title: humanize `FOLDER_NAME` → title-case, replace hyphens with spaces (e.g., `configure-webhooks-guide` → "Configure Webhooks Guide")
- Frontmatter:

```yaml
---
title: {humanized title}
excerpt: ''
deprecated: false
hidden: true
metadata:
  title: {humanized title}
  description: ''
  robots: noindex
next:
  description: ''
---
```

**Show staging check:**

```
Frontmatter check — confirm each file:

📄 index.md (overview merged from {overview-filename} if present, otherwise bare nav page)
   title: {title}
   excerpt: {excerpt from overview, or "(none)"}
   diataxis_type: overview (if overview doc found)
   robots: noindex
   hidden: true

📄 {filename}.md
   Drawn from: "{first 80 chars of H1 + intro}"
   title: {title}
   excerpt: {excerpt}
   robots: index
   hidden: true

[...repeat for each doc...]

All hidden: true. Approve and continue? (y/n/edit)
```

If `n` or `edit`: prompt for per-file edits. Loop until approved.

---

### 3. Copy docs into folder structure

**Create folder:**
```bash
mkdir -p {DOCS_REPO}/{TARGET_PATH}/{FOLDER_NAME}
```

**Write each output doc:**
For each `.md` in `DOCS_DIR`:
- If the file already has frontmatter with `title:`, strip the first body `# H1` heading (ReadMe renders the frontmatter title as the page H1; keeping both triggers MD025)
- Prepend the approved frontmatter YAML block to the file content (or keep existing frontmatter if already present)
- **Convert internal `.md` links to ReadMe slugs:** Find all markdown links matching `](./somefilename.md)` or `](somefilename.md)` and strip the `.md` extension and `./` prefix, producing `](doc:somefilename)`. This converts workspace-local links into ReadMe's `doc:slug` syntax. Only convert links to files that exist in `DOCS_DIR`; leave external URLs and anchors untouched.
- Write to `{DOCS_REPO}/{TARGET_PATH}/{FOLDER_NAME}/{original-filename}.md}`

If the file already exists in the target, stop:
`"File already exists: {path}. Delete it first or choose a different folder name."`

**Write `index.md`:**
- Check if any output doc has `diataxis_type: overview` in its frontmatter
- **If an overview doc exists:** merge it into `index.md` — use the `index.md` frontmatter structure (title from humanized folder name) but carry over the overview's `excerpt`, `description`, `keywords`, `diataxis_type: overview`, and `image` fields. Strip the overview doc's body H1 (ReadMe renders the frontmatter title as H1), then paste the remaining body content below the frontmatter. Do NOT copy the overview doc as a separate file — it lives only in `index.md`.
- **If no overview doc exists:** write `index.md` with frontmatter only, no body (the previous default behavior).

**Lint gate — run before proceeding:**
```bash
npx markdownlint-cli {DOCS_REPO}/{TARGET_PATH}/{FOLDER_NAME}/*.md
```

If errors are found, fix them before continuing:
- **MD025 (multiple H1):** The H1 strip above should prevent this. If it persists, check for a leftover `# ` line.
- **MD001 (heading increment):** Fix heading levels so they increment by one (e.g., `##` → `###`, not `##` → `####`).
- **MD040 (code fence language):** Add a language tag to bare code fences. Use `text` for plain output, `json` for JSON, etc.
- **MD051 (link fragment):** Fix broken anchor links. Markdown anchors strip `/` chars entirely (e.g., `/api/benefitspay/categories/` → `apiwiccategories`).

Show the lint results. If clean, continue. If errors remain after auto-fix, stop and list them.

---

### 4. `_order.yaml` and process artifacts

**Write inner `_order.yaml` (inside the new folder):**

Order docs by Diataxis type. Read `diataxis_type` from each file's frontmatter and sort by type. If frontmatter is absent, fall back to filename prefix for legacy docs.

**Exclude the overview doc** — its content is now embedded in `index.md`, so it does not get its own entry in `_order.yaml`.

Sort order:
1. `explanation`
3. `how-to`
4. `reference`
5. `tutorial`

Write `{DOCS_REPO}/{TARGET_PATH}/{FOLDER_NAME}/_order.yaml`:
```yaml
- {filename-stem-1}
- {filename-stem-2}
- {filename-stem-3}
```

(Stems only — no `.md` extension, no leading path.)

**Update parent `_order.yaml`:**
```bash
cat {DOCS_REPO}/{TARGET_PATH}/_order.yaml
```
Append `{FOLDER_NAME}` at the end of the list.

Write the updated file.

**Copy process artifacts:**
```bash
cp -r {PROCESS_DIR} {DOCS_REPO}/_extras/process/{SLUG}_{TICKET_ID}/
```

If `_extras/process/{SLUG}_{TICKET_ID}/` already exists: stop and confirm — `"Process artifacts already exist at _extras/process/{SLUG}_{TICKET_ID}/. Overwrite? (y/n)"`. Continue only on `y`.

---

### 5. Branch, commit, and PR

**Check for clean working tree:**
```bash
git -C {DOCS_REPO} status --porcelain
```

If there are uncommitted changes, warn:
```
⚠️  {DOCS_REPO} has uncommitted changes:
{git status output}

These will NOT be included in the commit (only the new docs are staged), but branching from a dirty tree may not be what you want. Continue? (y/n)
```

Continue only on `y`.

**Read API version:**
```bash
# Read your docs platform's API version identifier. Adjust this path for your repo structure.
grep "version:" {DOCS_REPO}/reference/.oas.yml | head -1 | sed "s/.*'\(.*\)'.*/\1/"
# → e.g., 2025-08-04
```

**Branch name:**
```
{YOUR_USERNAME}/doc-{TICKET_NUMBER}-{SLUG}-guide-split-v{API_VERSION}
```
Where `TICKET_NUMBER` is the numeric portion of `TICKET_ID` (e.g., `TICKET-1801` → `1801`), and `SLUG` is the guide slug (not the folder name — use slug, not slug-guide).

**Create branch:**
```bash
git -C {DOCS_REPO} checkout -b {YOUR_USERNAME}/doc-{TICKET_NUMBER}-{SLUG}-guide-split-v{API_VERSION}
```
Abort if branch already exists — `"Branch already exists. Delete it first with: git branch -D {branch-name}"`.

**Delete old guide (if replacing):**
```bash
# Only if REPLACE_EXISTING=true
git -C {DOCS_REPO} rm {TARGET_PATH}/{SLUG}.md
```

**Stage files** (two separate Bash calls):
```bash
git -C {DOCS_REPO} add {TARGET_PATH}/{FOLDER_NAME}/ _extras/process/{SLUG}_{TICKET_ID}/
```
```bash
git -C {DOCS_REPO} add {TARGET_PATH}/_order.yaml
```

**Commit:**
```bash
# If REPLACE_EXISTING=true:
git -C {DOCS_REPO} commit -m "publish {SLUG} v1.1 guide set, retire monolithic guide"
# If REPLACE_EXISTING=false:
git -C {DOCS_REPO} commit -m "docs({SLUG}): add Diataxis split — explanation, how-to, reference + nav page (hidden)"
```

**Draft the PR:**

Fill the `guide-audit.md` PR template. The template lives at `.github/PULL_REQUEST_TEMPLATE/guide-audit.md` and has: Context, Output documents, What to review, Review notes.

Generate content:

```
## Context

{If REPLACE_EXISTING: Publishes the v1.1 {humanized-slug} guide (Diataxis split) and retires the original monolithic guide. Merging this PR replaces the existing `{SLUG}` page with a multi-page guide set at the same URL. No URL breakage; tested on staging.}
{If not REPLACE_EXISTING: Diataxis audit and split of the {humanized-slug} guide. These {N} new docs are published hidden, pending stakeholder review.}

[{TICKET_ID}]({YOUR_TICKET_URL}/{TICKET_ID})

## Output documents

| Document | Type | Description |
|----------|------|-------------|
| `index.md` | Overview | Guide landing page with overview content embedded |
| `{each-doc}.md` | {type} | {One line: what this doc contains} |

Types: **Explanation** (concepts, how things work) · **How-to** (step-by-step procedures) · **Reference** (specs, tables, lookups)

## What to review

Your job is **content accuracy** — verify that the technical content in each doc is correct. Specifically:

- Are the facts, flows, and code samples accurate?
- Is anything missing that was in the original guide?
- Is anything misleading in its new context?

The structural decisions (which content lives in which file) are already made. You don't need to evaluate those unless something feels genuinely wrong.

**Start here:** `_extras/process/{SLUG}_{TICKET_ID}/editorial-changes.md` — it lists every content move, style change, and visual aid with a "why" for each.

## Review notes

{Free text — e.g., original guide left untouched, all pages hidden, temp folder name, known open questions. Omit section if nothing to add.}
```

**Show draft and confirm:**

```
PR draft:
---
{full draft PR body}
---

Push branch and open PR? (y/n/edit)
```

If `n`: stop — `"Stopped before push. Branch is committed locally at {branch-name}."`
If `edit`: show each section for inline edit. Loop until confirmed.

**Push and open PR** (separate Bash calls):
```bash
git -C {DOCS_REPO} push -u origin {YOUR_USERNAME}/doc-{TICKET_NUMBER}-{SLUG}-guide-split-v{API_VERSION}
```

Write the confirmed PR body to a temp file using the Write tool (`/tmp/pr-body.md`), then create the PR:
```bash
gh pr create --repo {YOUR_ORG}/{YOUR_DOCS_REPO} --title "docs({SLUG}): Diataxis guide split (hidden)" --body-file /tmp/pr-body.md --template guide-audit.md --draft
```

**Post ticket comment (optional):**
If your team tracks work in a ticket system, post a comment on `{TICKET_ID}` with:
- Branch name
- Target folder path
- PR link
- Note that all pages are hidden

---

### 6. Display summary

```
Done.

  Branch:   {YOUR_USERNAME}/doc-{TICKET_NUMBER}-{SLUG}-guide-split-v{API_VERSION}
  PR:       {PR_URL}
  Folder:   {DOCS_REPO}/{TARGET_PATH}/{FOLDER_NAME}/
  Files:    {N} docs + index.md + _order.yaml

  Process artifacts → _extras/process/{SLUG}_{TICKET_ID}/

{If REPLACE_EXISTING: ⚠️  Old "{SLUG}.md" deleted — folder takes over the same URL slug. Guide goes live on merge.}

  Ticket:   {TICKET_ID} (update manually if needed)
```

---

## Error Handling

| Situation | Behavior |
|-----------|----------|
| Missing required argument | Stop, show usage |
| `DOCS_DIR` not found or empty | Stop: "No output docs found in {DOCS_DIR}. Run the split first." |
| Target file already exists | Stop: "File already exists: {path}. Delete it first." |
| Branch already exists | Stop: "Branch already exists — delete it first." |
| Version config file not found | Stop: "Cannot read API version. Check that your version config file exists in {YOUR_DOCS_REPO}." |
| `_extras/process/{SLUG}_{TICKET_ID}/` exists | Confirm overwrite before proceeding |
| `git push` fails | Stop: show error, suggest checking remote/auth |
| `gh pr create` fails | Stop: show error — branch and commit are local; user can push manually |
| Ticket comment fails | Warn, continue — PR is open, Linear update is non-blocking |

---

## Notes

- **All docs are published `hidden: true`** unless `REPLACE_EXISTING=true`, in which case they're published `hidden: false` (the guide goes live on merge).
- **Process artifacts go to `_extras/process/`** — this directory is outside `docs/` and never synced to ReadMe. Hard guarantee.
- **URL continuity:** When replacing an existing guide, the new folder uses the same name as the old file's slug. The old file is deleted and the folder takes over the slug in the same commit. ReadMe handles this file-to-folder swap cleanly in a single push (tested 2026-03-16).
- **`index.md` is a new file** — not copied directly from workspace output. If the workspace contains an overview doc (`diataxis_type: overview`), its body is merged into `index.md` so the guide landing page renders the overview content. The overview doc is not published as a separate child page.
- **`_order.yaml` inside the folder** follows Diataxis reading order: Explanation → How-to → Reference → Tutorial. The overview doc is excluded (it lives in `index.md`).
- **PR is opened as a draft.** Stakeholder review happens before marking ready.
- **Branch naming** uses the API version from `reference/.oas.yml`, not today's date.
- **Trigger:** after the split, style pass, visual aids, editorial-changes, and link-check are done — and stakeholder review is pending.
