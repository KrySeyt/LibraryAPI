from dataclasses import asdict
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response

from .schema import UserIn, UserOut, User, LoginData
from .service import UserService
from .security import SESSION_DB, SESSION_EXPIRATION_TIME, hasher, create_session_id
from .dependencies import get_current_user, get_session_id
from ..dependencies import Stub, Dataclass


users_router = APIRouter(tags=["users"], prefix="/users")


@users_router.get("/me", response_model=UserOut)
def get_me(
        current_user: Annotated[User, Depends(get_current_user)]
) -> Dataclass:
    return asdict(current_user)


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
        user_data: LoginData,
        response: Response,
) -> str:

    requested_user = user_service.get_user_by_username(user_data.username)

    if not requested_user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    if not hasher.verify(user_data.password, requested_user.hashed_password):  # type: ignore[no-untyped-call]
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    session_id = create_session_id()
    response.set_cookie(key="Authorization", value=session_id, expires=SESSION_EXPIRATION_TIME)
    SESSION_DB[session_id] = requested_user.id

    return "success"


@users_router.post("/logout")
def logout(
        session_id: Annotated[str, Depends(get_session_id)],
        response: Response,
) -> str:

    response.delete_cookie("Authorization")
    SESSION_DB.delete(session_id)
    
    return "success"

