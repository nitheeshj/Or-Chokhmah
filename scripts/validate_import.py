import json
from pathlib import Path

from app.database import get_connection
from books import BOOKS

# --------------------------------------------------
# Dataset Location
#
# The entire Bible is stored in ONE JSON file.
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent

JSON_FILE = (
    PROJECT_ROOT.parent
    / "bible"
    / "json"
    / "en_kjv.json"
)

# --------------------------------------------------
# Load the Bible.
#
# This dataset contains a UTF-8 BOM, so use
# utf-8-sig instead of utf-8.
# --------------------------------------------------

with open(JSON_FILE, "r", encoding="utf-8-sig") as file:
    bible = json.load(file)

# --------------------------------------------------
# Connect to PostgreSQL
# --------------------------------------------------

conn = get_connection()
cursor = conn.cursor()

print("=" * 70)

# --------------------------------------------------
# Compare every book.
#
# zip() matches:
#
# Genesis JSON  <-> Genesis in BOOKS
# Exodus JSON   <-> Exodus in BOOKS
# ...
# Revelation JSON <-> Revelation in BOOKS
# --------------------------------------------------

for book_data, (book_name, testament) in zip(bible, BOOKS):
    # ----------------------------------------------
    # Collect every verse from the JSON.
    #
    # A set removes duplicates automatically.
    #
    # Each verse is stored as:
    #
    # (chapter_number, verse_number)
    # ----------------------------------------------

    json_verses = set()

    chapters = book_data["chapters"]

    for chapter_number, chapter in enumerate(chapters, start=1):

        for verse_number, verse_text in enumerate(chapter, start=1):

            json_verses.add(
                (
                    chapter_number,
                    verse_number,
                )
            )

    # ----------------------------------------------
    # Read every verse from PostgreSQL.
    # ----------------------------------------------

    cursor.execute(
        """
        SELECT
            c.chapter_number,
            v.verse_number
        FROM verses v
        JOIN chapters c
            ON c.id = v.chapter_id
        JOIN books b
            ON b.id = c.book_id
        WHERE b.name = %s;
        """,
        (book_name,)
    )

    db_verses = set(cursor.fetchall())

    # ----------------------------------------------
    # Compare JSON with PostgreSQL.
    # ----------------------------------------------

    print(
        f"{book_name:<20}"
        f"JSON={len(json_verses):5}"
        f" DB={len(db_verses):5}",
        end=""
    )

    if json_verses == db_verses:
        print("   OK")
    else:
        print("   MISMATCH")

# --------------------------------------------------
# Close PostgreSQL connection.
# --------------------------------------------------

cursor.close()
conn.close()