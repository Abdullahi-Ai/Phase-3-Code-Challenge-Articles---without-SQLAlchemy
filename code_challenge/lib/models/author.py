import sqlite3
from lib.db.connection import get_connection

class Author:
    def __init__(self, id=None, name=None):
        self.id = id
        self.name = name

    def save(self):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO authors (name) VALUES (?)", (self.name,))
            self.id = cursor.lastrowid
            conn.commit()
            print(f"[DEBUG] Saved new author: {self.name} with ID: {self.id}")
        except sqlite3.IntegrityError:
            cursor.execute("SELECT id FROM authors WHERE name = ?", (self.name,))
            row = cursor.fetchone()
            if row:
                self.id = row[0]
                print(f"[DEBUG] Author '{self.name}' already exists with ID: {self.id}")
            else:
                raise ValueError(f"Author with name '{self.name}' not found after IntegrityError.")
        finally:
            conn.close()

    @classmethod
    def find_by_id(cls, author_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM authors WHERE id = ?", (author_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            print(f"[DEBUG] Found author by ID {author_id}: {row}")
            return cls(id=row[0], name=row[1])
        print(f"[DEBUG] No author found with ID: {author_id}")
        return None
        
    @classmethod
    def find_by_name(cls, name):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT id, name FROM authors WHERE name = ?", (name,))
            row = cursor.fetchone()
            if row:
                print(f"[DEBUG] Found author by name '{name}': {row}")
                return cls(id=row[0], name=row[1])
            print(f"[DEBUG] No author found with name: {name}")
            return None
        except Exception as e:
            print(f"[ERROR] Error finding author by name: {e}")
            return None
        finally:
            conn.close()

    def articles(self):
        if not self.id:
            return []
        from lib.models.article import Article
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, title, author_id, magazine_id FROM articles WHERE author_id = ?", (self.id,))
        rows = cursor.fetchall()
        conn.close()
        return [Article(id=row[0], title=row[1], author_id=row[2], magazine_id=row[3]) for row in rows]

    def magazines(self):
        if not self.id:
            return []
        from lib.models.magazine import Magazine
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT DISTINCT m.id, m.name, m.category
            FROM magazines m
            JOIN articles a ON m.id = a.magazine_id
            WHERE a.author_id = ?
        """, (self.id,))
        rows = cursor.fetchall()
        conn.close()
        return [Magazine(id=row[0], name=row[1], category=row[2]) for row in rows]

    def add_article(self, magazine, title):
        from lib.models.article import Article
        if not self.id:
            raise ValueError("Author must be saved before adding articles.")
        if not magazine.id:
            raise ValueError("Magazine must be saved before being used.")
        article = Article(title=title, author_id=self.id, magazine_id=magazine.id)
        article.save()
        return article

    def topic_areas(self):
        if not self.id:
            return []
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT DISTINCT m.category
            FROM magazines m
            JOIN articles a ON m.id = a.magazine_id
            WHERE a.author_id = ?
        """, (self.id,))
        rows = cursor.fetchall()
        conn.close()
        return [row[0] for row in rows]

    @classmethod
    def top_author(cls):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT a.id, a.name, COUNT(ar.id) as article_count
            FROM authors a
            JOIN articles ar ON a.id = ar.author_id
            GROUP BY a.id
            ORDER BY article_count DESC
            LIMIT 1
        """)
        row = cursor.fetchone()
        conn.close()
        if row:
            print(f"[DEBUG] Top author is: {row}")
            return cls(id=row[0], name=row[1])
        print("[DEBUG] No top author found")
        return None
