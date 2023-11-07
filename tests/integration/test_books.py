from fastapi.testclient import TestClient
from libraryapi.main.api import app


client = TestClient(app)


def test_get_book():
    input_data = {
        "name": "string",
        "author": "string",
        "genre": "string",
        "release_year": "2023-11-05"
    }

    client.post("/books", json=input_data)

    expected_result = {
        "id": 1,
        "name": "String",
        "author": "String",
        "genre": "String",
        "release_year": "2023-11-05"
    }

    response = client.get("/books/1")

    assert response.json() == expected_result


def test_get_books():
    input_data = {
        "name": "string",
        "author": "string",
        "genre": "string",
        "release_year": "2023-11-05"
    }

    for _ in range(10):
        client.post("/books", json=input_data)

    expected_result = [
        {
            "id": i,
            "name": "String",
            "author": "String",
            "genre": "String",
            "release_year": "2023-11-05"
        }
        for i in range(1, 11)
    ]

    response = client.get("/books")

    assert response.json() == expected_result


def test_add_book():
    input_data = {
        "name": "string",
        "author": "string",
        "genre": "string",
        "release_year": "2023-11-05"
    }

    expected_result = {
        "id": 1,
        "name": "String",
        "author": "String",
        "genre": "String",
        "release_year": "2023-11-05"
    }

    response = client.post("/books", json=input_data)

    assert response.json() == expected_result


def test_update_book():
    input_data = {
        "name": "string",
        "author": "string",
        "genre": "string",
        "release_year": "2023-11-05"
    }

    book_id = client.post("/books", json=input_data).json()["id"]

    updated_book = {
        "name": "NewName",
        "author": "String",
        "genre": "newGenre",
        "release_year": "2025-11-05"
    }

    expected_result = {
        "id": 1,
        "name": "NewName",
        "author": "String",
        "genre": "NewGenre",
        "release_year": "2025-11-05"
    }

    response = client.put(f"/books/{book_id}", json=updated_book)

    assert response.json() == expected_result


def test_delete_book():
    input_data = {
        "name": "string",
        "author": "string",
        "genre": "string",
        "release_year": "2023-11-05"
    }

    book_id = client.post("/books", json=input_data).json()["id"]

    expected_result = {
        "id": 1,
        "name": "String",
        "author": "String",
        "genre": "String",
        "release_year": "2023-11-05"
    }

    response = client.delete(f"/books/{book_id}")

    assert response.json() == expected_result
    assert not client.get("/books").json()

