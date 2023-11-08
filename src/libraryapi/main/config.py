import os
from logging import getLogger
from dataclasses import dataclass

logger = getLogger(__name__)

POSTGRES_URI = "LIBRARYAPI_POSTGRESQL_URI"
REDIS_HOST = "LIBRARYAPI_REDIS_HOST"


class ConfigParseError(ValueError):
    pass


@dataclass
class PostgresConfig:
    url: str


@dataclass
class RedisConfig:
    host: str


def get_env_var(key: str) -> str:
    env_var = os.getenv(key)
    if not env_var:
        logger.error(f"{key} is not set")
        raise ConfigParseError(f"{key} is not set")
    return env_var


def get_postgres_config() -> PostgresConfig:
    db_uri = get_env_var(POSTGRES_URI)
    return PostgresConfig(db_uri)


def get_redis_config() -> RedisConfig:
    redis_host = get_env_var(REDIS_HOST)
    return RedisConfig(redis_host)
