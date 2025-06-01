import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


import sqlite3
from lib.models.author import Author

def setup_db(cursor):
    cursor.execute("""
    CREATE TABLE authors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
    )
    """)
    cursor.execute("""
    CREATE TABLE magazines (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
    )
    """)
    cursor.execute("""
    CREATE TABLE articles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        author_id INTEGER NOT NULL,
        magazine_id INTEGER NOT NULL,
        FOREIGN KEY(author_id) REFERENCES authors(id),
        FOREIGN KEY(magazine_id) REFERENCES magazines(id)
    )
    """)

def test_author():
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()

    setup_db(cursor)

    author = Author(name="Osman")
    author.create_author(cursor)
    conn.commit()

    print(f"Created author with id={author.id} and name={author.name}")

    authors = Author.get_all_authors(cursor)
    print("Authors in DB:")
    for a in authors:
        print(f"id={a.id}, name={a.name}")

    articles = author.articles(cursor)
    print("Articles for author:", articles)

    magazines = author.magazines(cursor)
    print("Magazines for author:", magazines)

    conn.close()

if __name__ == "__main__":
    test_author()
