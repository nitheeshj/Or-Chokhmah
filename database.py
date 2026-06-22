import psycopg2

def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="bibledb",
        user="postgres",
        password="postgres123"
    )