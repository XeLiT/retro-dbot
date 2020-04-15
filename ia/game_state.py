import logging
from utils.collection import Collection
from utils.entity import Entity
from utils.map import Map
from frames.map_infos import MapInfos
from config import PLAYER_NAME


class GameState:
    def __init__(self, gui):
        self.map: Map = None
        self.lastMap = None
        self.playerCell = 0
        self.isFighting = False
        self.entities = []
        self.map_id = 0
        self.gui = gui

    def update(self):
        if self.map:
            self.map.remove_entities()
            self.map.place_entities(self.entities)
            self.gui.table.set_data(self.map.matrixfy())

    def update_entities(self, map_infos: MapInfos):
        if map_infos.action == '+' and not self.entities:
            self.entities = map_infos.entities
        elif self.entities and map_infos.entities:
            entity_id = map_infos.entities[0].id
            if map_infos.action == '-':
                self.entities = list(filter(lambda x: x.id != entity_id))
            else:
                self.entities.append(map_infos.entities[0])
        self.update()

    def update_entity(self, game_action):
        entity = Collection(self.entities).find_one(id=game_action.entity_id)
        if entity:
            entity.cell = game_action.cell
            self.update()

    def update_map(self, map_change):
        self.entities = []
        self.lastMap = self.map
        self.map = map_change.map
        self.update()
