import typing
from collections import defaultdict

import solver


class Solver(solver.Solver):
    def __init__(self, input_file_path: str):
        super().__init__(input_file_path)
        self.l1, self.l2 = [], defaultdict(lambda: 0)
        with open(input_file_path) as f:
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
        res = []
        for k in sorted(d.keys()):
            for _ in range(d[k]):
                res.append(k)
        return res
