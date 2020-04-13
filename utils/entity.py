class Entity:
    def __init__(self, type, cell=0, **kwargs):
        self.type = type
        self.cell = cell
        self.__dict__.update(kwargs)

    def __str__(self):
        return str(self.__dict__)