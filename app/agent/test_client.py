from client import BibleClient

client = BibleClient()

print(client.get_books())

print()

print(client.get_book("Genesis"))

print()

print(client.get_chapter("Genesis", 1))

print()

print(client.get_verse("John", 3, 16))