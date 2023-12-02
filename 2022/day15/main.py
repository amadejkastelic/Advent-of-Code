import re

with open("2022/day15/input.txt") as file:
    rng = range(4_000_001 if True else 21) # change to False for sample data
    middle = rng.stop // 2
    covered_by_sensors = set()
    beacons = set()
    sensors = set()
    search_area = set()
    for line in file:
        sx, sy, bx, by = tuple(map(int, re.findall(r"-?\d+", line)))
        coverage = abs(sx - bx) + abs(sy - by)
        beacons.add((bx, by))
        sensors.add((sx, sy, coverage))
        dy = abs(sy - middle)
        dx = coverage - dy
        if dx > 0:
            covered_by_sensors |= set(range(sx - dx, sx + dx + 1))
        for cy in range(max(rng.start, sy - coverage - 1), min(rng.stop, sy + 1)):
            dx = coverage + cy - sy + 1
            search_area |= {(max(rng.start, sx - dx), cy), (min(rng.stop, sx + dx + 1), cy)}
        for cy in range(min(rng.stop, sy + coverage + 1), max(rng.start, sy), -1):
            dx = coverage - cy + sy + 1
            search_area |= {(max(rng.start, sx - dx), cy), (min(rng.stop, sx + dx + 1), cy)}
    for x, y in search_area:
        for sx, sy, coverage in sensors:
            distance = abs(sx - x) + abs(sy - y)
            if distance <= coverage:
                break
        else:
            break
    print(len(covered_by_sensors) - sum(1 for beacon in beacons if beacon[1] == middle))
    print(4_000_000 * x + y)