from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database import Base

if TYPE_CHECKING:
    from ..users.models import User


books_users_purchasers_table = Table(
    "books_users_purchasers",
    Base.metadata,
    Column("book_id", ForeignKey("books.id"), primary_key=True),
    Column("user_id", ForeignKey("users.id"), primary_key=True),
)


class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str]
    author: Mapped[str]
    genre: Mapped[str]
    release_year: Mapped[date]
    verified: Mapped[bool] = mapped_column(default=False)

    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    owner: Mapped["User"] = relationship(back_populates="owned_books")

    purchasers: Mapped[list["User"]] = relationship(
        secondary=books_users_purchasers_table,
        back_populates="purchased_books",
    )
