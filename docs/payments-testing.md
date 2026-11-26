# Payment test pass (Whop sandbox)

Before you start: `uv run --project apps/api python scripts/check_payments_setup.py --live`
must end with "All checks passed". Open the three printed checkout addresses to see Whop's
sandbox checkout (do not pay yet).

`send` below means `uv run --project apps/api python scripts/send_test_webhook.py`.

## A. The webhook

| # | Do | Expect |
|---|---|---|
| A1 | Whop sandbox dashboard, your webhook, send a test event | Delivery 200, result `ignored` |
| A2 | `curl -X POST localhost:8000/webhooks/whop -d '{}'` | 400 |
| A3 | Unset `WHOP_SANDBOX_WEBHOOK_SECRET`, restart, send any event | 503. Restore it |
| A4 | Change the tunnel, update the webhook URL with `PATCH /webhooks/{id}` | Events arrive again |

## B. Paying

| # | Do | Expect |
|---|---|---|
| B1 | Buy a $3 top-up in the web app (the minimum) | "We are confirming..." then "confirmed". Purchased +24, ledger `topup:pay_...`, payment `completed` |
| B2 | Buy a $12.75 top-up | +102 credits (12.75 / 0.25 x 2) |
| B3 | Subscribe to Next Move | Label `nextmove`, 150 monthly + 25 welcome (not stacked with the 15), subscription row `active` with a membership ID |
| B4 | Pay with the sandbox declined test card | Payment `failed`, plan and credits unchanged |
| B5 | Open a $5 top-up checkout, don't pay. `send succeeded USER topup 4.00 pay_test_under <providerCheckoutId>` | `underpaid`, nothing granted |
| B6 | Replay a delivery from the Whop dashboard (or send the same payment ID twice) | `duplicate`, nothing changes |
| B7 | `send succeeded USER topup 1.00` | `invalid_amount` (below the $3 minimum) |
| B8 | `send succeeded no-such-user topup 5.00` | `unknown_user`, no credit rows created |
| B9 | `send succeeded USER plan_nextmove 5.00` | `underpaid` ($7 expected) |

## C. The subscription

| # | Do | Expect |
|---|---|---|
| C1 | Spend a few credits, then `send renewal <membershipId> 7.00` | Monthly credits back to exactly 150, answer `applied`. Same payment ID again: `duplicate` |
| C2 | Settings, Cancel subscription | "Cancelled: your plan ends on ...". Whop shows it cancelling. Plan stays Next Move |
| C3 | Manage billing, undo the cancellation on Whop | Within seconds the row has `cancelAtPeriodEnd: false` again |
| C4 | Cancel again, then `send membership <membershipId> canceled` | Plan Explore, monthly 15, welcome bonus and purchased credits kept |
| C5 | Subscribe to Next Move, then to Urgent | Settings says Urgent, 300 monthly, no second welcome bonus. In Whop the Next Move membership is set to cancel at period end |
| C6 | `send membership <old Next Move membership> canceled` | `ignored`: the plan stays Urgent |

## D. Refunds

| # | Do | Expect |
|---|---|---|
| D1 | Refund the $3 top-up from the Whop dashboard | Its unspent credits are taken back, payment `refunded` |
| D2 | Spend some of a top-up's credits, then refund it | Only the unspent ones come back; the ledger says "N already used" |
| D3 | Partially refund a top-up | Proportional credits taken back, payment stays `completed` |
| D4 | Fully refund the plan payment | The subscription ends: Explore, welcome and purchased credits kept |

## E. Maintenance (`curl -X POST ".../internal/subscription-maintenance" -H "X-Cleanup-Token: $CLEANUP_TOKEN"`, dry run first)

| # | Set in the Appwrite console | Expect after `?dry_run=false` |
|---|---|---|
| E1 | An Explore user's `creditsRenewedAt` 40 days ago | Credits reset to 15 (no stacking) |
| E2 | A paid user's `currentPeriodEnd` 10 days ago | Back to Explore |
| E3 | A paid user's `currentPeriodEnd` 12 hours from now | Log line "Notification subscription_renewing", `renewalReminderSentAt` set. A second run does nothing |

## F. Accounts

| # | Do | Expect |
|---|---|---|
| F1 | Delete an account that has a renewing paid plan | Refused: cancel the subscription first |
| F2 | Cancel it, then delete | Deleted. The payment records stay |
| F3 | Stop Appwrite access briefly and send a payment event | 500. Restore access: Whop's retry (or a replay) applies it once |

Every row should end with the right numbers in `credit_balances`, `credit_ledger`,
`subscriptions`, and `payments`. If one doesn't, copy the API log line and the row.