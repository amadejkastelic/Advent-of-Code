import typing


class CPU(object):
    def __init__(self) -> None:
        self.x = 1
        self._cycle = 1
        self._history = {}
        self.crt = ''

    def value_at_cycle(self, cycle: int):
        return self._history[cycle] * cycle

    def execute_multiple(self, ops: typing.List[str]):
        for op in ops:
            self.execute(op=op)

    def execute(self, op: str):
        self._history[self._cycle] = self.x
        self._cycle += 1
        if ((len(self.crt)) % 40) in [self.x - 1, self.x, self.x + 1]:
            self.crt += '#'
        else:
            self.crt += '.'
        if op.startswith('addx'):
            self._history[self._cycle] = self.x
            self._cycle += 1
            if ((len(self.crt)) % 40) in [self.x - 1, self.x, self.x + 1]:
                self.crt += '#'
            else:
                self.crt += '.'
            self.x += int(op.split(' ')[1])


with open('2022/day10/input.txt') as file:
    operations = file.read().strip().split('\n')

cpu = CPU()

cpu.execute_multiple(ops=operations)

print(
    f'Part 1: {cpu.value_at_cycle(20) + cpu.value_at_cycle(60) + cpu.value_at_cycle(100) + cpu.value_at_cycle(140) + cpu.value_at_cycle(180) + cpu.value_at_cycle(220)}'
)

for i in range(6):
    print(cpu.crt[i * 40 : (i + 1) * 40])
