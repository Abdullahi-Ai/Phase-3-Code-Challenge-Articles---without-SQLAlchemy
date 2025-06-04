import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS authors")
cursor.execute("DROP TABLE IF EXISTS magazines")
cursor.execute("DROP TABLE IF EXISTS articles")

cursor.execute("""
CREATE TABLE authors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE
)
""")

cursor.execute("""
CREATE TABLE magazines (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    category TEXT
)
""")

cursor.execute("""
CREATE TABLE articles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    content TEXT,
    author_id INTEGER,
    magazine_id INTEGER,
    FOREIGN KEY(author_id) REFERENCES authors(id),
    FOREIGN KEY(magazine_id) REFERENCES magazines(id)
)
""")

conn.commit()
conn.close()
