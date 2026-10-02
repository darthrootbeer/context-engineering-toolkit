# Domain models

**Fill-in instructions.** Describe every core object in your API. For each one: what it represents, its key fields and types, the states it can be in and how it moves between them, and which other objects it relates to.

Ask: "Describe every core object in the API. For each: what it represents, its key fields and types, the states it can be in and how it moves between them, and which other objects it relates to."

## Objects

FICTIONAL EXAMPLE DATA. Replace these rows.

### Order

An order a customer places. Belongs to one `Customer`. Can have one `Invoice`.

| Field | Type | Notes |
|---|---|---|
| `id` | string | Starts with `ord_` |
| `customer_id` | string | The customer who placed the order |
| `total` | integer | In cents |
| `status` | string | One of `draft`, `created`, `paid`, `canceled` |

States: `draft` to `created` to `paid`. A `draft` or `created` order can move to `canceled`. A `paid` order cannot be canceled.

### Customer

A person or company that places orders. Fields: `id` (starts with `cus_`), `name`, `email`.

### Invoice

A bill for one order. Fields: `id` (starts with `inv_`), `order_id`, `due_date`, `status` (`open` or `paid`).
