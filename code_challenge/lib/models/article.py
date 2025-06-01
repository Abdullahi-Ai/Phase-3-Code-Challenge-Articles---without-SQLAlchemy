## Article.py

class Author:
    def __init__(self, id=None, name=None):
        self._id = id
        self.name = name

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

    
    def create_magazine(self, cursor):
        cursor.execute("INSERT INTO magazines (name, category) VALUES (?, ?)", (self._name, self._category))
        self._id = cursor.lastrowid

    @classmethod
    def get_all_authors(cls, cursor):
        """Fetch all authors from the database."""
        cursor.execute("SELECT * FROM authors")
        authors_data = cursor.fetchall()
        return [cls(id=row[0], name=row[1]) for row in authors_data]
    
    def articles(self, cursor):
        """Get all articles for this author."""
        cursor.execute("SELECT * FROM articles WHERE author_id = ?", (self._id,))
        return cursor.fetchall()
    
    def magazines(self, cursor):
        """Get all magazines linked to this author's articles."""
        cursor.execute("""
            SELECT DISTINCT magazines.*
            FROM magazines
            JOIN articles ON magazines.id = articles.magazine_id
            WHERE articles.author_id = ?
        """, (self._id,))
        return cursor.fetchall()
        

