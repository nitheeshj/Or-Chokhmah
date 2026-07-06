import json
from pathlib import Path

# --------------------------------------------
# Locate the JSON dataset
# --------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent

DATASET_PATH = (
    PROJECT_ROOT.parent
    / "world-english-bible"
    / "json"
)

# --------------------------------------------
# Process every JSON file
# --------------------------------------------

for json_file in sorted(DATASET_PATH.glob("*.json")):

    print("=" * 70)
    print(f"Book : {json_file.stem}")

    with open(json_file, "r", encoding="utf-8") as file:
        data = json.load(file)

    # ----------------------------------------
    # Statistics
    # ----------------------------------------

    types = set()

    unique_chapters = set()
    unique_verses = set()

    duplicate_count = 0

    seen = set()

    # ----------------------------------------
    # Read every JSON record
    # ----------------------------------------

    for item in data:

        record_type = item.get("type")

        types.add(record_type)

        if (
            "chapterNumber" not in item
            or
            "verseNumber" not in item
        ):
            continue

        chapter = item["chapterNumber"]
        verse = item["verseNumber"]

        unique_chapters.add(chapter)

        unique_verses.add(
            (
                chapter,
                verse
            )
        )

        key = (
            record_type,
            chapter,
            verse,
            item.get("sectionNumber")
        )

        if key in seen:
            duplicate_count += 1

        seen.add(key)

    # ----------------------------------------
    # Print report
    # ----------------------------------------

    print(f"Record Types      : {sorted(types)}")
    print(f"Chapters          : {len(unique_chapters)}")
    print(f"Unique Verses     : {len(unique_verses)}")
    print(f"Duplicate Records : {duplicate_count}")