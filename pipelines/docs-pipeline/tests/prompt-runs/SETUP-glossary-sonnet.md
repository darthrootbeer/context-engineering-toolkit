# SETUP-glossary on sonnet

Prompt (inputs filled with made-up samples):

```text
I have attached the setup guide for "docs-pipeline" and its placeholder file `_knowledge/glossary.yaml`. Below is some text from my own documentation.

An order draft is a saved order that has not been submitted yet. When a customer submits it, the draft becomes an order and an invoice is generated. Use the Ledger view to see every invoice. Webhook events for drafts are sent to the sandbox endpoint first.

Following section 5.1 of the guide and the structure in the placeholder file, draft a first `glossary.yaml` with the 10 most important terms from my text. For every entry give the canonical form, the aliases only if my text shows them, and the docs_facing flag. Where my text does not show a capitalization rule or a common mistake, leave that field out and write "needs review" instead of inventing one. Do not infer a capitalization rule from how a word happens to be capitalized in my text.

A good answer uses the field names from the placeholder file exactly, has no more than 10 entries, and marks everything it could not know as "needs review".
```

Answer:

Your text only supports 8 distinct terms, so this draft has 8 entries rather than padding to 10.

```yaml
terms:

  - canonical: customer
    docs_facing: true
    usage:
      capitalization: needs review
      mistakes: needs review

  - canonical: invoice
    docs_facing: true
    usage:
      capitalization: needs review
      mistakes: needs review

  - canonical: Ledger view
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
    aliases:
      - draft
    usage:
      capitalization: needs review
      mistakes: needs review

  - canonical: sandbox endpoint
    docs_facing: true
    usage:
      capitalization: needs review
      mistakes: needs review

  - canonical: submit
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

Things to check:

- **Aliases:** Only `order draft` has one. Your text uses "draft" and "drafts" for it. I left `aliases` out everywhere else because the text shows no alternate forms.
- **`docs_facing: true`:** I set this on every entry because all of these terms appear in your documentation. Your text doesn't say whether any of them are internal-only, so confirm that.
- **Canonical forms:** These are copied from your text. `Ledger view` is capitalized there, but that is only how I found it. I did not treat it as a rule, so its capitalization is "needs review". `webhook event` is lowercase because the only occurrence is at the start of a sentence, which makes that form a guess to confirm.
- **Placeholder file:** `API`, `webhook` and `sandbox` are already in the starter file with their own rules. None of them come from your text, so I didn't copy them. You can keep them, or fold `sandbox endpoint` and `webhook event` into those entries. If you merge this draft in, keep the file alphabetical, as its header asks.

