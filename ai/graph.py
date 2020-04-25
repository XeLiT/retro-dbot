
DATA = """
.................................................
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


class Edge:
    def __init__(self, to_node, distance=1):
        self.to_node = to_node
        self.distance = distance


class Node:
    def __init__(self, obj) -> None:
        self.obj = obj
        self.edges = []

    def __repr__(self):
        return self.obj.__repr__()

    def add_edge(self, node, distance=1):
        self.edges.append(Edge(node, distance))


class Graph:
    def __init__(self, nodes: [Node], initial=None, target=None):
        self.nodes = nodes
        self.initial = initial
        self.target = target
        print(self.nodes)

    def dijsktra(self, initial: Node, target: Node) -> [Node]:
        """"
        set all node distance infinity
        set initial distance 0
        init priority_queue

        start with S
        """

        next_nodes = initial.



    @staticmethod
    def from_matrix2d(matrix2d):
        size_i = len(matrix2d)
        size_j = len(matrix2d[0])
        nodes = [list(map(lambda x: Node(x), matrix2d[i])) for i in range(size_i)]
        target = None
        initial = None
        for i in range(size_i):
            for j in range(size_j):
                n = nodes[i][j]
                if n.obj == 'S':
                    initial = n
                elif n.obj == 'E':
                    target = n
                if i - 1 > 0:               # up
                    n.add_edge(nodes[i-1][j])
                if j + 1 < size_j:          # right
                    n.add_edge(nodes[i][j+1])
                if j - 1 > 0:               # left
                    n.add_edge(nodes[i][j-1])
                if i + 1 < size_i:          # down
                    n.add_edge(nodes[i+1][j])
        return Graph([node for rows in nodes for node in rows], initial=initial, target=target)


if __name__ == '__main__':
    Graph.from_matrix2d(DATA.split('\n')[1:])
