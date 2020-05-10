import logging
import math
import input.coordinates as coord
from utils.helpers.collection import Collection

TICK = 0.5

def dist(a: [int, int], b: [int, int]) -> float:
    return math.sqrt(pow(a[0] - b[0], 2) + pow(a[1] - b[1], 2))

def distX(a, b) -> int:
    return int(math.fabs(b[0] - a[0]))

def distY(a, b) -> int:
    return int(math.fabs(b[1] - a[1]))

class DummyFighter:
    def __init__(self, player) -> None:
        self.player = player
        self.gs = self.player.game_state
        self.w = self.player.window
        self.kb = self.player.keyboard

    def loop(self):
        logging.info('DummyFighter Loop')
        self.find_group_mob()
        self.fight_placement()
        self.fight_turn()

    def find_group_mob(self):
        logging.info(f'Player {self.player} not fighting, finding for a GroupMob')
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
        nearest = min(mob_cells, key=lambda x: dist(player_cell.cellXY, x.cellXY))
        return nearest.entity

    def fight_turn(self):
        # TODO find nearest enemy
        nearest = self.get_nearest()
        path = self.gs.map.graph

        pass

    def end_fight(self):
        # TODO close end message
        pass