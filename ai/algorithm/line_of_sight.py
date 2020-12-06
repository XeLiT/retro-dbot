import numpy as np
import matplotlib.pyplot as plt

WORLD="""
..................
..................
...#####..........
...#......#.......
.#...0............
..##....#.##......
....###...#.......
..................
"""
CELL_VALUES = {
    "0": 20,
    "#": 10,
    ".": 0,
}

def bresenham_line(x0, y0, x1, y1):
    dx = x1 - x0
    dy = y1 - y0

    xsign = 1 if dx > 0 else -1
    ysign = 1 if dy > 0 else -1

    dx = abs(dx)
    dy = abs(dy)

    if dx > dy:
        xx, xy, yx, yy = xsign, 0, 0, ysign
    else:
        dx, dy = dy, dx
        xx, xy, yx, yy = 0, ysign, xsign, 0

    D = 2*dy - dx
    y = 0

    for x in range(dx + 1):
        yield x0 + x*xx + y*yx, y0 + x*xy + y*yy
        if D >= 0:
            y += 1
            D -= 2*dx
        D += 2*dy

# Compute bresenham lines on each point of the map and evaluates if an obstacle is between
class Sight_Bresenham():
    def __init__(self, world_string, obstable, player_obj):
        lines = world_string.split('\n')[1:-1]
        self.player_obj = player_obj
        self.player_position = []
        self._max_x = len(lines)
        self._max_y = len(lines[0])
        self._obstable = CELL_VALUES[obstable]
        self.world = self._read_world(lines)
        self.sight = np.zeros([self._max_x, self._max_y])

    def is_obstable(self, p):
        return self.world[p[0]][p[1]] == self._obstable

    def distance(self, p):
        diff_x = abs(p[0] - self.player_position[0])
        diff_y = abs(p[1] - self.player_position[1])
        return diff_x + diff_y

    def _read_world(self, lines):
        output = np.zeros([self._max_x, self._max_y])
        for i in range(len(lines)):
            for j in range(len(lines[0])):
                obj = lines[i][j]
                if obj == self.player_obj:
                    self.player_position = [i, j]
                output[i][j] = CELL_VALUES[obj]
        return output

    def display(self):
        plt.imshow(self.world)
        plt.show()

    def compute_sight(self, max_range):
        sight_mask = np.zeros([self._max_x, self._max_y])
        for x in range(self._max_x):
            for y in range(self._max_y):
                target = (x, y)
                if self.distance(target) <= max_range and not self.is_obstable(target):
                    line = list(bresenham_line(self.player_position[0], self.player_position[1], target[0], target[1]))
                    has_obstacle = False
                    for pt in line:
                        if self.is_obstable(pt):
                            has_obstacle = True
                    if not has_obstacle:
                        sight_mask[target[0]][target[1]] = 4

        self.world += sight_mask

if __name__ == "__main__":
    s = Sight_Bresenham(WORLD, "#", "0")
    s.compute_sight(5)
    s.display()