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
    password: InitVar[str]
    hashed_password: str = field(init=False)

    def __post_init__(self, password: str) -> None:
        self.hashed_password = argon2.hash(password)  # type: ignore[no-untyped-call]


@dataclass
class UserOut(UserBase):
    id: int
