import time
import typing


EXPANSION = 1000000


class Galaxy(object):
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

    def __eq__(self, other: 'Galaxy') -> bool:
        return isinstance(other, Galaxy) and self.x == other.x and self.y == other.y

    def __str__(self) -> str:
        return f'({self.x}, {self.y})'

    def __repr__(self) -> str:
        return str(self)

    def __hash__(self) -> int:
        return hash(str(self))

    def distance_to(self, other: 'Galaxy') -> int:
        return abs(self.y - other.y) + abs(self.x - other.x)


if __name__ == '__main__':
    start = time.time()

    image: typing.List[str] = []
    expanded_rows: typing.List[int] = []
    expanded_columns: typing.List[int] = []
    with open('2023/day11/input.txt', 'r') as input_file:
        for i, line in enumerate(input_file):
            line = line.strip()
            image.append(line)
            if '#' not in line:
                expanded_rows.append(i)

    for i in range(len(image[0])):
        if all([image[j][i] == '.' for j in range(len(image))]):
            expanded_columns.append(i)

    galaxies: typing.List[Galaxy] = []
    for y in range(len(image)):
        for x in range(len(image[y])):
            if image[y][x] == '#':
                exp_y = [row < y for row in expanded_rows].count(True) * (EXPANSION-1)
                exp_x = [col < x for col in expanded_columns].count(True) * (EXPANSION-1)
                galaxies.append(Galaxy(x=x + exp_x, y=y + exp_y))

    pairs = [(g1, g2) for i, g1 in enumerate(galaxies) for g2 in galaxies[i + 1 :]]
    result = 0
    for g1, g2 in pairs:
        result += g1.distance_to(other=g2)
    print(f'Result: {result}')
    print(f'Took {round((time.time() - start)*1000)}ms')
