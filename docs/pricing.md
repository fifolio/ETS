# Pricing and credits

Owned by the API: `app/constants/plans.py`, `app/constants/topups.py`, `app/constants/credits.py`.
The web app reads the plans and the top-up rules from `GET /plans`. It never has its own copy.

| Plan | Price | Monthly credits |
|---|---|---|
| Explore | free | 15 |
| Next Move | $7 / month | 150 |
| Urgent | $14 / month | 300 |

Every account gets a one-time welcome bonus of 25 credits, whatever the plan. It is never
granted again (unique key `welcome:<user>`), and upgrades, downgrades, and renewals never grant
it.

## Top-ups (same on every plan)

$1.00 = 8 credits, in $0.25 steps (2 credits each), from $3.00 to $50.00. Credits are
calculated from the amount (`cents / 25 * 2`), and the server prices every top-up.

## How credits behave

- Order of use: monthly allowance, then welcome bonus, then purchased credits.
- The monthly allowance resets each billing period and does not roll over. An upgrade replaces
  the leftover with the new allowance; it never stacks.
- Welcome bonus and purchased credits do not expire.
- Top-ups never change the plan or unlock plan features.
- Each grant is applied once per unique key, so repeated notifications can't grant twice.

## Money (estimates: verify)

`uv run --project apps/api python scripts/pricing_report.py` prints cost per credit, fees,
AI cost, margin, and the AI break-even cost for every product. The assumptions at the top of
the script are Whop's card fee (2.7% + $0.30, plus $0.03 for 3D Secure and $0.07 for Radar)
and an AI cost of $0.002 per credit. A subscription credit costs $0.047, a top-up credit
$0.125 (2.7x). The $3 minimum loses about 16% to fees (`TOPUP_MIN_CENTS`).

## Time saved (an estimate)

One scan saves, on average, 5 minutes of reading: a 600-word posting at 0.5 seconds per word
(`apps/api/app/constants/time_saved.py`). Time saved = credits / credits per scan x minutes per
scan. The API serves the numbers in `GET /plans` (`time_saved`); the web app only multiplies.
Plan cards show it per month, and the top-up page shows it for the selected credits.