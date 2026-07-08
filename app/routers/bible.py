from fastapi import APIRouter, HTTPException
from app.database import get_connection
from app.schemas.bible import VerseResponse
from app.services import bible_service




# Create a router object.



router = APIRouter()



# -----------------------------
# GET /books
# -----------------------------


@router.get("/books")
def get_books():


    return bible_service.get_books()



# -----------------------------
# GET /books/{book}
# -----------------------------



@router.get("/books/{book}")
def get_book(book: str):


    return bible_service.get_book(book)



# -----------------------------
# GET /books/{book}/{chapter}
# -----------------------------



@router.get("/books/{book}/{chapter}")
def get_chapter(book: str, chapter: int):


    return bible_service.get_chapter(book, chapter)


# -----------------------------
# GET /books/{book}/{chapter}/{verse}
# -----------------------------


@router.get("/books/{book}/{chapter}/{verse}",
    response_model=VerseResponse)
def get_verse(
    book: str,
    chapter: int,
    verse: int
):


    return bible_service.get_verse(book, chapter, verse)



# --------------------------------------------
# Search the Bible using a keyword
#
# Example:
# GET /search?q=hope
#
# q is called a query parameter.
# FastAPI automatically extracts it from the URL.
# --------------------------------------------


@router.get("/search")
def search_bible(q: str):

    # Return JSON response
    return bible_service.search_bible(q)

