from graph import Graph, Theory
from graph.Node import Node
from .AbstractDefGT import AbstractDefGT


class HeuristicDefGT(AbstractDefGT):
    """Определитель глобальной гипотезы."""

    def __init__(self, graph: Graph, priority_index: int):
        super().__init__(graph)
        self.priority_index = priority_index
        self.last_node = graph.priority_node
        self.history = {
            self.last_node,
        }
        self.restricted = self.last_node.incompatibles.copy()

    def calculate(self) -> Theory:
        node = self.last_node
        priorities: list[Node] = []
        priority_node = None

        while (node.connections - self.history) - self.restricted:
            for connection in node.connections:
                if connection in self.history or connection in self.restricted:
                    continue
                priorities.append(connection)
                #print(priorities)
                # if priority_node is None:
                #     priority_node = connection
                # elif connection.priority > priority_node.priority:
                #     priority_node = connection

            priorities.sort(key=lambda _node: _node.priority, reverse=True)
            priority_node = priorities[
                self.priority_index
                if len(priorities) - 1 >= self.priority_index else
                -1
            ]

            self.history.add(priority_node)
            node = priority_node
            self.restricted.update(priority_node.incompatibles)
            priorities.clear()
            # priority_node = None

        return Theory(*self.history)
