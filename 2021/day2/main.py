import typing


def _main():
    file_name = input('Enter input path: ')

    with open(file_name, 'r') as f:
        content = f.read().splitlines()

    print(_calculate_position(moves=content, naive=True))
    print(_calculate_position(moves=content, naive=False))


def _calculate_position(moves: typing.List[str], naive=True) -> int:
    x, y, aim = 0, 0, 0

    for move in moves:
        direction, step = move.split(' ')
        if direction == 'forward':
            x += int(step)
            y += aim * int(step)
        elif direction == 'down':
            aim += int(step)
        elif direction == 'up':
            aim -= int(step)

    if naive:
        return x * aim

    return x * y


if __name__ == '__main__':
    _main()
