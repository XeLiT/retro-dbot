import logging
import time
import input.coordinates as coord
from utils.collection import Collection

TICK = 0.5


class DummyFighter:
    def __init__(self, player) -> None:
        self.player = player
        self.gs = self.player.game_state
        self.w = self.player.window
        self.kb = self.player.keyboard

    def find_group_mob(self):
        self.player.wait_until(lambda x: not x.is_fighting)
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
        self.player.wait_until(lambda x: x.game_fight.)

    def fight_turn(self):
        # TODO find nearest enemy
        pass

    def end_fight(self):
        # TODO close end message
        pass