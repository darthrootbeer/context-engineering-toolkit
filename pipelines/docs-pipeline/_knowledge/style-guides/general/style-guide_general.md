<!-- NOTE: This document is formatted for AI use and is not intended for human reading. The closing prompt block is the one part written for a human to paste into a model. -->

# ACME ORDERS GENERAL STYLE GUIDE — MACHINE RULESET

## VOICE AND TONE

- Use a smart, clear, confident tone.
- Do not write in a robotic style.
- Write like a technically sharp teammate.
- Be direct, helpful, and efficient.
- Be friendly but not chatty.
- Do not use marketing language.
- Prioritize clarity and brevity.
- Be technically honest and specific.

### VOICE EXAMPLES

| Usage                  | Example                                     |
| ---------------------- | ------------------------------------------- |
| Direct, confident tone | "You create an order with `POST /orders`." |
| Prohibited casual tone | "Let's go ahead and create an order!"  |

## READER ASSUMPTIONS

- Audience includes junior, mid-level, and senior developers.
- Use concise and precise language.
- Explain terms at first use.
- Provide runnable examples with minimal edits.

### READER EXAMPLES

| Usage                  | Example                                                   |
| ---------------------- | --------------------------------------------------------- |
| Introduce term         | "The `order_type` field controls fulfillment behavior." |
| Out-of-the-box example | Copy, replace placeholders, run.                          |

## STRUCTURE

- Paragraphs must be 1–3 lines.
- Place key idea first in each section or paragraph.
- Use sentence case for titles and callouts.

### STRUCTURE EXAMPLES

| Usage          | Example                                                 |
| -------------- | ------------------------------------------------------- |
| Concise title  | `Configure webhooks`                                    |
| Key idea first | "Use the `customer_id` field to identify the customer." |

## LISTS

- Bulleted lists MUST be used for conceptual or descriptive explanations of how a system works.
- Bulleted lists explain behavior, flow, states, or properties.
- Bulleted lists must not imply required execution order.
- Bulleted lists describe what happens, not what the reader does.
- All items in a conceptual bulleted list MUST be at the same level of indentation. Do not nest bullets within conceptual lists that describe how a system works.
- Numbered lists MUST be used for procedural instructions where a reader is expected to perform actions in a required order.
- Numbered lists represent task sequences.
- Numbered list steps must be written using imperative verbs.
- The order of steps in numbered lists is mandatory.
- Every numbered (procedural) list MUST be introduced with bold text (wrapped in double asterisks) that begins with "To" and ends with a colon (e.g., "**To check an order's status:**").
- Headings or subheadings may appear above the "To" lead-in for navigation purposes, but the "To" lead-in is always required immediately before the numbered steps.
- Every numbered (procedural) list MUST be followed immediately by a single, plain-language sentence that confirms successful completion of the steps and explains the expected outcome or resulting system state.
- The outcome sentence MUST NOT start with "After completing these steps" or similar phrases, as completion is assumed. Use direct phrasing such as "This will…" or state the outcome directly.

### LIST EXAMPLES

| Usage                      | Example                                                                                                                                                                                                                                                  |
| -------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Bulleted list (conceptual) | "When an order is canceled:\n- The system validates the order ID.\n- Reserved stock is released.\n- A confirmation email is sent to the customer."                                                                             |
| Numbered list (procedural) | "**To configure API authentication:**\n\n1. Navigate to the API settings page.\n2. Generate a new API key.\n3. Copy the key to your environment variables.\n\nYour application will authenticate using the new key."                                     |
| Numbered list with heading | "### Configure API authentication\n\n**To configure API authentication:**\n\n1. Navigate to the API settings page.\n2. Generate a new API key.\n3. Copy the key to your environment variables.\n\nYour application will authenticate using the new key." |
| Required outcome sentence  | "This will configure webhook delivery to your endpoint."                                                                                                                                                                                                 |
| Outcome sentence (avoid)   | "After completing these steps, the order is created."                                                                                                                                                                                                |

## TABLES

- Use minimal formatting. Separator rows use `|---|` per column, not padded dashes.
- Do not pad cells with extra spaces to align columns. Markdown renderers ignore whitespace.
- Empty cells must contain a single space (`| |`), not be completely empty (`||`).
- Use standard markdown tables, not ReadMe `[block:parameters]` JSON blocks.

