from uuid import uuid4

from passlib.hash import argon2


hasher = argon2

SESSION_DB: dict[str, int] = {}

SESSION_EXPIRATION_TIME = 60 * 60 * 24 * 7


def create_session_id() -> str:
    return str(uuid4())
