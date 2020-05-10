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


ENTITY_STAT_ID = {
    "100": "health",
    "102": "pa",
    "129": "pm",
}


class EntityModifier:
    def __init__(self, health=0, pa=0, pm=0, **kwargs):
        self.__dict__.update(kwargs)

    def apply(self, entity: Entity):
        if entity:
            for attr in ENTITY_STAT_ID.values():
                if hasattr(entity, attr) and hasattr(self, attr):
                    if isinstance(entity.__getattribute__(attr), int):
                        entity.__setattr__(attr, entity.__getattribute__(attr) + self.__getattribute__(attr))
                    else:
                        entity.__setattr__(attr, self.__getattribute__(attr))