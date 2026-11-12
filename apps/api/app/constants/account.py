SUBSCRIPTION_PLANS = ("explore", "nextmove", "urgent")
DEFAULT_SUBSCRIPTION = "explore"

# A plan is stored as a label on the user. Explore is the default and has no label.
PLAN_LABELS = ("nextmove", "urgent")

# Labels only the server can set
CV_DONE_LABEL = "cvdone"  # the user has uploaded a valid CV at least once
KEEP_LABEL = "keepaccount"  # never delete this account in the cleanup
FEEDBACK_DONE_LABEL = "feedbackdone"  # the user has sent their feedback