### TABLE FORMAT

Do this:

```
| Field | Type | Description |
|---|---|---|
| `ref` | string | A unique identifier. |
| `status` | string | The current state. |
```

Not this:

```
| Field    | Type   | Description            |
| -------- | ------ | ---------------------- |
| `ref`    | string | A unique identifier.   |
| `status` | string | The current state.     |
```

## TERMINOLOGY

- Use exact API field names.
- Do not rename internal terminology.
- Maintain consistency for all terms.

### TERMINOLOGY EXAMPLES

| Usage             | Example                  |
| ----------------- | ------------------------ |
| Exact field       | Use `order_type`         |
| Consistent naming | Always use `customer_id` |

## CODE SAMPLES

- Use realistic placeholders.
- Provide complete request/response pairs.
- Keep samples minimal but runnable.
- Use fenced code blocks with language hints.

### CODE SAMPLE EXAMPLES

| Usage             | Example                                                                                                                                                        |
| ----------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Request           | `bash\ncurl -X POST https://api.example.com/v1/orders \\\n  -H 'Authorization: Bearer YOUR_API_KEY' \\\n  -d '{\"customer_id\":\"cus_123\",\"total\":500}'\n` |
| Response          | `json\n{\"id\":\"ord_123\",\"status\":\"created\"}\n`                                                                                                        |
| Placeholder value | `your_client_id`                                                                                                                                               |

## CALLOUTS

### ALLOWED CALLOUT TYPES

- Only these four callout types are permitted: Info (📘), Warning (⚠️), Error or Critical (🛑), Okay (✅).
- No other callout types are allowed.
- Use Okay callouts sparingly.

### REQUIRED SYNTAX

- Callouts MUST use ReadMe blockquote syntax (lines starting with `>`).
- A callout is defined as a blockquote where the first visible character after the `>` is an emoji.
- Required structure:
  - Line 1: `> ` (blockquote symbol), space, emoji, space, **bold title text** (wrapped in `**`). Example: `> ⚠️ **Use the raw request body**`.
  - Line 2: `> ` (blockquote symbol) followed by nothing (empty line).
  - Line 3+: `> ` (blockquote symbol), space, callout body text.
- The emoji MUST be the first visible character after the blockquote symbol on line 1.
- All lines belonging to the callout MUST begin with `>`.
- A blank blockquote line between title and body is REQUIRED.

### PROHIBITED PATTERNS

- Inline prefixes such as `INFO:`, `WARNING:`, `CRITICAL:`.
- Token-based callouts.
- Custom or unsupported callout labels such as `NOTE`, `TIP`, `RELATED`.
- HTML-based callout containers.
- Bolded emojis (bold the title text, not the emoji itself), indented emojis, or text-prefixed emojis.
- Callouts used as navigation or internal references.

### SEMANTIC USAGE

- Info (📘): Use for optional context or clarifications.
- Warning (⚠️): Use for potential issues, limitations, or edge cases.
- Error or Critical (🛑): Use for blocking errors or required actions.
- Okay (✅): Use for positive confirmation after successful actions. Use sparingly.

### COMPLIANCE

- Any callout that violates these rules MUST be flagged as non-compliant.

### CALLOUT EXAMPLES

| Usage             | Example                                                                       |
| ----------------- | ----------------------------------------------------------------------------- |
| Info              | `> 📘 **Optional context**\n> \n> Tokens expire after 24 hours.`                  |
| Warning           | `> ⚠️ **Potential issue**\n> \n> Pagination defaults to 50 items per page.`       |
| Error or Critical | `> 🛑 **Required action**\n> \n> Field 'amount' is required in the request body.` |
| Okay              | `> ✅ **Success**\n> \n> Your API key has been generated successfully.`           |

## ADDRESSING THE READER

- Use "you" to address the developer in sentences and paragraphs.
- Use imperative form (without "you") in list items for brevity.
- Use imperative form (without "you") in headings, subheadings, and bold section labels.
- Use "customers" (not "your customers") when referring to the developer's customers. The context makes it clear whose customers are being discussed.
- Use active voice.
- Avoid passive voice.
- Do not use "we" unless the system is acting.

