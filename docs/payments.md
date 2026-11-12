# Payments

Plans are stored as labels on the Appwrite user: `nextmove` and `urgent`. No label means
Explore. Only the server can set labels, so users can't upgrade themselves.

The plan catalog (names, job board limits, prices) is `apps/api/app/constants/plans.py`.

## How a payment provider plugs in

1. Write a class in `apps/api/app/services/payments/` that follows the `PaymentProvider`
   contract in `app/types/payment_provider.py`: start a checkout, and read the provider's
   webhook.
2. Add one line to `PROVIDERS` in `get_payment_provider.py`.
3. Set `PAYMENT_PROVIDER=<name>` and the provider's keys in `.env`.
4. After a successful payment, the webhook handler calls `set_user_plan(user_id, plan)`.

With `PAYMENT_PROVIDER=none` (the default), the upgrade buttons are shown but disabled.

## Changing a plan by hand

    uv run --project apps/api python scripts/set_user_plan.py <user-id> <explore|nextmove|urgent>