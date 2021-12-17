import typing
from functools import reduce
from operator import mul


def main():
    file_name = input("Enter input path: ")

    with open(file_name, "r") as f:
        content = f.read().strip()

    content = content.split(': ')[1].split(', ')
    range_x = tuple(map(int, content[0][2:].split('..')))
    range_y = tuple(map(int, content[1][2:].split('..')))

    assert len(range_x) == 2
    assert len(range_y) == 2

    result = 0
    for i in range(range_x[1] + 1):
        for j in range(abs(range_y[0])):
            inside, pos = _run_steps(
                move_x=i, move_y=j, range_x=range_x, range_y=range_y
            )
            if inside:
                result = max([pos, result])
    print(f'Part 1: {result}')

    result = 0
    for i in range(range_x[1] + 1):
        for j in range(range_y[0], abs(range_y[0])):
            inside, pos = _run_steps(
                move_x=i, move_y=j, range_x=range_x, range_y=range_y
            )
            if inside:
                result += 1
    print(f'Part 2: {result}')


def _run_steps(
    move_x: int,
    move_y: int,
    range_x: typing.Tuple[int, int],
    range_y: typing.Tuple[int, int],
) -> typing.Tuple[bool, int]:
    result = 0
    x, y = 0, 0
    while y >= range_y[0]:
        x, y, move_x, move_y = _next_step(x=x, y=y, move_x=move_x, move_y=move_y)
        result = max([result, y])
        if range_x[0] <= x <= range_x[1] and range_y[0] <= y <= range_y[1]:
            return True, result
    return False, -1


def _next_step(
    x: int, y: int, move_x: int, move_y: int
) -> typing.Tuple[int, int, int, int]:
    x += move_x
    y += move_y
    if move_x > 0:
        move_x -= 1
    elif move_x < 0:
        move_x += 1
    move_y -= 1
    return x, y, move_x, move_y


if __name__ == "__main__":
    main()
