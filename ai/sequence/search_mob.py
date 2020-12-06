import logging
import math
import input.coordinates as coord
from utils.helpers.collection import Collection

TICK = 0.5

# SearchMob: Sequence to choose a mob and start a fight, use Observable design pattern
class SearchMob():
    def __init__(self, player) -> None:
        self.player = player
        self.gs = self.player.game_state
        self.w = self.player.window
        self.kb = self.player.keyboard

    def loop(self):
        logging.info('SearchMob Sequence')
        self.find_group_mob()
        self.fight_placement()
        self.fight_turn()


    def find_group_mob(self):
        logging.info(f'SearchMob find_group_mob')
        while not self.gs.is_fighting:
            self.player.wait_until(lambda x: Collection(x.entities).find_one(type='GroupMob'))
            entity = Collection(self.gs.entities).find_one(type='GroupMob')
            if entity.cell == 0:
                logging.error(f'Group {entity} has no cell !')
            self.w.click_cell(entity.cell, True)
            self.player.wait_until(lambda x: x.is_fighting, 15)

    def fight_placement(self):
        self.w.click(*coord.COORD_READY)
        self.player.wait_until(lambda x: x.game_fight.fight_started, 5)

    def get_player(self):
        return self.gs.map.cells[self.gs.get_player_entity().cell]

    def get_nearest(self):
        player_cell = self.get_player()
        mob_cells = list(map(lambda x: self.gs.map.cells[x.cell], self.gs.get_mob_entities()))
        nearest = min(mob_cells, key=lambda x: dist(player_cell.cellIJ, x.cellIJ))
        return nearest.entity

    def fight_turn(self):
        # TODO find nearest enemy
        nearest = self.get_nearest()
        path = self.gs.map.graph

        pass

    def in_range(self):
        pass

    def end_fight(self):
        # TODO close end message
        pass