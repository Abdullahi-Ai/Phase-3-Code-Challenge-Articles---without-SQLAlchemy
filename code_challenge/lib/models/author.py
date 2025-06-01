class Author:
    def __init__(self, id=None, name=None):
        self._id = id
        self.name = name  # triggers setter validation

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise TypeError("Name must be a string.")
        if len(value.strip()) == 0:
            raise ValueError("Name must not be empty.")
        if hasattr(self, '_name') and self._name is not None:
            raise AttributeError("Name cannot be changed after instantiation.")
        self._name = value

    def create_author(self, cursor):
        """Insert a new author into the database."""
        cursor.execute("INSERT INTO authors (name) VALUES (?)", (self._name,))
        self._id = cursor.lastrowid

    @classmethod
    def get_all_authors(cls, cursor):
        """Fetch all authors from the database."""
        cursor.execute("SELECT * FROM authors")
        authors_data = cursor.fetchall()
        return [cls(id=row[0], name=row[1]) for row in authors_data]

    def articles(self, cursor):
        """Get all articles for this author."""
        if self._id is None:
            raise ValueError("Author ID is not set. Cannot fetch articles.")
        cursor.execute("SELECT * FROM articles WHERE author_id = ?", (self._id,))
        return cursor.fetchall()

    def magazines(self, cursor):
        """Get all magazines linked to this author's articles."""
        if self._id is None:
            raise ValueError("Author ID is not set. Cannot fetch magazines.")
        cursor.execute("""
            SELECT DISTINCT magazines.*
            FROM magazines
            JOIN articles ON magazines.id = articles.magazine_id
            WHERE articles.author_id = ?
        """, (self._id,))
        return cursor.fetchall()

    def __repr__(self):
        return f"<Author id={self._id} name='{self._name}'>"
