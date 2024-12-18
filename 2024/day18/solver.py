import sys
import typing
from collections import defaultdict

import solver


class Solver(solver.Solver):
    def _init(self):
        self.grid_size = (71, 71) if 'input.txt' in self.input_file_path else (7, 7)
        self.grid = [['.'] * self.grid_size[0] for _ in range(self.grid_size[1])]
        self.grid2 = [['.'] * self.grid_size[0] for _ in range(self.grid_size[1])]
        self.bytes: typing.List[typing.Tuple[int, int]] = []
        with open(self.input_file_path) as f:
            for line in f.readlines():
                x, y = tuple(map(int, line.strip().split(',')))
                self.bytes.append((x, y))

    def _get(self, x: int, y: int) -> str:
        if x < 0 or x >= len(self.grid[0]) or y < 0 or y >= len(self.grid):
            return '#'
        return self.grid[y][x]

    def shortest_path(self) -> int:
        distances = defaultdict(lambda: sys.maxsize)
        distances[(0, 0)] = 0
        queue = [(0, 0)]
        while queue:
            x, y = queue.pop(0)

            for nx, ny in [
                (x - 1, y),
                (x + 1, y),
                (x, y - 1),
                (x, y + 1),
            ]:
                if distances[(nx, ny)] < sys.maxsize or self._get(nx, ny) == '#':
                    continue
                distances[(nx, ny)] = distances[(x, y)] + 1
                queue.append((nx, ny))

        return distances[(self.grid_size[0] - 1, self.grid_size[1] - 1)]

    def fill_grid(self, num_bytes: int) -> None:
        for i in range(num_bytes):
            x, y = self.bytes[i]
            self.grid[y][x] = '#'

    def _solve_part1(self) -> int:
        num_bytes = 12
        if 'input.txt' in self.input_file_path:
            num_bytes = 1024

        self.fill_grid(num_bytes)

        return self.shortest_path()

    def _solve_part2(self) -> str:
        self.grid = self.grid2
        num_bytes = 0
        if 'input.txt' in self.input_file_path:
            num_bytes = 1024
            self.fill_grid(num_bytes)
        for i in range(num_bytes, len(self.bytes)):
            x, y = self.bytes[i]
            self.grid[y][x] = '#'

            if self.shortest_path() == sys.maxsize:
                return ','.join(map(str, self.bytes[i]))

        return '?'
