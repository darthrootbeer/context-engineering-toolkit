# SETUP-glossary on haiku

Prompt (inputs filled with made-up samples):

```text
I have attached the setup guide for "docs-pipeline" and its placeholder file `_knowledge/glossary.yaml`. Below is some text from my own documentation.

An order draft is a saved order that has not been submitted yet. When a customer submits it, the draft becomes an order and an invoice is generated. Use the Ledger view to see every invoice. Webhook events for drafts are sent to the sandbox endpoint first.

Following section 5.1 of the guide and the structure in the placeholder file, draft a first `glossary.yaml` with the 10 most important terms from my text. For every entry give the canonical form, the aliases only if my text shows them, and the docs_facing flag. Where my text does not show a capitalization rule or a common mistake, leave that field out and write "needs review" instead of inventing one. Do not infer a capitalization rule from how a word happens to be capitalized in my text.

A good answer uses the field names from the placeholder file exactly, has no more than 10 entries, and marks everything it could not know as "needs review".
```

Answer:

I'll draft a glossary.yaml following section 5.1 and the placeholder structure. Let me extract the 10 most important product-specific terms from your text.

```yaml
# Domain Glossary
# Used by: docs-grammar-spelling
#
# Structure:
#
# - canonical: ExactTermHere
#   docs_facing: true          # false = internal-only; flag if found in customer docs
#   aliases:
#     - alternate spelling
#     - abbreviation
#   usage:
#     capitalization: |
#       Describe when to capitalize, abbreviate, or use code formatting.
#     mistakes:
#       - "wrong form" → "correct form": explanation
#
# Add one entry per term. Keep alphabetical.

terms:

  - canonical: customer
    docs_facing: true
    usage:
      capitalization: needs review
      mistakes: needs review

  - canonical: draft
    docs_facing: true
    usage:
      capitalization: needs review
      mistakes: needs review

  - canonical: endpoint
    docs_facing: true
    usage:
      capitalization: needs review
      mistakes: needs review

  - canonical: invoice
    docs_facing: true
    usage:
      capitalization: needs review
      mistakes: needs review

  - canonical: Ledger
    docs_facing: true
    usage:
      capitalization: needs review
      mistakes: needs review

  - canonical: order
    docs_facing: true
    usage:
      capitalization: needs review
      mistakes: needs review

  - canonical: order draft
    docs_facing: true
    usage:
      capitalization: needs review
      mistakes: needs review

  - canonical: sandbox
    docs_facing: true
    usage:
      capitalization: needs review
      mistakes: needs review

  - canonical: sandbox endpoint
    docs_facing: true
    usage:
      capitalization: needs review
      mistakes: needs review

  - canonical: webhook event
    docs_facing: true
    usage:
      capitalization: needs review
      mistakes: needs review
```

**Notes:**
- All 10 entries are docs-facing; your text shows them in customer-visible documentation.
- No aliases appear in your text (e.g., you don't show "order-draft" or "Order Draft"), so none are listed.
- All capitalization and mistake entries marked "needs review" because your text doesn't show explicit rules or common pitfalls—only single instances. ("Ledger" appears capitalized once, but that's not enough to infer a rule.)
- Alphabetical order maintained as specified.

