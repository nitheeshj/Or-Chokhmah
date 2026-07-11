from dotenv import load_dotenv
import os
from google import genai
from tool_schemas import bible_tools

from google.genai import types


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
response = client.models.generate_content(
    model="gemini-3.5-flash",
    contents=question,
    config=types.GenerateContentConfig(
        tools=[tool]
    )
)

# Print Gemini's response
print(response.function_calls)

