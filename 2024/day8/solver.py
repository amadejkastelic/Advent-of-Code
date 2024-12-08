import typing
from collections import defaultdict
from itertools import combinations

import solver


class Solver(solver.Solver):
    def _init(self):
        self.map = []
        self.antennas = defaultdict(lambda: [])
        with open(self.input_file_path) as f:
            for i, line in enumerate(f.readlines()):
                field = list(line.strip())
                self.map.append(field)
                for j, ch in enumerate(field):
                    if ch != '.':
                        self.antennas[ch].append((j, i))
        self.y = len(self.map)
        self.x = len(self.map[0])
        self.surrounding_cache = {}

    def _in_bounds(self, point: typing.Tuple[int, int]) -> bool:
        x, y = point
        return x >= 0 and x < self.x and y >= 0 and y < self.y

    def _get_line(self, y: int) -> typing.List[str]:
        if y < 0 or y >= self.y:
            return ['.']
        return self.map[y]

    def _get_col(self, x: int) -> typing.List[str]:
        if x < 0 or x >= self.x:
            return ['.']
        return [self.map[i][x] for i in range(self.y)]

    def _has_antenna_in_line(self, point: typing.Tuple[int, int]) -> bool:
        if point not in self.surrounding_cache:
            self.surrounding_cache[point] = not all(
                [
                    ch == '.'
                    for ch in self._get_col(point[0] - 1)
                    + self._get_col(point[0] + 1)
                    + self._get_line(point[1] - 1)
                    + self._get_line(point[1] + 1)
                ]
            )
        return self.surrounding_cache[point]

    def _solve_part1(self) -> int:
        antinodes = set()
        for positions in self.antennas.values():
            for a, b in combinations(positions, 2):
                distance = (abs(a[0] - b[0]), abs(a[1] - b[1]))
                if a[0] > b[0]:
                    antinode_a = (a[0] + distance[0], a[1] - distance[1])
                    antinode_b = (b[0] - distance[0], b[1] + distance[1])
                elif a[0] == b[0]:
                    antinode_a = (a[0], a[1] - distance[1])
                    antinode_b = (b[0], b[1] + distance[1])
                else:
                    antinode_a = (a[0] - distance[0], a[1] - distance[1])
                    antinode_b = (b[0] + distance[0], b[1] + distance[1])
                if self._in_bounds(antinode_a):
                    antinodes.add(antinode_a)
                if self._in_bounds(antinode_b):
                    antinodes.add(antinode_b)
        return len(antinodes)

    def _solve_part2(self) -> int:
        antinodes = set()

        for positions in self.antennas.values():
            for a, b in combinations(positions, 2):
                distance = (abs(a[0] - b[0]), abs(a[1] - b[1]))

                if self._has_antenna_in_line(a):
                    antinodes.add(a)

                if self._has_antenna_in_line(b):
                    antinodes.add(b)

                if a[0] > b[0]:
                    antinode = (a[0] + distance[0], a[1] - distance[1])
                    while self._in_bounds(antinode):
                        antinodes.add(antinode)
                        antinode = (antinode[0] + distance[0], antinode[1] - distance[1])

                    antinode = (b[0] - distance[0], b[1] + distance[1])
                    while self._in_bounds(antinode):
                        antinodes.add(antinode)
                        antinode = (antinode[0] - distance[0], antinode[1] + distance[1])
                else:
                    antinode = (a[0] - distance[0], a[1] - distance[1])
                    while self._in_bounds(antinode):
                        antinodes.add(antinode)
                        antinode = (antinode[0] - distance[0], antinode[1] - distance[1])

                    antinode = (b[0] + distance[0], b[1] + distance[1])
                    while self._in_bounds(antinode):
                        antinodes.add(antinode)
                        antinode = (antinode[0] + distance[0], antinode[1] + distance[1])

        return len(antinodes)
