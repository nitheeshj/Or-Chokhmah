"""
client.py

This file acts as a Python client for our Bible API.

Instead of writing HTTP requests everywhere in our code,
we write them once here and reuse them.

Later:

LLM
 ↓
Tool
 ↓
client.py
 ↓
FastAPI
 ↓
PostgreSQL
"""

import requests


class BibleClient:
    """
    BibleClient knows how to communicate with our FastAPI server.
    """

    def __init__(self):

        # Base URL of our FastAPI server
        self.base_url = "http://127.0.0.1:8000"

    # ---------------------------------------------------
    # GET /books
    # ---------------------------------------------------

    def get_books(self):
        """
        Fetch all books from the API.
        """

        response = requests.get(
            f"{self.base_url}/books"
        )

        response.raise_for_status()

        return response.json()

    # ---------------------------------------------------
    # GET /books/{book}
    # ---------------------------------------------------

    def get_book(self, book):

        response = requests.get(
            f"{self.base_url}/books/{book}"
        )

        response.raise_for_status()

        return response.json()

    # ---------------------------------------------------
    # GET /books/{book}/{chapter}
    # ---------------------------------------------------

    def get_chapter(self, book, chapter):

        response = requests.get(
            f"{self.base_url}/books/{book}/{chapter}"
        )

        response.raise_for_status()

        return response.json()

    # ---------------------------------------------------
    # GET /books/{book}/{chapter}/{verse}
    # ---------------------------------------------------

    def get_verse(self, book, chapter, verse):

        response = requests.get(
            f"{self.base_url}/books/{book}/{chapter}/{verse}"
        )

        response.raise_for_status()

        return response.json()