import typing
from functools import cmp_to_key
from itertools import zip_longest


def compare_lists(x: typing.List[int], y: typing.List[int]) -> typing.Optional[bool]:
    for i, j in zip_longest(x, y, fillvalue=None):
        if i is None:
            return True
        elif j is None:
            return False

        if isinstance(i, list) and isinstance(j, list):
            result = compare_lists(i, j)
            if result is not None:
                return result
            continue
        if isinstance(i, list):
            result = compare_lists(i, [j])
            if result is not None:
                return result
            continue
        elif isinstance(j, list):
            result = compare_lists([i], j)
            if result is not None:
                return result
            continue

        if i == j:
            continue
        elif i < j:
            return True
        elif i > j:
            return False


with open('2022/day13/input.txt') as file:
    raw = file.read().strip().split('\n\n')

result = 0
packets = []
for i, e in enumerate(raw):
    x, y = e.strip().split('\n')
    x, y = eval(x), eval(y)
    if compare_lists(x, y):
        result += i + 1
    packets.append(x)
    packets.append(y)

packets.append([[2]])
packets.append([[6]])

packets = sorted(packets, key=cmp_to_key(lambda x, y: -1 if compare_lists(x, y) else 1))

print(result)
print((packets.index([[2]]) + 1) * (packets.index([[6]]) + 1))
