from dataclasses import dataclass
from datetime import date


@dataclass
class BookBase:
    name: str
    author: str
    genre: str
    release_year: date


@dataclass
class Book(BookBase):
    id: int


@dataclass
class BookIn(BookBase):
    pass


@dataclass
class BookOut(BookBase):
    id: int
