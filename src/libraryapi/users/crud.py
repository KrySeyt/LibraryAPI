from dataclasses import asdict

from sqlalchemy import select
from sqlalchemy.orm import Session

from . import models
from . import schema


class UserCrud:
    def __init__(self, session: Session) -> None:
        self.db = session

    def get_user_by_id(self, user_id: int) -> models.User | None:
        return self.db.get(models.User, user_id)

    def get_user_by_username(self, username: str) -> models.User | None:
        return self.db.scalar(select(models.User).where(models.User.username == username))

    def create_user(self, user: schema.UserIn) -> models.User:
        user_model = models.User(**asdict(user))

        self.db.add(user_model)

        self.db.commit()
        self.db.refresh(user_model)

        return user_model
