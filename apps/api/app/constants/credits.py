SPEND_ORDER = ("subscription", "promotional", "purchased")  # promotional = the welcome bonus
WELCOME_CREDITS = 25  # granted once per account, whatever the plan
CREDIT_COLUMNS = {
    "promotional": "promotionalCredits",
    "subscription": "subscriptionCredits",
    "purchased": "purchasedCredits",
}
CREDITS_PER_SCAN = 1
MAX_SPEND_ATTEMPTS = 3  # maximum number of attempts to spend credits before failing the request
# False: unused monthly credits are replaced by the new allowance at renewal.
# True: they stay and the new allowance is added on top.
ROLL_OVER_SUBSCRIPTION_CREDITS = False
