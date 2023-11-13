from dataclasses import asdict

from sqlalchemy.orm import Session
from sqlalchemy import select, desc, insert

from . import models
from . import schema


class BookCrud:
    def __init__(self, session: Session) -> None:
        self.db = session

    def get_book(self, book_id: int) -> models.Book | None:
        return self.db.get(models.Book, book_id)

    def get_books(self, skip: int, limit: int) -> list[models.Book]:
        stmt = select(models.Book).order_by(desc(models.Book.id)).offset(skip).limit(limit)
        return list(self.db.scalars(stmt).all())

    def get_verified_books(self, skip: int, limit: int) -> list[models.Book]:
        stmt = (select(models.Book).where(models.Book.verified == True).  # noqa E712
                offset(skip).limit(limit).order_by(desc(models.Book.id)))

        return list(self.db.scalars(stmt).all())

    def get_user_books(self, user_id: int) -> list[models.Book]:
        stmt = select(models.Book).where(models.Book.owner_id == user_id)
        return list(self.db.scalars(stmt).all())

    def get_purchased_books(self, user_id: int) -> list[models.Book]:
        stmt = select(models.Book).join(models.books_users_purchasers_table).where(models.books_users_purchasers_table.columns.user_id == user_id)
        return list(self.db.scalars(stmt).all())

    def verify_book(self, book_id: int) -> models.Book | None:
        book = self.get_book(book_id)

        if not book:
            return None

        book.verified = True
        self.db.commit()

        return book

    def add_book(self, book_in: schema.BookIn) -> models.Book:
        book = models.Book(**asdict(book_in))
        self.db.add(book)
        self.db.commit()
        self.db.refresh(book)
        return book

    def add_book_purchaser(self, book_id: int, user_id: int) -> models.Book | None:
        book = self.get_book(book_id)

        if not book:
            return None

        stmt = insert(models.books_users_purchasers_table).values(book_id=book_id, user_id=user_id)
        self.db.execute(stmt)

        self.db.commit()
        self.db.refresh(book)

        return book

    def update_book(self, book_id: int, book_in: schema.BookIn) -> models.Book | None:
        book = self.get_book(book_id)

        if not book:
            return None

        book_in_as_dict = asdict(book_in)
        for field in book_in_as_dict:
            setattr(book, field, book_in_as_dict[field])

        self.db.commit()
        self.db.refresh(book)
        
        return book

    def delete_book(self, book_id: int) -> models.Book | None:
        book = self.get_book(book_id)

        if not book:
            return None

        self.db.delete(book)
        self.db.commit()

        return book
