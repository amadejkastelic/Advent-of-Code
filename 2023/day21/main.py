import time
import typing


STEPS = (
    (0, -1),  # N
    (0, 1),  # S
    (1, 0),  # E
    (-1, 0),  # W
)


class Garden(object):
    def __init__(self, garden: typing.List[typing.List[str]]) -> None:
        self.garden = garden
        self.height, self.width = len(garden), len(garden[0])

    def at_index(self, x: int, y: int) -> str:
        try:
            return self.garden[y][x]
        except IndexError:
            return '#'

    def at_index_inf(self, x: int, y: int) -> str:
        return self.at_index(x=x % self.width, y=y % self.height)


if __name__ == '__main__':
    garden: typing.List[typing.List[str]] = []
    start = (0, 0)
    with open('2023/day21/input.txt', 'r') as input_file:
        for i, line in enumerate(input_file):
            garden.append(list(line.strip()))
            if 'S' in line:
                start = (line.find('S'), i)
                garden[start[1]][start[0]] = '.'
    garden = Garden(garden=garden)

    # Part 1
    s = time.time()
    possible_positions = {start}
    for i in range(64):
        temp_positions = set()
        for x, y in possible_positions:
            for offset_x, offset_y in STEPS:
                if garden.at_index(x=x + offset_x, y=y + offset_y) == '.':
                    temp_positions.add((x + offset_x, y + offset_y))
        possible_positions = temp_positions

    print(f'Part 1: {len(possible_positions)}')
    print(f'Took {round((time.time() - s)*1000)}ms')

    # Part 2
    s = time.time()
    steps = 26501365
    n = steps // garden.height
    possible_positions = {start}
    a = []
    for i in range((garden.height // 2) + (2 * garden.height)):
        temp_positions = set()
        for x, y in possible_positions:
            for offset_x, offset_y in STEPS:
                if garden.at_index_inf(x=x + offset_x, y=y + offset_y) == '.':
                    temp_positions.add((x + offset_x, y + offset_y))
        possible_positions = temp_positions.union()

        if i + 1 in (
            garden.height // 2,
            (garden.height // 2) + garden.height,
            (garden.height // 2) + (garden.height * 2),
        ):
            a.append(len(possible_positions))

    b = [a[0], a[1] - a[0], a[2] - a[1]]
    print(f'Part 2: {b[0] + b[1]*n + (n*(n-1)//2)*(b[2]-b[1])}')
    print(f'Took {round((time.time() - s)*1000)}ms')
