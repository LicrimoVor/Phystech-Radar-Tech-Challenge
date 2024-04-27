from .Graph import Graph
from .AbstractDefGT import AbstractDefGT
from .NodeQueue import NodeQueue


class IteratorGlobalTheory(AbstractDefGT):
	"""Итератор для полного перебора всех глобальных гипотез."""

	queue: NodeQueue

	def __init__(self, graph: Graph):
		super().__init__(graph)
		self.queue = NodeQueue()

	def calculate(self):
		theories = []

		for node in self.graph.nodes.values():
			self.queue.add(node)
			self.restricted = node.incompatibles.copy()

			history = {node, }

			while not self.queue.is_empty():
				if not ((self.queue.get_last().connections - self.restricted) - history):
					theories.append(history)
					print(history)
					history.remove(self.queue.get_last())
					self.restricted = set()
					for i in history:
						self.restricted.update(i.incompatibles)
					print(history)
					self.queue.complete()

					if not self.queue.is_empty():
						history.add(self.queue.get_last())
					print(self.queue.get_last())
					print(history)

					continue

				for connection in self.queue.get_last().connections:
					if connection in self.restricted or connection in history:
						continue
					self.queue.add(connection)

				history.add(self.queue.get_last())
				self.restricted.update(self.queue.get_last().incompatibles)

			self.queue.clear()
