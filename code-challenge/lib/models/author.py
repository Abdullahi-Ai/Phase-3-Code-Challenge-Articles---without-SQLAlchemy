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
             """Insert a new author into the database."""
             cursor.execute("INSERT INTO authors (name) VALUES (?)", (self._name,))
            self._id = cursor.lastrowid


       
        



