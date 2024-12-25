import itertools
import typing

import solver


class Solver(solver.Solver):
    def _init(self):
        self.locks = []
        self.keys = []
        with open(self.input_file_path) as f:
            for schema in f.read().split('\n\n'):
                grid = schema.strip().splitlines()
                if grid[0][0] == '#':
                    heights = []
                    for x in range(len(grid[0])):
                        for y in range(1, len(grid)):
                            if grid[y][x] == '.':
                                heights.append(y - 1)
                                break
                    self.locks.append(tuple(heights))
                else:
                    heights = []
                    for x in range(len(grid[0])):
                        for y in range(len(grid) - 2, -1, -1):
                            if grid[y][x] == '.':
                                heights.append(len(grid) - y - 2)
                                break
                    self.keys.append(tuple(heights))
            self.height = len(grid) - 1

    def does_key_fit(self, key: typing.List[int], lock: typing.List[int]) -> bool:
        for k, l in zip(key, lock):
            if k + l >= self.height:
                return False
        return True

    def _solve_part1(self) -> int:
        return sum([1 if self.does_key_fit(key, lock) else 0 for key, lock in itertools.product(self.keys, self.locks)])

    def _solve_part2(self) -> int:
        pass
