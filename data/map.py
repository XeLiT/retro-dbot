import logging
from yaswfp import swfparser
from config import MAP_DIR
from data.refs.pos import MAPID_TO_POS

HEX_CHARS = "0123456789ABCDEF"
ZKARRAY = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_"
SUN_MAGICS = [1030, 1029, 4088]

class Map:
    def __init__(self, id, date, raw_key):
        self.path = '{}/{}_{}{}.swf'.format(MAP_DIR, id, date, 'X' if raw_key else '')
        pos = MAPID_TO_POS[id]
        self.x = pos[0]
        self.y = pos[1]
        raw_data = swfparser.parsefile(self.path).tags[2].Actions[0].ConstantPool[14]
        data = self.decrypt_mapdata(raw_data, raw_key)
        raw_cells = [data[i:i+10] for i in range(0, len(data), 10)]
        self.cells = [self.get_cell_data(i) for i in raw_cells]
        print(*self.cells, sep='\n')

    def decrypt_mapdata(self, raw_data, raw_key):
        key = ''.join([chr(int(raw_key[i:i+2], 16)) for i in range(0, len(raw_key), 2)])
        checksum = int(HEX_CHARS[sum(map(lambda x: ord(x) & 0xf, key)) & 0xf], 16) * 2
        key_length = len(key)
        data = ''
        for i in range(0, len(raw_data), 2):
            data += chr(int(raw_data[i:i+2], 16) ^ ord(key[(int(i / 2) + checksum) % key_length]))

        return data

    def get_cell_data(self, raw_cell):
        cd = [ZKARRAY.index(i) for i in raw_cell]
        layerObject1Num = ((cd[0] & 4) << 11) + ((cd[4] & 1) << 12) + (cd[5] << 6) + cd[6]
        layerObject2Num = ((cd[0]&2)<<12) + ((cd[7]&1)<<12) + (cd[8]<<6) + cd[9]
        movement = ((cd[2]&56) >> 3)
        return 'sun' if movement == 2 or layerObject1Num in SUN_MAGICS else layerObject2Num