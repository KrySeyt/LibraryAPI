import os
from logging import getLogger
from dataclasses import dataclass

logger = getLogger(__name__)

POSTGRES_URI = "LIBRARYAPI_POSTGRESQL_URI"


class ConfigParseError(ValueError):
    pass


@dataclass
class DatabaseConfig:
    uri: str


def get_env_var(key: str) -> str:
    env_var = os.getenv(key)
    if not env_var:
        logger.error(f"{key} is not set")
        raise ConfigParseError(f"{key} is not set")
    return env_var


def get_database_config() -> DatabaseConfig:
    db_uri = get_env_var(POSTGRES_URI)
    return DatabaseConfig(db_uri)
