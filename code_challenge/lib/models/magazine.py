from lib.db.connection import get_connection
from lib.models.author import Author

class Magazine:

    all = {}

    def __init__(self, name, category, id=None):
        self.id = id
        self.name = name
        self.category = category

    @property
    def name(self):
        return self._name 

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise ValueError("Name of magazine has to be a string")
        self._name = value

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        if not isinstance(value, str):
            raise ValueError("Category of magazine has to be a string")
        self._category = value

    @classmethod
    def clear_cache(cls):
        cls.all = {}

    @classmethod
    def create_table(cls):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS magazines (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    category TEXT NOT NULL
                )
            """)
            conn.commit()

    @classmethod
    def drop_table(cls):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DROP TABLE IF EXISTS magazines;")
            conn.commit()

    def save(self):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO magazines (name, category) VALUES (?, ?)",
                (self.name, self.category)
            )
            conn.commit()
            self.id = cursor.lastrowid
            type(self).all[self.id] = self

    @classmethod
    def create(cls, name, category):
        magazine = cls(name, category)
        magazine.save()
        return magazine

    @classmethod
    def instance_from_db(cls, row):
        if row is None:
            return None
        mag_id = row[0]
        if mag_id in cls.all:
            magazine = cls.all[mag_id]
            # Optional: update cached attributes if needed
            magazine.name = row[1]
            magazine.category = row[2]
        else:
            magazine = cls(row[1], row[2], id=mag_id)
            cls.all[mag_id] = magazine
        return magazine

    @classmethod
    def find_by_id(cls, id):
        with get_connection() as conn:
            cursor = conn.cursor()
            row = cursor.execute("SELECT * FROM magazines WHERE id = ?", (id,)).fetchone()
        return cls.instance_from_db(row)

    @classmethod
    def find_by_category(cls, category):
        cls.clear_cache()
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM magazines WHERE category = ?", (category,))
            rows = cursor.fetchall()
        return [cls.instance_from_db(row) for row in rows if row is not None]

    @classmethod
    def find_by_name(cls, name):
        with get_connection() as conn:
            cursor = conn.cursor()
            row = cursor.execute("SELECT * FROM magazines WHERE name = ?", (name,)).fetchone()
        return cls.instance_from_db(row)

    @property
    def contributors(self):
        if self.id is None:
            return []
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT DISTINCT a.id, a.name
                FROM authors a
                JOIN articles ar ON a.id = ar.author_id
                WHERE ar.magazine_id = ?
            """, (self.id,))
            rows = cursor.fetchall()
        return [Author(id=row[0], name=row[1]) for row in rows]

    def contributing_authors(self):
        # For backwards compatibility
        return self.contributors

    def article_titles(self):
        if self.id is None:
            return []
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT title FROM articles WHERE magazine_id = ?", (self.id,))
            rows = cursor.fetchall()
        return [row[0] for row in rows]

    @classmethod
    def with_multiple_authors(cls):
        cls.clear_cache()
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT m.id, m.name, m.category
                FROM magazines m
                JOIN articles a ON m.id = a.magazine_id
                GROUP BY m.id
                HAVING COUNT(DISTINCT a.author_id) > 1
                ORDER BY m.id
            """)
            rows = cursor.fetchall()
        return [cls.instance_from_db(row) for row in rows]

    @classmethod
    def article_counts(cls):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT m.id, m.name, m.category, COUNT(a.id) as count
                FROM magazines m
                LEFT JOIN articles a ON m.id = a.magazine_id
                GROUP BY m.id
                ORDER BY m.id
            """)
            rows = cursor.fetchall()

        result = []
        for row in rows:
            result.append({
                'id': row[0],
                'name': row[1],
                'category': row[2],
                'count': row[3]
            })
        return result
