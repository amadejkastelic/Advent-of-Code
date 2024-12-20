import copy
import sys
from collections import defaultdict


class Point3D:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return f'({self.x}, {self.y}, {self.z})'


class Brick:
    def __init__(self, id, a, b):
        self.a = Point3D(*a)
        self.b = Point3D(*b)
        self.id = id

    @property
    def minx(self):
        return min(self.a.x, self.b.x)

    @property
    def maxx(self):
        return max(self.a.x, self.b.x)

    @property
    def miny(self):
        return min(self.a.y, self.b.y)

    @property
    def maxy(self):
        return max(self.a.y, self.b.y)

    @property
    def minz(self):
        return min(self.a.z, self.b.z)

    @property
    def maxz(self):
        return max(self.a.z, self.b.z)

    def overlaps_xy(self, b):
        return (
            self.minx <= b.minx <= self.maxx
            or self.minx <= b.maxx <= self.maxx
            or b.minx <= self.minx <= b.maxx
            or b.minx <= self.maxx <= b.maxx
        ) and (
            self.miny <= b.miny <= self.maxy
            or self.miny <= b.maxy <= self.maxy
            or b.miny <= self.miny <= b.maxy
            or b.miny <= self.maxy <= b.maxy
        )

    def move(self, dx=0, dy=0, dz=0):
        for pt in (self.a, self.b):
            pt.x += dx
            pt.y += dy
            pt.z += dz

    def __hash__(self):
        return hash(self.id)

    def __repr__(self):
        return f'Brick({self.id:04d}, {self.a}, {self.b})'


def parse_input():
    with open('2023/day22/input.txt', 'r') as input_file:
        lines = [line for line in input_file]
    bricks = []
    for i, line in enumerate(lines):
        a, b = line.split('~')
        a = [int(_) for _ in a.split(',')]
        b = [int(_) for _ in b.split(',')]
        bricks.append(Brick(i, a, b))
    return bricks


def pack(bricks):
    bricks_by_minz = defaultdict(list)
    bricks_by_maxz = defaultdict(list)
    for b in bricks:
        bricks_by_minz[b.minz].append(b)
        bricks_by_maxz[b.maxz].append(b)

    moved = True
    while moved:
        moved = False
        for z, L in sorted(bricks_by_minz.items()):
            if z <= 1:
                continue

            for b in list(L):
                if not any(b.overlaps_xy(_) for _ in bricks_by_maxz[z - 1]):
                    # print('move', b)
                    bricks_by_minz[b.minz].remove(b)
                    bricks_by_maxz[b.maxz].remove(b)
                    b.move(dz=-1)
                    bricks_by_minz[b.minz].append(b)
                    bricks_by_maxz[b.maxz].append(b)
                    moved = True

    return bricks_by_maxz, bricks_by_minz


def part1(bricks):
    bricks_by_maxz, bricks_by_minz = pack(bricks)

    disintegrated = []

    for z, L in sorted(bricks_by_maxz.items()):
        for b in L:
            supporting = [_ for _ in bricks_by_minz[b.maxz + 1] if b.overlaps_xy(_)]
            if not supporting:
                disintegrated.append(b)
                continue

            needed = False
            for b2 in supporting:
                supported_by = [_ for _ in bricks_by_maxz[b2.minz - 1] if b2.overlaps_xy(_)]
                if len(supported_by) == 1:
                    assert supported_by[0] is b
                    needed = True
                    break

            if not needed:
                disintegrated.append(b)

    print(len(disintegrated))


def part2(bricks):
    bricks_by_maxz, bricks_by_minz = pack(bricks)

    tot = 0

    brick_supporting = {}
    brick_supported_by = {}
    for b in bricks:
        brick_supporting[b] = set([_ for _ in bricks_by_minz[b.maxz + 1] if b.overlaps_xy(_)])
        brick_supported_by[b] = set([_ for _ in bricks_by_maxz[b.minz - 1] if b.overlaps_xy(_)])

    for b in bricks:
        q = [b]
        fall = set([b])

        while q:
            x = q.pop()
            for b2 in brick_supporting[x]:
                s = brick_supported_by[b2]

                if s.issubset(fall):
                    fall.add(b2)
                    q.append(b2)

        fall.remove(b)
        tot += len(fall)

    print(tot)


def main():
    data = parse_input()
    part1(copy.deepcopy(data))
    part2(copy.deepcopy(data))


if __name__ == '__main__':
    main()
