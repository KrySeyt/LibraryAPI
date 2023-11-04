from sqlalchemy.orm import Session
from sqlalchemy import select

from . import models
from . import schema


class BookCrud:
    def __init__(self, session: Session) -> None:
        self.db = session

    def get_book(self, book_id: int) -> models.Book | None:
        return self.db.get(models.Book, book_id)

    def get_books(self) -> list[models.Book]:
        return list(self.db.scalars(select(models.Book)).all())

    def add_book(self, book_in: schema.BookIn) -> models.Book:
        book = models.Book(**book_in.model_dump())
        self.db.add(book)
        self.db.commit()
        return book
