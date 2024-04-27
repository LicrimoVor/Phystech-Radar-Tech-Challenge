from .Graph import Graph
from .Node import Node
from abc import abstractmethod, abstractproperty


class AbstractDefGT:
	"""Абстрактная модель поиска глобальных теорий"""

	graph: Graph
	restricted: set[Node]

	@abstractmethod
	def calculate(self) -> list[set[Node]]: pass

	def __init__(self, graph: Graph):
		self.graph = graph
		self.restricted = set()



