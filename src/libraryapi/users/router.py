from dataclasses import asdict
from typing import Annotated

from fastapi import APIRouter, Depends

from .schema import UserIn, UserOut
from .service import UserService
from ..dependencies import Stub, Dataclass


users_router = APIRouter(tags=["users"], prefix="/users")


@users_router.get("/{user_id}", response_model=UserOut | None)
def get_user(
        user_service: Annotated[UserService, Depends(Stub(UserService))],
        user_id: int
) -> Dataclass | None:

    user = user_service.get_user(user_id)
    return asdict(user) if user else None


@users_router.post("/", response_model=UserOut)
def register(
        user_service: Annotated[UserService, Depends(Stub(UserService))],
        user_in: UserIn,
) -> Dataclass:

    user = user_service.register(user_in)
    return asdict(user)

