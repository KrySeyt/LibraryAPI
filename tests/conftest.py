import passlib.hash
from pytest import fixture
from fastapi.testclient import TestClient

from sqlalchemy import create_engine

from libraryapi.main.api import app
from libraryapi.main.common import create_admin
from libraryapi.database import Base
from libraryapi.main.config import get_postgres_config
from libraryapi.users.service import RDBMSUserServiceFactory
from libraryapi.users.crud import UserCrud


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
def admin() -> dict[str, str]:
    admin_data = {
        "username": "admin",
        "password": "admin"
    }

    return admin_data


@fixture()
def client() -> TestClient:
    return TestClient(app)


@fixture
def authorized_client(user) -> TestClient:
    client = TestClient(app)
    client.post("/users/login", json=user)
    return client


@fixture
def admin_client(admin) -> TestClient:
    hasher = passlib.hash.argon2
    service = next(RDBMSUserServiceFactory(engine, UserCrud).create_user_service())

    create_admin(service, hasher)
    client = TestClient(app)

    response = client.post("/users/login", json=admin)
    assert response.status_code == 200

    return client
