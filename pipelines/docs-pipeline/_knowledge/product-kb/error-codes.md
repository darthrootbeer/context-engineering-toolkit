# Error codes

**Fill-in instructions.** List every error code or error type your API returns. For each one: the code, when it fires, what it means to a developer, and how your docs should describe it.

Ask: "List every error code or error type the API returns. For each: the code, when it fires, what it means to a developer, and how our docs should describe it."

## Codes

FICTIONAL EXAMPLE DATA. Replace these rows.

| Code | HTTP status | Fires when | How docs describe it |
|---|---|---|---|
| `invalid_order_id` | 404 | The `order_id` does not exist | "The provided `order_id` does not exist. Verify the value and try again." |
| `order_not_cancelable` | 409 | The order is already `paid` | "A paid order cannot be canceled. Create a credit note instead." |
| `rate_limited` | 429 | More than 100 requests in a minute | "Too many requests. Wait and retry." |
