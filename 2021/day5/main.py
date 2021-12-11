import math
import typing


def _main():
    file_name = input("Enter input path: ")

    with open(file_name, 'r') as f:
        content = f.read().splitlines()

    print(_count_overlapping_points(lines=content))
    print(_count_overlapping_points(lines=content, diagonal=True))


def _is_line_ok(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    theta = math.atan2(dy, dx) * (180 / math.pi)
    return theta in [0.0, 45.0, 90.0]


def _count_overlapping_points(lines: typing.List[str], diagonal=False):
    points: typing.Dict[str, int] = {}
    for line in lines:
        temp = line.split('->')
        x1, y1 = map(int, temp[0].split(','))
        x2, y2 = map(int, temp[1].split(','))
        if x2 < x1:
            x1, x2 = x2, x1
        if y2 < y1:
            y1, y2 = y2, y1
        if not _is_line_ok(x1, y1, x2, y2):
            print(f'Line: {line} not ok.')
            continue
        if x1 != x2 and y1 == y2:
            for i in range(x1, x2 + 1):
                point = f'{i},{y1}'
                points[point] = points.get(point, 0) + 1
        elif y1 != y2 and x1 == x2:
            for i in range(y1, y2 + 1):
                point = f'{x1},{i}'
                points[point] = points.get(point, 0) + 1
        elif diagonal:
            x1, y1 = map(int, temp[0].split(','))
            x2, y2 = map(int, temp[1].split(','))
            dx = x2 - x1
            dy = y2 - y1
            if dx != 0:
                dx = dx // abs(dx)
            if dy != 0:
                dy = dy // abs(dy)
            while x1 != x2 or y1 != y2:
                point = f'{x1},{y1}'
                points[point] = points.get(point, 0) + 1
                x1 += dx
                y1 += dy
            point = f'{x2},{y2}'
            points[point] = points.get(point, 0) + 1

    return len(list(filter(lambda x: x > 1, points.values())))


if __name__ == '__main__':
    _main()
