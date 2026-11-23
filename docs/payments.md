# Payments

Payments run through Whop. Plans are labels on the Appwrite user (`nextmove`, `urgent`; no label
is Explore), and credits are in `credit_balances`. Only verified payment confirmations change
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