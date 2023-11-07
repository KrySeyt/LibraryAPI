from dataclasses import asdict

from sqlalchemy.orm import Session

from . import models
from . import schema


class UserCrud:
    def __init__(self, session: Session) -> None:
        self.db = session

    def get_user(self, user_id: int) -> models.User | None:
        return self.db.get(models.User, user_id)

    def create_user(self, user: schema.UserIn) -> models.User:
        user_model = models.User(**asdict(user))

        self.db.add(user_model)

        self.db.commit()
        self.db.refresh(user_model)

        return user_model
