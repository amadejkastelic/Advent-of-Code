import typing


def main():
    file_name = input('Enter input path: ')

    with open(file_name, 'r') as f:
        content, instructions = f.read().split('\n\n')

    dots = set()
    for line in content.split('\n'):
        x, y = line.strip().split(',')
        dots.add((int(x), int(y)))

    for idx, instruction in enumerate(instructions.strip().split('\n')):
        fold, value = instruction.split('=')

        if fold[-1] == 'x':
            dots = _fold(dots=dots, x=int(value))
        else:
            dots = _fold(dots=dots, y=int(value))

        if idx == 0:
            print(f'Part 1: {len(dots)}')

    paper = [['.'] * 50 for _ in range(6)]
    for x, y in dots:
        paper[y][x] = '#'

    for row in paper:
        print(row, sep='')


def _fold(
    dots: typing.Set[typing.Tuple[int, int]], y: int = None, x: int = None
) -> typing.Set[typing.Tuple[int, int]]:
    result = set()
    for dot in dots:
        if y is not None and dot[1] > y:
            result.add((dot[0], y - (dot[1] - y)))
        elif x is not None and dot[0] > x:
            result.add((x - (dot[0] - x), dot[1]))
        else:
            result.add((dot[0], dot[1]))
    return result


if __name__ == '__main__':
    main()
