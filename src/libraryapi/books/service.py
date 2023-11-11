from abc import ABC, abstractmethod
from typing import Generator, Callable

from sqlalchemy import Engine
from sqlalchemy.orm import Session

from .schema import Book, BookIn
from .crud import BookCrud


class BookServiceImp(ABC):
    @abstractmethod
    def get_book(self, book_id: int) -> Book | None:
        raise NotImplementedError

    @abstractmethod
    def get_books(self) -> list[Book]:
        raise NotImplementedError

    @abstractmethod
    def get_user_books(self, user_id: int) -> list[Book]:
        raise NotImplementedError

    @abstractmethod
    def add_book(self, book_in: BookIn) -> Book:
        raise NotImplementedError

    @abstractmethod
    def update_book(self, book_id: int, book_in: BookIn) -> Book | None:
        raise NotImplementedError

    @abstractmethod
    def delete_book(self, book_id: int) -> Book | None:
        raise NotImplementedError


class RDBMSBookServiceImp(BookServiceImp):
    def __init__(self, crud: BookCrud) -> None:
        self.crud = crud

    def get_book(self, book_id: int) -> Book | None:
        book_model = self.crud.get_book(book_id)

        if not book_model:
            return None

        return Book.from_object(book_model)

    def get_books(self) -> list[Book]:
        book_models = self.crud.get_books()
        return [Book.from_object(model) for model in book_models]

    def get_user_books(self, user_id: int) -> list[Book]:
        book_models = self.crud.get_user_books(user_id)
        return [Book.from_object(model) for model in book_models]

    def add_book(self, book_in: BookIn) -> Book:
        book_model = self.crud.add_book(book_in)
        return Book.from_object(book_model)

    def update_book(self, book_id: int, book_in: BookIn) -> Book | None:
        book_model = self.crud.update_book(book_id, book_in)

        if not book_model:
            return None

        return Book.from_object(book_model)

    def delete_book(self, book_id: int) -> Book | None:
        book_model = self.crud.delete_book(book_id)

        if not book_model:
            return None

        return Book.from_object(book_model)


class BookService:
    def __init__(self, implementation: BookServiceImp) -> None:
        self.imp = implementation

    def get_book(self, book_id: int) -> Book | None:
        return self.imp.get_book(book_id)

    def get_books(self) -> list[Book]:
        return self.imp.get_books()

    def get_user_books(self, user_id: int) -> list[Book]:
        return self.imp.get_user_books(user_id)

    def add_book(self, book_in: BookIn) -> Book:
        return self.imp.add_book(book_in)

    def update_book(self, book_id: int, book_in: BookIn) -> Book | None:
        return self.imp.update_book(book_id, book_in)

    def delete_book(self, book_id: int) -> Book | None:
        return self.imp.delete_book(book_id)


class BookServiceFactory(ABC):
    @abstractmethod
    def create_book_service(self) -> Generator[BookService, None, None]:
        raise NotImplementedError


class RDBMSBookServiceFactory(BookServiceFactory):
    def __init__(self, engine: Engine, crud_factory: Callable[[Session], BookCrud]) -> None:
        self.engine = engine
        self.crud_factory = crud_factory

    def create_book_service(self) -> Generator[BookService, None, None]:
        with Session(self.engine) as session:
            crud = self.crud_factory(session)
            imp = RDBMSBookServiceImp(crud)
            yield BookService(imp)
