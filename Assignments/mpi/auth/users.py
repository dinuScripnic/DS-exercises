from __future__ import annotations

from schema import User, Role
from authentication import AuthHandler

authHandler = AuthHandler()
db = [
    User(
        username="admin",
        password=authHandler.get_password_hash("admin"),
        role=Role.Administrator,
    ),
    User(
        username="secretary",
        password=authHandler.get_password_hash("secretary"),
        role=Role.Secretary,
    ),
    User(
        username="manager",
        password=authHandler.get_password_hash("manager"),
        role=Role.Manager,
    ),
]


def get_role(username: str) -> Role | None:
    for user in db:
        if user.username == username:
            return user.role


def get_user(username: str) -> User | None:
    for user in db:
        if user.username == username:
            return user
