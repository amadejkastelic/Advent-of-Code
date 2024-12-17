import dataclasses
import math
import typing

import solver


@dataclasses.dataclass
class Computer:
    a: int
    b: int
    c: int
    program: typing.List[int]

    def _combo_to_value(self, op: int) -> int:
        match op:
            case 4:
                return self.a
            case 5:
                return self.b
            case 6:
                return self.c
            case 7:
                raise Exception('Invalid operand')

        return op

    def run(self) -> typing.List[int]:
        a, b, c = self.a, self.b, self.c
        output = []
        pointer = 0
        while pointer < len(self.program):
            match self.program[pointer]:
                case 0:
                    self.a = int(self.a / math.pow(2, self._combo_to_value(self.program[pointer + 1])))
                case 1:
                    self.b ^= self.program[pointer + 1]
                case 2:
                    self.b = self._combo_to_value(self.program[pointer + 1]) % 8
                case 3:
                    if self.a != 0:
                        pointer = self.program[pointer + 1]
                        continue
                case 4:
                    self.b ^= self.c
                case 5:
                    output.append(self._combo_to_value(self.program[pointer + 1]) % 8)
                case 6:
                    self.b = int(self.a / math.pow(2, self._combo_to_value(self.program[pointer + 1])))
                case 7:
                    self.c = int(self.a / math.pow(2, self._combo_to_value(self.program[pointer + 1])))

            pointer += 2

        self.a, self.b, self.c = a, b, c
        return output

    def find_a(self) -> int:
        search = [(len(self.program) - 1, 0)]
        for pointer, value in search:
            for a in range(value * 8, value * 8 + 8):
                self.a = a
                if self.run() == self.program[pointer:]:
                    search.append((pointer - 1, a))
                    if pointer == 0:
                        return a


class Solver(solver.Solver):
    def _init(self):
        with open(self.input_file_path) as f:
            lines = f.readlines()
        self.computer = Computer(
            a=int(lines[0].split(': ')[1].strip()),
            b=int(lines[1].split(': ')[1].strip()),
            c=int(lines[2].split(': ')[1].strip()),
            program=list(map(int, lines[4].split(': ')[1].split(','))),
        )

    def _solve_part1(self) -> str:
        return ','.join(map(str, self.computer.run()))

    def _solve_part2(self) -> int:
        return self.computer.find_a()
