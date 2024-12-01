import typing
from collections import defaultdict

import solver


class Solver(solver.Solver):
    def _init(self):
        self.l1, self.l2 = [], defaultdict(lambda: 0)
        with open(self.input_file_path) as f:
            for line in f:
                a, b = line.split()
                self.l1.append(int(a))
                self.l2[int(b)] += 1

    def _solve_part1(self) -> int:
        return sum([max(a, b) - min(a, b) for a, b in zip(sorted(self.l1), self._dict_to_list(self.l2))])

    def _solve_part2(self) -> int:
        return sum([num * self.l2[num] for num in self.l1])

    @staticmethod
    def _dict_to_list(d: typing.Dict[int, int]) -> typing.List[int]:
        return sum([[k] * d[k] for k in sorted(d.keys())], [])
