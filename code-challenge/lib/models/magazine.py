## magazine.py
class Magazine:
    def __init__(self, id=None, name=None, category=None):

        self._id = id
        self.name = name
        self.category = category

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name
    
    