import logging
import input.coordinates as coord
from utils.helpers.collection import Collection
from ai.sequence.sequence import Sequence
import time

# SearchMob: Sequence to choose a mob and start a fight, use Observable design pattern
class SearchMob(Sequence):
    def loop(self):
        logging.info('SearchMob Sequence')
        self.find_group_mob()

    def find_group_mob(self):
        logging.info(f'SearchMob find_group_mob')
        while not self.gs.is_fighting:
            self.wait_until(lambda x: Collection(x.entities).find_one(type='GroupMob'), self.gs, 5)
            entity = Collection(self.gs.entities).find_one(type='GroupMob')
            if entity.cell == 0:
                logging.error(f'Group {entity} has no cell !')
            else:
                logging.info(f'SearchMob: {entity}')
                self.w.click_cell(entity.cell, False)
                if not self.player.wait_until(lambda x: x.is_fighting, self.gs, timeout=5):
                    self.w.click_cell(entity.cell, True)  # Retry 2
