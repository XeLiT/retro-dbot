

class GameState:
    def __init__(self):
        self.map = None
        self.lastMap = None
        self.playerCell = 0
        self.isFighting = False
        self.entities = []

    def update(self):
        if self.map:
            self.map.debug()

    def update_entities(self, new_entities=None):
        if new_entities:
            self.entities = new_entities
        self.map.reset_cells()
        for e in self.entities:
            self.map.cells[e.cell].entity = e
        self.update()

    def update_entity(self, entity_id, cell):
        entity = next((e for e in self.entities if e.id == entity_id), None)
        entity.cell = cell
        self.update_entities()

    def update_map(self, new_map):
        self.lastMap = self.map
        self.map = new_map
        self.update()