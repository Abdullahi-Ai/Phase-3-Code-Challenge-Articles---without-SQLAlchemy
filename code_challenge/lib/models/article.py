

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

    def create_author(self, cursor):
        cursor.execute("INSERT INTO authors (name) VALUES (?)", (self._name,))
        self._id = cursor.lastrowid

    @classmethod
    def get_all_authors(cls, cursor):
        cursor.execute("SELECT * FROM authors")
        authors_data = cursor.fetchall()
        return [cls(id=row[0], name=row[1]) for row in authors_data]

    def articles(self, cursor):
        if self._id is None:
            raise ValueError("Author ID is not set. Cannot fetch articles.")
        cursor.execute("SELECT * FROM articles WHERE author_id = ?", (self._id,))
        return cursor.fetchall()

    def magazines(self, cursor):
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


class Article:
    def __init__(self, id=None, title=None, author_id=None, magazine_id=None):
        self._id = id
        self.title = title
        self.author_id = author_id
        self.magazine_id = magazine_id

    @property
    def id(self):
        return self._id

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if not isinstance(value, str):
            raise TypeError("Title must be a string.")
        if len(value.strip()) == 0:
            raise ValueError("Title must not be empty.")
        self._title = value

    def create_article(self, cursor):
        cursor.execute(
            "INSERT INTO articles (title, author_id, magazine_id) VALUES (?, ?, ?)",
            (self._title, self.author_id, self.magazine_id)
        )
        self._id = cursor.lastrowid

    @classmethod
    def get_all_articles(cls, cursor):
        cursor.execute("SELECT * FROM articles")
        articles_data = cursor.fetchall()
        return [
            cls(id=row[0], title=row[1], author_id=row[2], magazine_id=row[3])
            for row in articles_data
        ]

    def __repr__(self):
        return (f"<Article id={self._id} title='{self._title}' "
                f"author_id={self.author_id} magazine_id={self.magazine_id}>")
