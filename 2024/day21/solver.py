import dataclasses
import typing

import solver


NUMPAD_GRID = [
    ['7', '8', '9'],
    ['4', '5', '6'],
    ['1', '2', '3'],
    ['/', '0', 'A'],
]

KEYPAD_GRID = [
    ['/', '^', 'A'],
    ['<', 'v', '>'],
]

DIRECTION_TO_ARROW = {
    (1, 0): '>',
    (-1, 0): '<',
    (0, 1): 'v',
    (0, -1): '^',
}


@dataclasses.dataclass
class Robot:
    grid: typing.List[typing.List[str]]
    position: typing.Tuple[int, int]
    controlling_arm: typing.Optional['Robot']

    def type_code(self, code: str) -> str:
        keystrokes = ''
        if self.controlling_arm:
            for ch in code:
                keystrokes += self.controlling_arm.type_code(self.shortest_path(ch))
                keystrokes += self.controlling_arm.type_code(self.shortest_path('A')) + 'A'
        else:
            for ch in code:
                keystrokes += self.shortest_path(ch)+ 'A'
        return keystrokes

    def get(self, x: int, y: int) -> str:
        if x < 0 or y < 0 or y >= len(self.grid) or x >= len(self.grid[0]):
            return '/'
        return self.grid[y][x]

    def get_neighbor_offsets(self) -> typing.List[typing.Tuple[int, int]]:
        return [
            (1, 0),
            (-1, 0),
            (0, 1),
            (0, -1),
        ]

    def shortest_path(self, target: str) -> str:
        queue = [(self.position, '')]
        while queue:
            cur, path = queue.pop(0)

            if self.get(cur[0], cur[1]) == target:
                self.position = cur
                return path

            for nx_offset, ny_offset in self.get_neighbor_offsets():
                nx, ny = cur[0] + nx_offset, cur[1] + ny_offset
                if self.get(nx, ny) != '/':
                    queue.append(((nx, ny), path + DIRECTION_TO_ARROW[(nx_offset, ny_offset)]))

        raise Exception('Path not found')


class Solver(solver.Solver):
    def _init(self):
        with open(self.input_file_path) as f:
            self.desired_keypresses = [line.strip() for line in f.readlines()]

        self.robot = Robot(
            grid=NUMPAD_GRID,
            position=(2, 3),
            controlling_arm=Robot(
                grid=KEYPAD_GRID,
                position=(2, 0),
                controlling_arm=Robot(
                    grid=KEYPAD_GRID,
                    position=(2, 0),
                    controlling_arm=None,
                ),
            ),
        )

    def _solve_part1(self) -> int:
        return self.robot.type_code(self.desired_keypresses[0])

    def _solve_part2(self) -> int:
        pass
