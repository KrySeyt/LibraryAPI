from abc import ABC, abstractmethod
from dataclasses import asdict

from sqlalchemy import select
from sqlalchemy.orm import Session
from redis import Redis

from . import models
from . import schema


class UserCrud:
    def __init__(self, session: Session) -> None:
        self.db = session

    def get_user_by_id(self, user_id: int) -> models.User | None:
        return self.db.get(models.User, user_id)

    def make_admin(self, user_id: int) -> models.User | None:
        user = self.get_user_by_id(user_id)

        if not user:
            return None

        user.is_admin = True
        self.db.commit()

        return user

    def get_user_by_username(self, username: str) -> models.User | None:
        return self.db.scalar(select(models.User).where(models.User.username == username))

    def create_user(self, user: schema.UserIn) -> models.User:
        user_model = models.User(**asdict(user))

        self.db.add(user_model)

        self.db.commit()
        self.db.refresh(user_model)

        return user_model


class SessionCrud(ABC):
    @abstractmethod
    def get_user_id(self, token: str) -> int:
        raise NotImplementedError

    @abstractmethod
    def session_exists(self, token: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    def add_session(self, token: str, user_id: int) -> None:
        raise NotImplementedError

    @abstractmethod
    def delete_session(self, token: str) -> None:
        raise NotImplementedError


class RedisSessionCrud(SessionCrud):
    def __init__(self, redis: Redis) -> None:
        self.redis = redis

    def session_exists(self, token: str) -> bool:
        return self.redis.exists(token)  # type: ignore

    def get_user_id(self, token: str) -> int:
        return self.redis[token]  # type: ignore

    def add_session(self, token: str, user_id: int) -> None:
        self.redis[token] = user_id

    def delete_session(self, token: str) -> None:
        self.redis.delete(token)
