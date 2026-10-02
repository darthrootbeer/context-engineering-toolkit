---
name: docs-work-verify
description: Verify that documentation work has been successfully merged and is live. Use when user asks to verify PR status, check if changes are live, or validate documentation deployment.
allowed-tools: [Bash, Read, Write]
model: haiku
---

# docs-work-verify

Verify that work has been successfully merged and is live. Checks GitHub PR status, commits, and live documentation.

## Usage

```
/docs-work-verify [PR_NUMBER or BRANCH_NAME]
```

- If no argument provided, uses current branch
- Accepts PR number (e.g., `77`) or branch name

## Arguments

The user invoked this command with: $ARGUMENTS

## Steps

**IMPORTANT**: Use the authenticated GitHub CLI (`gh`) for all GitHub operations. Ensure `gh auth login` has been run for your org before using this skill.

### 1. Get PR number

- If PR number provided: use it directly → `PR_NUMBER`
- If branch name provided: `gh pr list --head [BRANCH] --json number --jq '.[0].number'` → `PR_NUMBER`
- If neither: `git branch --show-current` → `BRANCH`, then find PR
- If no PR found: stop with "No PR found for this branch"

### 2. Get PR information (single call)

```bash
gh pr view [PR_NUMBER] --json state,mergedAt,title,url,baseRefName,headRefName,mergeCommit,number,body
```

Extract: `STATE`, `MERGED_AT`, `TITLE`, `URL`, `BASE_BRANCH`, `HEAD_BRANCH`, `MERGE_COMMIT`, `PR_NUMBER`, `BODY`

Also scan `BODY`, `TITLE`, and `HEAD_BRANCH` for a ticket pattern `[A-Z]+-\d+` (case-insensitive) → `LINEAR_TICKET_ID` (e.g. `TICKET-1172`). Used in step 9.

Detect whether this is a **formatting-only PR**: if `BODY` contains phrases like "formatting-only", "no functional changes", "no content changes", or "markdownlint fixes" → set `FORMATTING_ONLY=true`.

### 3. Verify PR is merged

- If `STATE` != "MERGED": inform user but continue verification
- Get merge commit from PR JSON → `MERGE_COMMIT`

### 4. Verify commit in base branch

```bash
git -C {YOUR_DOCS_REPO_PATH} fetch origin [BASE_BRANCH]
git -C {YOUR_DOCS_REPO_PATH} branch -r --contains [MERGE_COMMIT] | grep origin/[BASE_BRANCH]
```

✅ if match found; ⚠️ if not.

### 5. Get changed files and map to documentation URLs

Get files from PR:
```bash
gh pr view [PR_NUMBER] --json files --jq '.files[].path'
```

Map each file to a `.md` endpoint URL:
- `docs/PATH/file.md` → `https://{YOUR_DOCS_SITE}/docs/[slug].md`
- `reference/PATH/file.md` → `https://{YOUR_DOCS_SITE}/reference/[slug].md`

Slug rules:
- Use the filename without `.md`, lowercase, spaces/underscores → dashes
- **Exception:** if filename is `index.md`, use the parent directory name as the slug

### 6. Verify live documentation

For each URL:
```bash
curl -sL "https://{YOUR_DOCS_SITE}/docs/[slug].md"
```

These return clean markdown — grep directly for headings, phrases, and absence of lint artifacts.

**Availability check:**
```bash
curl -s -o /dev/null -w "%{http_code}" -L "https://{YOUR_DOCS_SITE}/docs/[slug].md"
```

- 200 → ✅ Page accessible
- 404 with `hidden: true` in source → ℹ️ Hidden page, expected
- Other → ⚠️ Page returned status [HTTP_CODE]

**Fallback (if `.md` endpoint 404s unexpectedly):**

Check the file is present in the remote branch via the GitHub API:
```bash
gh api repos/{YOUR_ORG}/{YOUR_DOCS_REPO}/contents/[FILE_PATH]?ref=[BASE_BRANCH] --jq '.content' | base64 -d | grep -i "[PHRASE]"
```

- If found → ℹ️ File is in the merged remote branch but not yet live at the docs endpoint (possible propagation delay or hidden page)
- If not found → ⚠️ File not found in remote `[BASE_BRANCH]` — merge may not have landed

Do not grep local files — the goal is verifying live/remote state, not what's on disk.

### 7. Get specific change details

Extract field names or key phrases from PR body/commits and verify:
```bash
curl -sL "https://{YOUR_DOCS_SITE}/docs/[slug].md" | grep -i "[FIELD_NAME]"
```

### 8. Generate verification report

Write directly to `_extras/verification/[PR_NUMBER]-[DATE].md`:

```markdown
# Work Verification Report

**PR #[PR_NUMBER] Status:**
- **State**: [STATE]
- **Merged at**: [MERGED_AT]
- **Title**: [TITLE]
- **URL**: [URL]

**GitHub Verification:**
- ✅ Commit `[MERGE_COMMIT_SHORT]` is in the `[BASE_BRANCH]` branch

**Live Documentation Verification:**
[one bullet per file: ✅/ℹ️/⚠️ path → URL (HTTP status)]

**Summary:**
[1-2 sentences: what was verified, result]
```

### 9. Display summary

Show:
- PR number, state, merge status
- Documentation URLs checked
- Verification results (green checkmarks)

**Manual verification checklist:**

If `FORMATTING_ONLY=true`: skip per-change checklist. Instead output one generic check:

📝 Verify it yourself:

1. Open [Page Title](https://{YOUR_DOCS_SITE}/docs/[slug])
2. Confirm the page loads and renders cleanly (no raw lint markers or broken headings)
3. This proves the formatting fixes are live.

If `FORMATTING_ONLY=false`: write one group of 3 lines per major content change. Output as plain markdown (no code block) so links are clickable.

Format:
```
1. Open [Page Title](https://full-url)
2. Search for "[exact phrase from live page — 4–8 words, copy-paste ready]"
3. This proves [one sentence: what finding that phrase confirms about the change].
```

For deletions: step 2 says `Search for "[old phrase]"`, step 3 says `This proves we removed [X] — the phrase should NOT appear.`

Then show "Files changed:" list.

### 10. Linear actions

If `LINEAR_TICKET_ID` was found and PR is merged, output both blocks below as plain markdown (no code block around your output). The fence here only keeps the template links from rendering as links in this file:

```text
─────────────────────────────────────────────────────
💬 Want to add a comment to [TICKET-XXXX]({YOUR_ISSUE_TRACKER}/TICKET-XXXX)?

Here's a draft:

Merged. [one tight sentence summarising what shipped — human, no jargon.] Live at [Page Title](https://{YOUR_DOCS_SITE}/...).

Reply "yes" to post it, or edit the draft above.

🔔 Don't forget to mark [TICKET-XXXX]({YOUR_ISSUE_TRACKER}/TICKET-XXXX) as Done if it isn't already.
─────────────────────────────────────────────────────
```

If no ticket found or PR is not merged: skip silently.

## Notes

- GitHub CLI must be authenticated for your org. Run `gh auth login` if not already configured.
- Reports saved to: `_extras/verification/`
- Works with merged and unmerged PRs (different verification levels)
