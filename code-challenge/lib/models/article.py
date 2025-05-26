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
