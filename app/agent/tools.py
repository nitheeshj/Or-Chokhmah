from client import BibleClient

client = BibleClient()

def get_books():
    return client.get_books()

def get_book(book):
    return client.get_book(book)

def get_chapter(book, chapter):
    return client.get_chapter(book, chapter)

def get_verse(book, chapter, verse):
    return client.get_verse(book, chapter, verse)

def search_bible(query):
    return client.search(query)

