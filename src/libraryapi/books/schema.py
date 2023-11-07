from dataclasses import dataclass
from datetime import date


@dataclass
class BookBase:
    name: str
    author: str
    genre: str
    release_year: date

    def __post_init__(self) -> None:
        self.name = f"{self.name[0].capitalize()}{self.name[1:]}"
        self.author = f"{self.author[0].capitalize()}{self.author[1:]}"
        self.genre = f"{self.genre[0].capitalize()}{self.genre[1:]}"


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
