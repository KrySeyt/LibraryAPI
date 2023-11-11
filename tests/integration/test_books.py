from fastapi.testclient import TestClient
from libraryapi.main.api import app

client = TestClient(app)


def test_get_book(user):
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


def test_get_books(user):
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


def test_get_user_books(user):
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


def test_add_book(user):
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


def test_update_book(user):
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


def test_delete_book(user):
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
