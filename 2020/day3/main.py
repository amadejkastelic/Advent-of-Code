import typing


def main():
    file_name = input('Enter input path: ')

    with open(file_name, 'r') as f:
        content = f.read().splitlines()

    part_1 = _traverse(grid=content)
    print(f'Part 1: {part_1}')

    part_2 = (
        part_1
        * _traverse(grid=content, right=1, down=1)
        * _traverse(grid=content, right=5, down=1)
        * _traverse(grid=content, right=7, down=1)
        * _traverse(grid=content, right=1, down=2)
    )
    print(f'Part 2: {part_2}')


def _traverse(grid: typing.List[str], right: int = 3, down: int = 1) -> int:
    count = 0
    x = 0
    for y in range(down, len(grid), down):
        if down > right:
            x = (x + right) % len(grid[y])
        else:
            x = (y * right) % len(grid[y])
        if grid[y][x] == '#':
            count += 1
    return count


if __name__ == '__main__':
    main()
