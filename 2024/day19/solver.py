from collections import defaultdict
import typing

import solver


class Solver(solver.Solver):
    def _init(self):
        self.patterns: typing.Dict[str, typing.List[str]] = defaultdict(list)
        with open(self.input_file_path) as f:
            lines = f.readlines()
        for pattern in lines[0].strip().split(', '):
            self.patterns[pattern[0]].append(pattern)
        self.designs = [design.strip() for design in lines[2:]]
        self.cache = {}
        self.total = 0

    def can_make(self, design: str) -> int:
        if len(design) == 0:
            return 1
        if design in self.cache:
            return self.cache[design]

        total = 0
        for pattern in self.patterns[design[0]]:
            if design.startswith(pattern):
                total += self.can_make(design[len(pattern) :])

        self.cache[design] = total

        return total

    def _solve_part1(self) -> int:
        result = 0
        for design in self.designs:
            res = self.can_make(design)
            if res > 0:
                self.total += res
                result += 1

        return result

    def _solve_part2(self) -> int:
        if self.total == 0:
            self._solve_part1()
        return self.total
