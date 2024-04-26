from .Node import Node

class NodeFactory:
	"""Фабрика узлов."""

	@classmethod
	def build(cls, node_params: list[float]) -> list[Node]:
		nodes: list[Node] = []

		for weight in node_params:
			node = Node(weight)
			nodes.append(node)

		return nodes