import app.services.payments.cancel_replaced_membership as module


class FakeProvider:
    def __init__(self, error=None):
        self.error = error
        self.cancelled = []

    def cancel_subscription(self, subscription_id):
        if self.error:
            raise self.error
        self.cancelled.append(subscription_id)


def test_cancels_the_membership_with_the_provider(monkeypatch):
    provider = FakeProvider()
    monkeypatch.setattr(module, "get_payment_provider", lambda: provider)

    module.cancel_replaced_membership("mem_old")

    assert provider.cancelled == ["mem_old"]


def test_a_provider_failure_is_logged_and_never_raised(monkeypatch, caplog):
    monkeypatch.setattr(module, "get_payment_provider", lambda: FakeProvider(RuntimeError("down")))

    module.cancel_replaced_membership("mem_old")

    assert "billed twice" in caplog.text


def test_a_missing_provider_configuration_never_raises(monkeypatch):
    def fail():
        raise RuntimeError("Unknown PAYMENT_PROVIDER")

    monkeypatch.setattr(module, "get_payment_provider", fail)

    module.cancel_replaced_membership("mem_old")
