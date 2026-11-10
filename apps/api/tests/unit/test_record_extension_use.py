import app.services.extensions.record_extension_use as module


def test_nothing_happens_without_an_install_id(monkeypatch):
    def fail(*args):
        raise AssertionError("must not be called")

    monkeypatch.setattr(module, "touch_extension", fail)

    module.record_extension_use("user-1", None, counted=True)
    module.record_extension_use("user-1", "", counted=True)


def test_passes_the_use_on(monkeypatch):
    calls = []
    monkeypatch.setattr(module, "touch_extension", lambda *args: calls.append(args))

    module.record_extension_use("user-1", "install-12345678", counted=True)

    assert calls == [("user-1", "install-12345678", True)]


def test_a_failure_never_escapes(monkeypatch):
    def fail(*args):
        raise RuntimeError("table down")

    monkeypatch.setattr(module, "touch_extension", fail)

    module.record_extension_use("user-1", "install-12345678", counted=False)
