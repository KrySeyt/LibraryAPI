from dataclasses import asdict
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from .schema import BookIn, BookOut
from .service import BookService
from ..dependencies import Stub, Dataclass
from ..users.dependencies import get_current_user
from ..users.schema import User


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


@books_router.get("/user/{user_id}", response_model=list[BookOut])
def get_user_books(
        book_service: Annotated[BookService, Depends(Stub(BookService))],
        user_id: int
) -> list[Dataclass]:

    books = book_service.get_user_books(user_id)
    return [asdict(book) for book in books]


@books_router.post("/", response_model=BookOut, status_code=status.HTTP_201_CREATED)
def add_book(
        book_service: Annotated[BookService, Depends(Stub(BookService))],
        current_user: Annotated[User, Depends(get_current_user)],
        book_in: BookIn,
) -> Dataclass:

    if book_in.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_status.HTTP_403_FORBIDDEN_FORBIDDEN)

    book = book_service.add_book(book_in)
    return asdict(book)


@books_router.put("/{book_id}", response_model=BookOut | None)
def update_book(
        book_service: Annotated[BookService, Depends(Stub(BookService))],
        current_user: Annotated[User, Depends(get_current_user)],
        book_id: int,
        new_book_data: BookIn
) -> Dataclass | None:

    if new_book_data.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    requested_book = book_service.get_book(book_id)

    if requested_book.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    book = book_service.update_book(book_id, new_book_data)
    return asdict(book) if book else None


@books_router.delete("/{book_id}", response_model=BookOut | None)
def delete_book(
        book_service: Annotated[BookService, Depends(Stub(BookService))],
        current_user: Annotated[User, Depends(get_current_user)],
        book_id: int
) -> Dataclass | None:
    book = book_service.get_book(book_id)

    if not book:
        return None

    if book.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    book_service.delete_book(book_id)

    return asdict(book)
