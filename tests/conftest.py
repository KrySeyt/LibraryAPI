from pytest import fixture
from fastapi.testclient import TestClient

from sqlalchemy import create_engine

from libraryapi.main.api import app
from libraryapi.database import Base
from libraryapi.main.config import get_postgres_config


db_config = get_postgres_config()
engine = create_engine(db_config.url)

client = TestClient(app)


@fixture(scope="function", autouse=True)
def clear_db():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


@fixture
def user():
    input_data = {
        "username": "testusername",
        "password": "123456qwerty"
    }

    response = client.post("/users", json=input_data)
