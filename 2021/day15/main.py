import heapq
import math
import typing
from collections import defaultdict


def main():
    #file_name = input('Enter input path: ')
    file_name = 'input.txt'

    with open(file_name, 'r') as f:
        content = f.readlines()

    graph = list(list(map(int, line.strip())) for line in content)

    distance = _find_distance(
        start=(0, 0), end=(len(graph[0]) - 1, len(graph) - 1), graph=graph
    )
    print(f'Part 1: {distance}')

    width = len(graph)
    height = len(graph[0])
    for i in range(4):
        for row in graph:
            tail = row[-width:]
            row.extend((x + 1) if x < 9 else 1 for x in tail)
    for i in range(4):
        for row in graph[-height:]:
            row = [(x + 1) if x < 9 else 1 for x in row]
            graph.append(row)

    distance = _find_distance(
        start=(0, 0), end=(len(graph[0]) - 1, len(graph) - 1), graph=graph
    )
    print(f'Part 2: {distance}')


def _find_distance(
    start: typing.Tuple[int, int],
    end: typing.Tuple[int, int],
    graph: typing.List[typing.List[int]],
) -> float:
    visited = set()

    distances: typing.Dict[typing.Tuple[int, int], float] = defaultdict(lambda: math.inf)
    distances[start] = 0

    queue = [(start, 0)]
    while queue:
        node, distance = heapq.heappop(queue)
        if node == end:
            return distance

        visited.add(node)
        for neighbor in _get_neighbors(graph=graph, x=node[0], y=node[1]):
            if neighbor in visited:
                continue
            new_distance = distance + _get_weight(
                graph=graph, x=neighbor[0], y=neighbor[1]
            )
            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                heapq.heappush(queue, (neighbor, new_distance))

    return distances[end]


def _get_neighbors(
    graph: typing.List[typing.List[int]], x: int, y: int
) -> typing.Set[typing.Tuple[int, int]]:
    neighbors = set()

    adjacent = [
        (0, 1),
        (1, 0),
        (-1, 0),
        (0, -1),
    ]
    for offset_x, offset_y in adjacent:
        neighbor = (x + offset_x, y + offset_y)
        if 0 <= neighbor[0] < len(graph[0]) and 0 <= neighbor[1] < len(graph):
            neighbors.add(neighbor)

    return neighbors


def _get_weight(graph: typing.List[typing.List[int]], x: int, y: int):
    return graph[y][x]


if __name__ == '__main__':
    main()
