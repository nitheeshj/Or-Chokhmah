import json
from pathlib import Path

from database import get_connection


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
# --------------------------------------------------
# Dataset Location
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent

DATASET_PATH = (
    PROJECT_ROOT.parent
    / "world-english-bible"
    / "json"
)

GENESIS_FILE = DATASET_PATH / "genesis.json"

print(f"Reading: {GENESIS_FILE}")


# --------------------------------------------------
# Read JSON
# --------------------------------------------------

with open(GENESIS_FILE, "r", encoding="utf-8") as file:
    data = json.load(file)

print(f"Loaded {len(data)} JSON records")


# --------------------------------------------------
# Connect to PostgreSQL
# --------------------------------------------------

conn = get_connection()
cursor = conn.cursor()

print("Connected to PostgreSQL")


# --------------------------------------------------
# Insert Book
# --------------------------------------------------

book_id = insert_book(
    cursor,
    "Genesis",
    "Old Testament"
)

print(f"Inserted Book: Genesis (id={book_id})")


# --------------------------------------------------
# Variables used while importing
# --------------------------------------------------

current_chapter = None
chapter_id = None

current_verse = None
current_text = ""

chapter_count = 0
verse_count = 0


# --------------------------------------------------
# Loop through every JSON record
# --------------------------------------------------

for item in data:

    # Ignore formatting records
    if item.get("type") != "paragraph text":
        continue

    chapter_number = item["chapterNumber"]
    verse_number = item["verseNumber"]
    verse_text = item["value"].strip()

    # ------------------------------------------
    # First verse in the entire book?
    # ------------------------------------------

    if current_verse is None:

        current_chapter = chapter_number

        chapter_id = insert_chapter(
            cursor,
            book_id,
            chapter_number
        )

        chapter_count += 1

        current_verse = verse_number
        current_text = verse_text

        print(f"Inserted Chapter {chapter_number}")

        continue


    # ------------------------------------------
    # Same verse?
    #
    # Some verses are split into multiple JSON
    # records. Join them together.
    # ------------------------------------------

    if (
        chapter_number == current_chapter
        and
        verse_number == current_verse
    ):

        current_text += " " + verse_text
        continue


    # ------------------------------------------
    # A new verse has started.
    #
    # Save the previous verse first.
    # ------------------------------------------

    verse_id = insert_verse(
        cursor,
        chapter_id,
        current_verse
    )

    insert_verse_text(
        cursor,
        verse_id,
        1,
        current_text
    )

    verse_count += 1


    # ------------------------------------------
    # Did the chapter change?
    #
    # If yes, create the next chapter.
    # ------------------------------------------

    if chapter_number != current_chapter:

        current_chapter = chapter_number

        chapter_id = insert_chapter(
            cursor,
            book_id,
            chapter_number
        )

        chapter_count += 1

        print(f"Inserted Chapter {chapter_number}")


    # ------------------------------------------
    # Begin collecting the new verse.
    # ------------------------------------------

    current_verse = verse_number
    current_text = verse_text


# --------------------------------------------------
# Insert the final verse.
#
# The loop finishes without ever seeing another
# verse, so we save it manually.
# --------------------------------------------------

if current_verse is not None:

    verse_id = insert_verse(
        cursor,
        chapter_id,
        current_verse
    )

    insert_verse_text(
        cursor,
        verse_id,
        1,
        current_text
    )

    verse_count += 1
conn.commit()

cursor.close()
conn.close()


# --------------------------------------------------
# Summary
# --------------------------------------------------

print("\nImport completed successfully!")

print(f"Books Imported    : 1")
print(f"Chapters Imported : {chapter_count}")
print(f"Verses Imported   : {verse_count}")