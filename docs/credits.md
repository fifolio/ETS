# Credits

A user's credits live in three counters in `credit_balances` (row ID = user ID):
`promotionalCredits`, `subscriptionCredits`, `purchasedCredits`. They are spent in that order.
Every change is also written to `credit_ledger`, which is the history: a negative amount means
a credit was spent.

- Promotional (bonus) and purchased credits never expire.
- Subscription credits are the monthly allowance. At renewal they are reset to the plan's
  allowance (set `ROLL_OVER_SUBSCRIPTION_CREDITS` in `app/constants/credits.py` to add on top
  instead).
- A grant is applied once per `idempotencyKey` (unique index), so a repeated payment
  notification can't grant twice.
- Spending decrements a column atomically with a minimum of 0, so simultaneous requests can't
  spend the same credit twice.
- A new user gets an Explore subscription row and 15 credits the first time credits are needed.

## Scans

A scan costs 1 credit. It is reserved before the AI runs and refunded (with a ledger row) if the
AI fails. A page the user already scanned returns the stored result and costs nothing. With no
credits, `POST /analyze` answers 402.

Account deletion removes balances, the credit history, and the subscription row. Payment
records and testimonials are kept.

To give credits by hand: `uv run --project apps/api python scripts/grant_credits.py <user-id> <promotional|subscription|purchased> <amount>`