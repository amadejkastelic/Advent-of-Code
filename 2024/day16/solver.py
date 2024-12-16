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

    def get(self, x: int, y: int) -> str:
        if x < 0 or y < 0 or y >= len(self.grid) or x >= len(self.grid[0]):
            return '#'
        return self.grid[y][x]

    def get_neighbors(
        self,
        x: int,
        y: int,
        dir: typing.Tuple[int, int],
    ) -> typing.List[typing.Tuple[int, int, int, typing.Tuple[int, int]]]:
        return [(x + i, y + j, cost, (i, j)) for i, j, cost in NEIGHBORS_MAP[dir]]

    def _solve_part1(self) -> int:
        distances = defaultdict(lambda: sys.maxsize)
        distances[self.start] = 0
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
                    q.append(((nx, ny), distance, nd))

        return distances[self.end]

    def _solve_part2(self) -> int:
        end_dists = defaultdict(set)
        paths = defaultdict(set)
        q = [(self.start, 0, (1, 0), set())]
        while q:
            cur, cost, dir, path = q.pop(0)

            path = path.union({cur})

            frozen = frozenset(path)
            if frozen in paths[cur]:
                continue

            paths[cur].add(frozen)

            if cur == self.end:
                end_dists[cost].update(path)
                print(len(end_dists))
                continue

            for nx, ny, nc, nd in self.get_neighbors(
                cur[0],
                cur[1],
                dir,
            ):
                if self.get(nx, ny) != '#' and (nx, ny) not in path:
                    q.append(((nx, ny), cost + nc, nd, path))

        return len(end_dists[min(end_dists.keys())])
