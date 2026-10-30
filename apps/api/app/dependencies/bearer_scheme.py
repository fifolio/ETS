from fastapi.security import HTTPBearer

bearer_scheme = HTTPBearer(auto_error=False, description="Appwrite JWT of the logged-in user")
