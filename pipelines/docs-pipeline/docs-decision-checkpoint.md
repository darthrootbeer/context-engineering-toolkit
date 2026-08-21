---
name: docs-decision-checkpoint
description: Collect all unresolved recommendations from the docs pipeline, then walk the user through apply/skip/defer decisions one item at a time. Each item gets a clear recommendation with reasoning. Use after style passes and reviews are complete, before publish.
argument-hint: [path]
allowed-tools: [Read, Write, Edit, Glob, Grep, Bash]
---

# docs-decision-checkpoint

Collects all unresolved recommendations from the docs pipeline (style audit flags, cross-link candidates, visual aid suggestions) and walks the user through each one individually. For every item, state a clear recommendation (apply/skip/defer) and the reasoning. Apply changes immediately when the user confirms. Write `recommendations.md` at the end as a record.

## Arguments

The user provided: $ARGUMENTS

- `$ARGUMENTS[0]` — Path to the output docs folder or workspace project root. If omitted, use the current working directory.

**Required.** If missing, stop: `"Please provide a path: /docs-decision-checkpoint [path]"`

---

## Steps

### 1. Locate source artifacts

Resolve the workspace root from the provided path. Find and read:

- All style audit reports: `_process/style-audit/style-audit-*.md` — read every one. Collect items under **"Flags (manual review needed)"** from each.
- Links review: `_process/link-check/*.md` — read. Collect **"Cross-Link Candidates"** (overlaps are publish-time actions, not decisions for this checkpoint).
- Visual audit: `_process/visual-audit/*.md` — read. Collect all **"Recommendations"** entries.
- SME review: `_process/sme-review/sme-review-summary.md` — read. Collect all **HIGH** and **MEDIUM** findings.

If any artifact is missing, note it and proceed with what exists.

### 2. Build the item list

Combine all collected items into a single ordered list. Deduplicate: if the same issue appears in two sources, include it once (noting both sources).

Group by category:
1. SME review findings (domain accuracy, reader journey, naming) — highest impact, process first
2. Style flags (from style audit "Flags" sections)
3. Cross-link candidates (from links review)
4. Visual aid recommendations (from visual audit)

Within each group, order HIGH before MEDIUM, and MEDIUM before LOW.

Number them sequentially across all groups (1, 2, 3... N). This is the order you will present them.

If zero items: write `recommendations.md` with "No unresolved items" and skip to the summary.

### 3. Announce the queue

Before starting, tell the user how many items you found and what categories they fall into:

```
Found {N} items to review:
  - SME review: {N} findings
  - Style flags: {N} flags
  - Cross-links: {N} candidates
  - Visual aids: {N} recommendations

I'll go through them one at a time. For each one I'll give you my recommendation and why — then you decide: apply, skip, or defer.

Ready? Starting with item 1.
```

Then immediately present item 1 without waiting.

### 4. Present each item one at a time

For each item, present it in this format — then wait for the user's decision before moving on.

---

**Format for each item:**

```
## Item {N} of {total} — {Short title} [{HIGH/MEDIUM/LOW}]

**Category:** {SME review / Style flag / Cross-link / Visual aid}
**File:** `{filename}` — {section or line reference}

**What's happening:** {2–4 sentences. Describe the current state concretely. Quote the exact text or describe the exact location. Make it clear what the reader sees right now.}

**My recommendation: {APPLY / SKIP / DEFER}**

{2–4 sentences explaining why. Lead with the user impact: what goes wrong if this isn't fixed? Or why is it not worth fixing? Be direct. If recommending apply, show the before/after. If recommending skip, say clearly why it's fine as-is. If recommending defer, say what would need to be true before it's worth addressing.}

{If recommending APPLY, show:}
Before: `{exact current text}`
After: `{exact proposed text}`
{Or for structural changes: describe exactly what moves where.}

Apply, skip, or defer?
```

---

**Rules for the recommendation:**

- **APPLY** — the change clearly improves correctness, clarity, or compliance. No ambiguity. The before/after is better. Prioritize for: domain accuracy errors, missing context a reader needs, callout format violations, clear style guide violations.
- **SKIP** — the current state is acceptable. The "fix" is cosmetic or the recommendation doesn't apply to this doc's context. Say this directly: "The current phrasing is fine. This flag was over-cautious."
- **DEFER** — the change is real but not blocking publish. Typical reasons: (a) requires content from elsewhere that doesn't exist yet, (b) part of a larger pattern change across multiple docs, (c) waiting on another ticket to merge first. Name the condition: "Defer until PR #87 merges."

Never say "it depends" or hedge the recommendation. Commit to one: apply, skip, or defer.

### 5. Handle the user's response

After each decision:

- **apply** — make the edit immediately. Show a brief confirmation: `Done. {One sentence describing the change made.}` Then present the next item.
- **skip** — log it. Then present the next item.
- **defer** — ask "Defer to what? (ticket ID, future phase, or 'next pass')" Record the answer. Then present the next item.
- **user overrides the recommendation** — apply their decision, not yours. Don't argue. Log what they chose.
- **user asks a question** — answer it, then re-present the item with the same recommendation unless they've changed your view.

Keep a running log internally:
```
{item_number}: {short_title} → {apply|skip|defer} [{optional: defer context}]
```

### 6. Write recommendations.md

After all items are decided, write `recommendations.md` to the `_process/` directory as a permanent record.

```markdown
# Recommendations: {Guide Name}

**Date:** {YYYY-MM-DD}
**Items reviewed:** {N} total — {N} applied, {N} skipped, {N} deferred

---

## Applied

{List each applied item with: title, file, what changed, one sentence why.}

---

## Skipped

{List each skipped item with: title, file, one sentence why it was skipped.}

---

## Deferred

{List each deferred item with: title, file, one sentence description, and the defer condition (ticket, phase, or future pass).}

---

## Decisions log

| # | Item | Decision | Notes |
|---|---|---|---|
| 1 | {short title} | {apply/skip/defer} | {brief note} |
| 2 | ... | ... | ... |
```

### 7. Summary

```
Decision checkpoint complete.

Applied: {N} items
Skipped: {N} items
Deferred: {N} items

Recommendations record: {path}/_process/recommendations.md
```

Then present the Stage 5 → Stage 6 gate:

```
→ Stage 5 complete. Next: Stage 6 (publish).
Proceed to Stage 6?
```

**Wait for user response.**

---

## Error Handling

| Situation | Behavior |
|---|---|
| No path provided | Stop: show usage message |
| Path doesn't exist | Stop: "Directory not found: [path]" |
| No style audit or editorial changes found | Warn, proceed with whatever artifacts exist |
| Zero unresolved items | Write recommendations.md noting "No unresolved items" and go to summary |

---

## Notes

- Go through items in order. Don't present item N+1 until item N is decided.
- Be opinionated. A wishy-washy recommendation wastes the user's time. If unsure between apply and defer, pick apply if the change is clearly better; defer if it depends on something external.
- Apply changes immediately — don't batch them up. The user should see the edit happen before moving to the next item.
- The recommendations.md is a permanent record, not a pre-review worksheet. Write it after decisions are made, not before.
- Deferred items stay in recommendations.md. They don't block publish; they're picked up in a future pass.
