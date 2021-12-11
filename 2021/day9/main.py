import sys
import typing
import heapq
import math


def main():
    file_name = input("Enter input path: ")

    with open(file_name, 'r') as f:
        content = f.readlines()

    heightmap = []
    for line in content:
        heightmap.append([int(num) for num in line.strip()])

    print(_low_points(heightmap=heightmap))
    print(_find_basins(heightmap=heightmap))


def _low_points(heightmap: typing.List[typing.List[int]]) -> int:
    result = 0
    for y in range(len(heightmap)):
        for x in range(len(heightmap[y])):
            current = _get_height(x=x, y=y, heightmap=heightmap)
            if current < min(_get_neighbours(x=x, y=y, heightmap=heightmap)):
                result += current + 1
    return result


def _find_basins(heightmap: typing.List[typing.List[int]]) -> int:
    low_points = [
        (i, j)
        for i, row in enumerate(heightmap)
        for j, height in enumerate(row)
        if all(height > heightmap[y][x] for y, x in _get_neighbours_indexes(x=j, y=i, heightmap=heightmap))
    ]

    highest = []
    for y, x in low_points:
        area = _get_area(x=x, y=y, heightmap=heightmap)
        heapq.heappush(highest, area)
        if len(highest) > 3:
            heapq.heappop(highest)

    return math.prod(highest)


def _get_height(x: int, y: int, heightmap: typing.List[typing.List[int]]) -> int:
    if y < 0 or y >= len(heightmap) or x < 0 or x >= len(heightmap[0]):
        return sys.maxsize
    return int(heightmap[y][x])


def _get_neighbours(x: int, y: int, heightmap: typing.List[typing.List[int]]) -> typing.List[int]:
    return [
        _get_height(x=x - 1, y=y, heightmap=heightmap),
        _get_height(x=x, y=y - 1, heightmap=heightmap),
        _get_height(x=x + 1, y=y, heightmap=heightmap),
        _get_height(x=x, y=y + 1, heightmap=heightmap),
    ]


def _get_neighbours_indexes(x: int, y: int, heightmap: typing.List[typing.List[int]]) -> typing.List[typing.Tuple[int, int]]:
    neighbors = []

    if y > 0:
        neighbors.append((y - 1, x))
    if x > 0:
        neighbors.append((y, x - 1))
    if y + 1 < len(heightmap):
        neighbors.append((y + 1, x))
    if x + 1 < len(heightmap[0]):
        neighbors.append((y, x + 1))

    return neighbors


def _get_area(x: int, y: int, heightmap: typing.List[typing.List[int]]) -> int:
    if heightmap[y][x] >= 9 or heightmap[y][x] == -1:
        return 0
    heightmap[y][x] = -1
    return 1 + sum(_get_area(y=i, x=j, heightmap=heightmap) for i, j in _get_neighbours_indexes(x=x, y=y, heightmap=heightmap))


if __name__ == '__main__':
    main()
