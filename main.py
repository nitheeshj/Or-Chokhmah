from fastapi import FastAPI
from database import get_connection

app = FastAPI()


@app.get("/")
def home():
    return {"message": "Bible API is running"}


@app.get("/books")
def get_books():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT name
        FROM books
        ORDER BY id;
    """)

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return [row[0] for row in rows]


@app.get("/books/{book}")
def get_book(book: str):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id
        FROM books
        WHERE name = %s;
    """, (book,))

    result = cursor.fetchone()

    if not result:
        cursor.close()
        conn.close()
        return {"error": "Book not found"}

    book_id = result[0]

    cursor.execute("""
        SELECT chapter_number
        FROM chapters
        WHERE book_id = %s
        ORDER BY chapter_number;
    """, (book_id,))

    chapters = cursor.fetchall()

    cursor.close()
    conn.close()

    return {
        "book": book,
        "chapters": [row[0] for row in chapters]
    }