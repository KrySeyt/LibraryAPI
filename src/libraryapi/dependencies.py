from typing import Annotated, Generator

from fastapi import Depends
from sqlalchemy import Engine
from sqlalchemy.orm import Session


def get_engine_stub() -> Engine:
    raise NotImplementedError


def get_db_stub() -> Session:
    raise NotImplementedError


def get_db(engine: Annotated[Engine, Depends(get_engine_stub)]) -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
