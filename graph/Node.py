from __future__ import annotations


class Node:
	"""Траекторная гипотеза."""

	__examplers: dict[int, Node] = {}
	__n: int = 0

	lost_magic_ratio = 0.25
	useful_magic_ratio = 0.08

	connections: set[Node]
	incompatibles: set[Node]
	priority: float = None

	def __init__(self, weight: float):
		self.__class__.__n += 1
		self.indx = self.__class__.__n
		self.__class__.__examplers[self.indx] = self
		self.weight = weight
		self.connections = set()
		self.incompatibles = set()

	def __repr__(self):
		return f"{self.indx}"

	def add_connection(self, node):
		if node in self.connections:
			return

		self.connections.add(node)
		node.add_connection(self)

	def add_incompatible(self, node):
		if node in self.incompatibles:
			return

		self.incompatibles.add(node)
		node.add_incompatible(self)

	def define_priority(self) -> float:
		self.priority = self.weight

		lost_sum = 0.0
		for incompatible in self.incompatibles:
			lost_sum += incompatible.weight * self.__class__.lost_magic_ratio

		useful_sum = 0.0
		for connection in self.connections:
			useful_sum += connection.weight * self.__class__.useful_magic_ratio

		self.priority += useful_sum - lost_sum

		return self.priority

	def iterate_neighbor(self) -> set[Node]:
		return self.connections