import typing

import solver


class Solver(solver.Solver):
    def _init(self):
        with open(self.input_file_path) as f:
            self.stones = list(map(int, f.read().split()))

    @staticmethod
    def _blink_stone(stone: int) -> typing.List[int]:
        if stone == 0:
            return [1]
        elif len(str(stone)) % 2 == 0:
            return [int(str(stone)[0 : len(str(stone)) // 2]), int(str(stone)[len(str(stone)) // 2 :])]
        return [stone * 2024]

    def blink(self, n: int) -> int:
        steps = {stone: 1 for stone in self.stones}

        for _ in range(n):
            next_step = {}
            for stone in steps:
                for next_stone in self._blink_stone(stone):
                    next_step[next_stone] = next_step.get(next_stone, 0) + steps[stone]

            steps = next_step

        return sum(steps.values())

    def _solve_part1(self) -> int:
        return self.blink(25)

    def _solve_part2(self) -> int:
        return self.blink(75)
