import os
import logging
from yaswfp import swfparser
from config import MAP_DIR

ZKARRAY = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_"
SUN_MAGICS = [1030, 1029, 4088]

class Map:
    def __init__(self, id, date, key):
        self.path = '{}_{}{}'.format(MAP_DIR, date, 'X' if key else '')
        logging.debug('Opening map ' + self.path)
        # map = swfpar
        # ser.parsefile(self.path)
        # mapId =   swfparser.parsefile(self.path).tags[2] #    Actions[0].ConstantPool
        self.mapData = swfparser.parsefile(self.path)
        new_key = ''.join([ chr(int(key[i:i+2], 16)) for i in range(0, len(key), 2)])
        print(self.new_key)
        print(self.mapData.__dict__)
        # self.mapDataLength = len(self.mapData)
        # self.raw_cells = [self.mapData[i:i+10] for i in range(0, self.mapDataLength, 10)]
        # self.cells = [self.get_cell_data(i) for i in self.raw_cells]
        # print(*self.cells, sep='\n')

        # c = Convert.ToInt64(checksum(preparedKey), 16) * 2
        def decrypt_mapdata(self, data, key, checksum):
            _loc5 = ""
            _loc6 = len(key)
            _loc7 = 0
            i = 0

            # TODO
            while i < len(data) :
                a = int(data[i:i+2], 16)
                b = Asc(k.Substring((_loc7 + c) Mod _loc6, 1))
                _loc5 &= Chr(a Xor b)
                _loc7 += 1
                i += 2
            End While

            _loc5 = unescape(_loc5)

            Return _loc5

            End Function



    def mapid_to_path(self, id):
        files = os.listdir(DIR)
        return [f for f in files if f.startswith('{}_'.format(id))][0]

    def get_cell_data(self, raw_cell):
        # Todo
        cd = [ZKARRAY.index(i) for i in raw_cell]
        layerObject1Num = ((cd[0] & 4) << 11) + ((cd[4] & 1) << 12) + (cd[5] << 6) + cd[6]
        layerObject2Num = ((cd[0]&2)<<12) + ((cd[7]&1)<<12) + (cd[8]<<6) + cd[9]
        movement = ((cd[2]&56) >> 3)
        return 'sun' if movement == 2 or layerObject1Num in SUN_MAGICS else layerObject2Num


if __name__ == '__main__':
    map = Map(364)
