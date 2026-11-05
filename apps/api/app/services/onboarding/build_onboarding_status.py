from app.constants.onboarding import ONBOARDING_STEPS
from app.schemas.onboarding_status import OnboardingStatus
from app.services.onboarding.find_next_step import find_next_step
from app.services.profile.missing_profile_fields import missing_profile_fields
from app.types.authenticated_user import AuthenticatedUser


def build_onboarding_status(user: AuthenticatedUser, has_cv: bool) -> OnboardingStatus:
    missing = missing_profile_fields(user.prefs)
    done = {"verify": user.email_verified, "cv": has_cv, "profile": not missing}
    steps = {name: done[name] for name in ONBOARDING_STEPS}
    next_step = find_next_step(steps)
    return OnboardingStatus(
        steps=steps,
        next_step=next_step,
        complete=next_step is None,
        missing_profile_fields=missing,
    )
