import typing
from math import floor, ceil
from functools import reduce as func_reduce


snailfish_typing = typing.Union[typing.List, int]


def main():
    file_name = input("Enter input path: ")

    with open(file_name, "r") as f:
        content = f.readlines()

    snailfish = [eval(line.strip()) for line in content]

    result = func_reduce(_combine, snailfish)
    print(f'Part 1: {_magnitude(number=result)}')

    result = -1
    for fish_1 in snailfish:
        for fish_2 in snailfish:
            if fish_1 == fish_2:
                continue
            result = max([_magnitude(number=_combine(x=fish_1, y=fish_2)), result])
    print(f'Part 2: {result}')


def _reduce(number: snailfish_typing) -> int:
    while True:
        exploded, number, _, _ = _explode(number=number)
        if not exploded:
            temp, number = number, _split(number=number)
            if number == temp:
                break
    return number


def _split(number: snailfish_typing) -> snailfish_typing:
    if isinstance(number, int):
        return [floor(number / 2), ceil(number / 2)] if number > 9 else number

    left = _split(number=number[0])
    if left != number[0]:
        return [left, number[1]]

    right = _split(number=number[1])
    return [number[0], right]


def _explode(
    number: snailfish_typing, depth: int = 0
) -> typing.Tuple[bool, snailfish_typing, snailfish_typing, snailfish_typing]:
    if isinstance(number, int):
        return False, number, 0, 0
    elif depth < 4:
        exploded, next_number, left, right = _explode(number=number[0], depth=depth + 1)
        if exploded:
            result = [next_number, _add_left(number=number[1], add=right)]
            return True, result, left, 0

        exploded, next_number, left, right = _explode(number=number[1], depth=depth + 1)
        if exploded:
            result = [_add_right(number=number[0], add=left), next_number]
            return True, result, 0, right
        return False, number, 0, 0

    return True, 0, number[0], number[1]


def _add_right(number: snailfish_typing, add: int) -> snailfish_typing:
    if isinstance(number, int):
        return number + add

    return [number[0], _add_right(number=number[1], add=add)]


def _add_left(number: snailfish_typing, add: int) -> snailfish_typing:
    if isinstance(number, int):
        return number + add

    return [_add_left(number=number[0], add=add), number[1]]


def _magnitude(number: snailfish_typing) -> int:
    if isinstance(number, int):
        return number

    return _magnitude(number=number[0]) * 3 + _magnitude(number=number[1]) * 2


def _combine(x: int, y: int) -> int:
    return _reduce(number=[x, y])


if __name__ == '__main__':
    main()
