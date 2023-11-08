from pytest import fixture

from sqlalchemy import create_engine

from libraryapi.database import Base
from libraryapi.main.config import get_postgres_config


db_config = get_postgres_config()
engine = create_engine(db_config.url)


@fixture(scope="function", autouse=True)
def clear_db():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
