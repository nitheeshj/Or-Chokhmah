# Or-Chokhmah

> A RESTful Bible API built with FastAPI and PostgreSQL to demonstrate backend engineering concepts.

## About

Or-Chokhmah is a backend engineering portfolio project focused on building a production-style Bible API.

The goal of this project is not to recreate existing Bible applications, but to deepen understanding of backend development through practical implementation of:

- REST API design
- Relational database modeling
- SQL
- Authentication
- Caching
- Docker
- Deployment
- Clean project architecture

---

## Tech Stack

- Python
- FastAPI
- PostgreSQL
- psycopg2
- Uvicorn

**Planned**

- JWT Authentication
- Redis
- Docker
- Nginx
- Linux Deployment

---

## Project Structure

```
or-chokhmah/
│
├── main.py
├── database.py
├── requirements.txt
├── README.md
└── ...
```

---

## Database Design

Current schema:

```
Books
│
└── Chapters
      │
      └── Verses
```

Tables

- books
- chapters
- verses

---

## API Endpoints

### Bible

| Method | Endpoint | Description |
|---------|----------|-------------|
| GET | /books | List all books |
| GET | /books/{book} | Get chapters of a book |
| GET | /books/{book}/{chapter} | Get all verses in a chapter |
| GET | /verse/{id} | Get a verse by ID |

---

## Planned Features

### Authentication

- User registration
- Login
- JWT Authentication

### Bookmarks

- Save verses
- Remove bookmarks
- View bookmarks

### Notes

- Create notes
- Edit notes
- Delete notes

### Search

- Search verses
- PostgreSQL Full-Text Search

### Performance

- Redis caching
- Query optimization
- Database indexing

### Deployment

- Docker
- Docker Compose
- Nginx
- Linux VPS deployment

---

## Learning Goals

This project is designed to strengthen understanding of:

- FastAPI
- PostgreSQL
- SQL
- Database relationships
- Indexes
- REST API design
- Authentication
- Authorization
- Docker
- Redis
- Linux deployment

---

## Getting Started

### Clone the repository

```bash
git clone https://github.com/<your-username>/or-chokhmah.git
cd or-chokhmah
```

### Create a virtual environment

```bash
python -m venv .venv
```

Activate it

Linux/macOS

```bash
source .venv/bin/activate
```

Windows

```bash
.venv\Scripts\activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Run the API

```bash
uvicorn main:app --reload
```

Open

```
http://127.0.0.1:8000/docs
```

to access the Swagger UI.

---

## Roadmap

- [x] Project setup
- [x] PostgreSQL database
- [x] Database schema
- [x] GET /books
- [x] GET /books/{book}
- [x] GET /books/{book}/{chapter}
- [ ] GET /verse/{id}
- [ ] JWT Authentication
- [ ] Bookmarks
- [ ] Notes
- [ ] Search
- [ ] Redis
- [ ] Docker
- [ ] Deployment

---

## Why this project?

Backend engineering is more than writing API endpoints.

This project explores how production backend systems are designed by covering:

- API development
- Database modeling
- Query optimization
- Authentication
- Caching
- Deployment
- Software engineering best practices

---

## License

This project is licensed under the MIT License.