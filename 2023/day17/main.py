import heapq
import sys
import typing
from collections import defaultdict


def _get_neighbors(
    graph: typing.List[typing.List[int]],
    x: int,
    y: int,
    direction: str,
) -> typing.Set[typing.Tuple[int, int, str]]:
    neighbors = set()

    adjacent = [
        (0, 1, 'down'),
        (1, 0, 'right'),
        (-1, 0, 'left'),
        (0, -1, 'up'),
    ]

    match direction:
        case 'down':
            adjacent.pop(3)
        case 'up':
            adjacent.pop(0)
        case 'right':
            adjacent.pop(2)
        case 'left':
            adjacent.pop(1)

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
    min_steps: int = 0,
) -> int:
    visited: typing.Set[typing.Tuple[int, int, int]] = set()

    distances: typing.Dict[typing.Tuple[int, int], int, int] = defaultdict(lambda: sys.maxsize)
    distances[start, 0, 0] = 0
    distances[(start[0] + 1, start[1]), 'right', 1] = graph[start[1]][start[0] + 1]
    distances[(start[0], start[1] + 1), 'down', 1] = graph[start[1] + 1][start[0]]

    queue = [
        (graph[start[1]][start[0] + 1], (start[0] + 1, start[1]), 'right', 1),
        (graph[start[1] + 1][start[0]], (start[0], start[1] + 1), 'down', 1),
    ]
    results = []
    while queue:
        distance, node, direction, steps = heapq.heappop(queue)

        if node == end and steps >= min_steps:
            results.append(distance)

        if (node, direction, steps) in visited:
            continue

        visited.add((node, direction, steps))
        for x, y, n_direction in _get_neighbors(graph=graph, x=node[0], y=node[1], direction=direction):
            n_steps = steps + 1 if direction == n_direction else 1

            if (x, y, n_direction, n_steps) in visited or (direction == n_direction and n_steps > max_steps):
                continue

            if steps < min_steps and direction != n_direction:
                continue

            new_dist = distance + graph[y][x]
            if new_dist <= distances[(x, y, n_direction, n_steps)]:
                distances[(x, y, n_direction, n_steps)] = new_dist
                heapq.heappush(
                    queue,
                    (new_dist, (x, y), n_direction, n_steps),
                )

    return min(results)


if __name__ == '__main__':
    graph: typing.List[typing.List[int]] = []
    with open('2023/day17/input.txt', 'r') as input_file:
        for line in input_file:
            graph.append(list(map(int, list(line.strip()))))

    print(dijkstra(graph=graph, start=(0, 0), end=(len(graph[0]) - 1, len(graph) - 1), max_steps=3))
    print(dijkstra(graph=graph, start=(0, 0), end=(len(graph[0]) - 1, len(graph) - 1), max_steps=10, min_steps=4))
