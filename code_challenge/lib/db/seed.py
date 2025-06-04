from connection import get_connection

def seed_data():
    conn = get_connection()
    cursor = conn.cursor()

    # Create tables if they don't exist
    cursor.executescript("""
    CREATE TABLE IF NOT EXISTS authors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE
    );

    CREATE TABLE IF NOT EXISTS magazines (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        category TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS articles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        author_id INTEGER NOT NULL,
        magazine_id INTEGER NOT NULL,
        FOREIGN KEY (author_id) REFERENCES authors(id),
        FOREIGN KEY (magazine_id) REFERENCES magazines(id)
    );
    """)

    # Clear existing data
    cursor.executescript("""
    DELETE FROM articles;
    DELETE FROM authors;
    DELETE FROM magazines;
    """)

    # Seed data
    authors = [
        ("Alice Smith",),
        ("Bob Johnson",),
        ("Carol Williams",),
    ]

    magazines = [
        ("Tech Monthly", "Technology"),
        ("Health Weekly", "Health"),
        ("Fashion Daily", "Fashion"),
    ]

    articles = [
        ("AI and the Future", 1, 1),
        ("Healthy Living Tips", 2, 2),
        ("Spring Fashion Trends", 3, 3),
    ]

    cursor.executemany("INSERT INTO authors(name) VALUES (?)", authors)
    cursor.executemany("INSERT INTO magazines(name, category) VALUES (?, ?)", magazines)
    cursor.executemany("INSERT INTO articles(title, author_id, magazine_id) VALUES (?, ?, ?)", articles)

    conn.commit()
    conn.close()

    print("Database seeded successfully.")

if __name__ == "__main__":
    seed_data()
