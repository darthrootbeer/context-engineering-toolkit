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
| `style-guides/style-guide.md` | `docs-style-check-voice` | General voice, tone, and formatting rules for your docs |

## Keeping knowledge current

The SME review skill checks the `extracted:` frontmatter date on `product-kb/index.md`. If it is more than 90 days old, every SME review report will include a staleness warning. Update the date when you refresh the KB files.

## Note on this copy of the pipeline

The `product-kb/` files listed above are intentionally not included in this repo — they hold a specific product's proprietary API surface and domain model, which is exactly the kind of content this knowledge folder is designed to hold *for your own project*, not something to ship generically. Populate `product-kb/` with your own product's equivalent before running `docs-sme-review`. Everything else in this folder (the glossary, the style guides) is generic and ready to use or adapt.
