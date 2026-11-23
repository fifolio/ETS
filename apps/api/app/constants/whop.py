# environment -> (API base, checkout host). The two share no accounts, keys, or plans.
WHOP_ENVIRONMENTS = {
    "sandbox": ("https://sandbox-api.whop.com/api/v1", "https://sandbox.whop.com"),
    "production": ("https://api.whop.com/api/v1", "https://whop.com"),
}
WHOP_SKUS = ("plan_nextmove", "plan_urgent")
WHOP_TIMEOUT_SECONDS = 15
