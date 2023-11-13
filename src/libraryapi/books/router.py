from dataclasses import asdict
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status

from .schema import BookIn, BookOut
from .service import BookService
from ..dependencies import Stub, Dataclass
from ..users.dependencies import get_current_user
from ..users.schema import User


books_router = APIRouter(tags=["books"], prefix="/books")


@books_router.get("/all", response_model=list[BookOut])
def get_books(
        book_service: Annotated[BookService, Depends(Stub(BookService))],
        skip: Annotated[int, Query()],
        limit: Annotated[int, Query()]
) -> list[Dataclass]:

    books = book_service.get_books(skip, limit)
    return [asdict(book) for book in books]


@books_router.get("/verified", response_model=list[BookOut])
def get_verified_books(
        book_service: Annotated[BookService, Depends(Stub(BookService))],
        skip: Annotated[int, Query()],
        limit: Annotated[int, Query()]
) -> list[Dataclass]:

    books = book_service.get_verified_books(skip, limit)
    return [asdict(book) for book in books]


@books_router.get("/{book_id}", response_model=BookOut)
def get_book(
        book_service: Annotated[BookService, Depends(Stub(BookService))],
        book_id: int,
) -> Dataclass:

    book = book_service.get_book(book_id)

    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return asdict(book)


@books_router.get("/user/{user_id}", response_model=list[BookOut])
def get_user_books(
        book_service: Annotated[BookService, Depends(Stub(BookService))],
        user_id: int
) -> list[Dataclass]:

    books = book_service.get_user_books(user_id)
    return [asdict(book) for book in books]


@books_router.get("/purchased/me", response_model=list[BookOut])
def get_my_purchased_books(
        book_service: Annotated[BookService, Depends(Stub(BookService))],
        current_user: Annotated[User, Depends(get_current_user)],
) -> list[Dataclass]:

    books = book_service.get_purchased_books(current_user.id)
    return [asdict(book) for book in books]


@books_router.get("/purchased/{user_id}", response_model=list[BookOut])
def get_purchased_books(
        book_service: Annotated[BookService, Depends(Stub(BookService))],
        user_id: int,
) -> list[Dataclass]:

    books = book_service.get_purchased_books(user_id)
    return [asdict(book) for book in books]


@books_router.post("/verify/{book_id}", response_model=BookOut)
def verify_book(
        book_service: Annotated[BookService, Depends(Stub(BookService))],
        book_id: int,
) -> Dataclass:

    book = book_service.verify_book(book_id)

    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return asdict(book)


@books_router.post("/", response_model=BookOut, status_code=status.HTTP_201_CREATED)
def add_book(
        book_service: Annotated[BookService, Depends(Stub(BookService))],
        current_user: Annotated[User, Depends(get_current_user)],
        book_in: BookIn,
) -> Dataclass:

    if book_in.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    book = book_service.add_book(book_in)
    return asdict(book)


@books_router.post("/purchase/{book_id}", response_model=BookOut, status_code=status.HTTP_201_CREATED)
def purchase_book(
        book_service: Annotated[BookService, Depends(Stub(BookService))],
        current_user: Annotated[User, Depends(get_current_user)],
        book_id: int,
) -> Dataclass:

    book = book_service.add_book_purchaser(book_id, current_user.id)

    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return asdict(book)


@books_router.put("/{book_id}", response_model=BookOut)
def update_book(
        book_service: Annotated[BookService, Depends(Stub(BookService))],
        current_user: Annotated[User, Depends(get_current_user)],
        book_id: int,
        new_book_data: BookIn
) -> Dataclass:

    if new_book_data.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    requested_book = book_service.get_book(book_id)

    if not requested_book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    if requested_book.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    book = book_service.update_book(book_id, new_book_data)

    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return asdict(book)


@books_router.delete("/{book_id}", response_model=BookOut)
def delete_book(
        book_service: Annotated[BookService, Depends(Stub(BookService))],
        current_user: Annotated[User, Depends(get_current_user)],
        book_id: int
) -> Dataclass:

    book = book_service.get_book(book_id)

    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    if book.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    book_service.delete_book(book_id)

    return asdict(book)
