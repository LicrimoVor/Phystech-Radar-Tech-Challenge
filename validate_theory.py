from graph.Node import Node


def validate(theory: set[Node]):

    restricted: dict[Node, int] = {}

    for node in theory:
        for incompatible in node.incompatibles:
            if restricted.get(incompatible) is None:
                restricted[incompatible] = 0
            restricted[incompatible] += 1

    for node in theory:
        if restricted.get(node):
            return False

    return True
