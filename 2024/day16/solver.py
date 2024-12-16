import functools
import sys
import typing
from collections import defaultdict

import solver


NEIGHBORS_MAP = {
    (0, 1): [(1, 0, 1001), (-1, 0, 1001), (0, 1, 1)],
    (0, -1): [(1, 0, 1001), (-1, 0, 1001), (0, -1, 1)],
    (1, 0): [(0, 1, 1001), (0, -1, 1001), (1, 0, 1)],
    (-1, 0): [(0, 1, 1001), (0, -1, 1001), (-1, 0, 1)],
}


class Solver(solver.Solver):
    def _init(self):
        with open(self.input_file_path) as f:
            self.grid = [list(line.strip()) for line in f.readlines()]
        for j, line in enumerate(self.grid):
            for i, ch in enumerate(line):
                if ch == 'S':
                    self.start = (i, j)
                elif ch == 'E':
                    self.end = (i, j)

    @functools.lru_cache(maxsize=100000)
    def get(self, x: int, y: int) -> str:
        if x < 0 or y < 0 or y >= len(self.grid) or x >= len(self.grid[0]):
            return '#'
        return self.grid[y][x]

    @functools.lru_cache(maxsize=100000)
    def get_neighbors(
        self,
        x: int,
        y: int,
        dir: typing.Tuple[int, int],
    ) -> typing.List[typing.Tuple[int, int, int, typing.Tuple[int, int]]]:
        return [(x + i, y + j, cost, (i, j)) for i, j, cost in NEIGHBORS_MAP[dir]]

    def _solve_part1(self) -> int:
        distances = defaultdict(lambda: sys.maxsize)
        distances_dir = defaultdict(lambda: sys.maxsize)
        distances[self.start] = 0
        distances_dir[(self.start, (1, 0))] = 0
        q = [(self.start, 0, (1, 0))]
        while q:
            cur, cost, dir = q.pop(0)

            if cost > distances[cur]:
                continue

            for nx, ny, nc, nd in self.get_neighbors(
                cur[0],
                cur[1],
                dir,
            ):
                distance = cost + nc
                if distance < distances[(nx, ny)] and self.get(nx, ny) != '#':
                    distances[(nx, ny)] = distance
                    distances_dir[(nx, ny), dir] = distance
                    q.append(((nx, ny), distance, nd))

        self.end_dist = distances[self.end]
        self.distances = distances_dir
        return self.end_dist

    def _solve_part2(self) -> int:
        visited = set()
        q = [(self.start, 0, (1, 0), set())]
        while q:
            cur, cost, dir, path = q.pop(0)

            if cost > self.distances[(cur, dir)]:
                continue

            if cost > self.end_dist:
                continue

            next_path = path.union({cur})

            if cur == self.end:
                visited.update(next_path)
                continue

            for nx, ny, nc, nd in self.get_neighbors(cur[0], cur[1], dir):
                distance = cost + nc
                if distance <= self.end_dist and (nx, ny) not in path and self.get(nx, ny) != '#':
                    q.append(((nx, ny), distance, nd, next_path))

        return len(visited)
