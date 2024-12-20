import sys
import typing
from collections import defaultdict

import solver


class Solver(solver.Solver):
    def _init(self):
        self.walkable_tiles = 1
        self.grid: typing.List[typing.List[str]] = []
        with open(self.input_file_path) as f:
            for y, line in enumerate(f.readlines()):
                self.grid.append([])
                for x, ch in enumerate(line):
                    if ch == 'S':
                        self.start = (x, y)
                        self.grid[y].append('.')
                    elif ch == 'E':
                        self.end = (x, y)
                        self.grid[y].append('.')
                    else:
                        if ch == '.':
                            self.walkable_tiles += 1
                        self.grid[y].append(ch)

    def get(self, x: int, y: int) -> str:
        if x < 0 or y < 0 or y >= len(self.grid) or x >= len(self.grid[0]):
            return '/'
        return self.grid[y][x]

    def get_neighbors(
        self,
        x: int,
        y: int,
    ) -> typing.List[typing.Tuple[int, int]]:
        return [
            (x + 1, y),
            (x - 1, y),
            (x, y + 1),
            (x, y - 1),
        ]

    def shortest_path(self, start: typing.Tuple[int, int]) -> typing.Dict[typing.Tuple[int, int], int]:
        optimal_path = {}
        distances = defaultdict(lambda: sys.maxsize)
        distances[start] = 0

        q = [(start, 0)]
        while q:
            cur, dist = q.pop(0)

            if dist > distances[cur]:
                continue

            for nx, ny in self.get_neighbors(cur[0], cur[1]):
                distance = dist + 1
                if distance < distances[(nx, ny)] and self.get(nx, ny) == '.':
                    distances[(nx, ny)] = distance
                    optimal_path[cur] = (nx, ny)
                    q.append(((nx, ny), distance))

        return distances

    def print_grid_with_cheats(self, cheats: typing.Set[typing.Tuple[int, int]]) -> None:
        for y, line in enumerate(self.grid):
            for x, ch in enumerate(line):
                if (x, y) in cheats:
                    print('X', end='')
                else:
                    print(ch, end='')

    def shortest_path_with_cheats(self, max_cheats: int = 2, min_dist_diff: int = 100) -> int:
        start_to_end = self.shortest_path(self.start)
        end_to_start = self.shortest_path(self.end)

        time_saved = defaultdict(lambda: 0)
        for y, line in enumerate(self.grid):
            for x, ch in enumerate(line):
                if ch == '#':
                    continue

                for y1 in range(-max_cheats, max_cheats + 1):
                    for x1 in range(-max_cheats, max_cheats + 1):
                        if abs(y1) + abs(x1) > max_cheats:
                            continue

                        y2, x2 = y + y1, x + x1
                        if 0 <= y2 < len(self.grid) and 0 <= x2 <= len(self.grid[0]) and self.get(x2, y2) != '#':
                            new_time = start_to_end[(x, y)] + abs(y1) + abs(x1) + end_to_start[(x2, y2)]
                            if new_time < self.walkable_tiles:
                                time_saved[self.walkable_tiles - new_time] += 1

        cheats = 0
        for k, v in time_saved.items():
            if k >= min_dist_diff:
                cheats += v
        return cheats

    def _solve_part1(self) -> int:
        return self.shortest_path_with_cheats(
            max_cheats=2, min_dist_diff=100 if 'input.txt' in self.input_file_path else 0
        )

    def _solve_part2(self) -> int:
        return self.shortest_path_with_cheats(
            max_cheats=20, min_dist_diff=100 if 'input.txt' in self.input_file_path else 50
        )
