from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database import Base

if TYPE_CHECKING:
    from ..books.models import Book


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)

    username: Mapped[str]
    hashed_password: Mapped[str]

    owned_books: Mapped[list["Book"]] = relationship(back_populates="owner")

    purchased_books: Mapped[list["Book"]] = relationship(
        secondary="books_users",
        back_populates="purchasers",
    )
