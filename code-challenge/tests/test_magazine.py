import sqlite3
from lib.models.magazine import Magazine

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
        name TEXT NOT NULL,
        category TEXT NOT NULL
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

def test_magazine():
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    setup_db(cursor)

   
    mag = Magazine(name="Tech Today", category="Technology")
    mag.create_magazine(cursor)
    conn.commit()

    print(f"Created magazine with id={mag.id}, name={mag.name}, category={mag.category}")

    
    magazines = Magazine.get_all_magazines(cursor)
    print("Magazines in DB:")
    for m in magazines:
        print(f"id={m.id}, name={m.name}, category={m.category}")

   
    print("Articles for magazine:", mag.articles(cursor))
    print("Contributors for magazine:", mag.contributors(cursor))

    conn.close()

def test_create_another_magazine():
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    setup_db(cursor)

    mag = Magazine(name="Health Weekly", category="Health")
    mag.create_magazine(cursor)
    conn.commit()

    assert mag.id is not None
    assert mag.name == "Health Weekly"
    assert mag.category == "Health"

    conn.close()

def test_create_another_magazine():
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    setup_db(cursor)

    mag = Magazine(name="Health Weekly", category="Health")
    mag.create_magazine(cursor)
    conn.commit()

    assert mag.id is not None
    assert mag.name == "Health Weekly"
    assert mag.category == "Health"

    conn.close()

def test_articles_for_magazine_empty():
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    setup_db(cursor)

    mag = Magazine(name="Empty Mag", category="Misc")
    mag.create_magazine(cursor)
    conn.commit()

    articles = mag.articles(cursor)
    assert articles == []

    conn.close()

if __name__ == "__main__":
    test_magazine()
