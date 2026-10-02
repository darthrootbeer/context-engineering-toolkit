---
extracted: 2026-10-01
product: Acme Orders API (FICTIONAL EXAMPLE DATA, replace with your own product)
---

# Product knowledge base: index

This folder is the source of truth that `/docs-sme-review` (Stage 4c) checks drafts against. The skill reads this file first, then the files it links to.

**This copy is a starter.** The product here, the "Acme Orders API" with orders, customers and invoices, is made up. It exists so the pipeline runs end to end on the sample doc. Replace every example row with facts about your own product before you run Stage 4c on real docs.

## How to fill this in

1. Replace the `product:` line above with your product's name.
2. Fill in each file listed below. Delete the fictional example rows as you go.
3. Set `extracted:` above to today's date (`YYYY-MM-DD`). Do this again every time you change any file in this folder.
4. Stage 4c prints a staleness warning in every report when `extracted:` is more than 90 days old.

## Files

| File | What goes in it |
|---|---|
| [integration-types.md](./integration-types.md) | Each integration type or product tier, and what it can and cannot do |
| [endpoints.md](./endpoints.md) | Each API endpoint: path, parameters, response, who can call it |
| [domain-models.md](./domain-models.md) | Each core object: key fields, states, relationships |
| [error-codes.md](./error-codes.md) | Each error code: meaning, when it fires, how docs should describe it |
| [webhooks.md](./webhooks.md) | Each webhook event: when it fires, payload, who receives it |
| [recent-changes.md](./recent-changes.md) | API or product changes from the last 90 days that could make existing docs wrong |

## Refresh instructions

Ask your engineers, or your own API spec, the question listed at the top of each file. Paste the answers in as tables. Keep each file short enough to read in one pass: this folder is loaded into the model's context on every Stage 4c run.
