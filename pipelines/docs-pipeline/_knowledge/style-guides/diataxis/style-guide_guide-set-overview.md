# Diátaxis Overview Document Rules

The overview is the customer's entry point to a guide set. It explains what the guide covers, who it's for, and what each document in the set contains. In the published docs, this content lives in `index.md` inside the guide's subdirectory and renders as the collapsible parent page in ReadMe's sidebar.

## What This Document Is

The overview document is not one of the four Diataxis content types. It is a The Product-specific entry point that sits above the guide set. Every multi-doc guide set must have one.

It can draw from any Diataxis type (a paragraph of explanation here, a conceptual diagram there, a brief prerequisite list) to help the reader understand the guide and orient themselves within it. There is no single prescribed form. The only hard rule is its function: it is the first thing a customer reads, and it explains all the Diataxis pieces that sit alongside it.

### How it's published

During the Diataxis split workflow, the overview is written as `{area}-overview.md` in the workspace output. At publish time, `/docs-publish` merges the overview's body content into `index.md` inside the guide's subdirectory. The overview is not published as a separate child page.

```text
docs/{Category}/
└── {area}-guide/
    ├── index.md             ← overview content lives here
    ├── {area}-explanation.md
    ├── {area}-how-to.md
    └── {area}-reference.md
```

## Classification Criteria

**Use an overview document when:**

- You are creating or shipping a multi-doc guide set (any combination of Explanation, How-to, Reference, Tutorial)
- A reader arriving at the guide for the first time needs to understand what the guide covers before choosing where to go
- The guide has defined prerequisites (e.g. an existing integration, credentials, prior knowledge)

**Do NOT use the overview document for:**

- Conceptual explanation of the product or feature → Explanation doc
- Step-by-step implementation instructions → How-to Guide
- API specifications or technical details → Reference doc
- Hands-on learning exercises → Tutorial

## Hard Structural Rules

### Title Format

Required pattern: `[Product/Feature] [Guide Type]`

Good: "BenefitsPay Integration Guide", "HSA/FSA Payment Guide", "Backend-to-Backend Integration Guide"
Bad: "Introduction to BenefitsPay", "Getting Started with BenefitsPay", "BenefitsPay Overview" (too vague or instructional)

### Required Sections (always present, always in this order)

1. **Lead paragraph**. One to two sentences. What this guide covers at the highest level and why it exists. No section heading.
2. **## Audience**. Who this guide is written for. One to two sentences. Name the role (e.g. "payment engineers and product managers") and any assumed baseline (e.g. "who have integrated benefits-program with The Product").
3. **## Prerequisites**. What the reader needs before starting. One to two sentences or a short bullet list. Be specific.
4. **## What's in this guide**. A bullet list of every document in the guide set. Each bullet: `**[Linked doc title]**. One sentence describing what that doc covers.`

### Length

As long as it needs to be to properly orient the reader, no more. If a section of the overview would be more useful in its own Explanation, How-to, or Reference doc, put it there and link to it instead.

### "What's in this guide" format

Each entry must:

- Link to the document using a relative path
- Bold the linked title
- Follow the link with a period and a single sentence
- Cover the core Diataxis docs in this order: Explanation → How-to → Reference → Tutorial (if present)

Example:
```markdown
- **[Understanding BenefitsPay Payments](./benefitspay-payments.md)**. How BenefitsPay differs from dollar-based payment methods: the item-based voucher model, the payment lifecycle, and straddle rules.
- **[How to Integrate BenefitsPay with The Product](./benefitspay-integration.md)**. Step-by-step instructions for each phase of the integration: syncing APL data, retrieving benefits, building the cart, capturing payment, and processing refunds.
- **[BenefitsPay API Reference](./benefitspay-api-reference.md)**. Complete endpoint specifications, capture action codes, error codes, transaction limits, and receipt requirements.
```

## Core Content Rules

### DO Include

- What the guide covers at the highest level
- Audience: who it's for, what baseline is assumed
- Prerequisites: what must exist before the reader can start
- Links to every document in the guide set, each with a description of what it covers
- Whatever else helps the reader orient themselves (a conceptual overview, a diagram showing how the pieces relate, a brief summary of the product domain) if it belongs in the overview and not more naturally in one of the other docs

### Do NOT Include

- Content that duplicates what's in the other guide docs. The overview describes each doc's content; it doesn't repeat it.
- Detail that belongs in the Explanation, How-to, or Reference doc. If a piece of content would be at home in one of those, put it there and link to it from the overview.

## Writing Style Rules

### Voice

- Second person where natural ("you need", "your integration")
- Direct and efficient. Every sentence earns its place.
- No marketing language, no filler phrases

Good: "Your BenefitsPay integration builds on your existing benefits-program integration."
Bad: "Welcome to the BenefitsPay Integration Guide! We're excited to help you get started."

### Language

- One sentence per idea
- Prefer concrete over abstract: "payment engineers" not "technical users"
- Audience and Prerequisites sections can use bullets if there are multiple discrete items; otherwise prose

## Common Mistakes

1. **Duplicates content from the other docs**. Repeats what's already in the Explanation, How-to, or Reference instead of describing and linking. Fix: Describe what's there, don't reproduce it.
2. **Missing a doc in "What's in this guide"**. Not all docs in the set are listed. Fix: Every doc in the set must appear.
3. **Vague descriptions in "What's in this guide"**. "Reference information" or "How-to guide" without specifics. Fix: Name the actual content the reader will find.
4. **Becomes a full Explanation doc**. Goes deep into conceptual territory that has its own dedicated doc. Fix: Keep the conceptual content at orientation depth; link to the Explanation for the full treatment.
5. **No clear entry into the guide**. Reads like a table of contents only, with no orientation. The reader still doesn't know what this guide is or whether it's for them. Fix: Lead with scope and audience before the doc list.

## Template

```markdown
# [Product/Feature] [Guide Type]

[One to two sentences. What this guide covers and why it exists.]

## Audience

[Who this is for. Name the role and assumed baseline.]

## Prerequisites

[What the reader needs before starting.]

## What's in this guide

- **[Explanation doc title](./explanation-doc.md)**. [One sentence: the concepts and mental models this doc covers.]
- **[How-to doc title](./how-to-doc.md)**. [One sentence: the tasks and phases this doc walks through.]
- **[Reference doc title](./reference-doc.md)**. [One sentence: the specifications, codes, and rules this doc contains.]
```

## Quality Checklist

- [ ] Title follows `[Product] [Guide Type]` pattern
- [ ] Scope is clear; a new reader knows immediately what this guide covers and whether it's for them
- [ ] Audience names a role and a baseline
- [ ] Prerequisites are specific and actionable
- [ ] Every doc in the guide set is listed in "What's in this guide"
- [ ] Each doc description names the actual content, not just the doc type
- [ ] No content duplicates what's already in one of the other docs
- [ ] Length is appropriate; nothing present that would be better placed in its own Explanation, How-to, or Reference doc

## Cross-references

The overview document links to every other doc in the guide set. Each of those docs should include a brief back-reference to the overview (e.g. a note at the top pointing readers there for prerequisites and context).

## Maintenance Triggers

Update when: a new document is added to the guide set, prerequisites change, the audience expands, or the scope of the guide changes.
