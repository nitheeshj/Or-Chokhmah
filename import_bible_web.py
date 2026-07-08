#imports

import json
from pathlib import Path

from app.database import get_connection
from books import BOOKS

# --------------------------------------------------
# Helper Functions
# --------------------------------------------------

def insert_book(cursor, name, testament):
    """
    Insert one book into the books table.
    Returns the generated book_id.
    """
    cursor.execute("""
        INSERT INTO books (name, testament)
        VALUES (%s, %s)
        RETURNING id;
    """, (name, testament))

    return cursor.fetchone()[0]


def insert_chapter(cursor, book_id, chapter_number):
    """
    Insert one chapter into the chapters table.
    Returns the generated chapter_id.
    """
    cursor.execute("""
        INSERT INTO chapters (book_id, chapter_number)
        VALUES (%s, %s)
        RETURNING id;
    """, (book_id, chapter_number))

    return cursor.fetchone()[0]


def insert_verse(cursor,
                 chapter_id,
                 verse_number
               ):
    """
    Insert one verse into the verses table.
    """

    cursor.execute("""
        INSERT INTO verses
        (
            chapter_id,
           verse_number
        )
        VALUES (%s, %s)
        RETURNING id;
    """,
    (
        chapter_id,
        verse_number,
    ))
    return cursor.fetchone()[0]

def insert_verse_text(
    cursor,
    verse_id,
    translation_id,
    text
):
    """
    Insert one verse text into the verse_texts table.
    """

    cursor.execute("""
        INSERT INTO verse_texts
        (
            verse_id,
            translation_id,
            text
        )
        VALUES (%s, %s, %s);
    """,
    (
        verse_id,
        translation_id,
        text,
    ))

def import_book(cursor, book, testament):
    """
    Import one Bible book.

    book is one dictionary from en_kjv.json.

    Example:

    {
        "name": "Genesis",
        "chapters": [
            [...],
            [...],
            ...
        ]
    }
    """

    # -------------------------------
    # Insert the book
    # -------------------------------

    book_id = insert_book(
        cursor,
        book["name"],
        testament
    )

    chapter_count = 0
    verse_count = 0

    # -------------------------------
    # Loop through chapters
    # -------------------------------

    for chapter_number, chapter in enumerate(book["chapters"], start=1):

        chapter_id = insert_chapter(
            cursor,
            book_id,
            chapter_number
        )

        chapter_count += 1

        # ---------------------------
        # Loop through verses
        # ---------------------------

        for verse_number, verse_text in enumerate(chapter, start=1):

            verse_id = insert_verse(
                cursor,
                chapter_id,
                verse_number
            )

            insert_verse_text(
                cursor,
                verse_id,
                1,
                verse_text.strip()
            )

            verse_count += 1

    print(
        f"{book['name']}: "
        f"{chapter_count} chapters, "
        f"{verse_count} verses imported."
    )



# --------------------------------------------------
# Dataset Location
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent

DATASET_PATH = (
    PROJECT_ROOT.parent
    / "bible"
    / "json"
)

BIBLE_FILE = DATASET_PATH / "en_kjv.json"


# --------------------------------------------------
# Connect to PostgreSQL
# --------------------------------------------------

conn = get_connection()
cursor = conn.cursor()

print("Connected to PostgreSQL")

for filename, book_name, testament in BOOKS:

    json_file = DATASET_PATH / f"{filename}.json"

    import_book(
        cursor,
        json_file,
        book_name,
        testament
    )


conn.commit()

cursor.close()
conn.close()


# --------------------------------------------------
# Summary
# --------------------------------------------------

print("\nImport completed successfully!")

