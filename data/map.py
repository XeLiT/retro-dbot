import copy
from urllib.parse import unquote
from yaswfp import swfparser
from config import MAP_DIR
from data.refs.pos import MAPID_TO_POS

HEX_CHARS = "0123456789ABCDEF"
ZKARRAY = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_"
SUN_MAGICS = [1030, 1029, 4088, 34]
MAP_LENGTH = 15
RED = lambda x: '\033[1;31m{}\033[0m'.format(x)
YELLOW = lambda x: '\033[0;33m{}\033[0m'.format(x)
DIM = lambda x: '\e[2m{}\e[22'.format(x)

def unhash_cell(raw_cell):
    return [ZKARRAY.index(i) for i in raw_cell]

class Cell:
    def __init__(self, raw_data):
        cd = unhash_cell(raw_data)
        self.isActive = (cd[0] & 32 >> 5) == 1
        self.lineOfSight = (cd[0] & 1) == 1
        self.layerGroundRot = cd[1] & 48 >> 4
        self.groundLevel = cd[1] & 15
        self.movement = ((cd[2] & 56) >> 3)
        self.layerGroundNum = (cd[0] & 24 << 6) + (cd[2] & 7 << 6) + cd[3]
        self.layerObject1Num = ((cd[0] & 4) << 11) + ((cd[4] & 1) << 12) + (cd[5] << 6) + cd[6]
        self.layerObject2Num = ((cd[0]&2)<<12) + ((cd[7]&1)<<12) + (cd[8]<<6) + cd[9]
        self.isSun = self.layerObject1Num in SUN_MAGICS
        self.entity = None

    def __str__(self):
        if self.isSun:
            return YELLOW('S')
        elif self.entity:
            return RED(self.entity.type[0])
        if not self.isActive:
            return 'X'
        return DIM(str(self.movement))


class Map:
    def __init__(self, id, date, raw_key):
        self.path = '{}/{}_{}{}.swf'.format(MAP_DIR, id, date, 'X' if raw_key else '')
        pos = MAPID_TO_POS[id]
        self.x = pos[0]
        self.y = pos[1]
        raw_map_data = swfparser.parsefile(self.path).tags[2].Actions[0].ConstantPool[14]
        data = self.decrypt_mapdata(raw_map_data, raw_key)
        raw_cells = [data[i:i+10] for i in range(0, len(data), 10)]
        self.default_cells = [Cell(i) for i in raw_cells]
        self.reset_cells()

    def debug(self):
        strings = list(map(str, self.cells))
        rows = [''.join(strings[i:i+MAP_LENGTH]) for i in range(0, len(self.cells), MAP_LENGTH)]
        for row in rows:
            print(row)

    def decrypt_mapdata(self, raw_data, raw_key):
        key = unquote(''.join([chr(int(raw_key[i:i+2], 16)) for i in range(0, len(raw_key), 2)]))
        checksum = int(HEX_CHARS[sum(map(lambda x: ord(x) & 0xf, key)) & 0xf], 16) * 2
        key_length = len(key)
        data = ''
        for i in range(0, len(raw_data), 2):
            data += chr(int(raw_data[i:i+2], 16) ^ ord(key[(int(i / 2) + checksum) % key_length]))

        return data

    def reset_cells(self):
        self.cells = copy.deepcopy(self.default_cells)