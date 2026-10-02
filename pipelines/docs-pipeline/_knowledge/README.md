# _knowledge/

This folder holds the knowledge sources the pipeline skills load at runtime. Populate these before running the pipeline on your docs.

## Contents

| Path | Used by | What it is |
|------|---------|-----------|
| `glossary.yaml` | `docs-grammar-spelling` | Domain terminology, canonical forms, aliases, and common mistakes |
| `product-kb/index.md` | `docs-sme-review` | Product knowledge base index — links to all KB files |
| `product-kb/integration-types.md` | `docs-sme-review` | Your product's integration types, scopes, and capabilities |
| `product-kb/endpoints.md` | `docs-sme-review` | API surface: endpoints, params, responses |
| `product-kb/domain-models.md` | `docs-sme-review` | Core objects, lifecycles, and relationships |
| `product-kb/error-codes.md` | `docs-sme-review` | Error codes and their meanings |
| `product-kb/webhooks.md` | `docs-sme-review` | Webhook events, payloads, and integration scopes |
| `product-kb/recent-changes.md` | `docs-sme-review` | Recent API changes that may affect existing docs |
| `style-guides/general/style-guide_general.md` | `docs-style-check-voice` | General voice, tone, and formatting rules for your docs |
| `style-guides/diataxis/` | `docs-diataxis-audit`, `docs-style-check-structure` | Diataxis framework and per-type structure rules |
| `style-guides/write-like-a-human/` | `docs-style-check-human` | Rules for removing machine-written patterns |

## Keeping knowledge current

The SME review skill checks the `extracted:` frontmatter date on `product-kb/index.md`. If it is more than 90 days old, every SME review report will include a staleness warning. Update the date when you refresh the KB files.

## Note on this copy of the pipeline

Every file here is a working starter. The `product-kb/` files describe a made-up product, the "Acme Orders API" with orders, customers and invoices, and are marked `FICTIONAL EXAMPLE DATA`. They are there so the pipeline runs end to end on the sample doc in `../sample/`. Replace the example rows with facts about your own product before you run `docs-sme-review` on real docs. The glossary and the style guides are generic: their examples use the same made-up product, and every rule applies to any API docs.

Stage 0 (`/docs-workspace-setup`) copies this whole folder into each new workspace, because the skills read `./_knowledge/` relative to the workspace.
