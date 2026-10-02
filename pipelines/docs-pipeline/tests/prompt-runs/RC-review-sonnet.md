# RC-review on sonnet

Prompt (inputs filled with made-up samples):

```text
I have attached the README for "docs-readability-check". Below is a description of how I write and publish documentation.

My readers are backend developers who integrate with a payments-free orders API. I write how-to guides, reference pages and a few conceptual pages. One colleague reviews each change.

Using only the README, tell me:
1. Which of my doc types match the doc types the README gives a target grade for, and which do not.
2. Whether the skill's target grades suit my readers. Say "my description does not say" if you cannot tell.
3. What I should check by hand after the skill runs.

A good answer ties every point to something in my description or in the README, uses the README's own doc types and grade ranges, and does not invent a target grade for a doc type the README does not list.
```

Answer:

## 1. Doc type matches

The README sets the target grade from the `diataxis_type` in each doc's frontmatter.

| Your doc type | README doc type and target | Match |
|---|---|---|
| How-to guides | how-to: 11th to 12th grade | Direct match |
| Reference pages | reference: 12th to college freshman | Direct match |
| Conceptual pages | explanation and overview: 10th to 11th grade | Not a named match |

The README never uses the word "conceptual." Explanation or overview is the closest listed type, but you would have to tag those pages that way in the frontmatter. Your description doesn't say whether you use `diataxis_type` at all. If a page has no type, the README gives it 11th to 12th grade. That would apply to all three of your doc types if none are tagged.

## 2. Do the target grades suit your readers?

My description does not say. You've told me your readers are backend developers integrating with an orders API. You haven't given their reading level or whether they read English as a second language, and the README doesn't say who the grades were chosen for. The README's author also says they ran it only on their own docs, not yours.

The README does say that reference docs full of technical terms will score high whatever you do. The skill reports that rather than forcing the number down. For your reference pages, a high score is not necessarily a sign of a problem.

## 3. What to check by hand

- **Frontmatter types.** Confirm each page has the right `diataxis_type`, especially the conceptual pages. A wrong or missing type means the wrong target grade.
- **Tables, code blocks and callouts.** The skill never edits these, and it strips them before scoring. Parameter tables, request and response examples, and warnings in an API doc are all untouched, so review their wording yourself.
- **Flagged paragraphs.** The skill flags paragraphs it can't safely rewrite for a person. Work through them.
- **The rewrites themselves.** The skill edits in place, and the README gives no undo step. It also says it doesn't add or remove information, but you should still confirm that meaning is intact. Look at step order in how-tos and conditions or limits in reference text. Give your reviewing colleague the diff against your original, not just the final text.
- **The grade numbers.** The score comes from a 250-word sample of the middle of the prose, so it is an estimate. Read the start and end of longer pages yourself.
- **The report.** Read it in `_process/style-audit/readability-audit-{folder-name}.md`, or in `_system-audits/` if your docs sit in an Obsidian vault. Check the before and after grades against the targets above, bearing in mind the reference-page caveat in point 2.

