from typing import Type

from passlib.ifc import PasswordHash

from libraryapi.users.dependencies import get_user_in
from libraryapi.users.schema import RawUserIn
from libraryapi.users.service import UserService


def create_admin(service: UserService, password_hasher: Type[PasswordHash]) -> None:
    raw_user = RawUserIn(username="admin", password="admin")
    user = get_user_in(password_hasher, raw_user)
    registered_user = service.register(user)
    service.make_admin(registered_user.id)
