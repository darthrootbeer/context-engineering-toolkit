<!-- NOTE: This document is formatted for AI use only and is not intended for human reading. -->

## Formatting Rules

- Use sentence case for descriptions
- Use backticks for inline code: field names, parameters, schema keys
- Pluralize code terms by placing “s” outside backticks unless plural exists in API
  - `Invoice`s
  - not `Invoices`
- Use fenced code blocks with language hints (`json`, `bash`)
- Use tables for parameters and schemas
- Use bullet lists for constraints or options
- Avoid sentences longer than 20 words in descriptions

## Field Name & Terminology

- Use exact API field names as in spec
- Be consistent across endpoints
- Use only approved terms:

| Usage                | Example                |
| -------------------- | ---------------------- |
| Authentication token | `Authentication token` |
| Redirect URL         | `Redirect URL`         |
| Customer ID          | `customer_id`          |
| Order ID             | `order_id`             |

- Examples:

| Usage | Example                                                       |
| ----- | ------------------------------------------------------------- |
| Do    | Use the `order_id` field to identify the order.               |
| Don’t | Use the order ID to identify the order.                      |

## Error Message Structure

- Format: Cause → Resolution → Example
- State problem clearly
- Provide actionable guidance
- Use backticks for error codes and fields

| Usage | Example                                                                                            |
| ----- | -------------------------------------------------------------------------------------------------- |
| Do    | `Invalid order_id` — The provided `order_id` does not exist. Verify the value and try again. |
| Do    | `Expired session` — The session has expired. Create a new session and retry the request.           |
| Don’t | Invalid order ID — This order ID is wrong.                                                   |
| Don’t | Session expired. Please try again.                                                                 |

## Example Ordering and Content

- Show minimal working example first
- Include both request and response
- Annotate key fields with purpose
- Use realistic placeholder values
- Use `curl` for requests and JSON for responses

| Usage | Example                                                        |
| ----- | -------------------------------------------------------------- |
| Do    | Show `curl` request and JSON response with field explanations. |
| Don’t | Show only the endpoint path.                                   |

## Structure & Format for API Reference

| Usage                  | Example                                                |
| ---------------------- | ------------------------------------------------------ |
| Endpoint summaries     | One sentence, purpose-first                            |
| Parameter descriptions | Tables with columns: name, type, required, description |
| Schema descriptions    | Start with what it is, then list constraints           |
| Inline code            | Use backticks for all code terms                       |
| Examples               | Minimal working example first, then variations         |

| Usage | Example                                                           |
| ----- | ----------------------------------------------------------------- |
| Do    | Use tables for parameters with name, type, required, description. |
| Do    | Lead endpoint description with the main action.                   |
| Don’t | Write multi-clause paragraphs for parameters.                     |
| Don’t | Hide requirements in prose.                                       |

## Voice & Tone

- Clarity, warmth, technical confidence
- Tone must be:
  - Friendly, not casual
  - Smart and human
  - Clear and confident
  - Technical but readable

| Usage | Example                                                         |
| ----- | --------------------------------------------------------------- |
| Do    | A POST request to `/orders` creates a new order.                 |
| Do    | Tokens expire after 24 hours. Refresh them before they do.      |
| Don’t | Let's now go ahead and try creating an order!                  |
| Don’t | Developers may want to consider refreshing tokens occasionally. |

## Avoid Marketing or Sales Language

- No promotional or vague language
- Focus on problem-solving and technical clarity

| Usage | Example                                                            |
| ----- | ------------------------------------------------------------------ |
| Do    | You can use this endpoint to check an order's status.             |
| Do    | This endpoint returns the order ID for a successful request.       |
| Don’t | Our powerful API makes ordering a breeze!                          |
| Don’t | Unlock the full potential of your integration.                     |

## Reader Assumptions

- Write for all skill levels
- Provide:
  - Senior engineers: exact definitions
  - Mid-level devs: clear examples
  - Junior devs: enough context to proceed confidently

| Usage | Example                                                        |
| ----- | -------------------------------------------------------------- |
| Do    | Include first-use explanations with request/response examples. |
| Do    | Annotate examples with purpose of each field.                  |
| Don’t | Use unexplained jargon like `idempotent retries`.              |
| Don’t | Show only raw endpoints with no example.                       |

## Callouts in API Reference

- Use callouts for important notices
- BREAKING_CHANGE for breaking changes
- DEPRECATION for deprecations or non-obvious behavior

Example:

```markdown
> DEPRECATION
>
> The `legacy_field` will be removed in API version 2025-01-14.
```

## Do / Don’t Examples

### Endpoint Summary

| Usage | Example                                                                                                               |
| ----- | --------------------------------------------------------------------------------------------------------------------- |
| Do    | Retrieves the status of an order by its `order_id`. Requires API authentication.                                       |
| Don’t | This endpoint will let you check the order status when you have the order ID and API authentication.             |

### Parameter Description

| Usage | Example                                    |
| ----- | ------------------------------------------ |
| Do    | The `total` of the order, in cents.         |
| Don’t | Total for the order.                        |

### Error Message

| Usage | Example                                                                                            |
| ----- | -------------------------------------------------------------------------------------------------- |
| Do    | `Invalid order_id` — The provided `order_id` does not exist. Verify the value and try again. |
| Don’t | Invalid order ID — This order ID is wrong.                                                   |

### Terminology Consistency

| Usage | Example                                                                           |
| ----- | --------------------------------------------------------------------------------- |
| Do    | Always use `Authentication token` unless explicitly referring to OAuth or Bearer. |
| Don’t | Mix `Authentication token`, `OAuth token`, and `Bearer token` interchangeably.    |

### Phrasing Consistency

| Usage | Example                       |
| ----- | ----------------------------- |
| Do    | Expire after 15 minutes       |
| Don’t | Expires after fifteen minutes |
