from utils.map import unhash_cell
import logging
from ia.game_state import GameState

DATA = 'GA0;1;80146042;agtfge'


# GA
class GameAction:
    def __init__(self, raw_data):
        self.debug_action_name = ''
        self.entity_id = None
        self.cell = None
        data = raw_data[2:].split(';')

        if raw_data.startswith('GA;1;'):
            self.debug_action_name = 'GroupMob Move'
            self.entity_id = int(data[2])
            self.set_cell(data[3])

        elif raw_data.startswith('GA0;1'):
            self.debug_action_name = 'Player Move'
            # map_id = data[2]
            # entity_id = int(data[1])
            self.set_cell(data[3])

        logging.debug(self.__dict__)

    def set_cell(self, raw_cell):
        cell_data = unhash_cell(raw_cell[len(raw_cell)-2:])
        self.cell = cell_data[0] * 64 + cell_data[1]


if __name__ == '__main__':
    ga = GameAction(DATA)