import logging
from urllib.parse import unquote
from yaswfp import swfparser
from config import MAP_DIR
from utils.refs.pos import MAPID_TO_POS
from utils.entity import Entity
from utils.cell import Cell
from utils.collection import Collection
from utils.contants import *


class Map:
    def __init__(self, id, date, raw_key):
        self.path = '{}/{}_{}{}.swf'.format(MAP_DIR, id, date, 'X' if raw_key else '')
        pos = MAPID_TO_POS[id]
        self.x = pos[0]
        self.y = pos[1]
        raw_map_data = swfparser.parsefile(self.path).tags[2].Actions[0].ConstantPool[14]
        data = self.decrypt_mapdata(raw_map_data, raw_key)
        raw_cells = [data[i:i+10] for i in range(0, len(data), 10)]
        self.cells = [Cell(i) for i in raw_cells]

    def debug(self):
        for row in self.matrixfy():
            print(''.join(list(map(str, row))))
        print('_'*MAP_WIDTH)

    def matrixfy(self) -> [[Cell]]:
        rows = []
        i = 0
        row_number = 0
        while row_number < MAP_HEIGHT:
            if row_number % 2 == 0:
                take = MAP_WIDTH - 1
                rows.append(self.cells[i:i+take])
                i += take
            else:
                take = MAP_WIDTH
                rows.append(self.cells[i:i+take])
                i += take
            row_number += 1
        return rows

    def decrypt_mapdata(self, raw_data, raw_key):
        key = unquote(''.join([chr(int(raw_key[i:i+2], 16)) for i in range(0, len(raw_key), 2)]))
        checksum = int(HEX_CHARS[sum(map(lambda x: ord(x) & 0xf, key)) & 0xf], 16) * 2
        key_length = len(key)
        data = ''
        for i in range(0, len(raw_data), 2):
            data += chr(int(raw_data[i:i+2], 16) ^ ord(key[(int(i / 2) + checksum) % key_length]))
        return data

    def remove_entities(self):
        for c in self.cells:
            c.entity = None

    def place_entities(self, entities: [Entity]):
        indexed_by_cell = Collection(entities).index_by('cell')
        for cell in indexed_by_cell.keys():
            logging.debug(cell)
            self.cells[int(cell)].set_entity(indexed_by_cell[cell])

