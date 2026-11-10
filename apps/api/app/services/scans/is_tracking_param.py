from app.constants.job_url import TRACKING_PARAMS, TRACKING_PREFIXES


def is_tracking_param(name: str) -> bool:
    lowered = name.lower()
    return lowered in TRACKING_PARAMS or lowered.startswith(TRACKING_PREFIXES)
