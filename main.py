# flake8: noqa E501
from graph import Graph, NodeFactory, DefinitionGlobalTheory
import time

time_start = time.time()
connections = {
    i + 1: list(map(lambda x: bool(int(x)), v.split()))
    for i, v in enumerate(open("data/matrix.txt").readlines())
}
# fmt: off
weight = [2.0851, 3.3362, 5.8383, 2.5021, 5.8383, 4.1702, 0.4170, 5.8383, 4.5872, 6.2553, 1.2511, 1.2511, 5.8383, 4.5872, 0.4170, 5.0043, 5.0043, 5.8383, 4.5872, 0.8340, 0.4170, 0.4170, 0.4170, 1.6681, 5.4213, 3.7532, 3.7532, 5.4213]
# weight = [6.7871, 0.4965, 0.5813, 6.3638, 7.7534, 6.7388, 2.1945, 5.7203, 2.5396, 0.0394, 12.3052, 5.3397, 0.7031, 4.5140, 1.4971, 5.8530, 1.8569, 3.5543, 1.9219, 11.8509, 2.2925, 5.1243, 9.2748, 2.9068, 5.4177, 3.3817, 3.5976, 0.5599]
# weight = [0.9828, 2.7646, 12.1911, 0.0595, 1.9019, 0.1593, 8.8003, 0.8516, 3.0777, 2.8822, 2.9568, 8.2451, 8.3665, 3.7213, 2.6592, 3.0582, 1.2158, 9.7197, 4.1748, 7.9339, 3.6058, 0.4407, 1.7124, 1.6688, 0.2121, 1.7937, 0.0706, 4.5202,]
# weight = [2.2572, 2.8694, 0.9850, 5.6483, 0.6029, 0.9266, 3.7141, 11.1835, 0.8188, 1.8852, 1.5597, 1.4445, 2.1545, 4.9897, 8.5985, 3.0642, 6.1070, 8.4169, 2.8637, 3.5046, 2.3553, 1.1666, 2.3105, 0.7346, 2.4317, 0.3172, 3.9294, 2.3420]
# fmt: on

node_factory = NodeFactory()
nodes = node_factory.build(weight)

graph = Graph(nodes, connections)
for i in range(1):
    graph.calculate_priority(0.25, 0.08)
    def_global_theory = DefinitionGlobalTheory(graph)
    history = def_global_theory.calculate()
    print(history, sum([i.weight for i in list(history)]))


time_end = time.time()
print(time_end - time_start)
