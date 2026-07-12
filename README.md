# Or-Chokhmah – AI Powered Bible Agent

## Overview

Or-Chokhmah is an AI-powered Bible assistant built from scratch using:

- FastAPI
- PostgreSQL
- Python
- Google Gemini API
- Function Calling (Tool Calling)

The project demonstrates how an LLM can interact with external tools instead of relying only on its pretrained knowledge.

---

## Architecture

User
↓
Gemini
↓
Function Calling
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

---

## Components

### FastAPI

Provides REST APIs for accessing Bible data.

Examples:

- GET /books
- GET /books/{book}
- GET /books/{book}/{chapter}
- GET /books/{book}/{chapter}/{verse}
- GET /search?q=love

---

### client.py

A reusable Python HTTP client that communicates with the FastAPI server.

---

### tools.py

Wraps the HTTP client into Python functions that can be exposed to the LLM.

Examples:

- get_verse()
- get_book()
- get_chapter()
- search_bible()

---

### tool_schemas.py

Defines tool schemas using Gemini Function Declarations.

This tells Gemini:

- what tools exist
- what parameters they require
- when they can be used

---

### agent.py

The orchestrator.

Responsibilities:

- Read user questions
- Send them to Gemini
- Receive Function Calls
- Dispatch Python tools
- Execute the selected tool
- Return structured results

---

## Current Status

Implemented:

- Backend API
- PostgreSQL integration
- HTTP client
- Python tools
- Gemini Function Calling
- Manual tool dispatcher

Planned:

- Complete tool response loop
- Conversation memory
- Retrieval-Augmented Generation (RAG)
- Multi-tool orchestration
- Multi-agent workflows
- Model Context Protocol (MCP)

---

## Learning Goals

This project focuses on understanding:

- Backend Engineering
- REST APIs
- Tool Calling
- AI Agents
- LLM Orchestration
- Agentic Engineering

instead of relying on high-level frameworks.