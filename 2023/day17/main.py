import heapq
import sys
import typing
from collections import defaultdict


def _get_neighbors(graph: typing.List[typing.List[int]], x: int, y: int) -> typing.Set[typing.Tuple[int, int, str]]:
    neighbors = set()

    adjacent = [
        (0, 1, 'down'),
        (1, 0, 'right'),
        (-1, 0, 'left'),
        (0, -1, 'up'),
    ]
    for offset_x, offset_y, direction in adjacent:
        neighbor = (x + offset_x, y + offset_y, direction)
        if 0 <= neighbor[1] < len(graph) and 0 <= neighbor[0] < len(graph[neighbor[1]]):
            neighbors.add(neighbor)

    return neighbors


def dijkstra(
    graph: typing.List[typing.List[int]],
    start: typing.Tuple[int, int],
    end: typing.Tuple[int, int],
    max_steps: int = 3,
) -> int:
    visited: typing.Set[typing.Tuple[int, int, int]] = set()

    distances: typing.Dict[typing.Tuple[int, int], int] = defaultdict(lambda: sys.maxsize)
    distances[start] = 0

    queue = [(0, start, 0, 0)]
    while queue:
        distance, node, direction, steps = heapq.heappop(queue)

        if (node, direction) in visited:
            continue

        visited.add((node, direction))
        for x, y, n_direction in _get_neighbors(graph=graph, x=node[0], y=node[1]):
            if (x, y, n_direction) in visited or direction == n_direction and steps > max_steps:
                continue

            new_dist = distance + graph[y][x]
            if new_dist <= distances[(x, y, direction)]:
                distances[(x, y, direction)] = new_dist
                heapq.heappush(
                    queue,
                    (new_dist, (x, y), n_direction, steps + 1 if direction == n_direction else 1),
                )

    print(distances)
    return min([distances[(end[0], end[1], i)] for i in ('left', 'right', 'up', 'down')])


if __name__ == '__main__':
    graph: typing.List[typing.List[int]] = []
    with open('2023/day17/small.txt', 'r') as input_file:
        for line in input_file:
            graph.append(list(map(int, list(line.strip()))))

    print(dijkstra(graph=graph, start=(0, 0), end=(len(graph) - 1, len(graph[0]) - 1), max_steps=3))
