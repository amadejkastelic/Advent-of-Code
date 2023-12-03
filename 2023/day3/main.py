import time
import typing
from functools import reduce


class Number(object):
    def __init__(self, value: int, y: int, x: typing.Tuple[int]):
        self.x = x
        self.y = y
        self.value = value

    def __eq__(self, other: 'Number') -> bool:
        return self.x == other.x and self.y == other.y

    def __ne__(self, other: 'Number') -> bool:
        return not self == other

    def __str__(self) -> str:
        return str(self.value)

    def __repr__(self) -> str:
        return self.__str__()

    def __hash__(self) -> int:
        return hash(tuple(self.__dict__[k] for k in sorted(self.__dict__)))


def get_symbol(schematic: typing.List[str], x: int, y: int) -> str:
    try:
        return schematic[y][x]
    except IndexError:
        return '.'


def get_adjacent_symbols(schematic: typing.List[str], x: int, y: int) -> typing.List[str]:
    res = []
    for i in range(-1, 2):
        for j in range(-1, 2):
            current = get_symbol(schematic=schematic, x=x + i, y=y + j)
            if not current.isdigit() and current != '.':
                res.append(current)
    return res


def get_adjacent_numbers(schematic: typing.List[str], x: int, y: int) -> typing.Set[Number]:
    res: typing.Set[Number] = set()
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            current = get_symbol(schematic=schematic, x=x + i, y=y + j)
            if current.isdigit():
                res.add(extract_number(schematic=schematic, x=x + i, y=y + j))
    return res


def extract_number(schematic: typing.List[str], x: int, y: int) -> Number:
    res = schematic[y][x]
    x_pos: typing.Set[int] = {x}
    for i in range(x - 1, -1, -1):
        current = get_symbol(schematic=schematic, x=i, y=y)
        if current.isdigit():
            res = current + res
            x_pos.add(i)
        else:
            break
    for i in range(x + 1, len(schematic[y])):
        current = get_symbol(schematic=schematic, x=i, y=y)
        if current.isdigit():
            res = res + current
            x_pos.add(i)
        else:
            break
    return Number(value=int(res), y=y, x=tuple(sorted(x_pos)))


if __name__ == '__main__':
    result: typing.Set[Number] = set()
    result2 = 0
    with open('2023/day3/input.txt', 'r') as input_file:
        schematic = [line.strip() for line in input_file]
        start = time.time()
        for j in range(len(schematic)):
            for i in range(len(schematic[j])):
                if schematic[j][i].isdigit() and get_adjacent_symbols(schematic=schematic, x=i, y=j):
                    result.add(extract_number(schematic=schematic, x=i, y=j))
                elif schematic[j][i] == '*':
                    adj_num = get_adjacent_numbers(schematic=schematic, x=i, y=j)
                    if len(adj_num) == 2:
                        result2 += reduce(lambda x, y: x.value * y.value, adj_num)
        print(f'Took {round((time.time() - start)*1000)}ms')

    print(f'Part 1: {sum([num.value for num in result])}')
    print(f'Part 2: {result2}')
