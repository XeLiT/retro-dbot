import logging
import input.coordinates as coord
from utils.helpers.collection import Collection
from ai.sequence.sequence import Sequence
from ai.eye import IMAGE_CLOSE_BUTTON_2, IMAGE_BUTTON_OK
import time
import config

ENGAGE_TRIES_PER_MAP = 3
ENGAGE_TRIES_PER_MOB = 2

# SearchMob: Sequence to choose a mob and start a fight, use Observable design pattern
class SearchMob(Sequence):

    def loop(self):
        logging.info('SearchMob Sequence')
        tries = 1
        while not self.gs.is_fighting:
            self.check_menus()
            group_mobs = self.get_group_mobs()
            if len(group_mobs) > 0:
                for group_mob in group_mobs:
                    is_engaged = self.engage_group_mob(group_mob)
                    if is_engaged:
                        return

            tries += 1
            logging.error(f"SearchMob loop retry {tries}, len(group_mobs)={len(group_mobs)}")
            if tries > ENGAGE_TRIES_PER_MAP:
                self.next_map()

    def engage_group_mob(self, group_mob):
        logging.info(f'SearchMob: engaging {group_mob}')
        tries = 1
        while not self.player.wait_until(lambda x: x.is_fighting, self.gs, timeout=5) and tries <= ENGAGE_TRIES_PER_MOB:
            self.w.click_rescue()
            self.check_menus()
            self.tick()
            self.w.click_fight(group_mob.cell)
            tries += 1

        if self.gs.is_fighting:
            return True
        else:
            logging.error(f"SearchMob click_fight too many retries for mob {str(group_mob)}")
            return False

    def next_map(self):
        pass # TODO

    def get_group_mobs(self):
        mobs = self.wait_until(lambda x: Collection(x.entities).find_all(type='GroupMob'), self.gs, 5)
        if not mobs or len(mobs) == 0:
            return None
        return list(filter(lambda m: m.cell != 0 and sum(m.levels) <= config.MAX_MOB_GROUP_LEVEL and not self.gs.map.cells[m.cell].isSun, mobs))

    def check_menus(self):
        match = self.eye.wait_for_image(IMAGE_CLOSE_BUTTON_2)
        logging.info(f"SearchMob check_menus {str(match)}")
        if match[0]:
            self.w.click(*match[1].center)

        match = self.eye.wait_for_image(IMAGE_BUTTON_OK)
        if match[0]:
            self.w.click(*match[1].center)
