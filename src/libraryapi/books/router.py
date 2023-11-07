from dataclasses import asdict
from typing import Annotated

from fastapi import APIRouter, Depends

from .schema import BookIn, BookOut
from .service import BookService
from ..dependencies import Stub, Dataclass


books_router = APIRouter(tags=["books"], prefix="/books")


@books_router.get("/{book_id}", response_model=BookOut | None)
def get_book(
        book_service: Annotated[BookService, Depends(Stub(BookService))],
        book_id: int,
) -> Dataclass | None:

    book = book_service.get_book(book_id)
    return asdict(book) if book else None


@books_router.get("/", response_model=list[BookOut])
def get_books(
        book_service: Annotated[BookService, Depends(Stub(BookService))],
) -> list[Dataclass]:

    books = book_service.get_books()
    return [asdict(book) for book in books]


@books_router.post("/", response_model=BookOut)
def add_book(
        book_service: Annotated[BookService, Depends(Stub(BookService))],
        book_in: BookIn,
) -> Dataclass:

    book = book_service.add_book(book_in)
    return asdict(book)


@books_router.put("/{book_id}", response_model=BookOut | None)
def update_book(
        book_service: Annotated[BookService, Depends(Stub(BookService))],
        book_id: int,
        new_book_data: BookIn
) -> Dataclass | None:

    book = book_service.update_book(book_id, new_book_data)
    return asdict(book) if book else None


@books_router.delete("/{book_id}", response_model=BookOut | None)
def delete_book(
        book_service: Annotated[BookService, Depends(Stub(BookService))],
        book_id: int
) -> Dataclass | None:

    book = book_service.delete_book(book_id)
    return asdict(book) if book else None
