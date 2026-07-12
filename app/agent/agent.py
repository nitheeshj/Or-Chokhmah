from dotenv import load_dotenv
import os
from google import genai
from tool_schemas import bible_tools

from google.genai import types
from tools import (
    search_bible,
    get_verse,
    get_book,
    get_chapter,
)

# Wrap our function declarations into one Tool object.
#
# bible_tools is the list defined in tool_schemas.py.
#
# We are NOT executing anything here.
#
# We are simply telling Gemini:
#
# "These are the tools you may use."
tool = types.Tool(
    function_declarations=bible_tools
)


# Load variables from .env
load_dotenv()

# Create a Gemini client
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

# Read a question from the terminal
question = input("Ask: ")

# Send the request to Gemini
#here SDK is being used and it hides a lot of repititive work
try:
    response = client.models.generate_content(
        model="gemini-flash-latest",
        contents=question,
        config=types.GenerateContentConfig(
            tools=[tool]
        )
    )

except Exception as e:
    print(e)
    exit()

# Did Gemini ask us to call a tool?
if response.function_calls:

    # Get the first requested function
    function_call = response.function_calls[0]

    tool_name = function_call.name

    arguments = function_call.args


# Decide which Python function to execute

    if tool_name == "search_bible":

        result = search_bible(**arguments)

    elif tool_name == "get_verse":

        result = get_verse(**arguments)

    elif tool_name == "get_book":

        result = get_book(**arguments)

    elif tool_name == "get_chapter":

        result = get_chapter(**arguments)

    else:

        raise ValueError(f"Unknown tool requested: {tool_name}")


# NOW result exists

print("\n========== TOOL CALL ==========\n")

print("Tool Name:")
print(tool_name)

print()

print("Arguments:")
print(arguments)

print()

print("Tool Result:")
print(result)

# --------------------------------------------
# Build the conversation history
#
# We send THREE things:
#
# 1. The original user question
# 2. Gemini's function call
# 3. The tool result
#
# Gemini can now continue reasoning.
# --------------------------------------------

history = [

    # Original user question
    types.Content(
        role="user",
        parts=[
            types.Part(text=question)
        ]
    ),

    # Gemini's previous response
    response.candidates[0].content,

    # Tool result
    types.Content(
        role="user",
        parts=[
            types.Part.from_function_response(
                name=tool_name,
                response={
                    "result": result
                }
            )
        ]
    )
]

# --------------------------------------------
# Second Gemini call
#
# Gemini now receives the tool result and
# generates the final natural-language answer.
# --------------------------------------------

final_response = client.models.generate_content(

    model="gemini-flash-latest",

    contents=history,

    config=types.GenerateContentConfig(

        tools=[tool]

    )

)

print("\n========== FINAL ANSWER ==========\n")

print(final_response.text)