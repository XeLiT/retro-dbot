import logging
import math
from urllib.parse import unquote
import yaswfp.swfparser as swfparser
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
        swf = swfparser.parsefile(self.path)
        raw_map_data = swf.tags[2].Actions[0].ConstantPool[14]
        self.width = int(swf.tags[2].Actions[17].Integer)
        self.height = (int(swf.tags[2].Actions[20].Integer) - 1) * 2
        data = self.decrypt_mapdata(raw_map_data, raw_key)
        raw_cells = [data[i:i+10] for i in range(0, len(data), 10)]
        self.cells = [Cell(i) for i in raw_cells]

    def debug(self):
        for row in self.matrixfy():
            print(''.join(list(map(str, row))))
        print('_'*self.width)

    def matrixfy(self) -> [[Cell]]:
        rows = []
        i = self.width - 1
        row_number = 1
        while row_number < self.height:
            if row_number % 2 == 0:
                take = self.width - 1
                rows.append(self.cells[i+1:i+take] + [Cell()])
                i += take
            else:
                take = self.width
                rows.append(self.cells[i+1:i+take])
                i += take
            row_number += 1
        return Map.rotate(rows)

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
            c.set_entity(None)

    def place_entities(self, entities: [Entity]):
        indexed_by_cell = Collection(entities).index_by('cell')
        for cell in indexed_by_cell.keys():
            self.cells[int(cell)].set_entity(indexed_by_cell[cell])

    @staticmethod
    def _diag(matrix, size_i, size_j, i, j):
        padding = [Cell()] * j + [Cell()] * int(i / 2)
        l = j
        data = []
        for k in range(i, size_i):  # loop on rows
            if l >= size_j:
                break
            data.append(matrix[k][l])
            if k % 2 == 1:
                l += 1
        ret = padding + data + padding
        paddr_len = size_i - len(ret)
        if paddr_len > 0:
            ret += [Cell()] * paddr_len
        return ret

    @staticmethod
    def rotate(matrix):
        size_i = len(matrix)
        size_j = len(matrix[0])

        diags = [Map._diag(matrix, size_i, size_j, 0, 0)]
        for j in range(1, size_j):  # right side
            diags.append(Map._diag(matrix, size_i, size_j, 0, j))

        for i in range(2, size_i, 2):  # low side
            diags.insert(0, Map._diag(matrix, size_i, size_j, i, 0))

        matrix_out = []
        for j in range(len(diags[0])):
            matrix_out.append([])
            for i in range(len(diags)):
                matrix_out[j].append(diags[i][j])
        return matrix_out


if __name__ == '__main__':
    DATA = '364b23364e7c58203471383e6a517d573d5b316144232451213543776a267e5830364e74646867274875594c235f4b214f495e3172253242644a415e35477d4a6c32697d34282837652532352a452e262c7d732532356e3c443131726467515970542e6961413d5228374723716a656740204d282679634967645c5b492e594f683d375f4a7d5e71413b322f642930336c4f582667234f426c665f3b7435622f582a3a356c6850427a665b6e7d29745e5336562c6b6e3978253235433e24742e7e5e704265752132402064645b73'
    m = Map('7438', '0706131721', DATA)
    m.debug()
    # matrix = ['abc', 'def', 'ghi', 'jkl', 'mno', 'pqr']
    # Map.rotate(matrix)






