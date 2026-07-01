"""
Or-Chokhmah Bible Importer

Purpose:
    Import the World English Bible JSON dataset into PostgreSQL.

Pipeline:

    JSON Files
        ↓
    Load JSON
        ↓
    Group Verse Sections
        ↓
    Insert Book
        ↓
    Insert Chapters
        ↓
    Insert Verses
        ↓
    Commit Transaction
"""

import json
from collections import OrderedDict
from pathlib import Path

from database import get_connection


# ==================================================
# DATASET LOCATION
# ==================================================

PROJECT_ROOT = Path(__file__).resolve().parent

DATASET_PATH = (
    PROJECT_ROOT.parent
    / "world-english-bible"
    / "json"
)


# ==================================================
# DATABASE HELPERS
# ==================================================

def insert_book(cursor, name, testament):
    """Insert one book and return its id."""
    ...


def insert_chapter(cursor, book_id, chapter_number):
    """Insert one chapter and return its id."""
    ...


def insert_verse(
    cursor,
    chapter_id,
    verse_number,
    verse_text,
    translation_id=1
):
    """Insert one verse."""
    ...


# ==================================================
# JSON HELPERS
# ==================================================

def load_json(file_path):
    """Load one JSON file."""

    with open(file_path, encoding="utf-8") as file:
        return json.load(file)


def group_verses(data):
    """
    Merge multiple JSON fragments belonging to the same verse.

    Returns:
        [
            {
                "chapter": 1,
                "verse": 1,
                "text": "In the beginning..."
            },
            ...
        ]
    """

    grouped = OrderedDict()

    # ----------------------------------------
    # Group all text fragments by
    # (chapter, verse)
    # ----------------------------------------

    for item in data:

        if item.get("type") != "paragraph text":
            continue

        key = (
            item["chapterNumber"],
            item["verseNumber"]
        )

        if key not in grouped:
            grouped[key] = []

        grouped[key].append(
            item["value"].strip()
        )

    # ----------------------------------------
    # Convert grouped fragments into
    # complete verses
    # ----------------------------------------

    verses = []

    for (chapter, verse), parts in grouped.items():

        verses.append({

            "chapter": chapter,

            "verse": verse,

            "text": " ".join(parts)

        })

    return verses

# ==================================================
# IMPORT ONE BOOK
# ==================================================

def import_book(cursor, file_path):
    """
    Import one book.

    Steps

    1. Load JSON
    2. Group verse fragments
    3. Insert book
    4. Insert chapters
    5. Insert verses
    """

    data = load_json(file_path)

    verses = group_verses(data)

    ...

    print("Imported", file_path.name)


# ==================================================
# MAIN
# ==================================================

def main():

    conn = get_connection()
    cursor = conn.cursor()

    try:

        files = sorted(DATASET_PATH.glob("*.json"))

        for file in files:

            import_book(cursor, file)

        conn.commit()

    except Exception:

        conn.rollback()
        raise

    finally:

        cursor.close()
        conn.close()


if __name__ == "__main__":
    main()