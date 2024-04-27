from .Node import Node


class Graph:
    """Граф."""

    def __init__(self, nodes: list[Node], connections: dict[int, list[bool]]):
        self.nodes = {node.indx: node for node in nodes}

        for key, value in connections.items():
            node = self.nodes[key]

            if key == 9:
                print(value)

            for index, is_compatible in enumerate(value):
                if key >= index + 1:
                    continue

                if is_compatible:
                    node.add_connection(self.nodes[index + 1])
                else:
                    node.add_incompatible(self.nodes[index + 1])

        self.priority_node = None

    def get_node(self, index: int) -> Node:
        return self.nodes[index]

    def calculate_priority(self, lost_ratio: float, useful_ratio: float):
        Node.lost_magic_ratio = lost_ratio
        Node.useful_magic_ratio = useful_ratio

        for node in self.nodes.values():
            priority = node.define_priority()

            if self.priority_node is None:
                self.priority_node = node
            elif priority > self.priority_node.priority:
                self.priority_node = node
