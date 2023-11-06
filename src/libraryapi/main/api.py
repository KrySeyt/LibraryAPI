from fastapi import FastAPI
from sqlalchemy import create_engine

from ..books.router import books_router
from ..books.service import RDBMSBookServiceFactory, BookService
from ..books.crud import BookCrud
from .config import get_database_config


def create_app() -> FastAPI:
    db_config = get_database_config()
    engine = create_engine(db_config.uri)

    book_service_factory = RDBMSBookServiceFactory(engine, BookCrud)

    app = FastAPI()
    app.include_router(books_router)

    app.dependency_overrides[BookService] = book_service_factory.create_book_service

    return app


app = create_app()
