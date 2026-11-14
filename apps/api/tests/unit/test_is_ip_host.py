import pytest
from app.services.suggestions.is_ip_host import is_ip_host


@pytest.mark.parametrize(
    ("host", "expected"),
    [("192.168.1.1", True), ("::1", True), ("example.com", False), ("999.1.1.1", False)],
)
def test_recognizes_ip_addresses(host, expected):
    assert is_ip_host(host) is expected
