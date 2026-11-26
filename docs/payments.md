# Payments

Payments run through Whop. Plans are labels on the Appwrite user (`nextmove`, `urgent`; no label
is Explore), and credits are in `credit_balances`. Only verified Whop webhook events change
either (see the webhook, added in the next step). Starting a checkout never does.

## Products

- Next Move (plan ID `WHOP_<ENV>_PLAN_NEXTMOVE`)
- Urgent (`WHOP_<ENV>_PLAN_URGENT`)
- Top-ups: an inline one-time variant priced from the amount, under the product
  `WHOP_<ENV>_PRODUCT_TOPUP`.

The prices are in `docs/pricing.md`.

## Sandbox and production

`WHOP_ENVIRONMENT` (`sandbox` or `production`) chooses which set of `WHOP_SANDBOX_*` or
`WHOP_PRODUCTION_*` values is used. The two share no accounts, keys, plans, or webhooks. Every
row in `payments` records its `environment`.

## Flow

1. The web app opens `/subscribe?product=nextmove|urgent|topup`.
2. `POST /subscription/checkout` builds the order on the server (price and top-up tier come
   from the catalog and the user's plan), creates a Whop checkout, and records a pending payment.
3. The page mounts Whop Elements' `CheckoutElement`, passing the server-created checkout
   configuration ID to `Checkout`. The card form lives on Whop; we never see card data.
4. A confirmed payment arrives by webhook (next step). The embed's "complete" callback only
   updates the screen.

## Changing a plan by hand

    uv run --project apps/api python scripts/set_user_plan.py <user-id> <explore|nextmove|urgent>

## Trying the provider

    uv run --project apps/api python scripts/whop_smoke_test.py plan_nextmove

## Adding another provider

Write a class in `apps/api/app/services/payments/` with `name`, `environment`, and
`create_checkout(order)`, then add it to `PROVIDERS` in `get_payment_provider.py`.

## Webhook

`POST /webhooks/whop` (hidden from the public docs). Whop signs each event; the API checks the
signature and refuses requests more than 5 minutes off. It acts on `payment.succeeded` for a
payment that is `paid`, and records `payment.failed`.

- Applied once per payment ID, however many times Whop delivers it. Credit grants are also
  protected by unique keys.
- The amount paid (the total without added tax) must be at least what we recorded at checkout.
  Otherwise the payment is stored as `underpaid` and nothing is granted.
- A payment for a deleted account, in another currency, or that disagrees with our record is
  stored as `failed` and nothing is granted.
- A payment without our metadata is acknowledged and ignored.
- Failures return 500 so Whop retries (for about 3 days).

Events to subscribe to: `payment.succeeded`, `payment.failed`, `membership.updated`,
`refund.created`, `refund.updated`.

## Lifecycle

- A renewal payment has no checkout metadata: it is matched through the membership ID stored on
  the subscription row (`providerSubscriptionId`). It resets the monthly credits.
- Only the user's current membership counts. A replaced membership's events are ignored.
- `membership.updated` with `canceled` or `expired` sends the user back to Explore: the monthly
  credits become Explore's, and the welcome bonus and purchased credits are kept.
- A full refund of a top-up takes back its unspent credits (the history says how many were
  already used). A full refund of a plan payment ends the subscription. Partial refunds of a plan
  change nothing.
- An upgrade immediately cancels the replaced membership (needs the `membership:cancel`
  permission on the Whop key).
- `POST /internal/subscription-maintenance` (same token as the cleanup, dry run by default)
  resets Explore's monthly credits every 30 days, ends paid plans 7 days after their period end
  when no renewal arrived, and sends renewal reminders 24 hours before a period ends. Run it
  every 6 hours once deployed.
- `send_notification` is the one place a real notifier plugs in.

## Development with cloudflared

1. `cloudflared tunnel --url http://localhost:8000` prints a `trycloudflare.com` address. It changes every time the tunnel restarts.
2. Create the sandbox webhook (URL `<address>/webhooks/whop`, these events, `api_version_date` `2026-11-20`) with `POST https://sandbox-api.whop.com/api/v1/webhooks`. Keep the returned `webhook_secret` in `.env` as `WHOP_SANDBOX_WEBHOOK_SECRET`.
3. When the address changes, update the URL with `PATCH /webhooks/{id}`.
4. For production, create a separate webhook on the production account with the real domain and put its secret in `WHOP_PRODUCTION_WEBHOOK_SECRET`.

## Testing without paying

    uv run --project apps/api python scripts/send_test_webhook.py succeeded <user-id> topup 5.00

## What users see (Settings)

- Subscription: the plan, "Renews on ..." or "Cancelled: your plan ends on ...", Manage billing
  (the provider's billing page, read on click), and Cancel subscription (ends access immediately;
  no prorated refund is issued).
- Credits and credit history (latest 20), and payments (latest 10, abandoned checkouts hidden).
- After paying, a message confirms the payment by watching our own payment history (the
  webhook records it), on the checkout page and on Settings when the provider redirects back.