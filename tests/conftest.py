from pytest import fixture
from fastapi.testclient import TestClient

from sqlalchemy import create_engine

from libraryapi.main.api import app
from libraryapi.database import Base
from libraryapi.main.config import get_postgres_config


db_config = get_postgres_config()
engine = create_engine(db_config.url)


@fixture(scope="function", autouse=True)
def clear_db():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


@fixture
def user(client) -> dict[str, str]:
    input_data = {
        "username": "testusername",
        "password": "123456qwerty"
    }

    client.post("/users", json=input_data)

    return input_data


@fixture
def authorized_client(user) -> TestClient:
    client = TestClient(app)
    client.post("/users/login", json=user)
    return client


@fixture()
def client() -> TestClient:
    return TestClient(app)
