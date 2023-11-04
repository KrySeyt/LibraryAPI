from datetime import date

from sqlalchemy.orm import Mapped, mapped_column

from ..database import Base


class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str]
    author: Mapped[str]
    genre: Mapped[str]
    release_year: Mapped[date]