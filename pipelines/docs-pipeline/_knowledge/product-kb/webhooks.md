# Webhooks

**Fill-in instructions.** List every webhook event. For each one: the event name, when it fires, the payload structure, and which integration types or product tiers receive it.

Ask: "List every webhook event. For each: the event name, when it fires, the payload structure, and which integration types or product tiers receive it."

## Events

FICTIONAL EXAMPLE DATA. Replace these rows.

| Event | Fires when | Payload | Sent to |
|---|---|---|---|
| `order.created` | An order moves from `draft` to `created` | `Order` object | Server API |
| `order.canceled` | An order moves to `canceled` | `Order` object | Server API |
| `invoice.paid` | An invoice moves to `paid` | `Invoice` object | Server API |

Hosted order form integrations do not receive webhooks.
