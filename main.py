from graph import Graph, NodeFactory, HeuristicDefGT
import time

time_start = time.time()

connections = {
	i + 1: list(map(lambda x: bool(int(x)), v.split()))
	for i, v in enumerate(open("data/matrix4.txt").readlines())
}
# fmt: off
#weight = [2.0851, 3.3362, 5.8383, 2.5021, 5.8383, 4.1702, 0.4170, 5.8383, 4.5872, 6.2553, 1.2511, 1.2511, 5.8383, 4.5872, 0.4170, 5.0043, 5.0043, 5.8383, 4.5872, 0.8340, 0.4170, 0.4170, 0.4170, 1.6681, 5.4213, 3.7532, 3.7532, 5.4213]
#weight = [0.7713, 0.1660, 8.2374, 7.4880, 5.4836, 1.1240, 2.7729, 8.3658, 1.5220, 0.2650, 4.1122, 10.4873]
#weight = [7.7877, 2.3481, 0.8485, 7.8411, 9.3727, 4.3102, 0.1482, 1.5009, 1.0563, 0.9170, 5.6443, 0.9680]
weight = [7.8205, 0.0889, 6.7477, 1.7684, 8.3869, 0.3297, 4.5826, 5.0875, 3.3844, 11.3794, 0.2233, 1.3463]
# fmt: on

node_factory = NodeFactory()
nodes = node_factory.build(weight)

graph = Graph(nodes, connections)
for i in range(1):
	graph.calculate_priority(0.25, 0.08)
	def_global_theory = HeuristicDefGT(graph)
	history = def_global_theory.calculate()
	print(history, sum([i.weight for i in list(history)]))


time_end = time.time()
print(time_end - time_start)
