import sqlite3
import pytest
from lib.models.author import Author, Article, Magazine  # Ensure this matches your module structure

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
            content TEXT,
            author_id INTEGER,
            magazine_id INTEGER,
            FOREIGN KEY(author_id) REFERENCES authors(id),
            FOREIGN KEY(magazine_id) REFERENCES magazines(id)
        )
    """)

def test_create_author():
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    setup_db(cursor)

    author = Author(name="Osman")
    author.create_author(cursor, conn)
    conn.commit()

    assert author.id is not None
    assert author.name == "Osman"

    cursor.execute("SELECT * FROM authors WHERE id = ?", (author.id,))
    row = cursor.fetchone()
    assert row is not None
    assert row[1] == "Osman"

    conn.close()

def test_get_all_authors():
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    setup_db(cursor)

    cursor.execute("INSERT INTO authors (name) VALUES (?)", ("Author1",))
    cursor.execute("INSERT INTO authors (name) VALUES (?)", ("Author2",))
    conn.commit()

    authors = Author.get_all_authors(cursor)
    assert len(authors) == 2
    names = [author.name for author in authors]
    assert "Author1" in names
    assert "Author2" in names

    conn.close()

def test_update_author_name():
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    setup_db(cursor)

    author = Author(name="Original Name")
    author.create_author(cursor, conn)
    conn.commit()

    author.name = "Updated Name"
    author.save(cursor, conn)
    conn.commit()

    cursor.execute("SELECT name FROM authors WHERE id = ?", (author.id,))
    row = cursor.fetchone()
    assert row[0] == "Updated Name"

    conn.close()

def test_author_articles():
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    setup_db(cursor)

    # Create a magazine so the foreign key is valid
    cursor.execute("INSERT INTO magazines (name) VALUES (?)", ("Magazine A",))
    cursor.execute("INSERT INTO magazines (name) VALUES (?)", ("Magazine B",))
    magazine1_id = 1
    magazine2_id = 2

    author = Author(name="Writer")
    author.create_author(cursor, conn)
    conn.commit()

    cursor.execute(
        "INSERT INTO articles (title, content, author_id, magazine_id) VALUES (?, ?, ?, ?)",
        ("Article 1", "Content 1", author.id, magazine1_id)
    )
    cursor.execute(
        "INSERT INTO articles (title, content, author_id, magazine_id) VALUES (?, ?, ?, ?)",
        ("Article 2", "Content 2", author.id, magazine2_id)
    )
    conn.commit()

    articles = author.articles(cursor)
    assert len(articles) == 2
    titles = [article.title for article in articles]
    assert "Article 1" in titles
    assert "Article 2" in titles

    conn.close()
