import re

import solver


class Solver(solver.Solver):
    def _init(self):
        with open(self.input_file_path) as f:
            self.instructions = re.findall(r"(do\(\)|don't\(\)|mul\(\d+,\d+\))", f.read(), re.MULTILINE)

    def _solve_part1(self) -> int:
        return sum(
            [
                int(a) * int(b)
                for a, b in map(lambda x: x[4:-1].split(',') if x.startswith('mul') else (0, 0), self.instructions)
            ]
        )

    def _solve_part2(self) -> int:
        res = 0
        work = True
        for instruction in self.instructions:
            if instruction == 'do()':
                work = True
            elif instruction == 'don\'t()':
                work = False
            elif work:
                a, b = instruction[4:-1].split(',')
                res += int(a) * int(b)
        return res
