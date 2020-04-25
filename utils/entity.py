class Entity:
    def __init__(self, type=None, cell=0, **kwargs):
        self.type = type
        self.name = ''
        self.cell = cell
        self.health = 0
        self.pa = 0
        self.pm = 0
        self.dead = False
        self.ready = False
        self.__dict__.update(kwargs)

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return self.__str__()