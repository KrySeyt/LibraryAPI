from fastapi.testclient import TestClient
from libraryapi.main.api import app

client = TestClient(app)


def test_get_book(create_user):
    input_data = {
        "name": "string",
        "author": "string",
        "genre": "string",
        "release_year": "2023-11-05",
        "owner_id": 1,
    }

    client.post("/books", json=input_data)

    expected_result = {
        "id": 1,
        "name": "String",
        "author": "String",
        "genre": "String",
        "release_year": "2023-11-05",
        "owner_id": 1,
    }

    response = client.get("/books/1")

    assert response.json() == expected_result


def test_get_books(create_user):
    input_data = {
        "name": "string",
        "author": "string",
        "genre": "string",
        "release_year": "2023-11-05",
        "owner_id": 1,
    }

    for _ in range(10):
        client.post("/books", json=input_data)

    expected_result = [
        {
            "id": i,
            "name": "String",
            "author": "String",
            "genre": "String",
            "release_year": "2023-11-05",
            "owner_id": 1,
        }
        for i in range(1, 11)
    ]

    response = client.get("/books")

    assert response.json() == expected_result


def test_get_user_books(create_user):
    input_data = [
        {
            "name": "string",
            "author": "string",
            "genre": "string",
            "release_year": "2023-11-05",
            "owner_id": 1,
        },
        {
            "name": "string",
            "author": "string",
            "genre": "string",
            "release_year": "2023-11-05",
            "owner_id": 1,
        },
    ]

    for data in input_data:
        client.post("/books", json=data).json()

    expected_result = [
        {
            "name": "String",
            "author": "String",
            "genre": "String",
            "release_year": "2023-11-05",
            "owner_id": 1,
            "id": 1,
        },
        {
            "name": "String",
            "author": "String",
            "genre": "String",
            "release_year": "2023-11-05",
            "owner_id": 1,
            "id": 2
        },
    ]

    response = client.get("/books/user/1")

    assert response.json() == expected_result


def test_add_book(create_user):
    input_data = {
        "name": "string",
        "author": "string",
        "genre": "string",
        "release_year": "2023-11-05",
        "owner_id": 1,
    }

    expected_result = {
        "id": 1,
        "name": "String",
        "author": "String",
        "genre": "String",
        "release_year": "2023-11-05",
        "owner_id": 1,
    }

    response = client.post("/books", json=input_data)

    assert response.json() == expected_result


def test_update_book(create_user):
    input_data = {
        "name": "string",
        "author": "string",
        "genre": "string",
        "release_year": "2023-11-05",
        "owner_id": 1,
    }

    book_id = client.post("/books", json=input_data).json()["id"]

    updated_book = {
        "name": "NewName",
        "author": "String",
        "genre": "newGenre",
        "release_year": "2025-11-05",
        "owner_id": 1,
    }

    expected_result = {
        "id": 1,
        "name": "NewName",
        "author": "String",
        "genre": "NewGenre",
        "release_year": "2025-11-05",
        "owner_id": 1,
    }

    response = client.put(f"/books/{book_id}", json=updated_book)

    assert response.json() == expected_result


def test_delete_book():
    input_user_data = {
        "username": "testusername",
        "password": "123456qwerty"
    }

    client.post("/users", json=input_user_data)
    client.post("/users/login", json=input_user_data)

    input_data = {
        "name": "string",
        "author": "string",
        "genre": "string",
        "release_year": "2023-11-05",
        "owner_id": 1,
    }

    book_id = client.post("/books", json=input_data).json()["id"]

    expected_result = {
        "id": 1,
        "name": "String",
        "author": "String",
        "genre": "String",
        "release_year": "2023-11-05",
        "owner_id": 1,
    }

    response = client.delete(f"/books/{book_id}")

    assert response.json() == expected_result
    assert not client.get("/books").json()


def test_delete_book_without_permission(create_user):
    user2_data = {
        "username": "user",
        "password": "password"
    }

    current_user = client.post("/users", json=user2_data).json()
    assert current_user["id"] != 1

    book_input_data = {
        "name": "string",
        "author": "string",
        "genre": "string",
        "release_year": "2023-11-05",
        "owner_id": 1,
    }

    expected_result = {
        "name": "String",
        "author": "String",
        "genre": "String",
        "release_year": "2023-11-05",
        "owner_id": 1,
        "id": 1,
    }

    book_id = client.post("/books", json=book_input_data).json()["id"]

    client.post("/users/login", json=user2_data)
    response = client.delete(f"/books/{book_id}")

    assert client.get("/books/1").json() == expected_result
    assert response.status_code == 403
