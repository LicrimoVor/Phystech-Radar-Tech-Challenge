# flake8: noqa E501
import time

time_start = time.time()

from graph import Graph, NodeFactory, Theory
from definition_GT import HeuristicDefGT

file = open("data/input_with_weights.csv")
connections = file.readlines()
weight = [float(i) for i in connections[-1].split(",")]
connections = connections[-2::-1][::-1]

connections = {
    i + 1: list(map(lambda x: bool(int(x)), v.replace("\n", "").split(",")))
    for i, v in enumerate(connections)
}

node_factory = NodeFactory()
nodes = node_factory.build(weight)
global_theoryes: dict[int, tuple[Theory, float]] = {}
graph = Graph(nodes, connections)

for i in range(1, 10):
    graph.calculate_priority(i / 10, i / 25)

    for j in range(10):
        def_global_theory = HeuristicDefGT(graph, j)
        theory = def_global_theory.calculate()

        if not theory.is_full(graph):
            continue

        if global_theoryes.get(theory.unique_hash) is None:
            global_theoryes[theory.unique_hash] = theory, theory.summ_weight

print("*\t" + "".join([f"TH{i + 1}\t" for i in range(len(connections))]))
for index, GH in enumerate(list(sorted(global_theoryes.values(), key=lambda _gh: _gh[1], reverse=True))[:5]):
    print(f"GH{index + 1}\t" + "".join([
        str(int((i + 1) in list(map(lambda node: node.indx, list(GH[0]))))) + "\t"
        for i in range(len(connections))
    ]) + str(GH[1]))
time_end = time.time()
print(time_end - time_start)
