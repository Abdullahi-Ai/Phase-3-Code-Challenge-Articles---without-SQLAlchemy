import sqlite3

def seed():
    conn = sqlite3.connect('path/to/your/database.db')  # adjust path
    cursor = conn.cursor()

    # Insert authors
    cursor.execute("INSERT INTO authors (name) VALUES (?)", ("Osman",))
    cursor.execute("INSERT INTO authors (name) VALUES (?)", ("Noor",))

    # Insert magazines
    cursor.execute("INSERT INTO magazines (name, category) VALUES (?, ?)", ("Tech Monthly", "Technology"))
    cursor.execute("INSERT INTO magazines (name, category) VALUES (?, ?)", ("Health Weekly", "Health"))

    # Insert articles
    cursor.execute("INSERT INTO articles (title, content, author_id, magazine_id) VALUES (?, ?, ?, ?)",
                   ("The Future of AI", "Content about AI...", 1, 1))
    cursor.execute("INSERT INTO articles (title, content, author_id, magazine_id) VALUES (?, ?, ?, ?)",
                   ("Healthy Living Tips", "Content about health...", 2, 2))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    seed()
