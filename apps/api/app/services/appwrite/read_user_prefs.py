from typing import Any


def read_user_prefs(prefs: Any) -> dict[str, Any]:
    """Return the account preferences as a plain dict, whatever shape the SDK gives us."""
    if isinstance(prefs, dict):
        return prefs
    data = getattr(prefs, "data", None)
    if isinstance(data, dict):
        return data
    dump = getattr(prefs, "model_dump", None)
    if callable(dump):
        dumped = dump()
        nested = dumped.get("data")
        return nested if isinstance(nested, dict) else dumped
    return {}
