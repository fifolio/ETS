from app.services.notifications.send_notification import send_notification


def test_the_notification_is_logged_until_a_real_notifier_is_plugged_in(caplog):
    caplog.set_level("INFO")

    send_notification("user-1", "subscription_renewing", {"plan": "nextmove"})

    assert "subscription_renewing" in caplog.text and "user-1" in caplog.text
