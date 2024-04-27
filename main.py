# flake8: noqa E501
import time

from graph import Graph, NodeFactory
from definition_GT import HeuristicDefGT, MutationDefGT
from graph.Node import Node
from validate_theory import validate

time_start = time.time()

connections = {
    i + 1: list(map(lambda x: bool(int(x)), v.split()))
    for i, v in enumerate(open("data/matrix2.txt").readlines())
}
# fmt: off
# weight = [2.0851, 3.3362, 5.8383, 2.5021, 5.8383, 4.1702, 0.4170, 5.8383, 4.5872, 6.2553, 1.2511, 1.2511, 5.8383, 4.5872, 0.4170, 5.0043, 5.0043, 5.8383, 4.5872, 0.8340, 0.4170, 0.4170, 0.4170, 1.6681, 5.4213, 3.7532, 3.7532, 5.4213]
weight = [0.7713, 0.1660, 8.2374, 7.4880, 5.4836, 1.1240, 2.7729, 8.3658, 1.5220, 0.2650, 4.1122, 10.4873]
# weight = [7.7877, 2.3481, 0.8485, 7.8411, 9.3727, 4.3102, 0.1482, 1.5009, 1.0563, 0.9170, 5.6443, 0.9680]
# weight = [7.8205, 0.0889, 6.7477, 1.7684, 8.3869, 0.3297, 4.5826, 5.0875, 3.3844, 11.3794, 0.2233, 1.3463]
# weight = [0.2651, 9.0549, 2.4429, 1.2812, 1.3307, 3.7778, 8.1834, 1.1499, 10.0754, 2.0518, 1.7285, 2.1045, 7.4367, 6.3412, 4.4906, 8.8235, 0.1094, 5.2609, 1.5481, 2.1420, 4.1189, 3.6614, 3.7000, 2.0298, 0.9968, 5.8923, 5.6270, 4.9405]
# fmt: on

node_factory = NodeFactory()
nodes = node_factory.build(weight)
global_theoryes: dict[int, Node] = {}
graph = Graph(nodes, connections)

for i in range(1, 10):
    graph.calculate_priority(i / 10, i / 25)
    def_global_theory = HeuristicDefGT(graph)
    history = def_global_theory.calculate()
    sum_hash = sum([hash(node) for node in history])

    if global_theoryes.get(sum_hash) is None:
        result = sum([i.weight for i in list(history)])
        theory = list(history)
        theory.sort(key=lambda x: x.indx)
        global_theoryes[sum_hash] = theory, result


for theory in global_theoryes.copy().values():
    def_mutation_theory = MutationDefGT(graph, theory[0])
    mutation_theories = def_mutation_theory.calculate()

    for sum_hash, theory in mutation_theories.items():
        if global_theoryes.get(sum_hash) is None:
            result = sum([i.weight for i in list(theory)])
            theory = list(theory)
            theory.sort(key=lambda x: x.indx)
            global_theoryes[sum_hash] = theory, result

result = sorted(global_theoryes.values(), key=lambda x: x[1], reverse=True)[:5]

print(*result, sep="\n")
time_end = time.time()
print(time_end - time_start)
