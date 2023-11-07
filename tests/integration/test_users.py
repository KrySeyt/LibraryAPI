from fastapi.testclient import TestClient
from libraryapi.main.api import app


client = TestClient(app)


def test_get_user():
    input_data = {
        "username": "testusername",
        "password": "123456qwerty"
    }

    user_id = client.post("/users", json=input_data).json()["id"]

    expected_result = {
        "id": 1,
        "username": "testusername",
    }

    response = client.get(f"/users/{user_id}")
    assert response.json() == expected_result


def test_register():
    input_data = {
        "username": "testusername",
        "password": "123456qwerty"
    }

    expected_result = {
        "id": 1,
        "username": "testusername",
    }

    response = client.post("/users", json=input_data)

    assert response.json() == expected_result