import fileinput
from collections import defaultdict
from pprint import pprint
import networkx as nx
import matplotlib.pyplot as plt


def main():
    graph = defaultdict(list)
    without = [('zjm', 'zcp'), ('nsk', 'rsg'), ('rfg', 'jks')]
    for i, line in enumerate(fileinput.input()):
        line = line.strip()
        src, dests = line.split(':')
        src = src.strip()
        for dest in dests.split():
            if (src, dest) not in without and (dest, src) not in without:
                graph[src.strip()].append(dest)
    G = nx.Graph()
    G.add_nodes_from(graph.keys())
    G.add_edges_from([(s,d) for s, ds in graph.items() for d in ds])
    nx.draw_spring(G, with_labels=True)
    # plt.show()

    print([len(c) for c in nx.connected_components(G)])
    print(sum(len(c) for c in nx.connected_components(G)))


if __name__ == '__main__':
    main()

