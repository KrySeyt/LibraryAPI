from fastapi import FastAPI
from ..books.router import router as books_router


app = FastAPI()
app.include_router(books_router)
