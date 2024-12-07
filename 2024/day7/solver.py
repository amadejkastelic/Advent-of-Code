import dataclasses
import enum
import typing

import solver


class Operator(enum.Enum):
    ADD = '+'
    MUL = '*'
    CON = '||'


@dataclasses.dataclass
class Equation:
    numbers: typing.List[int]
    expected_result: int

    def _eval(self, a: int, b: int, op: Operator = Operator.ADD) -> int:
        if op == Operator.CON:
            return int(f'{a}{b}')
        return int(eval(f'{a} {op.value} {b}'))

    def is_valid(self, with_con: bool = False) -> bool:
        paths = {(self.numbers[0], self.numbers[1], 2)}
        while paths:
            a, b, i = paths.pop()
            ev1 = self._eval(a, b, Operator.ADD)
            ev2 = self._eval(a, b, Operator.MUL)
            ev3 = self._eval(a, b, Operator.CON)
            if i < len(self.numbers):
                if ev1 < self.expected_result:
                    paths.add((ev1, self.numbers[i], i + 1))
                if ev2 < self.expected_result:
                    paths.add((ev2, self.numbers[i], i + 1))
                if with_con and ev3 < self.expected_result:
                    paths.add((ev3, self.numbers[i], i + 1))
                continue

            if ev1 == self.expected_result or ev2 == self.expected_result:
                return True
            if with_con and ev3 == self.expected_result:
                return True
        return False


class Solver(solver.Solver):
    def _init(self):
        self.equations: typing.List[Equation] = []
        with open(self.input_file_path) as f:
            for line in f.read().splitlines():
                res, nums = line.split(':')
                self.equations.append(
                    Equation(
                        numbers=list(map(int, nums.strip().split())),
                        expected_result=int(res),
                    )
                )

    def _solve_part1(self) -> int:
        return sum([eq.expected_result if eq.is_valid() else 0 for eq in self.equations])

    def _solve_part2(self) -> int:
        return sum([eq.expected_result if eq.is_valid(with_con=True) else 0 for eq in self.equations])
