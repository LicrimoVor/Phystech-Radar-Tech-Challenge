from graph import Graph, Theory
from .AbstractDefGT import AbstractDefGT


class HeuristicDefGT(AbstractDefGT):
    """Определитель глобальной гипотезы."""

    def __init__(self, graph: Graph):
        super().__init__(graph)
        self.last_node = graph.priority_node
        self.history = {
            self.last_node,
        }
        self.restricted = self.last_node.incompatibles.copy()

    def calculate(self) -> Theory:
        node = self.last_node

        priority_node = None

        while (node.connections - self.history) - self.restricted:
            for connection in node.connections:
                if connection in self.history or connection in self.restricted:
                    continue
                if priority_node is None:
                    priority_node = connection
                elif connection.priority > priority_node.priority:
                    priority_node = connection

            self.history.add(priority_node)
            node = priority_node
            self.restricted.update(priority_node.incompatibles)
            priority_node = None

        return Theory(*self.history)
