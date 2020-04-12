from utils.map import unhash_cell
import logging
from ia.game_state import GameState

DATA = 'GA0;1;80146042;agtfge'


# GA
class GameAction:
    def __init__(self, raw_data, game_state: GameState):
        data = raw_data[2:].split(';')

        if raw_data.startswith('GA;1;'):    # MobGroup move
            entity_id = int(data[2])
            cell = int(self.get_cell(data[3]))
            logging.debug('GroupMob {} moving to {}'.format(entity_id, cell))
            game_state.update_entity(entity_id, cell)

        elif raw_data.startswith('GA0;1'):  # PlayerMove
            # map_id = data[2]
            entity_id = int(data[1])
            cell = int(self.get_cell(data[3]))
            logging.info('Player {} moving to {}'.format(entity_id, cell))
            game_state.update_player_pos(cell)

    def get_cell(self, raw_cell):
            cell_data = unhash_cell(raw_cell[len(raw_cell)-2:])
            return cell_data[0] * 64 + cell_data[1]


if __name__ == '__main__':
    ga = GameAction(DATA)