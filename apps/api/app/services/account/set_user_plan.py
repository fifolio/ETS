from app.services.account.labels_for_plan import labels_for_plan
from app.services.appwrite.get_users import get_users


def set_user_plan(user_id: str, plan: str) -> None:
    users = get_users()
    current = list(users.get(user_id=user_id).labels)
    users.update_labels(user_id=user_id, labels=labels_for_plan(current, plan))
