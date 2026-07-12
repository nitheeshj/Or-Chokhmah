# Or-Chokhmah – AI Powered Bible Agent

An AI-powered Bible Assistant built from scratch using FastAPI, PostgreSQL, Python, and Google Gemini Function Calling.

The goal of this project is to understand backend engineering and agentic engineering from first principles rather than relying on high-level AI frameworks.

---

# Features

- Bible REST API
- PostgreSQL Database
- FastAPI Backend
- Swagger Documentation
- Search Endpoint
- Python HTTP Client
- Gemini Function Calling
- Manual Tool Dispatcher
- AI Agent Prototype

---

# Motivation

Traditional LLMs answer questions using their pretrained knowledge.

Or-Chokhmah demonstrates a better approach.

Instead of asking the model to remember Scripture, the model retrieves the requested verses from a backend API before generating a response.

This makes responses more reliable, grounded, and extensible.

---

# Project Architecture

```
                         User
                           │
                           ▼
                     Gemini LLM
                           │
                 Function Calling
                           │
                           ▼
                      agent.py
                           │
                    Tool Dispatcher
                           │
             ┌─────────────┴─────────────┐
             ▼                           ▼
         get_verse()                search_bible()
             │                           │
             └─────────────┬─────────────┘
                           ▼
                      client.py
                           │
                    HTTP Requests
                           │
                           ▼
                      FastAPI API
                           │
                     bible_service.py
                           │
                      database.py
                           │
                           ▼
                      PostgreSQL
```

---

# Project Structure

```
or-chokhmah/

app/

├── main.py

├── database.py

├── routers/

│ └── bible.py

├── services/

│ └── bible_service.py

├── schemas/

│ └── bible.py

└── agent/

    ├── agent.py

    ├── client.py

    ├── tools.py

    └── tool_schemas.py
```

---

# Component Responsibilities

## main.py

Starts the FastAPI application.

Registers routers.

---

## routers/

Defines REST API endpoints.

Example:

```
GET /books

GET /books/John

GET /books/John/3

GET /books/John/3/16

GET /search?q=love
```

Routers contain almost no business logic.

They simply receive HTTP requests and forward them to the service layer.

---

## services/

Contains the business logic.

Responsibilities:

- Execute SQL
- Validate inputs
- Convert SQL rows into Python objects
- Return results

---

## database.py

Responsible for creating PostgreSQL connections.

Every service that needs the database uses this module.

---

## PostgreSQL

Stores:

- Books
- Chapters
- Verses
- Verse Texts

---

## client.py

Acts as a Python HTTP client.

Instead of writing HTTP requests everywhere:

```
requests.get(...)
```

they are wrapped inside reusable Python methods.

Example:

```
client.get_verse("John",3,16)
```

Internally:

```
↓

GET /books/John/3/16
```

---

## tools.py

Converts backend APIs into Python tools.

Example:

```
get_verse()

search_bible()

get_book()

get_chapter()
```

These functions are what the LLM ultimately executes.

---

## tool_schemas.py

Defines Gemini Function Declarations.

This file tells Gemini:

- which tools exist
- required parameters
- descriptions
- argument types

Gemini **cannot inspect Python code**.

It only knows about tools described here.

---

## agent.py

Acts as the orchestrator.

Responsibilities:

- Receive user input
- Send prompt to Gemini
- Register tools
- Receive FunctionCall
- Determine which Python function to execute
- Execute the tool
- Return structured data

Current version implements a manual dispatcher using if/elif statements.

---

# Current Workflow

Current execution flow:

```
User

↓

Gemini

↓

Function Call

↓

agent.py

↓

tools.py

↓

client.py

↓

FastAPI

↓

PostgreSQL

↓

JSON Result
```

The second Gemini call (Tool Response Loop) is the next planned enhancement.

---

# Current Features

Implemented

- FastAPI backend
- PostgreSQL integration
- Bible search
- Bible retrieval
- Swagger UI
- Python HTTP client
- Tool layer
- Gemini SDK integration
- Function Calling
- Manual tool dispatcher

---

# Current Limitations

The current agent can:

- decide which tool to call

- execute the tool

- retrieve structured data

But it does **not yet**:

- send tool results back to Gemini

- generate a natural language response

- maintain conversation memory

- perform multiple tool calls

- plan tasks

- retrieve external knowledge

---

# Installation

## Clone

```bash
git clone https://github.com/nitheeshj/Or-Chokhmah.git

cd Or-Chokhmah
```

---

## Create Virtual Environment

Linux

```bash
python -m venv venv

source venv/bin/activate
```

Windows

```bash
venv\Scripts\activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file.

```
GEMINI_API_KEY=YOUR_API_KEY
```

---

## Start PostgreSQL

Ensure PostgreSQL is running.

Import the Bible dataset.

---

## Start FastAPI

```bash
uvicorn app.main:app --reload
```

Swagger

```
http://127.0.0.1:8000/docs
```

---

## Run the Agent

```bash
cd app/agent

python agent.py
```

Example

```
Ask:

Search the Bible for love
```

Gemini decides

```
search_bible(query="love")
```

Python executes

```
tools.py

↓

client.py

↓

FastAPI

↓

PostgreSQL
```

Result

```
JSON verses
```

---

# Technologies Used

- Python
- FastAPI
- PostgreSQL
- Requests
- Google Gemini API
- Function Calling
- dotenv

---

# Learning Objectives

This project focuses on learning:

- Backend Engineering
- REST APIs
- SQL
- PostgreSQL
- FastAPI
- API Design
- HTTP
- Tool Calling
- Function Calling
- LLM APIs
- AI Agents
- Agentic Engineering

---

# Future Roadmap

Backend

- JWT Authentication
- Users
- Bookmarks
- Notes
- Redis Cache
- Docker
- Deployment
- Testing

AI

- Tool Response Loop
- Agent Loop
- Conversation Memory
- Long-Term Memory
- Retrieval-Augmented Generation (RAG)
- Multi-Tool Planning
- Multi-Agent Systems
- Model Context Protocol (MCP)

---

# Project Goal

This project aims to understand how modern AI systems interact with backend applications.

Instead of treating an LLM as the application, Or-Chokhmah treats the LLM as an intelligent orchestration layer capable of selecting backend tools, retrieving authoritative data, and generating grounded responses.

The backend remains the source of truth, while the AI agent becomes the interface that reasons about user requests and decides how to use the available tools.