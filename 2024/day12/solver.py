import enum
import typing
from collections import defaultdict

import solver


class Direction(enum.Enum):
    UP_DOWN = 0
    SIDE = 1


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
                    for nx, ny, _ in self._get_existing_neighbors(x, y):
                        if self._get(x, y) == self._get(nx, ny):
                            self.regions[plot].add((nx, ny))
                            q.append((nx, ny))

                existing_plots.add(plot)
                visited.add((i, j))

    def _get_neighbors(
        self,
        x: int,
        y: int,
        direction: typing.Optional[Direction] = None,
    ) -> typing.List[typing.Tuple[int, int]]:
        if not direction:
            return [
                (x - 1, y, Direction.UP_DOWN),
                (x + 1, y, Direction.UP_DOWN),
                (x, y - 1, Direction.SIDE),
                (x, y + 1, Direction.SIDE),
            ]

        if direction == Direction.UP_DOWN:
            return [
                (x - 1, y, Direction.UP_DOWN),
                (x + 1, y, Direction.UP_DOWN),
            ]

        return [
            (x, y - 1, Direction.SIDE),
            (x, y + 1, Direction.SIDE),
        ]

    def _get_existing_neighbors(self, x: int, y: int) -> typing.List[typing.Tuple[int, int]]:
        return list(
            filter(
                lambda p: self._get(p[0], p[1]) != '.',
                self._get_neighbors(x, y),
            )
        )

    def _is_neighbor(self, reg: str, x: int, y: int) -> bool:
        return len(self.regions[reg]) <= 1 or any(
            [(i, j) in self.regions[reg] for i, j, _ in self._get_neighbors(x, y)]
        )

    def _get(self, x: int, y: int) -> str:
        if y < 0 or y >= len(self.garden) or x < 0 or x >= len(self.garden[y]):
            return '.'
        return self.garden[y][x]

    def _perimeter(self, region_name: str) -> int:
        res = 0
        for x, y in self.regions[region_name]:
            for n_x, n_y, _ in self._get_neighbors(x, y):
                if (n_x, n_y) not in self.regions[region_name]:
                    res += 1
        return res

    def _get_fences(self, region_name: str) -> typing.List[typing.Tuple[int, int, Direction]]:
        fences = set()
        for x, y in self.regions[region_name]:
            for n_x, n_y, direction in self._get_neighbors(x, y):
                if (n_x, n_y) not in self.regions[region_name]:
                    direction = Direction.SIDE
                    if x == n_x:
                        direction = Direction.UP_DOWN

                    fences.add((n_x, n_y, direction))
        return fences

    def _perimeter_2(self, region_name: str) -> int:
        fences = self._get_fences(region_name)
        new_fences = []
        visited = set()

        for fence in fences:
            x, y, direction = fence

            if fence in visited:
                continue
            visited.add(fence)

            new_fence = {fence}

            q = self._get_neighbors(x, y, direction)
            while q:
                neighbor = q.pop()
                if neighbor in visited:
                    continue
                visited.add(neighbor)

                if (x == neighbor[0] or y == neighbor[1]) and neighbor in fences:
                    new_fence.add(neighbor)
                    q += self._get_neighbors(neighbor[0], neighbor[1], direction)

            new_fences.append(new_fence)

        ln = len(new_fences)
        return len(new_fences)

    def _solve_part1(self) -> int:
        return sum([self._perimeter(reg) * len(plots) for reg, plots in self.regions.items()])

    def _solve_part2(self) -> int:
        return sum([self._perimeter_2(reg) * len(plots) for reg, plots in self.regions.items()])
