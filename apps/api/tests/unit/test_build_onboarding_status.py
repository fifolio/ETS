from app.services.onboarding.build_onboarding_status import build_onboarding_status
from app.types.authenticated_user import AuthenticatedUser


def make_user(verified=True, prefs=None):
    return AuthenticatedUser("user-1", "Jane Doe", "jane.doe@example.com", verified, prefs or {})


def test_an_unverified_user_starts_at_verify():
    status = build_onboarding_status(make_user(verified=False), has_cv=False, has_extension=False)

    assert status.next_step == "verify"
    assert status.complete is False


def test_a_verified_user_without_a_cv_goes_to_the_cv_step():
    status = build_onboarding_status(make_user(), has_cv=False, has_extension=False)

    assert status.next_step == "cv"


def test_a_user_with_a_cv_but_no_profile_goes_to_the_profile_step():
    status = build_onboarding_status(make_user(), has_cv=True, has_extension=False)

    assert status.next_step == "profile"
    assert "role" in status.missing_profile_fields


def test_a_finished_profile_leads_to_the_extension_step(complete_prefs):
    user = make_user(prefs=complete_prefs)

    status = build_onboarding_status(user, has_cv=True, has_extension=False)

    assert status.next_step == "extension"
    assert status.complete is False


def test_everything_done_is_complete(complete_prefs):
    user = make_user(prefs=complete_prefs)

    status = build_onboarding_status(user, has_cv=True, has_extension=True)

    assert status.complete is True
    assert status.next_step is None
    assert status.steps == {"verify": True, "cv": True, "profile": True, "extension": True}
