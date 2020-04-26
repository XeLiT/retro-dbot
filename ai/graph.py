from math import inf, sqrt
from collections import defaultdict
import heapq

DATA = """.................................................
.................................................
.................................................
.................................................
........E........................................
.................................................
.................................................
.................................................
.................................................
.................................................
.................................................
.................................................
.................................................
..XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX...
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
.........................S.......................
.................................................
.................................................
................................................."""

DATA1 = """......
......
......
......
S.....
......
......
......
......
XXXX..
......
......
......
......
......
......
..E...
......
......
......"""

DATA2 = """E.X.
...S"""


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

        # a-star
        self.distance_to_target = inf
        self.score = inf   #  combined heuristic, g cost + distance to_target
        # g cost = distance to other node on edge

    def set_score(self, target_node, edge_weight):
        self._compute_distance(target_node)
        self.score = self.distance_to_target + edge_weight

    def _compute_distance(self, target_node):
        c1 = self.obj['coord']
        c2 = target_node.obj['coord']
        self.distance_to_target = sqrt(pow(c1[0] - c2[0], 2) + pow(c1[1] - c2[1], 2))

    def __repr__(self):
        return self.obj.__repr__()
        #return self.score.__repr__()

    def __eq__(self, o) -> bool:
        return self.obj == o.obj

    def __lt__(self, other):
        return self.score < other.score

class Graph:
    def __init__(self, nodes: [Node], initial=None, target=None):
        self.nodes = nodes
        self.edges = defaultdict(list)
        self.initial: Node = initial
        self.target: Node = target

    def add_edge(self, from_node, to_node, weight=1):
        self.edges[id(from_node)].append(Edge(to_node, weight))
        self.edges[id(to_node)].append(Edge(from_node, weight))

    def dijsktra(self) -> [Node]:
        self.initial.traveled = 0
        queue = [self.initial]
        found = False
        visited = []
        d1, d2 = 0, 0
        while len(queue) and not found:
            from_node = queue[0]
            edges = sorted(self.edges[id(from_node)], key=lambda k: k.weight)
            for e in edges:
                to_node = e.node
                d1 += 1
                if to_node not in visited:
                    d2 += 1
                    to_node.traveled = e.weight + from_node.traveled
                    to_node.previous = from_node
                    if to_node == self.target:
                        found = True
                        break
                    queue.append(to_node)
            visited.append(from_node)
            queue.remove(from_node)
            queue.sort(key=lambda x: x.traveled)

        print(d1, d2)
        return [] if not found else self._build_path()

    def _build_path(self):
        path = []
        n = self.target
        while n.traveled != 0:
            path.append(n)
            n = n.previous
        return path

    def astar(self) -> [Node]:
        self.initial.traveled = 0
        self.initial.set_score(self.target, 0)
        queue = [self.initial]
        heapq.heapify([self.initial])
        found = False
        d1, d2 = 0, 0

        while len(queue) and not found:
            from_node = heapq.heappop(queue)
            from_node.visited = True
            edges = self.edges[id(from_node)]
            for edge in edges:
                node = edge.node
                d1 += 1
                if not node.visited:
                    d2 += 1
                    node.set_score(self.target, edge.weight)
                    node.previous = from_node
                    if node == self.target:
                        found = True
                        break
                    heapq.heappush(queue, node)
        print(d1, d2)
        return [] if not found else self._build_path()


    @staticmethod
    def from_matrix2d(matrix2d):
        size_i = len(matrix2d)
        size_j = len(matrix2d[0])
        nodes = [list(map(lambda x: Node(x), matrix2d[i])) for i in range(size_i)]
        is_dead = lambda x: x.obj['s'] == 'X'
        graph = Graph([node for rows in nodes for node in rows])
        for i in range(size_i):
            for j in range(size_j):
                n = nodes[i][j]
                if not is_dead(n):
                    if j + 1 < size_j and not is_dead(nodes[i][j+1]):
                        graph.add_edge(n, nodes[i][j+1])
                    if i + 1 < size_i and not is_dead(nodes[i+1][j]):
                        graph.add_edge(n, nodes[i+1][j])
        return graph

if __name__ == '__main__':
    # upvote https://stackoverflow.com/questions/7803121/in-python-heapq-heapify-doesnt-take-cmp-or-key-functions-as-arguments-like-sor

    rows = DATA.split('\n')
    matrix2d = []
    for i in range(len(rows)):
        matrix2d.append([])
        for j in range(len(rows[0])):
            matrix2d[i].append({'coord': [i, j], 's': rows[i][j]})
    g: Graph = Graph.from_matrix2d(matrix2d)
    for node in g.nodes:
        if node.obj['s'] == 'S':
            g.initial = node
        elif node.obj['s'] == 'E':
            g.target = node

    path = g.astar()
    for node in path:
        coord = node.obj['coord']
        matrix2d[coord[0]][coord[1]]['s'] = 'o'

    for i in range(len(matrix2d)):
        s = ''
        for j in range(len(matrix2d[0])):
            s += matrix2d[i][j]['s']
        print(s)