### ADDRESSING EXAMPLES

| Usage                      | Example                                                                       |
| -------------------------- | ----------------------------------------------------------------------------- |
| Active instruction         | "You update the key every 90 days."                                           |
| Heading/subheading         | "Pass the customer ID to subsequent requests."                         |
| Heading/subheading (avoid) | "You pass the customer ID to subsequent requests."                     |
| List item (imperative)     | "Pass the `customer_id` field in the request body."                           |
| List item (imperative)     | "Store the `ref` in your database."                                           |
| Customer reference         | "Acme Orders allows customers to reuse their saved shipping addresses."      |
| Customer reference (avoid) | "Acme Orders allows your customers to reuse their saved shipping addresses." |
| System subject             | "We return a 200 OK on success."                                              |

## CROSS-REFERENCING

- Use inline links when needed.
- Do not list multiple links in one sentence.
- Use `RELATED` callouts for critical references.

### CROSS-REFERENCING EXAMPLES

| Usage           | Example                          |
| --------------- | -------------------------------- |
| Inline link     | "See the `Order` object."       |
| RELATED callout | `RELATED: Order API reference.` |

## VISUALS

- Use diagrams only when text is insufficient.
- Use placeholders if diagrams are missing.
- Image placeholders must use a callout block format with the red circle emoji.

### VISUAL EXAMPLES

| Usage               | Example                                                                |
| ------------------- | ---------------------------------------------------------------------- |
| Image placeholder   | `> 🔴 **IMAGE PLACEHOLDER**\n> image showing the save address option on the order form` |
| Image placeholder   | `> 🔴 **IMAGE PLACEHOLDER**\n> saved address displayed on the order form`   |
| Diagram placeholder | `[Placeholder: fulfillment flow for orders]`                           |

## INFORMATION ARCHITECTURE

- Group documents by developer workflow.
- Organize content to match how developers use the system.
- Avoid excessive nesting.
- Keep related topics together.

### IA EXAMPLES

| Usage          | Example                            |
| -------------- | ---------------------------------- |
| Workflow group | `Integration > Orders > Cancellations` |
| Topic grouping | `Authentication > API Keys`        |

## GENERAL PRINCIPLES

- Do not use filler.
- Do not use redundant intros.
- Ensure every element has a concrete purpose.
- Optimize for scanning, copying, and immediate use.

### PRINCIPLE EXAMPLES

| Usage             | Example                           |
| ----------------- | --------------------------------- |
| Useful heading    | "Create a sandbox account" |
| Prohibited filler | "In this guide, we will discuss…" |

## DO AND DON'T

- Prefer precise, actionable instructions.
- Avoid vague or casual phrasing.

### DO/DON'T EXAMPLES

| Usage | Example                                    |
| ----- | ------------------------------------------ |
| DO    | "You can cancel an order using `/orders`." |
| DON'T | "Insert the ID for the shipment."            |

## END EVERY DOC WITH A PROMPT FOR THE READER'S AI MODEL

Readers now work with an AI model beside the doc. Give them a prompt that is ready to paste, so the doc teaches, checks, and adapts itself on request.

- End every doc with a prompt block.
- End every H2 section with a prompt block when the section is self-contained and longer than about 40 lines of prose (code blocks and tables do not count).
- Use the exact block shape below. Do not rename the heading.
- Each prompt is self-contained. It says which files the reader attaches, what the model must do, and what a good answer contains.
- A good answer is described in checkable terms: things the answer must include, and things it must not invent.
- Cover these purposes across a doc's blocks, each where it fits: understand and teach, review against the reader's own setup, customize, fix, test, run.
- The block at the end of a doc carries three prompts at minimum: understand and teach, review against the reader's own setup, adapt and test.
- A block at the end of a section carries one prompt, for whichever purpose fits that section.
- Never tell the reader the prompt works with "any AI model" unless the doc also says which models it was actually run against.
- Check every prompt before it ships: run it against a model with the doc attached, read the answer against the "good answer" list, and record the result in the doc. If the prompt fails, fix the prompt and run it again.
- Exempt: skill files (instructions for an agent, not a document for a reader), anything under `_archive/`, `_templates/`, `_attachments/` or `_process/`, and index or README files under about 25 lines that only route the reader elsewhere.

