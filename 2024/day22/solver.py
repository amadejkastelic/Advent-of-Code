import typing
from collections import defaultdict

import solver


class Secret:
    def __init__(self, value: str):
        self.cache: typing.Dict[int, int] = {0: int(str(value.strip())[-1])}
        self.value = int(value)

    def __hash__(self) -> int:
        return self.value

    def value_on_iter(self, iter: int) -> int:
        value = self.value
        for i in range(1, iter + 1):
            value = self.calculate_next(value)
            self.cache[i] = int(str(value)[-1])
        return value

    @staticmethod
    def _mix_and_prune(secret: int, result: int) -> int:
        return (secret ^ result) % 16777216

    def calculate_next(self, cur: int) -> int:
        next_num = Secret._mix_and_prune(cur, cur * 64)
        next_num = Secret._mix_and_prune(next_num, int(next_num / 32))
        return Secret._mix_and_prune(next_num, next_num * 2048)

    def sequences(self) -> typing.Dict[typing.Tuple[int, int, int, int], int]:
        res = {}

        for i in range(4, len(self.cache)):
            seq = tuple(
                [
                    self.cache[i - 3] - self.cache[i - 4],
                    self.cache[i - 2] - self.cache[i - 3],
                    self.cache[i - 1] - self.cache[i - 2],
                    self.cache[i] - self.cache[i - 1],
                ]
            )
            if seq not in res:
                res[seq] = self.cache[i]

        return res


class Solver(solver.Solver):
    def _init(self):
        with open(self.input_file_path) as f:
            self.secrets = list(map(Secret, f.readlines()))

    def _solve_part1(self) -> int:
        return sum([secret.value_on_iter(2000) for secret in self.secrets])

    def _solve_part2(self) -> int:
        res = defaultdict(int)
        for secret in self.secrets:
            for sequence, cost in secret.sequences().items():
                res[sequence] += cost
        return max(res.values())
