from typing import Annotated

from fastapi import APIRouter, Depends

from .schema import BookIn, BookOut, Book
from .service import BookService
from .dependencies import get_book_service_stub


router = APIRouter(tags=["books"], prefix="/books")


@router.get("/{book_id}", response_model=BookOut | None)
def get_book(
        book_service: Annotated[BookService, Depends(get_book_service_stub)],
        book_id: int,
) -> Book | None:

    return book_service.get_book(book_id)


@router.get("/", response_model=list[BookOut])
def get_books(
        book_service: Annotated[BookService, Depends(get_book_service_stub)],
) -> list[Book]:
    return book_service.get_books()


@router.post("/", response_model=BookOut)
def add_book(
        book_service: Annotated[BookService, Depends(get_book_service_stub)],
        book_in: BookIn,
) -> Book:

    return book_service.add_book(book_in)
