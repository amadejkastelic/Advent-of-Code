from functools import reduce

import matplotlib.pyplot as plt
import networkx


def draw(graph: networkx.Graph) -> None:
    networkx.draw(graph, with_labels=True, font_weight='bold')
    plt.show()


if __name__ == '__main__':
    graph = networkx.Graph()
    with open('2023/day25/small.txt', 'r') as input_file:
        for line in input_file:
            component, connected_components = line.strip().split(': ')
            for connected_component in connected_components.split():
                graph.add_edge(component, connected_component)

    for node1, node2, _ in sorted(networkx.local_bridges(graph), key=lambda x: x[2], reverse=True)[:3]:
        graph.remove_edge(node1, node2)

    print(reduce(lambda x, y: len(x) * len(y), networkx.connected_components(graph)))
