from dataclasses import dataclass


@dataclass(frozen=True)
class AuthenticatedUser:
    id: str
    name: str
    email: str
