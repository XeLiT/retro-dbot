from utils.cell import unhash_cell
import logging
from utils.entity import EntityModifier, ENTITY_STAT_ID


class GameAction:
    def __init__(self):
        self.debug_action_name = ''
        self.entity_id = 0
        self.cell = 0
        self.is_enter_fight = False
        self.is_moving = False
        self.action_type = 0
        self.modifier = None

    def parse_action(self, raw_data):
        data = raw_data[2:].split(';')
        if len(data) > 2:
            self.action_type = int(data[1])

            if self.action_type == 1:
                self.debug_action_name = 'Moving to'
                self.entity_id = int(data[2])
                self._set_cell(data[3])
                self.is_moving = True

            elif self.action_type == 103:
                self.modifier = EntityModifier(entity=int(data[3]), dead=True)

            elif self.action_type in [100, 108, 110, 127, 129, 128, 78, 169, 101, 102, 111, 120, 168]:   # GA;100;-1;80146042,-14
                if str(self.action_type) in ENTITY_STAT_ID.keys():
                    entity, value = map(int, data[3].split(','))
                    self.modifier = EntityModifier(entity=entity)
                    self.modifier.__setattr__(ENTITY_STAT_ID[str(self.action_type)], value)
                    logging.info('Modifier {}'.format(self.modifier.__dict__))

            elif self.action_type == 905:
                self.entity_id = int(data[2])
                self.is_enter_fight = True
            logging.debug(self.__dict__)
        return self

    def _set_cell(self, raw_cell):
        cell_data = unhash_cell(raw_cell[len(raw_cell)-2:])
        self.cell = cell_data[0] * 64 + cell_data[1]

    def parse_entity_start_cell(self, raw_data):  # GIC|-1;182;1|80146042;252;1
        entity = raw_data[4:].split('|')[0].split(';')
        self.is_moving = True
        self.entity_id = int(entity[0])
        self.cell = int(entity[1])
        return self

if __name__ == '__main__':
    ga = GameAction(DATA)