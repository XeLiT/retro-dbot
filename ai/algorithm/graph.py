from math import inf, sqrt
from collections import defaultdict
import heapq
import numpy as np
import matplotlib.pyplot as plt
from timeit import default_timer as timer
import logging

DATA = """
.................................................
.................................................
.................................................
.................................................
.........X.E.....................................
.................................................
.................................................
.................................................
.................................................
.................................................
.................................................
.................................................
.................................................
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
.................................................
.................................................
.................................................
........................S........................
.................................................
.................................................
.................................................
.................................................
.................................................
.................................................
.................................................
.................................................
.................................................
.................................................
.................................................
.................................................
"""

DATA1 = """
......
......
..S...
......
......
XXXXXX
..E...
"""

DATA2 = """
E.X.
...S
"""

CELL_VALUES = {
    "E": 5,
    "S": 5,
    "X": 1,
    "o": 10,
    ".": 0,
}

class Edge:
    def __init__(self, node, weight=1):
        self.node = node
        self.weight = weight

class Node:
    def __init__(self, obj) -> None:
        self.obj = obj
        self.traveled = inf  # lower is better
        self.previous: Node
        self.visited = False
        self.in_queue = False

        # a-star
        self.distance_to_target = inf
        self.score = inf   #  combined heuristic, g cost + distance to_target
        # g cost = distance to other node on edge
        self.debug_edge_count = 0

    def set_score(self, target_node, edge_weight):
        self._compute_distance(target_node)
        self.score = self.distance_to_target + edge_weight

    def _compute_distance(self, target_node):
        c1 = self.obj.posIJ
        c2 = target_node.obj.posIJ
        self.distance_to_target = sqrt(pow(c1[0] - c2[0], 2) + pow(c1[1] - c2[1], 2))

    def __repr__(self):
        return self.obj.__repr__()

    def __eq__(self, o) -> bool:
        return self.obj == o.obj

    def __lt__(self, other):
        return self.score < other.score

class Graph():
    def __init__(self, nodes: [[Node]]):
        # threading.Thread.__init__(self)
        self.nodes = nodes
        self.edges = defaultdict(list)
        self.initial = None
        self.target = None

    def add_edge(self, from_node, to_node, weight=1):
        self.edges[id(from_node)].append(Edge(to_node, weight))
        self.edges[id(to_node)].append(Edge(from_node, weight))
        from_node.debug_edge_count += 1
        to_node.debug_edge_count += 1

    def _build_path(self):
        path = []
        n = self.target
        while n.traveled != 0:
            path.append(n)
            n = n.previous
        return path

    def astar(self, initial=None, target=None, entity_cb=None) -> [Node]:
        start = timer()
        if not initial or not target:
            return []
        self.initial = initial
        self.target = target

        self.initial.traveled = 0
        self.initial.set_score(self.target, 0)
        queue = [self.initial]
        self.initial.in_queue = True
        heapq.heapify(queue)
        debug_visited_edge = 0

        while len(queue):
            from_node = heapq.heappop(queue)
            from_node.visited = True
            edges = self.edges[id(from_node)]
            for edge in edges:
                debug_visited_edge += 1
                node = edge.node
                if not node.visited and not node.in_queue:
                    node.set_score(self.target, edge.weight)
                    node.previous = from_node
                    if node == self.target:
                        end = timer()
                        path = self._build_path()
                        logging.debug(f"Graph astar: PATH FOUND of lenght {len(path)} in {(end - start) * 1000}ms")
                        return self._build_path()
                    heapq.heappush(queue, node)
                    node.in_queue = True
        end = timer()
        logging.debug(f"Graph astar: PATH NOT FOUND completed in {(end - start) * 1000}ms")
        return []

    @staticmethod
    def from_matrix2d(matrix2d, is_dead_cb):
        size_i = len(matrix2d)
        size_j = len(matrix2d[0])
        nodes = [list(map(lambda x: Node(x), matrix2d[i])) for i in range(size_i)]
        graph = Graph(nodes)
        for i in range(size_i):
            for j in range(size_j):
                n = nodes[i][j]
                n.obj.graph_node_ref = n
                if not is_dead_cb(n):
                    if j + 1 < size_j and not is_dead_cb(nodes[i][j+1]):
                        graph.add_edge(n, nodes[i][j+1])
                    if i + 1 < size_i and not is_dead_cb(nodes[i+1][j]):
                        graph.add_edge(n, nodes[i+1][j])
        return graph

    def debug_edges(self):
        image = np.zeros([50, 50])
        for lists in self.nodes:
            for node in lists:
                image[node.obj.posIJ[0]][node.obj.posIJ[1]] = node.debug_edge_count
        plt.imshow(image)
        plt.show()

    def debug_path(self, path):
        image = np.zeros([50, 50])
        for lists in self.nodes:
            for node in lists:
                image[node.obj.posIJ[0]][node.obj.posIJ[1]] = node.debug_edge_count

        for obj in path:
            image[obj.posIJ[0]][obj.posIJ[1]] = 10
        plt.imshow(image)
        plt.show()

class SimpleObj:
    def __init__(self, posIJ, s):
        self.posIJ = posIJ
        self.s = s

if __name__ == '__main__':
    rows = DATA.split('\n')[1:-1]
    matrix2d = []
    for i in range(len(rows)):
        matrix2d.append([])
        for j in range(len(rows[0])):
            matrix2d[i].append(SimpleObj([i, j], rows[i][j]))
    g: Graph = Graph.from_matrix2d(matrix2d, lambda x: x.obj.s == 'X')
    g.debug_edges()
    initial, target = None, None
    for lines in g.nodes:
        for node in lines:
            if node.obj.s == 'S':
                initial = node
            elif node.obj.s == 'E':
                target = node

    path = g.astar(initial, target)
    for node in path:
        coord = node.obj.posIJ
        matrix2d[coord[0]][coord[1]].s = 'o'

    image = np.zeros([len(matrix2d), len(matrix2d[0])])
    for i in range(len(matrix2d)):
        for j in range(len(matrix2d[0])):
            image[i][j] = CELL_VALUES[matrix2d[i][j].s]

    plt.imshow(image)
    plt.show()