import sys
import typing

sys.setrecursionlimit(10000)


DIRECTIONS = {
    '.': [(-1, 0), (1, 0), (0, -1), (0, 1)],
    '^': [(0, -1)],
    'v': [(0, 1)],
    '<': [(-1, 0)],
    '>': [(1, 0)],
}


def at_index(grid: typing.List[typing.List[str]], x: int, y: int) -> str:
    try:
        return grid[y][x]
    except IndexError:
        return '#'


def maxPath(grid: typing.List[typing.List[str]], start: typing.Tuple[int, int], end: typing.Tuple[int, int]) -> int:
    if not grid or not grid[0]:
        return 0

    rows, cols = len(grid), len(grid[0])
    visited: typing.Set[typing.Tuple[int, int]] = set()

    def dfs(x: int, y: int) -> int:
        if (x, y) == end:
            return 1

        if (x, y) in visited:
            return 0

        visited.add((x, y))

        result = 0
        for offset_x, offset_y in DIRECTIONS[grid[y][x]]:
            x2, y2 = x + offset_x, y + offset_y
            if at_index(grid=grid, x=x2, y=y2) != '#':
                result = max(result, dfs(x2, y2) + 1)

        visited.remove((x, y))

        return result

    return dfs(*start)


if __name__ == '__main__':
    matrix: typing.List[typing.List[str]] = []
    start, end = (0, 0), (0, 0)
    with open('2023/day23/input.txt', 'r') as input_file:
        for i, line in enumerate(input_file):
            matrix.append(list(line.strip()))
            if i == 0:
                start = (line.index('.'), 0)
            elif i == len(line) - 1:
                end = (line.index('.'), len(line) - 1)

    print(f'Part 1: {maxPath(grid=matrix, start=start, end=end)-1}')

    result = 0
    longest_paths = []
    queue = [(start, [start])]
    while queue:
        current, path = queue.pop(0)
        x, y = current
        for offset_x, offset_y in DIRECTIONS['.']:
            x2, y2 = x + offset_x, y + offset_y
            if (x2, y2) == end:
                result = max(result, len(path + [(x2, y2)]))
                longest_paths = path + [(x2, y2)]
            elif (x2, y2) not in path and at_index(grid=matrix, x=x2, y=y2) != '#':
                queue.append(((x2, y2), path + [(x2, y2)]))

    print(f'Part 2: {result - 1}')
