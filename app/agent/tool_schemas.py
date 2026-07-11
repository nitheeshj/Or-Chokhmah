"""
tool_schemas.py

Purpose
-------
This file describes the tools that our AI agent can use.

IMPORTANT:
----------
This file DOES NOT execute the tools.

Instead, it tells Gemini:

1. What tools exist.
2. What each tool does.
3. What parameters each tool needs.

Think of this as the "instruction manual" for Gemini.

Gemini never reads tools.py directly.

Instead, agent.py will send these tool descriptions
to Gemini.
"""

from google.genai import types


# ============================================================
# Tool: get_verse
# ============================================================

get_verse_tool = types.FunctionDeclaration(
    # The name Gemini will use when requesting this tool.
    #
    # IMPORTANT:
    # This should match the Python function name
    # in tools.py.
    #
    # tools.py
    #
    # def get_verse(...):
    #
    name="get_verse",

    # Explain to Gemini when this tool should be used.
    #
    # The clearer this description is,
    # the better Gemini can decide when
    # to call it.
    description="Retrieve a Bible verse by specifying the book, chapter, and verse number.",

    # Parameters required for this tool.
    #
    # Gemini reads this schema before deciding
    # whether it can call the tool.
    parameters=types.Schema(
        type=types.Type.OBJECT,

        properties={

            # -------------------------------
            # book
            # -------------------------------
            "book": types.Schema(
                type=types.Type.STRING,
                description="The name of the Bible book, for example John or Romans."
            ),

            # -------------------------------
            # chapter
            # -------------------------------
            "chapter": types.Schema(
                type=types.Type.INTEGER,
                description="Chapter number."
            ),

            # -------------------------------
            # verse
            # -------------------------------
            "verse": types.Schema(
                type=types.Type.INTEGER,
                description="Verse number."
            ),
        },

        # Gemini MUST provide all three.
        required=["book", "chapter", "verse"],
    ),
)


# ============================================================
# Tool: search_bible
# ============================================================

search_bible_tool = types.FunctionDeclaration(
    name="search_bible",

    description="Search the Bible for verses containing a keyword or phrase.",

    parameters=types.Schema(
        type=types.Type.OBJECT,

        properties={

            "query": types.Schema(
                type=types.Type.STRING,
                description="The keyword or phrase to search for."
            ),

        },

        required=["query"],
    ),
)


# ============================================================
# Tool Collection
# ============================================================

"""
Instead of sending each tool individually,
we place them into one list.

Later, agent.py will import this list.

Example:

from tool_schemas import bible_tools
"""

bible_tools = [
    get_verse_tool,
    search_bible_tool,
]