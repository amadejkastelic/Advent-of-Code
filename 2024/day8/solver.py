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

    def _in_bounds(self, point: typing.Tuple[int, int]) -> bool:
        x, y = point
        return x >= 0 and x < self.x and y >= 0 and y < self.y

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
                if a[0] > b[0]:
                    tmp_dist = distance[:]
                    while a[0] + tmp_dist[0] < self.x and a[1] - tmp_dist[1] >= 0:
                        antinodes.add((a[0] + tmp_dist[0], a[1] - tmp_dist[1]))
                        tmp_dist = (tmp_dist[0] + distance[0], tmp_dist[1] + distance[1])
                    tmp_dist = distance[:]
                    while b[0] - tmp_dist[0] >= 0 and b[1] + tmp_dist[1] < self.y:
                        antinodes.add((b[0] - tmp_dist[0], b[1] + tmp_dist[1]))
                        tmp_dist = (tmp_dist[0] + distance[0], tmp_dist[1] + distance[1])
                elif a[0] == b[0] or a[1] == b[1]:
                    pass
                else:
                    tmp_dist = distance[:]
                    while a[0] - tmp_dist[0] >= 0 and a[1] - tmp_dist[1] >= 0:
                        antinodes.add((a[0] - tmp_dist[0], a[1] - tmp_dist[1]))
                        tmp_dist = (tmp_dist[0] + distance[0], tmp_dist[1] + distance[1])
                    tmp_dist = distance[:]
                    while b[0] + tmp_dist[0] < self.x and b[1] + tmp_dist[1] < self.y:
                        antinodes.add((b[0] + tmp_dist[0], b[1] + tmp_dist[1]))
                        tmp_dist = (tmp_dist[0] + distance[0], tmp_dist[1] + distance[1])
        print(antinodes)
        return len(antinodes)
