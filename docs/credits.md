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