from queue import Queue

from graph import Graph, Theory, TheoryException
from graph.Node import Node
from .AbstractDefGT import AbstractDefGT


class MutationDefGT(AbstractDefGT):

    MIN_NODE_COUNT = 10

    def __init__(self, graph: Graph, theory: Theory):
        super().__init__(graph)
        self.init_theory = theory

    def calculate(self) -> list[Theory]:
        sorted_nodes = sorted(list(self.init_theory), key=lambda node: node.priority)
        theories: dict[int, Theory] = {}
        short_theory = self.init_theory.copy()
        connections: set[Node] = set()

        for node in sorted_nodes[: self.MIN_NODE_COUNT]:
            short_theory.remove(node)
            connections |= short_theory.get_ways()
            if short_theory.restricted.get(node) is None:
                short_theory.restricted[node] = 0
                connections.add(node)

            for connection in connections:
                restricted_history = set()
                neighbors: list[Node] = []
                queue = Queue()
                queue.put(connection)
                history = []

                while not queue.empty():
                    inner_node: Node = queue.get()
                    history.append(inner_node)
                    if not short_theory.check_way(inner_node):
                        continue

                    inner_connections = (
                        short_theory.get_ways()
                        - set(history)
                        - inner_node.incompatibles
                        - restricted_history
                    )
                    if not inner_connections:
                        neighbors.append(history)
                        history.pop()
                        continue

                    for inner_connection in inner_connections:
                        queue.put(inner_connection)
                        restricted_history |= inner_node.incompatibles

                for _neighbors in neighbors:
                    try:
                        theory = short_theory | Theory(*_neighbors)
                    except TheoryException:
                        continue
                    theories[theory.unique_hash] = theory

        return list(theories.values())
