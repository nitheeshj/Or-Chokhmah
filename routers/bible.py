from fastapi import APIRouter, HTTPException
from database import get_connection

# Create a router object.
router = APIRouter()

# -----------------------------
# GET /books
# -----------------------------
@router.get("/books")
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


# -----------------------------
# GET /books/{book}
# -----------------------------
@router.get("/books/{book}")
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

        raise HTTPException(
            status_code=404,
            detail="Book not found"
    )

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

# -----------------------------
# GET /books/{book}/{chapter}
# -----------------------------
@router.get("/books/{book}/{chapter}")
def get_chapter(book: str, chapter: int):

    conn = get_connection()
    cursor = conn.cursor()

    #Step 1: Find the book
    cursor.execute("""
        SELECT id
        FROM books
        WHERE name = %s ;
    """, (book,))

    book_result = cursor.fetchone()

    if not book_result:
        cursor.close()
        conn.close()

        raise HTTPException(
        status_code=404,
        detail="Book not found"
    )

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

        raise HTTPException(
        status_code=404,
        detail="Chapter not found"
    )

    chapter_id = chapter_result[0]
    
        # Step 3: Get verses
    cursor.execute("""
            SELECT
                verses.verse_number,
                verse_texts.text
            FROM verses
            JOIN verse_texts
            ON verses.id = verse_texts.verse_id
            WHERE verses.chapter_id = %s
            ORDER BY verses.verse_number;
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


# -----------------------------
# GET /books/{book}/{chapter}/{verse}
# -----------------------------
@router.get("/books/{book}/{chapter}/{verse}")
def get_verse(
    book: str,
    chapter: int,
    verse: int
):
    conn = get_connection()
    cursor = conn.cursor()

    # Step 1: Find the book
    cursor.execute("""
        SELECT id
        FROM books
        WHERE name = %s;
    """, (book,))

    book_result = cursor.fetchone()

    if not book_result:
        cursor.close()
        conn.close()
        raise HTTPException(
        status_code=404,
        detail="Book not found"
    )

    book_id = book_result[0]

    # Step 2: Find the chapter
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

        raise HTTPException(
            status_code=404,
            detail="Chapter not found"
    )

    chapter_id = chapter_result[0]

    # Step 3: Find the verse
    cursor.execute("""
            SELECT
                verses.verse_number,
                verse_texts.text
            FROM verses
            JOIN verse_texts
            ON verses.id = verse_texts.verse_id
            WHERE verses.chapter_id = %s
            AND verses.verse_number = %s;
    """, (chapter_id, verse))

    verse_result = cursor.fetchone()

    cursor.close()
    conn.close()

    if not verse_result:

        raise HTTPException(
            status_code=404,
            detail="Verse not found"
    )

    return {
        "book": book,
        "chapter": chapter,
        "verse": verse_result[0],
        "text": verse_result[1]
    }


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


    # Validate the search query first
    if not q.strip():
        raise HTTPException(
            status_code=400,
            detail="Search query cannot be empty."
        )
    
    # Only connect if the input is valid
    conn = get_connection()
    cursor = conn.cursor()


    # ----------------------------------------
    # SQL Query
    #
    # We need information from FOUR tables:
    #
    # books
    #    ↓
    # chapters
    #    ↓
    # verses
    #    ↓
    # verse_texts
    #
    # because:
    #
    # books contains the book name
    # chapters contains chapter number
    # verses contains verse number
    # verse_texts contains the actual verse text
    #
    # They are connected using foreign keys.
    # ----------------------------------------

    cursor.execute("""
        SELECT
            b.name,
            c.chapter_number,
            v.verse_number,
            vt.text

        FROM verse_texts vt

        JOIN verses v
            ON vt.verse_id = v.id

        JOIN chapters c
            ON v.chapter_id = c.id

        JOIN books b
            ON c.book_id = b.id

        -- Search inside the verse text
        WHERE vt.text ILIKE %s

        ORDER BY
            b.id,
            c.chapter_number,
            v.verse_number;

    """, (f"%{q}%",))

    # ----------------------------------------
    # Retrieve all matching rows
    #
    # fetchall() returns something like:
    #
    # [
    #   ("Romans",8,28,"All things...")
    # ]
    # ----------------------------------------
    rows = cursor.fetchall()

    # Close cursor and database connection
    cursor.close()
    conn.close()

    # ----------------------------------------
    # Convert SQL rows into JSON
    #
    # FastAPI automatically converts
    # this Python list into JSON.
    # ----------------------------------------
    results = []

    for row in rows:

        results.append({

            "book": row[0],

            "chapter": row[1],

            "verse": row[2],

            "text": row[3]

        })

    # Return JSON response
    return results