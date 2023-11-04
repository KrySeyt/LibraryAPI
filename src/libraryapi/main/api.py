import os

from fastapi import FastAPI
from sqlalchemy import create_engine

from ..books.router import router as books_router
from ..dependencies import get_db, get_db_stub, get_engine_stub


db_uri = os.getenv("LIBRARYAPI_POSTGRESQL_URI")

if not db_uri:
    raise RuntimeError("No LIBRARYAPI_POSTGRESQL_URI environment variable")

engine = create_engine(db_uri)

app = FastAPI()
app.include_router(books_router)
app.dependency_overrides[get_db_stub] = get_db
app.dependency_overrides[get_engine_stub] = lambda: engine