### PROMPT BLOCK SHAPE

````markdown
### Prompt for your AI model

Paste this into any AI model, together with this document and the files it describes.

**Understand and teach**

```text
<prompt text>
```

**Review against your own setup**

```text
<prompt text>
```

**Adapt and test**

```text
<prompt text>
```

**How these prompts were checked.** <date, the models used, how each answer was judged, and the result>
````

- Put the label line (bold purpose) above each prompt. A section-end block has one prompt, so it may skip the label.
- Put reader-supplied input in square brackets inside the prompt, for example `[PASTE a short description of your setup]`.
- Name any extra files the reader must attach, in the prompt text itself.

### PROMPT BLOCK EXAMPLES

| Usage | Example |
| ----- | ------- |
| Good: names the files | "I have attached the setup guide and my `glossary.yaml`." |
| Good: checkable answer | "A good answer lists every placeholder in the doc and does not invent any." |
| Bad: vague | "Tell me about this doc." |
| Bad: untested claim | "Works with any AI model." (with no models named) |

## AI TELLS

All rules for identifying and removing AI-generated writing patterns (em dashes, banned words, filler phrases, sentence structure) live in the **Write Like a Human** style guide:

`_knowledge/style-guides/write-like-a-human/style-guide_write-like-a-human.md`

Apply that guide as a final editing pass on all documentation before publication.

### Prompt for your AI model

Paste this into any AI model, together with this document and the files it describes.

**Understand and teach**

```text
I have attached the general style guide for the docs-pipeline. Teach me the rule "End every doc with a prompt for the reader's AI model".

1. Say what the rule requires and why it exists.
2. Show me the exact block shape.
3. List what is exempt.
4. Then ask me three questions to check that I understood, one at a time. Wait for my answer before the next one, and correct me where I am wrong.

A good answer gives the exact heading and intro sentence, says the end-of-doc block holds three prompts (understand and teach, review against the reader's own setup, adapt and test), says every prompt must be run against a model and the result recorded, and lists the exemptions as the guide gives them. It must not invent a requirement.
```

**Review against your own setup**

```text
I have attached the general style guide for the docs-pipeline. Below is one of my own docs.

[PASTE a short doc of yours, including its last heading.]

Check my doc against the rule "End every doc with a prompt for the reader's AI model". For every requirement in the rule, say pass or fail and quote the heading or line from my doc that shows it. List what is missing. Do not write the missing prompts yet.

A good answer has a verdict for each requirement, quotes evidence from my doc for every verdict, and does not write any prompt.
```

**Adapt and test**

```text
I have attached the general style guide for the docs-pipeline. Below is one of my own docs.

[PASTE a short doc of yours.]

Write the closing prompt block for my doc in the exact shape the guide gives, with the three required prompts. Each prompt must say which files to attach and what a good answer contains. Then give me step-by-step instructions to test each prompt against a model, and tell me what to write in the "How these prompts were checked" line. Do not write a test result yourself. Leave the result for me to fill in after I have run the tests.

A good answer uses the exact heading and intro sentence from the guide, has three labeled prompts, gives every prompt a checkable good-answer clause, explains how to run, judge, and record each test, and leaves the test result blank.
```

**How these prompts were checked.** On 2026-10-01 I ran every prompt in this document through the Claude Code command line, once against Claude Sonnet and once against Claude Haiku (the `sonnet` and `haiku` model names in Claude Code 2.1.287). Each run was a fresh session with no tools and no other instructions. I attached this document and any other file the prompt names, replaced each bracketed input with a made-up sample, and read every answer against that prompt's "good answer" list. I have not run them against models from other vendors, so "any AI model" means "should work", not "verified".

| Prompt | Sonnet | Haiku |
| --- | --- | --- |
| Understand and teach | Pass | Pass |
| Review against your own setup | Pass | Pass |
| Adapt and test | Pass | Pass after a fix. The first version let Haiku write a passing test result into the "How these prompts were checked" line for tests it had not run. The prompt now tells the model to leave the result blank. |

