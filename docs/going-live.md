# Going live with Whop

Do this only after `docs/payments-testing.md` passes in the sandbox.

1. **Decide where production data lives.** Use a separate Appwrite project (or database) for
   production. If you reuse the sandbox one, first delete the test users and the `payments`
   rows whose `environment` is `sandbox`.
2. **Whop production account.** Complete the business and identity verification and add a
   payout method. Check that Whop pays out to your country before launching.
3. **Create the same products in production:** Next Move ($7 monthly), Urgent ($14 monthly),
   both in USD, and a product named ETS Credits. Copy their IDs.
4. **Create a production API key** that can create and read checkouts, read and cancel
   memberships, and manage webhooks.
5. **Set the production values** (never reuse the sandbox ones; the names are different on
   purpose): `WHOP_PRODUCTION_API_KEY`, `WHOP_PRODUCTION_PLAN_NEXTMOVE`,
   `WHOP_PRODUCTION_PLAN_URGENT`, `WHOP_PRODUCTION_PRODUCT_TOPUP`. Then
   `PAYMENT_PROVIDER=whop`, `WHOP_ENVIRONMENT=production`,
   `PAYMENT_SUCCESS_URL=https://<your domain>/settings?payment_result=success`, a long random
   `CLEANUP_TOKEN`, and CORS for your domain. In the web app: `NEXT_PUBLIC_API_URL` and
   `NEXT_PUBLIC_DEV_TOOLS=false`.
6. **Create the production webhook** with the real domain (not a tunnel):
       curl -X POST "https://api.whop.com/api/v1/webhooks" \
         -H "Authorization: Bearer $WHOP_PRODUCTION_API_KEY" -H "Content-Type: application/json" \
         -d '{"url":"https://<your domain>/webhooks/whop","events":["payment.succeeded","payment.failed","membership.updated","refund.created","refund.updated"],"api_version_date":"2026-11-20"}'
   Keep the returned secret as `WHOP_PRODUCTION_WEBHOOK_SECRET`.
7. **Preflight:** `uv run --project apps/api python scripts/check_payments_setup.py --live`
   with the production values. Open the printed checkouts but don't pay.
8. **A real-money test with your own card:** buy the $3 top-up, check the credits, refund it in
   the Whop dashboard, check they come back (the processing fee is not returned: about $0.38).
   Then buy Next Move, cancel it in Settings, refund it, and check you are back on Explore.
9. **Turn on maintenance:** set the repository variable `API_URL` and the secret
   `CLEANUP_TOKEN` in GitHub. Run the workflow once by hand (dry run).
10. **Watch it:** Whop emails you when webhook deliveries fail. Check the API logs for
    "was not applied" and "may be billed twice", and look at `payments` rows that are `failed`
    or `underpaid`.
11. **Pages and tax:** publish terms, a privacy policy, a refund policy, and a contact address,
    and check how Whop handles sales tax for your buyers' countries.

## Switching payments off in an emergency

Set `PAYMENT_PROVIDER=none` and restart: checkout is refused and the buttons are disabled.
The webhook keeps applying payments that were already in flight.