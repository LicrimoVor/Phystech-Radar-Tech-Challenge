from __future__ import annotations
from typing import AbstractSet, Iterable

from .Node import Node


def isinstans_return(method):

    def wrapper(*args, **kwargs):
        cls = method.__closure__[0].cell_contents
        result = method(*args, **kwargs)
        if len(args) == 0:
            return cls(result)

        if len(args) == 1 and isinstance(args[0], cls):
            return cls(result)

        if len(args) == 2 and isinstance(args[0], cls) and isinstance(args[1], cls):
            return cls(result)
        return result

    return wrapper


class TheoryException(Exception):
    """Ошибка гипотиз."""

    def __init__(self) -> None:
        super().__init__("""Невалидная гипотиза!""")


class Theory(set[Node]):

    def __init__(self, *nodes: Node):
        if len(nodes) != 0 and isinstance(nodes[0], Iterable):
            nodes = nodes[0]
        self.summ_weight = sum([node.weight for node in nodes])
        self.unique_hash = sum([hash(node) for node in nodes])
        is_valid, restricted = self.validate(nodes, True)
        self.restricted = restricted
        if not is_valid:
            raise TheoryException()
        return super().__init__(nodes)

    def check_way(self, node: Node) -> bool:
        return self.restricted.get(node, 0) == 0

    def sort(self) -> list[Node]:
        nodes = sorted(list(self), key=lambda x: x.indx)
        return nodes

    def get_ways(self) -> set[Node]:
        ways = set()
        for node_restricted, value in self.restricted.items():
            if value == 0:
                ways.add(node_restricted)
        return ways

    @staticmethod
    def validate(
        nodes: Iterable[Node], more: bool = False
    ) -> bool | tuple[bool, dict[Node, int]]:
        restricted: dict[Node, int] = {}

        for node in nodes:
            for incompatible in node.incompatibles:
                restricted[incompatible] = restricted.get(incompatible, 0) + 1

        for node in nodes:
            if restricted.get(node):
                if more:
                    return False, restricted
                return False

        if more:
            return True, restricted
        return True

    @isinstans_return
    def copy(self) -> Theory:
        return super().copy()

    @isinstans_return
    def __or__(self, __value: AbstractSet) -> Theory | set[Node]:
        return super().__or__(__value)

    @isinstans_return
    def __and__(self, __value: AbstractSet) -> Theory | set[Node]:
        return super().__or__(__value)

    @isinstans_return
    def __sub__(self, __value: AbstractSet) -> Theory | set[Node]:
        return super().__sub__(__value)

    def remove(self, __element: Node) -> None:
        if __element not in self:
            print("Такого не было")
            return self

        for incompatible in __element.incompatibles:
            self.restricted[incompatible] -= 1
        return super().remove(__element)

    def __repr__(self) -> str:
        return f"Theory {self.summ_weight}"
