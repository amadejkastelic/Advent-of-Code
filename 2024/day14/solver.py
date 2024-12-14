import functools
import typing
from collections import defaultdict

import solver


# MAP_SIZE = (11, 7)
MAP_SIZE = (101, 103)


class Robot:
    def __init__(self, pos: typing.Tuple[int, int], vel: typing.Tuple[int, int]):
        self.x, self.y = pos
        self.vx, self.vy = vel
        self.visited: typing.Dict[typing.Tuple[int, int], int] = {}
        self.initial = (self.x, self.y)

    @classmethod
    def parse(cls, robot: str) -> 'Robot':
        p, v = robot.strip().split()
        x, y = tuple(map(int, p[2:].split(',')))
        vx, vy = tuple(map(int, v[2:].split(',')))
        return cls(pos=(x, y), vel=(vx, vy))

    def __str__(self) -> str:
        return f'p={(self.x, self.y)} v={(self.vx, self.vy)}'

    def __repr__(self) -> str:
        return str(self)

    def reset(self) -> None:
        self.x, self.y = self.initial
        self.visited = {}

    def pass_time(self, seconds: int) -> None:
        for second in range(1, seconds + 1):
            self.x, self.y = self.x + self.vx, self.y + self.vy
            if self.x < 0:
                self.x = MAP_SIZE[0] + self.x
            elif self.x >= MAP_SIZE[0]:
                self.x -= MAP_SIZE[0]
            if self.y < 0:
                self.y = MAP_SIZE[1] + self.y
            elif self.y >= MAP_SIZE[1]:
                self.y -= MAP_SIZE[1]

            if (self.x, self.y) in self.visited:
                offset = self.visited[(self.x, self.y)]
                diff = second - offset
                search = ((seconds - offset) % diff) + 1
                for pos, s in self.visited.items():
                    if s == search:
                        self.x, self.y = pos
                        exit(0)
                        return

            self.visited[(self.x, self.y)] = second


class Solver(solver.Solver):
    def _init(self):
        self.robots: typing.List[Robot] = []
        with open(self.input_file_path) as f:
            for line in f.readlines():
                self.robots.append(Robot.parse(line))

    def _solve_part1(self) -> int:
        quadrant_offsets = ((MAP_SIZE[0] - 1) / 2, (MAP_SIZE[1] - 1) / 2)
        quadrant_cnts = [0, 0, 0, 0]
        for robot in self.robots:
            robot.pass_time(100)
            if robot.x < quadrant_offsets[0] and robot.y < quadrant_offsets[1]:
                quadrant_cnts[0] += 1
            elif robot.x > quadrant_offsets[0] and robot.y < quadrant_offsets[1]:
                quadrant_cnts[1] += 1
            elif robot.x < quadrant_offsets[0] and robot.y > quadrant_offsets[1]:
                quadrant_cnts[2] += 1
            elif robot.x > quadrant_offsets[0] and robot.y > quadrant_offsets[1]:
                quadrant_cnts[3] += 1
        return functools.reduce(lambda x, y: x * y, quadrant_cnts)

    def reset_robots(self) -> None:
        for robot in self.robots:
            robot.reset()

    def _solve_part2(self) -> int:
        self.reset_robots()
        for i in range(1000000):
            positions = defaultdict(lambda: 0)
            for robot in self.robots:
                robot.pass_time(1)
                positions[(robot.x, robot.y)] += 1
            if all([cnt <= 1 for cnt in positions.values()]):
                grid = []
                for y in range(MAP_SIZE[1]):
                    grid.append([])
                    for x in range(MAP_SIZE[0]):
                        if (x, y) in positions:
                            grid[y].append('*')
                        else:
                            grid[y].append('.')
                for line in grid:
                    print(''.join(line))

                return i + 1
