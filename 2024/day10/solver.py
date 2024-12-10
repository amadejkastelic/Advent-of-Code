import typing

import solver


class Map:
    def __init__(self, top_map: typing.List[typing.List[int]]):
        self.map = top_map
        self.starting_positions = set()
        for j in range(len(self.map)):
            for i in range(len(self.map[j])):
                if self.map[j][i] == 0:
                    self.starting_positions.add((i, j))

    def _get(self, x: int, y: int) -> int:
        if x < 0 or x >= len(self.map[0]) or y < 0 or y >= len(self.map):
            return -1
        return self.map[y][x]

    def _neighbors(self, x: int, y: int) -> typing.List[typing.Tuple[int, int]]:
        return [
            (x - 1, y),
            (x + 1, y),
            (x, y - 1),
            (x, y + 1),
        ]

    def score(self, distinct_paths: bool = False) -> int:
        res = 0
        for x, y in self.starting_positions:
            res += self._can_walk_distinct_paths(x, y) if distinct_paths else self._can_walk(x, y, set())
        return res

    def _can_walk(
        self,
        x: int,
        y: int,
        visited: typing.Set[typing.Tuple[int, int]],
    ) -> None:
        visited.add((x, y))
        val = self._get(x, y)
        if val == 9:
            return 1

        return sum(
            [
                self._can_walk(nx, ny, visited) if (nx, ny) not in visited and self._get(nx, ny) == val + 1 else 0
                for nx, ny in self._neighbors(x, y)
            ]
        )

    def _can_walk_distinct_paths(self, x: int, y: int) -> int:
        queue = [(x, y, {(x, y)})]
        paths = set()
        while queue:
            curx, cury, visited = queue.pop(-1)

            val = self._get(curx, cury)
            if val == 9:
                paths.add(frozenset(visited))
                continue

            for nx, ny in self._neighbors(curx, cury):
                if val + 1 == self._get(nx, ny):
                    queue.append((nx, ny, visited | {(nx, ny)}))

        return len(paths)


class Solver(solver.Solver):
    def _init(self):
        with open(self.input_file_path) as f:
            top_map = []
            for line in f.readlines():
                top_map.append(list(map(int, list(line.strip()))))
        self.map = Map(top_map)

    def _solve_part1(self) -> int:
        return self.map.score()

    def _solve_part2(self) -> int:
        return self.map.score(distinct_paths=True)
