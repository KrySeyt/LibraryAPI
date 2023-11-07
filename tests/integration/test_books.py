from fastapi.testclient import TestClient
from libraryapi.main.api import app

client = TestClient(app)


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
    print(response.request.method)
    print(app.router.routes)
    print(response.url)
    print(response.status_code)
    print(response.text)

    assert response.json() == expected_result
    assert not client.get("/books").json()

