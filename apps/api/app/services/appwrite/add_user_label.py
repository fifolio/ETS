from app.services.appwrite.get_users import get_users


def add_user_label(user_id: str, current_labels: list[str], label: str) -> None:
    """Add a label, keeping the existing ones (Appwrite replaces the whole list)."""
    labels = sorted({*current_labels, label})
    get_users().update_labels(user_id=user_id, labels=labels)
