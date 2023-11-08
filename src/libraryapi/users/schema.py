from dataclasses import dataclass, InitVar, field

from passlib.hash import argon2

from ..schema import BaseSchema


@dataclass
class UserBase(BaseSchema):
    username: str


@dataclass
class User(UserBase):
    id: int
    hashed_password: str


@dataclass
class UserIn(UserBase):
    hashed_password: str = field(init=False)
    password: InitVar[str]

    def __post_init__(self, password: str) -> None:
        if not password:
            raise ValueError("No password")

        self.hashed_password = argon2.hash(password)  # type: ignore[no-untyped-call]


@dataclass
class UserOut(UserBase):
    id: int
