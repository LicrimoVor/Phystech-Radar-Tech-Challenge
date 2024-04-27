from queue import Queue

from graph import Graph
from graph.Node import Node
from validate_theory import validate
from .AbstractDefGT import AbstractDefGT


class MutationDefGT(AbstractDefGT):

    MIN_NODE_COUNT = 5

    def __init__(self, graph: Graph, theory: set[Node]):
        super().__init__(graph)
        self.init_theory = theory

    def calculate(self) -> dict[int, set[Node]]:
        restricted: dict[Node, int] = {}
        nodes = set(self.graph.nodes.values())

        for node in self.init_theory:
            for incompatible in node.incompatibles:
                if restricted.get(incompatible) is None:
                    restricted[incompatible] = 0
                restricted[incompatible] += 1

        sorted_nodes = sorted(list(self.init_theory), key=lambda node: node.priority)
        theories: dict[int, set[Node]] = {}

        pussy_theory = set(self.init_theory.copy())
        connections: set[Node] = set()
        for node in sorted_nodes[: self.MIN_NODE_COUNT]:
            pussy_theory.remove(node)

            for node_restricted in restricted:
                if node_restricted in node.incompatibles:
                    restricted[node_restricted] -= 1

                if restricted[node_restricted] == 0:
                    connections.add(node_restricted)

            if restricted.get(node) is None:
                restricted[node] = 0
                connections.add(node)

            # print(node, connections, restricted.get(node))
            for connection in connections:
                restricted_history = set()
                neighbors = []
                queue = Queue()
                queue.put(connection)
                history = []

                while not queue.empty():
                    inner_node: Node = queue.get()
                    history.append(inner_node)
                    if restricted.get(inner_node):
                        continue

                    _restricted = set(
                        [node for node, value in restricted.items() if value]
                    )
                    inner_connections = (
                        nodes
                        - pussy_theory
                        - _restricted
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
                    theory = pussy_theory | set(_neighbors)
                    sum_hash = sum([hash(node) for node in theory])
                    # print(theory, sum([i.weight for i in theory]))
                    if theories.get(sum_hash) or not validate(theory):
                        continue
                    theories[sum_hash] = theory

        return theories
