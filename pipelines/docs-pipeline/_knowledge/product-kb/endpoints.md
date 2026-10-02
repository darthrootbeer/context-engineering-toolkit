# Endpoints

**Fill-in instructions.** List every API endpoint. For each one: the HTTP method and path, required and optional request parameters, the response object and its key fields, and any limits on which integration types can call it.

Ask: "List every API endpoint. For each: the HTTP method and path, required and optional request parameters, the response object and key fields, and any restrictions on which integration types can call it."

## Endpoint list

FICTIONAL EXAMPLE DATA. Replace these rows.

| Method and path | Required parameters | Optional parameters | Returns | Integration types |
|---|---|---|---|---|
| `POST /v1/orders` | `customer_id`, `total` | `currency`, `notes` | `Order` object | Server API, Hosted order form |
| `GET /v1/orders/{order_id}` | `order_id` | none | `Order` object | Server API |
| `POST /v1/orders/{order_id}/cancel` | `order_id` | `reason` | `Order` object with `status` set to `canceled` | Server API |
| `POST /v1/invoices` | `order_id` | `due_date` | `Invoice` object | Server API |

## Limits

FICTIONAL EXAMPLE DATA.

- Rate limit: 100 requests per minute per API key.
- `total` is an integer in cents.
