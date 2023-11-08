from typing import Annotated

from fastapi import Depends, HTTPException, status, Request

from .schema import User
from .service import UserService
from .security import SESSION_DB
from ..dependencies import Stub


def get_session_id(request: Request) -> str:
    session_id = request.cookies.get("Authorization")

    if not session_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return session_id


def get_current_user(
        user_service: Annotated[UserService, Depends(Stub(UserService))],
        session_id: Annotated[str, Depends(get_session_id)]
) -> User:

    if not SESSION_DB.exists(session_id):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_id = SESSION_DB.get(session_id)
    user = user_service.get_user_by_id(user_id)  # type: ignore

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user
