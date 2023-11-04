from fastapi import APIRouter


router = APIRouter(tags=["books"], prefix="/books")


@router.get("/book")
def get_book() -> str:
    return "Book!"
