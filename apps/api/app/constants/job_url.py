# Query parameters that only track where a visitor came from. They don't identify the job.
# Parameters that DO identify a job (like LinkedIn's currentJobId) must never be listed here.
TRACKING_PARAMS = frozenset(
    {
        "fbclid",
        "gclid",
        "msclkid",
        "mc_cid",
        "mc_eid",
        "ref",
        "refid",
        "referrer",
        "trackingid",
        "trk",
        "gh_src",
        "lever-source",
    }
)
TRACKING_PREFIXES = ("utm_",)
DEFAULT_PORTS = {"http": 80, "https": 443}
