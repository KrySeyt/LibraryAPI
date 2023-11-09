from fastapi import FastAPI
from sqlalchemy import create_engine
from passlib.ifc import PasswordHash
from passlib.hash import argon2
from redis import Redis

from ..books.router import books_router
from ..users.router import users_router
from ..books.service import RDBMSBookServiceFactory, BookService
from ..users.service import RDBMSUserServiceFactory, UserService
from ..books.crud import BookCrud
from ..users.crud import UserCrud, RedisSessionCrud
from ..users.security import SessionProvider
from .config import get_postgres_config, get_redis_config


def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(books_router)
    app.include_router(users_router)

    postgres_config = get_postgres_config()
    engine = create_engine(postgres_config.url)

    book_service_factory = RDBMSBookServiceFactory(engine, BookCrud)
    app.dependency_overrides[BookService] = book_service_factory.create_book_service

    user_service_factory = RDBMSUserServiceFactory(engine, UserCrud)
    app.dependency_overrides[UserService] = user_service_factory.create_user_service

    redis_config = get_redis_config()
    redis = Redis(host=redis_config.host, port=6379, decode_responses=True)
    redis_sessions_crud = RedisSessionCrud(redis)
    session_provider = SessionProvider(redis_sessions_crud)
    app.dependency_overrides[SessionProvider] = lambda: session_provider

    hasher = argon2
    app.dependency_overrides[PasswordHash] = lambda: hasher

    return app


app = create_app()
