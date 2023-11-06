from dataclasses import dataclass
from datetime import date


@dataclass
class BookBase:
    name: str
    author: str
    genre: str
    release_year: date

    def __post_init__(self) -> None:
        self.name = self.name.capitalize()
        self.author = self.author.capitalize()
        self.genre = self.genre.capitalize()


@dataclass
class Book(BookBase):
    id: int

    def __post_init__(self) -> None:
        if self.id <= 0:
            raise ValueError


@dataclass
class BookIn(BookBase):
    pass


@dataclass
class BookOut(BookBase):
    id: int

    def __post_init__(self) -> None:
        if self.id <= 0:
            raise ValueError
