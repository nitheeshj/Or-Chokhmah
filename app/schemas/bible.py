from pydantic import BaseModel

class VerseResponse(BaseModel):
    book: str
    chapter: int
    verse: int
    text: str