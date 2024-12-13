import typing
from collections import defaultdict

import solver


class Solver(solver.Solver):
    def _init(self):
        self.garden = []
        with open(self.input_file_path) as f:
            for j, line in enumerate(f.readlines()):
                self.garden.append(line.strip())

        self.regions: typing.Dict[str, typing.Set[typing.Tuple[int, int]]] = defaultdict(set)
        visited = set()
        existing_plots = set()
        for j in range(len(self.garden)):
            for i in range(len(self.garden[j])):
                if (i, j) in visited:
                    continue
                plot = self._get(i, j)
                while plot in existing_plots:
                    plot = plot + '_'

                self.regions[plot].add((i, j))

                q = [(i, j)]
                while q:
                    x, y = q.pop()
                    if (x, y) in visited:
                        continue
                    visited.add((x, y))
                    for nx, ny in self._get_existing_neighbors(x, y):
                        if self._get(x, y) == self._get(nx, ny):
                            self.regions[plot].add((nx, ny))
                            q.append((nx, ny))

                existing_plots.add(plot)
                visited.add((i, j))

    def _get_neighbors(self, x: int, y: int) -> typing.List[typing.Tuple[int, int]]:
        return [
            (x - 1, y),
            (x + 1, y),
            (x, y - 1),
            (x, y + 1),
        ]

    def _get_existing_neighbors(self, x: int, y: int) -> typing.List[typing.Tuple[int, int]]:
        return list(
            filter(
                lambda p: self._get(p[0], p[1]) != '.',
                self._get_neighbors(x, y),
            )
        )

    def _is_neighbor(self, reg: str, x: int, y: int) -> bool:
        return len(self.regions[reg]) <= 1 or any([(i, j) in self.regions[reg] for i, j in self._get_neighbors(x, y)])

    def _get(self, x: int, y: int) -> str:
        if y < 0 or y >= len(self.garden) or x < 0 or x >= len(self.garden[y]):
            return '.'
        return self.garden[y][x]

    def _perimeter(self, region_name: str) -> int:
        res = 0
        for x, y in self.regions[region_name]:
            for n_x, n_y in self._get_neighbors(x, y):
                if (n_x, n_y) not in self.regions[region_name]:
                    res += 1
        return res

    def _get_fences(self, region_name: str) -> typing.List[typing.Tuple[int, int]]:
        fences = set()
        for x, y in self.regions[region_name]:
            for n_x, n_y in self._get_neighbors(x, y):
                if (n_x, n_y) not in self.regions[region_name]:
                    fences.add((n_x, n_y))
        return list(fences)

    def _perimeter_2(self, region_name: str) -> int:
        res = 0
        fences = sorted(self._get_fences(region_name))
        combinations = set()
        for x, y in fences:
            for x2, y2 in fences:
                if x == x2 and y == y2:
                    continue

                if (x + 1 == x2 and y + 1 == y2) or (x + 1 == x2 and y - 1 == y2):
                    print(f'{region_name} - {(x, y)} - {(x2, y2)}')
                    combinations.add(frozenset({(x, y), (x2, y2)}))
                    res += 1

            if all(
                [
                    self._get(i, j) == region_name.strip('_') and frozenset({(x, y), (i, j)}) not in combinations
                    for i, j in [(x - 1, y), (x, y - 1)]
                ]
            ):
                res += 1

            if all(
                [
                    self._get(i, j) == region_name.strip('_') and frozenset({(x, y), (i, j)}) not in combinations
                    for i, j in [(x + 1, y), (x, y - 1)]
                ]
            ):
                res += 1

            if all(
                [
                    self._get(i, j) == region_name.strip('_') and frozenset({(x, y), (i, j)}) not in combinations
                    for i, j in [(x - 1, y), (x, y + 1)]
                ]
            ):
                res += 1

            if all(
                [
                    self._get(i, j) == region_name.strip('_') and frozenset({(x, y), (i, j)}) not in combinations
                    for i, j in [(x + 1, y), (x, y + 1)]
                ]
            ):
                res += 1

        return res

    def _solve_part1(self) -> int:
        return sum([self._perimeter(reg) * len(plots) for reg, plots in self.regions.items()])

    def _solve_part2(self) -> int:
        return sum([self._perimeter_2(reg) * len(plots) for reg, plots in self.regions.items()])
