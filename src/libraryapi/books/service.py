from abc import ABC, abstractmethod

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
    def add_book(self, book_in: BookIn) -> Book:
        raise NotImplementedError


class RDBMSBookServiceImp(BookServiceImp):
    def __init__(self, crud: BookCrud) -> None:
        self.crud = crud

    def get_book(self, book_id: int) -> Book | None:
        book_model = self.crud.get_book(book_id)

        if not book_model:
            return None

        return Book.model_validate(book_model)

    def get_books(self) -> list[Book]:
        book_models = self.crud.get_books()
        return [Book.model_validate(model) for model in book_models]

    def add_book(self, book_in: BookIn) -> Book:
        book_model = self.crud.add_book(book_in)
        return Book.model_validate(book_model)


class BookService:
    def __init__(self, implementation: BookServiceImp) -> None:
        self.imp = implementation

    def get_book(self, book_id: int) -> Book | None:
        return self.imp.get_book(book_id)

    def get_books(self) -> list[Book]:
        return self.imp.get_books()

    def add_book(self, book_in: BookIn) -> Book:
        return self.imp.add_book(book_in)


class BookServiceFactory(ABC):
    @abstractmethod
    def create_book_service(self) -> BookService:
        raise NotImplementedError


class RDBMSBookServiceFactory(BookServiceFactory):
    def __init__(self, session: Session) -> None:
        self.session = session

    def create_book_service(self) -> BookService:
        crud = BookCrud(self.session)
        imp = RDBMSBookServiceImp(crud)
        return BookService(imp)
