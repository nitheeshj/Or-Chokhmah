import json
from pathlib import Path

from database import get_connection

from books import BOOKS

# --------------------------------------------------
# Dataset Location
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent

DATASET_PATH = (
    PROJECT_ROOT.parent
    / "world-english-bible"
    / "json"
)



# --------------------------------------------------
# Connect to PostgreSQL
# --------------------------------------------------

conn = get_connection()
cursor = conn.cursor()

print("=" * 70)


# --------------------------------------------------
# Check every book
# --------------------------------------------------

for filename, book_name, testament in BOOKS:

    json_file = DATASET_PATH / f"{filename}.json"

    with open(json_file, "r", encoding="utf-8") as file:
        data = json.load(file)

    # ------------------------------------------
    # Collect every UNIQUE verse found in JSON.
    #
    # A set automatically removes duplicates.
    # ------------------------------------------

    json_verses = set()

    for item in data:

        if item.get("type") not in (
            "paragraph text",
            "line text",
        ):
            continue

        json_verses.add(
            (
                item["chapterNumber"],
                item["verseNumber"],
            )
        )

    # ------------------------------------------
    # Read verses from PostgreSQL.
    # ------------------------------------------

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

    # ------------------------------------------
    # Print comparison.
    # ------------------------------------------

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
# Close PostgreSQL
# --------------------------------------------------

cursor.close()
conn.close()