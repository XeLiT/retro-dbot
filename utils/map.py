from urllib.parse import unquote
import yaswfp.swfparser as swfparser
from config import MAP_DIR
from utils.refs.pos import MAPID_TO_POS
from utils.entity import Entity
from utils.cell import *
from utils.helpers.collection import Collection
from ai.algorithm.graph import Graph
from ai.algorithm.line_of_sight import Sight_Bresenham
import logging

class Map:
    def __init__(self, id, date, raw_key):
        self.path = '{}/{}_{}{}.swf'.format(MAP_DIR, id, date, 'X' if raw_key else '')
        self.x, self.y = MAPID_TO_POS[id]
        swf = swfparser.parsefile(self.path)
        raw_map_data = swf.tags[2].Actions[0].ConstantPool[14]
        self.width = int(swf.tags[2].Actions[17].Integer)
        self.height = (int(swf.tags[2].Actions[20].Integer) - 1) * 2
        data = self.decrypt_mapdata(raw_map_data, raw_key)
        raw_cells = [data[i:i+10] for i in range(0, len(data), 10)]
        self.cells = [Cell(i) for i in raw_cells]
        self.matrix = self.matrixfy()
        self.graph = Graph.from_matrix2d(self.matrix, lambda x: x.obj.dead)
        self.sight = Sight_Bresenham.from_matrix2d(self.matrix, lambda pos: self.matrix[pos[0]][pos[1]].is_obstacle())

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
            if cell in indexed_by_cell and int(cell) < len(self.cells):
                self.cells[int(cell)].set_entity(indexed_by_cell[cell])
            else:
                logging.error("indexed_by_cell out of range key: {cell} obj: {indexed_by_cell}")

    def _cell_to_node(self, cell: Cell):
        i, j = cell.posIJ
        node_index = j + i * len(self.graph.nodes[0])
        return self.graph.nodes[node_index]

    def get_path(self, from_cell, to_cell):
        self.graph.initial = self._cell_to_node(from_cell)
        self.graph.target = self._cell_to_node(to_cell)
        return list(map(lambda x: x.obj, self.graph.astar()))

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
                cell = diags[i][j]
                cell.posIJ = [i, j]
                matrix_out[j].append(cell)
        return matrix_out
