from utils.cell import unhash_cell
import logging
from utils.entity import Entity

TURN_END = ' GTF80146042'
END_FIGHT = 'GCK|1|Xelit'

"""
DEBUG:root:   Data: GIC|80146042;252;1
DEBUG:root:   Data: GR180146042  # READY
DEBUG:root:   Data: GIC|-1;182;1|80146042;252;1
DEBUG:root:   Data: GS
DEBUG:root:   Data: GTL|80146042|-1
DEBUG:root:   Data: Gd17;0;;25;0;25;0
DEBUG:root:   Data: GTM|-1;0;10;4;6;182;;10|80146042;0;534;8;5;252;;534
DEBUG:root:   Data: GTS80146042|29000
DEBUG:root:   Data: GA300157;210
DEBUG:root:   Data: As28311469,28264000,29882000|1707804|2|2|0~0,0,0,0,0,0|534,534|10000,10000|410|110|6,2,0,0,8|3,2,0,0
,5|0,-100,0,0|0,114,0,0|121,40,0,0|0,-100,0,0|0,410,0,0|0,-100,0,0|0,0,0,0|1,0,0,0|0,8,0,0|0,0,0,0|0,0,0,0|0,0,0,0|0,0,0
,0|0,2,0,0|0,0,0,0|0,0,0,0|0,8,0,0|0,0,0,0|30,10,0,0|30,10,0,0|0,0,0,0|0,0,0,0|0,0,0,0|0,0,0,0|0,0,0,0|0,0,0,0|0,0,0,0|0
,0,0,0|0,0,0,0|0,0,0,0|0,0,0,0|0,0,0,0|0,0,0,0|0,5,0,0|0,0,0,0|0,0,0,0|0,0,0,0|0,5,0,0|0,0,0,0|0,0,0,0|5
DEBUG:root:   Data: GAS80146042
DEBUG:root:   Data: GA;300;80146042;157,210,808,5,11,1,1
DEBUG:root:{'debug_action_name': '', 'entity_id': 0, 'cell': 0, 'type': 300}
DEBUG:root:   Data: GA;100;80146042;-1,-10
DEBUG:root:{'debug_action_name': '', 'entity_id': 0, 'cell': 0, 'type': 100}
DEBUG:root:   Data: GA;103;80146042;-1
DEBUG:root:{'debug_action_name': '', 'entity_id': 0, 'cell': 0, 'type': 103}
DEBUG:root:   Data: GdOK17
DEBUG:root:   Data: OQ57182663|3
DEBUG:root:   Data: Ow319|1005
DEBUG:root:   Data: OQ57182664|4
DEBUG:root:   Data: Ow320|1005
DEBUG:root:   Data: GE14917|80146042|0|2;80146042;Xelit;74;0;28264000;28311469;29882000;0;0;;365~1,519~1;36|0;-1;52;1;1;;;;;;;;
DEBUG:root:   Data: GCK|1|Xelit
DEBUG:root:   Data: As28311469,28264000,29882000|1707840|2|2|0~0,0,0,0,0,0|534,534|10000,10000|410|110|6,2,0,0,8|3,2,0,0
,5|0,-100,0,0|0,114,0,0|121,40,0,0|0,-100,0,0|0,410,0,0|0,-100,0,0|0,0,0,0|1,0,0,0|0,8,0,0|0,0,0,0|0,0,0,0|0,0,0,0|0,0,0
,0|0,2,0,0|0,0,0,0|0,0,0,0|0,8,0,0|0,0,0,0|30,10,0,0|30,10,0,0|0,0,0,0|0,0,0,0|0,0,0,0|0,0,0,0|0,0,0,0|0,0,0,0|0,0,0,0|0
,0,0,0|0,0,0,0|0,0,0,0|0,0,0,0|0,0,0,0|0,0,0,0|0,5,0,0|0,0,0,0|0,0,0,0|0,0,0,0|0,5,0,0|0,0,0,0|0,0,0,0|5
DEBUG:root:   Data: ILS2000
"""


# Helper class for fight sequence
class GameFight:
    def __init__(self):
        self.start_cells = []
        self.entity_turn = 0
        self.modifier = None
        self.new_entity_states: [Entity] = []
        self.fight_started = False

    def set_fight_start_cells(self, raw_data):  # GP
        infos = raw_data[2:].split('|')
        self.start_cells = []

        parsed_data = unhash_cell(infos[0])
        for i in range(0, len(parsed_data), 2):
            self.start_cells.append((parsed_data[i] << 6) + parsed_data[i+1])

        logging.debug('Fight: StartCells {}'.format(self.start_cells))

    def set_entity_turn(self, raw_data):  # GTS80146042|29000
        self.entity_turn = int(raw_data[3:].split('|')[0])
        logging.info('Turn {}'.format(self.entity_turn))

    @staticmethod
    def parse_fight_state(raw_data):  # GTM|-1;0;190;7;4;222;;190|-2;1|-3;1|80146042;0;534;8;5;311;;534
        infos = raw_data[4:].split('|')
        entities = []
        for info in infos:
            data = list(map(lambda x: int(x) if x.lstrip('-').isdigit() else x, info.split(';')))
            if data[1] == 1:
                entities.append(Entity(id=data[0], dead=True))
            elif len(data) > 5:
                entities.append(Entity(id=data[0], health=data[2], pa=data[3], pm=data[4], cell=data[5]))
        return entities

    @staticmethod
    def parse_fight_ready(raw_data):  # GR180146042
        state = int(raw_data[2])
        id = int(raw_data[3:])
        return {"entity_id": id, "ready_state": True if state > 0 else False}

if __name__ == '__main__':
    GameFight.parse_fight_ready('GR180146042')