from appwrite.services.users import Users

from app.services.appwrite.admin_client import admin_client


def get_users() -> Users:
    return Users(admin_client())
