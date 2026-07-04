# Or-Chokhmah

## Overview

Or-Chokhmah is a production-oriented Bible Reader API built with FastAPI and PostgreSQL.

The project is designed to strengthen backend engineering skills through a real-world application while providing a foundation for future AI-powered Bible study tools.

Rather than building a simple CRUD application, the project focuses on:

- REST API design
- PostgreSQL database design
- SQL
- Data modelling
- Authentication
- Search
- Performance
- Agentic AI integration

---

## Motivation

Most Bible applications focus on the user interface.

Or-Chokhmah focuses on the backend.

The goal is to build a scalable, production-style backend that can later serve as a trusted tool for AI agents.

---

## Tech Stack

- Python
- FastAPI
- PostgreSQL
- psycopg2
- Uvicorn
- Swagger / OpenAPI

Planned

- JWT Authentication
- Redis
- Docker
- AI Agents
- RAG

---

## Database Design

```
books
│
├── chapters
│
├── verses
│
└── verse_texts
        │
        └── translations
```

Current tables

- books
- chapters
- verses
- verse_texts
- translations

---

## Features

Current

- Import Bible dataset into PostgreSQL
- Normalized relational schema
- Bible Reader API
- Swagger documentation

Planned

- Complete Bible import
- Search API
- Authentication
- Bookmarks
- Notes
- Reading history
- Redis caching
- Docker
- AI Agent integration

---

## API Endpoints

Current

```
GET /books
GET /books/{book}
GET /books/{book}/{chapter}
GET /books/{book}/{chapter}/{verse}
```

Planned

```
GET /search
POST /register
POST /login
GET /bookmarks
GET /notes
```

---

## Project Structure

```
Or-Chokhmah/

├── main.py
├── database.py
├── import_bible.py
├── requirements.txt
├── README.md
├── venv/
└── world-english-bible/
```

Later

```
app/

routers/
schemas/
models/
services/
utils/
```

---

## Learning Objectives

This project is intended to develop practical knowledge of

- REST APIs
- FastAPI
- PostgreSQL
- SQL
- Database normalization
- Transactions
- Indexes
- Backend architecture
- Authentication
- Caching
- AI Tool Calling

---

## Roadmap

### Phase 1

- [x] PostgreSQL setup
- [x] Database schema
- [x] Swagger UI
- [ ] Import complete Bible

### Phase 2

- [ ] REST API improvements
- [ ] Validation
- [ ] Error handling

### Phase 3

- [ ] SQL optimization
- [ ] Indexes
- [ ] Query optimization

### Phase 4

- [ ] JWT Authentication

### Phase 5

- [ ] Search API

### Phase 6

- [ ] Bookmarks

### Phase 7

- [ ] Notes

### Phase 8

- [ ] Redis

### Phase 9

- [ ] Docker

### Phase 10

- [ ] AI Agent Integration

---

## Long-Term Vision

Or-Chokhmah aims to become an AI-powered Bible study platform.

The backend will expose reliable APIs that can be used as tools by AI agents rather than relying solely on an LLM's internal knowledge. Planned capabilities include:

- Verse retrieval
- Bible search
- Context retrieval
- Personalized study
- Reading history
- Tool calling
- Retrieval-Augmented Generation (RAG)

This follows an architecture where the AI agent orchestrates backend APIs instead of replacing them, allowing grounded, trustworthy responses. :contentReference[oaicite:1]{index=1}

---

## Dataset

Bible text is imported from the World English Bible (WEB) dataset.

The importer loads JSON files into a normalized PostgreSQL schema.

---

## Author

Nitheesh

Backend Engineering • FastAPI • PostgreSQL • Python