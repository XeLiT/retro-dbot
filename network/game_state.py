import logging
from utils.helpers.collection import Collection, Dictionary
from utils.entity import Entity
from utils.map import Map
from network.map_infos import MapInfos
from network.game_action import GameAction
from network.game_fight import GameFight
from network.player_infos import PlayerInfos


class GameState:
    def __init__(self, gui, player_name):
        self.player_name = player_name
        self.player_entity_id = 0
        #self.player_infos = PlayerInfos()
        self.player_level = 0
        self.map: Map = None
        self.is_fighting = False
        self.entities: [Entity] = []
        self.map_id = 0
        self.gui = gui
        self.game_fight: GameFight = GameFight()
        self._map_needs_update = False

    def update_gui(self):
        self._find_player()
        if self.map:
            self.map.remove_entities()
            self.map.place_entities(self.entities)
            self.gui.table.set_data(self.map.matrix)

    def get_player_entity(self):
        entity = Collection(self.entities).find_one(id=self.player_entity_id) if self.player_entity_id else None
        return entity if entity else Collection(self.entities).find_one(name=self.player_name)

    def get_mob_entities(self):
        return Collection(self.entities).find_all(type='Mob')

    def update_player_gui(self):
        entity = self.get_player_entity()
        if entity:
            self.gui.update_player_info(entity)

    def _find_player(self):
        if not self.player_entity_id:
            entity = Collection(self.entities).find_one(name=self.player_name)
            print(entity)
            if entity:
                self.player_entity_id = entity.id
                logging.info("Found Player id: {}".format(self.player_entity_id))

    def update_map_infos(self, map_infos: MapInfos):
        if map_infos.action == '+':
            self.entities = map_infos.entities if not self.entities else self.entities + map_infos.entities
        elif map_infos.action == '-':
            entity_id = map_infos.entities[0].id
            self.entities = list(filter(lambda x: x.id != entity_id, self.entities))
        self.update_gui()
        self.update_player_gui()

    def update_entities(self, entities: [Entity]):
        for e in entities:
            to_update = Collection(self.entities).find_one(id=e.id)
            if to_update:
                to_update.__dict__.update(Dictionary(e.__dict__).filter_keys(['health', 'pa', 'pm', 'dead', 'cell']))
                logging.info('Update Entity {}'.format(e))
        self.update_player_gui()

    def update_from_action(self, game_action: GameAction):
        if game_action.is_enter_fight:
            self.set_fighting(True)
        elif game_action.is_moving:
            entity = Collection(self.entities).find_one(id=game_action.entity_id)
            if entity:
                entity.cell = game_action.cell
                self.update_gui()
        elif game_action.modifier:
            game_action.modifier.apply(Collection(self.entities).find_one(id=game_action.modifier.entity))
        self.update_player_gui()

    def update_map(self, map_change):
        self.entities = []
        self.map = map_change.map
        self.gui.table.clear()

    def set_fighting(self, fighting):
        self.is_fighting = fighting
        self.entities = []
        logging.info('Fighting {}'.format(fighting))
        self.gui.set_fighting_state(fighting)
        self.gui.table.clear()
        if fighting:
            self.game_fight = GameFight()

    def set_player_ready(self, entity_id=0, ready_state=False):
        entity = Collection(self.entities).find_one(id=entity_id)
        entity.ready = ready_state
        logging.info('set_player_ready: {} {}'.format(entity_id, ready_state))