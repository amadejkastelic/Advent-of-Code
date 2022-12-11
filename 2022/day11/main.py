import operator
import typing

OPS = {
    '+': operator.add,
    '*': operator.mul,
}


class Monkey(object):
    def __init__(
        self,
        items: typing.List[int],
        operation: str,
        test: int,
        throw_to: typing.Tuple[int, int],
    ) -> None:
        self.items = items
        self.test = test
        self.throw_to = throw_to
        self.inspections = 0

        op = operation.strip().split(' ')
        self.operation = OPS[op[1]]
        self.multiplier = op[2]

    def _worry_level(self, item: int, worry: int) -> int:
        if self.multiplier == 'old':
            result = item**2
        else:
            result = self.operation(item, int(self.multiplier))

        return int(result / worry) if worry == 3 else result % worry

    def throw(self, worry: int = 3) -> typing.Tuple[int, int]:
        item = self.items.pop(0)

        self.inspections += 1

        worry_level = self._worry_level(item=item, worry=worry)
        if worry_level % self.test == 0:
            return self.throw_to[0], worry_level

        return self.throw_to[1], worry_level


with open('2022/day11/input.txt') as file:
    raw = file.read().strip().split('\n\n')

monkeys: typing.List[Monkey] = []
for el in raw:
    el = el.split('\n')
    monkeys.append(
        Monkey(
            items=list(map(int, list(el[1].strip()[16:].split(', ')))),
            operation=el[2].strip().split('= ')[-1],
            test=int(el[3].strip().split(' ')[-1]),
            throw_to=(
                int(el[4].strip().split(' ')[-1]),
                int(el[5].strip().split(' ')[-1]),
            ),
        )
    )

for i in range(20):
    for monkey in monkeys:
        while len(monkey.items) > 0:
            throw_to, item = monkey.throw()
            monkeys[throw_to].items.append(item)

l = [monkey.inspections for monkey in monkeys]
highest_1 = max(l)
l.remove(highest_1)
highest_2 = max(l)
print(f'Part 1: {highest_1*highest_2}')


# P2
monkeys: typing.List[Monkey] = []
modulo = 1
for el in raw:
    el = el.split('\n')
    monkeys.append(
        Monkey(
            items=list(map(int, list(el[1].strip()[16:].split(', ')))),
            operation=el[2].strip().split('= ')[-1],
            test=int(el[3].strip().split(' ')[-1]),
            throw_to=(
                int(el[4].strip().split(' ')[-1]),
                int(el[5].strip().split(' ')[-1]),
            ),
        )
    )
    modulo *= int(el[3].strip().split(' ')[-1])

for i in range(10000):
    for monkey in monkeys:
        while len(monkey.items) > 0:
            throw_to, item = monkey.throw(worry=modulo)
            monkeys[throw_to].items.append(item)

l = [monkey.inspections for monkey in monkeys]
highest_1 = max(l)
l.remove(highest_1)
highest_2 = max(l)
print(f'Part 2: {highest_1*highest_2}')
