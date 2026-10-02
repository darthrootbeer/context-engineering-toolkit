<!-- FICTIONAL EXAMPLE DATA: a made-up doc about a made-up product, used to try out the docs-pipeline. -->

# Canceling orders in Acme Orders

Let's dive in! In this guide, we will explore the exciting world of canceling orders with the Acme Orders API. It's a robust, powerful way to manage your customers' orders — and it's easier than you might think.

## What a cancellation is

A cancellation moves an order to the `canceled` status. Acme Orders keeps the order record so that you can still look it up later, and it releases any stock that was reserved for the order. Cancellations exist because customers change their minds, and because the same order record is used for invoicing, so a clean status trail matters.

You can cancel any order, even one that has already been paid. Paid orders are refunded automatically.

## How to cancel an order

1. Find the `order_id` of the order you want to cancel.
2. Send a request to `POST /v1/orders/{order_id}/cancel`.
3. Check that the response has `status` set to `canceled`.

Here is an example request:

```bash
curl -X POST https://api.example.com/v1/orders/ord_123/cancel \
  -H 'Authorization: Bearer YOUR_API_KEY' \
  -d '{"reason":"customer_request"}'
```

If the order id is wrong, the API returns an error. The error is 404 and the code is `invalid_order_id`.

## Webhooks

Every integration type receives the `order.canceled` webhook, including the hosted order form. The webhook is sent when an order moves to `canceled`.

## Things to know

The API is rate limited, so don't send more than a thousand cancellation requests in a minute. Utilize the `reason` field to record why an order was canceled, as it is helpful for reporting purposes.
