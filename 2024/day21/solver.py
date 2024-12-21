import dataclasses
import typing

import solver


NUMPAD_GRID = [
    ['7', '8', '9'],
    ['4', '5', '6'],
    ['1', '2', '3'],
    ['/', '0', 'A'],
]

NUMPAD_GRID_TO_IDX = {
    '7': (0, 0),
    '8': (1, 0),
    '9': (2, 0),
    '4': (0, 1),
    '5': (1, 1),
    '6': (2, 1),
    '1': (0, 2),
    '2': (1, 2),
    '3': (2, 2),
    '0': (1, 3),
    'A': (2, 3),
}

KEYPAD_GRID = [
    ['/', '^', 'A'],
    ['<', 'v', '>'],
]

KEYPAD_GRID_TO_IDX = {
    '^': (1, 0),
    'A': (2, 0),
    '<': (0, 1),
    'v': (1, 1),
    '>': (2, 1),
}

DIRECTION_TO_ARROW = {
    (1, 0): '>',
    (-1, 0): '<',
    (0, 1): 'v',
    (0, -1): '^',
}


@dataclasses.dataclass
class Robot:
    id: int
    grid: typing.List[typing.List[str]]
    position: typing.Tuple[int, int]
    controlling_arm: typing.Optional['Robot']
    cache: typing.Dict[typing.Tuple[typing.Tuple[int, int], typing.Tuple[int, int]], str]

    def key_to_pos(self, key: str) -> typing.Tuple[int, int]:
        if self.id == 1:
            return NUMPAD_GRID_TO_IDX[key]

        return KEYPAD_GRID_TO_IDX[key]

    def set_arm(self, arm: 'Robot') -> None:
        if self.controlling_arm is not None:
            self.controlling_arm.set_arm(arm)
        else:
            self.controlling_arm = arm

    def type_code(self, code: str) -> str:
        keystrokes = ''
        if self.controlling_arm:
            for ch in code:
                target_pos = self.key_to_pos(ch)
                cache_key = (self.id, self.get(*self.position), ch)
                if cache_key in self.cache:
                    keystrokes += self.cache[cache_key]
                    self.position = target_pos
                    continue

                tmp_keystrokes = ''
                for path in self.paths(ch):
                    ks = self.controlling_arm.type_code(path)
                    if tmp_keystrokes and len(ks) > len(tmp_keystrokes):
                        continue
                    tmp_keystrokes = ks
                self.cache[cache_key] = tmp_keystrokes
                self.position = target_pos
                keystrokes += tmp_keystrokes
        else:
            for ch in code:
                keystrokes += min(self.paths(ch), key=len)
                self.position = self.key_to_pos(ch)
        return keystrokes

    def get(self, x: int, y: int) -> str:
        if x < 0 or y < 0 or y >= len(self.grid) or x >= len(self.grid[0]):
            return '/'
        return self.grid[y][x]

    def get_neighbor_offsets(self) -> typing.List[typing.Tuple[int, int]]:
        return DIRECTION_TO_ARROW.keys()

    def paths(self, target: str) -> typing.Set[str]:
        queue = [(self.position, '', set())]
        paths = set()

        while queue:
            cur, path, visited = queue.pop(0)

            if cur in visited:
                continue

            visited = visited.union({cur})

            if self.get(cur[0], cur[1]) == target:
                paths.add(path + 'A')
                continue

            for nx_offset, ny_offset in self.get_neighbor_offsets():
                nx, ny = cur[0] + nx_offset, cur[1] + ny_offset
                if self.get(nx, ny) != '/':
                    queue.append(((nx, ny), path + DIRECTION_TO_ARROW[(nx_offset, ny_offset)], visited))

        return paths


class Solver(solver.Solver):
    def _init(self):
        with open(self.input_file_path) as f:
            self.desired_keypresses = [line.strip() for line in f.readlines()]

    def calculate(self, keypad_arms_cnt: int = 2) -> int:
        numpad_cache = {}
        keypad_cache = {}
        robot = Robot(
            id=1,
            grid=NUMPAD_GRID,
            position=(2, 3),
            controlling_arm=None,
            cache=numpad_cache,
        )
        for i in range(keypad_arms_cnt):
            robot.set_arm(
                Robot(
                    id=i + 2,
                    grid=KEYPAD_GRID,
                    position=(2, 0),
                    controlling_arm=None,
                    cache=keypad_cache,
                )
            )

        return sum([len(robot.type_code(dk)) * int(dk[:-1]) for dk in self.desired_keypresses])

    def _solve_part1(self) -> int:
        return self.calculate(2)

    def _solve_part2(self) -> int:
        return self.calculate(25)
