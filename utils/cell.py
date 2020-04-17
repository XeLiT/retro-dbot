from utils.contants import *


def unhash_cell(raw_cell):
    return [ZKARRAY.index(i) for i in raw_cell]


class Cell:
    def __init__(self, raw_data):
        self.raw_data = raw_data
        self.entity = None
        self.color = 'black'
        cd = unhash_cell(raw_data)
        self.isActive = (cd[0] & 32 >> 5) == 1
        self.lineOfSight = (cd[0] & 1) == 1
        self.layerGroundRot = cd[1] & 48 >> 4
        self.groundLevel = cd[1] & 15
        self.movement = ((cd[2] & 56) >> 3)
        self.layerGroundNum = (cd[0] & 24 << 6) + (cd[2] & 7 << 6) + cd[3]
        self.layerObject1Num = ((cd[0] & 4) << 11) + ((cd[4] & 1) << 12) + (cd[5] << 6) + cd[6]
        self.layerObject2Num = ((cd[0]&2)<<12) + ((cd[7]&1)<<12) + (cd[8]<<6) + cd[9]
        self.isSun = self.layerObject1Num in SUN_MAGICS or self.layerObject2Num in SUN_MAGICS
        self.text = str(self.movement)

    def set_default_color(self):
        if self.isSun:
            self.color = 'yellow'
            self.text = 'S'
        elif self.isActive:
            self.text = ' '
            self.color = 'white'

    def set_entity(self, entity):
        if not entity:
            self.entity = None
            self.set_default_color()
        else:
            self.entity = entity
            self.color = 'red'
            self.text = self.entity.type[0]

    def __str__(self):
        return self.text
