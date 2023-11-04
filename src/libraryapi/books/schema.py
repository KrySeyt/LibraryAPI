from datetime import date

from pydantic import BaseModel, field_validator


class BookBase(BaseModel):
    name: str
    author: str
    genre: str
    release_year: date

    @field_validator("name", "author", "genre")
    @classmethod
    def capitalize(cls, value: str) -> str:
        return value.capitalize()

    class Config:
        from_attributes = True


class Book(BookBase):
    id: int


class BookIn(BookBase):
    pass


class BookOut(BookBase):
    id: int
