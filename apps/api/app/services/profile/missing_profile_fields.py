from typing import Any

from app.constants.profile import EMPLOYMENT_TYPES, SENIORITY_LEVELS, WORK_ARRANGEMENTS
from app.services.profile.is_filled_list import is_filled_list
from app.services.profile.is_filled_text import is_filled_text
from app.services.profile.is_valid_rate import is_valid_rate
from app.services.profile.is_valid_years import is_valid_years


def missing_profile_fields(prefs: dict[str, Any]) -> list[str]:
    """Names of the required profile answers that are missing or invalid."""
    checks = {
        "industryId": is_filled_text(prefs.get("industryId")),
        "jobId": is_filled_text(prefs.get("jobId")),
        "role": is_filled_text(prefs.get("role")),
        "hourlyRateUsd": is_valid_rate(prefs.get("hourlyRateUsd")),
        "seniority": prefs.get("seniority") in SENIORITY_LEVELS,
        "yearsOfExperience": is_valid_years(prefs.get("yearsOfExperience")),
        "currentLocation": is_filled_text(prefs.get("currentLocation")),
        "desiredLocations": is_filled_list(prefs.get("desiredLocations")),
        "workArrangements": is_filled_list(prefs.get("workArrangements"), WORK_ARRANGEMENTS),
        "employmentTypes": is_filled_list(prefs.get("employmentTypes"), EMPLOYMENT_TYPES),
    }
    return [name for name, ok in checks.items() if not ok]
