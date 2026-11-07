def find_orphan_user_ids(existing_ids: set[str], owner_ids: set[str]) -> list[str]:
    """Owners of stored data whose account no longer exists."""
    return sorted(owner_ids - existing_ids)
