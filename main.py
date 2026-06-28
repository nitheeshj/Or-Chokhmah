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


@app.get("/books/{book}/{chapter}")
def get_chapter(book: str, chapter: int):

    conn = get_connection()
    cursor = conn.cursor()

    #Step 1: Find the book
    cursor.execute("""
        SELECT id
        FROM chapters
        WHERE book= %s
        AND chapter_number = %s;           ;
    """, (book,))

    book_result = cursor.fetchone()

    if not book_result:
        cursor.close()
        conn.close()
        return {"error": "Book not found"}
    
    book_id = book_result[0]


    # Step2: Find the chapter
    cursor.execute(""" 
    SELECT id
    FROM chapters
    WHERE book_id = %s
    AND chapter_number = %s;
""", (book_id, chapter))
    
    chapter_result = cursor.fetchone()

    if not chapter_result:
        cursor.close()
        conn.close()
        return {"error": "Chapter not found"}

    chapter_id = chapter_result[0]
    
        # Step 3: Get verses
    cursor.execute("""
        SELECT verse_number, verse_text
        FROM verses
        WHERE chapter_id = %s
        ORDER BY verse_number;
    """, (chapter_id,))

    verses = cursor.fetchall()

    cursor.close()
    conn.close()

    return [
        {
            "verse": row[0],
            "text": row[1]
        }
        for row in verses
    ]

#Create the route
@app.get("/verse/{id}")
def get_verse(id: int):

    conn = get_connection() #opens a connection to PostgreSQL
    
    cursor = conn.cursor

    #Run the SQL
    cursor.execute(""" 
        SELECT verse_number, verse_text
        FROM verses
        WHERE verse_id = %s
    """, (id, ))

    result = cursor.fetchone()

    cursor.close()
    conn.close()

    if not result:
        return {"error": "Verse not found"}
    
    return{
        "verse": result[0],
        "text" : result[1]
    }
