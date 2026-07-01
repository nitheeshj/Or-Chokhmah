# Or-Chokhmah

> **Wisdom for every seeker. AI-powered Bible Study Platform built with FastAPI and PostgreSQL.**

## Overview

Or-Chokhmah is a production-oriented backend project that provides a complete Bible API and serves as the foundation for an AI-powered Bible study assistant.

The project demonstrates modern backend engineering concepts such as REST API design, relational database modeling, authentication, search, caching, and API documentation. It is also designed so that AI agents can use the backend as a trusted source of Scripture instead of relying solely on LLM knowledge.

The long-term goal is to build an intelligent Bible study platform where AI retrieves verses, searches Scripture, understands user context, and assists with Bible study through tool calling and retrieval-based workflows.

---

# Features

## Bible API

* List all Bible books
* Retrieve chapters
* Retrieve verses
* Verse lookup
* Structured JSON responses
* Complete Bible stored in PostgreSQL

Example endpoints

```
GET /books

GET /books/{book}

GET /books/{book}/{chapter}

GET /books/{book}/{chapter}/{verse}
```

---

## Planned Features

* JWT Authentication
* User Registration & Login
* Personal Notes
* Bookmarks
* Reading History
* Bible Search
* Cross References
* Redis Cache
* Docker Deployment
* Testing
* CI/CD

---

# AI Roadmap

Or-Chokhmah is designed so that an AI agent can interact with backend APIs as tools.

Instead of:

```
User
   ↓
LLM
   ↓
Answer
```

The architecture becomes:

```
                 User
                  │
                  ▼
            AI Study Assistant
                  │
     ┌────────────┼────────────┐
     ▼            ▼            ▼
 Bible API     Search Tool   User Memory
     │            │            │
     ▼            ▼            ▼
 PostgreSQL   PostgreSQL   PostgreSQL
```

The AI agent retrieves authoritative Bible data from the backend before generating responses.

---

# Planned AI Capabilities

### Verse Retrieval

```
User:
Show me Romans 8:28

↓

Agent

↓

Calls Bible API

↓

Returns verse
```

---

### Bible Search

```
User:
Find verses about hope

↓

Agent

↓

Calls Search API

↓

Returns matching verses
```

---

### Verse Explanation

```
User:
Explain John 3:16

↓

Agent retrieves verse

↓

LLM explains passage

↓

Grounded response
```

---

### Personalized Study

Future versions will allow the AI assistant to:

* Explain bookmarked verses
* Continue previous reading sessions
* Summarize personal notes
* Generate Bible study outlines
* Suggest reading plans
* Compare passages
* Create reflection questions

---

# Tech Stack

| Layer                      | Technology        |
| -------------------------- | ----------------- |
| Language                   | Python            |
| Framework                  | FastAPI           |
| Database                   | PostgreSQL        |
| ORM / Database Driver      | psycopg2          |
| API Documentation          | Swagger / OpenAPI |
| Validation                 | Pydantic          |
| Authentication (Planned)   | JWT               |
| Cache (Planned)            | Redis             |
| Containerization (Planned) | Docker            |
| AI Integration (Planned)   | OpenAI / Gemini   |
| Retrieval (Planned)        | RAG               |

---

# Project Structure

```
or-chokhmah/

│
├── app/
│   ├── main.py
│   ├── database.py
│   ├── routers/
│   ├── services/
│   ├── models/
│   ├── schemas/
│   └── utils/
│
├── bible_data/
│
├── import_bible.py
│
├── requirements.txt
│
├── README.md
│
└── .env
```

---

# Database Design

```
Books
------
id
name
testament

Chapters
---------
id
book_id
chapter_number

Verses
-------
id
chapter_id
verse_number
text
```

Relationships

```
Book

1

↓

Many Chapters

↓

Many Verses
```

---

# API Documentation

Swagger UI

```
http://localhost:8000/docs
```

ReDoc

```
http://localhost:8000/redoc
```

---

# Current Progress

* FastAPI project setup
* PostgreSQL integration
* Relational database schema
* Bible import script
* REST API endpoints
* Swagger documentation

---

# Planned Roadmap

### Phase 1

* Complete Bible API
* Import full Bible
* Validation
* Error handling

### Phase 2

* SQL optimization
* Clean project architecture

### Phase 3

* JWT Authentication

### Phase 4

* Notes

### Phase 5

* Bookmarks

### Phase 6

* Search

### Phase 7

* AI Tool Calling

### Phase 8

* Retrieval-Augmented Generation (RAG)

### Phase 9

* Redis Cache

### Phase 10

* Docker & Deployment

---

# Why This Project?

Most Bible applications simply display Scripture.

Or-Chokhmah is designed as a backend platform that enables AI systems to retrieve trusted Scripture through APIs, reducing hallucinations and demonstrating how backend engineering and AI can work together.

The project focuses on:

* Backend Engineering
* Database Design
* REST APIs
* SQL
* Authentication
* AI Tool Calling
* Retrieval-Augmented Generation
* Production Software Design

---

# Learning Objectives

This project is intended to deepen understanding of:

* FastAPI
* PostgreSQL
* REST API Design
* Database Normalization
* SQL Queries
* JWT Authentication
* API Documentation
* Redis
* Docker
* Agentic Engineering
* Tool Calling
* RAG
* Production AI Systems

---

# Future Vision

Or-Chokhmah aims to evolve into an AI-powered Bible study platform capable of:

* Understanding natural language questions
* Retrieving Scripture from backend APIs
* Searching Bible knowledge
* Remembering user study history
* Building personalized Bible studies
* Integrating commentaries through RAG
* Supporting intelligent Bible research while grounding responses in trusted data

---

# License

This project is intended for educational purposes and backend engineering practice. Please ensure that any Bible translation included is used in accordance with its respective licensing terms.

---

## Author

**Nitheesh**

Backend Engineering • FastAPI • PostgreSQL • AI Engineering • Agentic Systems
