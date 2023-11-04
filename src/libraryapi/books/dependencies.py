from typing import Annotated

from sqlalchemy.orm import Session
from fastapi import Depends

from .service import BookService, RDBMSBookServiceFactory, BookServiceFactory
from ..dependencies import get_db_stub


def get_book_service_stub() -> None:
    raise NotImplementedError


def get_book_service_factory(db: Annotated[Session, Depends(get_db_stub)]) -> BookServiceFactory:
    return RDBMSBookServiceFactory(db)


def get_book_service(service_factory: Annotated[BookServiceFactory, Depends(get_book_service_factory)]) -> BookService:
    return service_factory.create_book_service()
