from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .schema import BookIn, BookOut, Book
from .service import RDBMSBookServiceFactory
from ..dependencies import get_db_stub


router = APIRouter(tags=["books"], prefix="/books")


@router.get("/{book_id}", response_model=BookOut | None)
def get_book(db: Annotated[Session, Depends(get_db_stub)], book_id: int) -> Book | None:
    service = RDBMSBookServiceFactory(db).create_book_service()
    return service.get_book(book_id)


@router.get("/", response_model=list[BookOut])
def get_books(db: Annotated[Session, Depends(get_db_stub)]) -> list[Book]:
    service = RDBMSBookServiceFactory(db).create_book_service()
    return service.get_books()


@router.post("/", response_model=BookOut)
def add_book(db: Annotated[Session, Depends(get_db_stub)], book_in: BookIn) -> Book:
    service = RDBMSBookServiceFactory(db).create_book_service()
    return service.add_book(book_in)
