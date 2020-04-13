import logging
from utils.collection import Collection
from utils.entity import Entity
from frames.map_discover import MapDiscover
from config import PLAYER_NAME


class GameState:
    def __init__(self, gui):
        self.map = None
        self.lastMap = None
        self.playerCell = 0
        self.isFighting = False
        self.entities = []
        self.map_id = 0
        self.gui = gui

    def update(self):
        if self.map:
            self.map.reset_cells()
            for e in self.entities:
                self.map.cells[e.cell].entity = e
            self.map.debug()

    def update_entities(self, map_frame: MapDiscover):
        logging.debug(map_frame)
        self.entities = map_frame.entities
        self.update()

    def update_entity(self, game_action):
        entity = Collection(self.entities).find_one(id=game_action.entity_id) if game_action.entity_id < 0 else None
        if entity:
            entity.cell = game_action
            self.update_entities()

    # def update_player_pos(self, cell):
    #     entity = next((e for e in self.entities if hasattr(e, 'name') and e.name == PLAYER_NAME), None)
    #     if entity:
    #         self.entities.remove(entity)
    #     self.entities.append(Entity(type='Player', cell=cell, name=PLAYER_NAME))
    #     self.update_entities()

    def update_map(self, map_change):
        self.entities = []
        self.lastMap = self.map
        self.map = map_change.map
        self.update()
