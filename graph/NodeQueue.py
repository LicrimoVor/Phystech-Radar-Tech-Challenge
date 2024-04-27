from .Node import Node


class NodeQueue:
    """Очередь узлов."""

    queue: list[Node]

    def __init__(self):
        self.queue = []

    def add(self, node: Node):
        self.queue.append(node)

    def clear(self):
        self.queue.clear()

    def size(self):
        return len(self.queue)

    def is_empty(self):
        return self.size() == 0

    def complete(self):
        self.queue.pop()

    def get_last(self):
        return self.queue[-1]
