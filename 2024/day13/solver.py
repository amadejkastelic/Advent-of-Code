import dataclasses
import typing

import numpy as np

import solver


@dataclasses.dataclass
class Button:
    name: int
    x: int
    y: int
    cost: int

    @classmethod
    def parse(cls, b: str) -> 'Button':
        b = b.split(': ')
        x, y = b[1].split(', ')
        x = int(x.split('+')[1])
        y = int(y.split('+')[1])

        return cls(
            name=b[0][-1],
            x=x,
            y=y,
            cost=3 if b[0][-1] == 'A' else 1,
        )


@dataclasses.dataclass
class Equation:
    a: Button
    b: Button
    x: int
    y: int

    def cost_to_win(self) -> int:
        cost = 0

        while self.x > 0 and self.y > 0:
            if self.x % self.b.x == 0 and self.y % self.b.y == 0 and self.x // self.b.x == self.y // self.b.y:
                return cost + self.x // self.b.x

            self.x -= self.a.x
            self.y -= self.a.y
            cost += self.a.cost

        return cost if self.x == 0 and self.y == 0 else 0

    def cost_to_win_2(self, offset: int = 0) -> int:
        x, y = np.linalg.solve(
            np.array([[self.a.x, self.b.x], [self.a.y, self.b.y]]),
            np.array([self.x + offset, self.y + offset]),
        )
        if round(x, 2).is_integer() and round(y, 2).is_integer():
            return int(round(x, 0) * self.a.cost + round(y, 0) * self.b.cost)
        return 0


class Solver(solver.Solver):
    def _init(self):
        self.equations = []
        with open(self.input_file_path) as f:
            for eq in f.read().split('\n\n'):
                lines = eq.splitlines()
                x, y = lines[2].split(':')[1].split(', ')
                x = int(x.split('=')[1])
                y = int(y.split('=')[1])
                self.equations.append(
                    Equation(
                        a=Button.parse(lines[0]),
                        b=Button.parse(lines[1]),
                        x=x,
                        y=y,
                    )
                )

    def _solve_part1(self) -> int:
        return sum([eq.cost_to_win_2() for eq in self.equations])

    def _solve_part2(self) -> int:
        return sum([eq.cost_to_win_2(10000000000000) for eq in self.equations])
