---
title: Style Guide — Read Next Section
created: 2026-05-30
modified: 2026-05-30
tags: [style-guide, documentation, navigation]
---

# Style Guide — Read Next Section

Every technical documentation article ends with a **Read next** section. This gives readers a clear path to related content and makes guide sets navigable without requiring them to return to the overview.

---

## The Standard

Every article in a technical guide set must have a `## Read next` section immediately before the `## Links` section (if one exists) and the sign-off.

Each entry is a bullet point with:
- A wikilink to the related article
- An em dash
- One sentence describing what that article covers and why a reader coming from this article would want it

```markdown
## Read next

- [[article-slug]] — One sentence: what this article covers and why it's the next logical read.
- [[another-article]] — One sentence description.
```

---

## Rules

**Every entry gets exactly one sentence.** It should answer: "if I just read this article, why would I go there next?" Not "what is that article about" in the abstract — what does it offer *this* reader.

**Link to 3–6 articles.** Fewer than 3 suggests the doc set is too thin. More than 6 overwhelms.

**Order by likely reading sequence.** The most natural next step goes first. Related deep-dives go later.

**No bare wikilinks.** `[[kirby-pipeline]]` alone is not enough — the reader needs to know why they'd click it.

**No Linear ticket links here.** Ticket links go in a separate `## Links` section below Read next. Read next is for vault docs only.

**Use plain sentence descriptions.** Don't write marketing copy. Don't start with "Learn how to..." or "Discover...". Just say what the doc contains.

---

## Placement in the doc

```markdown
[... end of article body ...]

---

## Read next

- [[related-doc]] — Description.
- [[another-doc]] — Description.

## Links                          ← only if there are external ticket/URL links

- [STRY-NNN — Ticket title](url)

---

*Attribution line.*

— [Sign-off](obsidian-link)
```

---

## Scope

This standard applies to all Storyteller technical documentation guide sets, including:
- Kirby vault docs
- Any other multi-doc guide set covering a tool, system, or process

It does not apply to:
- One-off research notes
- Meeting notes or decision logs
- The guide set overview/MOC itself (that already has a doc index table)

---

## Example

From `kirby-pipeline.md`:

```markdown
## Read next

- [[kirby-verification]] — The six tools that run after encoding completes, including when to use each and what the output means.
- [[kirby-syspack-files]] — Annotated walkthrough of the four system pack files the pipeline produces, with real Open Adventure examples.
- [[kirby-mod-encoding]] — What mods are, the four mod types, and how to write a declaration file for Phase 0.
- [[kirby-architecture]] — Engineering reference: phase internals, CLI commands, schemas, and failure modes.
- [[kirby-overview]] — What Kirby is, what it produces, and who uses a system pack.
```
