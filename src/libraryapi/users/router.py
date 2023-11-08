from dataclasses import asdict
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.hash import argon2

from .schema import UserIn, UserOut
from .service import UserService
from ..dependencies import Stub, Dataclass


users_router = APIRouter(tags=["users"], prefix="/users")
security = OAuth2PasswordBearer(tokenUrl="/login")


@users_router.get("/{user_id}", response_model=UserOut | None)
def get_user(
        user_service: Annotated[UserService, Depends(Stub(UserService))],
        user_id: int
) -> Dataclass | None:

    user = user_service.get_user_by_id(user_id)
    return asdict(user) if user else None


@users_router.post("/", response_model=UserOut)
def register(
        user_service: Annotated[UserService, Depends(Stub(UserService))],
        user_in: UserIn,
) -> Dataclass:

    user = user_service.register(user_in)
    return asdict(user)


@users_router.post("/login")
def login(
        user_service: Annotated[UserService, Depends(Stub(UserService))],
        user_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> dict[str, str]:

    requested_user = user_service.get_user_by_username(user_data.username)

    if not requested_user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    if argon2.verify(user_data.password, requested_user.hashed_password):  # type: ignore[no-untyped-call]
        return {"access_token": user_data.username, "token_type": "bearer"}

    raise HTTPException(status_code=400, detail="Incorrect username or password")

