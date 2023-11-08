from uuid import uuid4

from passlib.hash import argon2
from redis import Redis
from ..main.config import get_redis_config


hasher = argon2

redis_host = get_redis_config().host
SESSION_DB = Redis(host=redis_host, port=6379, decode_responses=True)

SESSION_EXPIRATION_TIME = 60 * 60 * 24 * 7


def create_session_id() -> str:
    return str(uuid4())
