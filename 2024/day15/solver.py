import typing

import solver


MOVE_TO_DIRECTION = {
    '>': (1, 0),
    'v': (0, 1),
    '<': (-1, 0),
    '^': (0, -1),
}


class Solver(solver.Solver):
    def _init(self):
        with open(self.input_file_path) as f:
            grid, moves = f.read().strip().split('\n\n')

        self.grid = list(map(list, grid.split()))
        self.moves: typing.List[str] = []
        for line in moves.splitlines():
            for move in line:
                self.moves.append(move)
        self.illegal_moves: typing.Set[typing.Tuple[int, int, str]] = set()

        self.grid2: typing.List[typing.List[str]] = []
        for j in range(len(self.grid)):
            self.grid2.append([])
            for i in range(len(self.grid[j])):
                match self.grid[j][i]:
                    case '@':
                        self.pos = (i, j)
                        self.grid2[j].append('@')
                        self.grid2[j].append('.')
                        self.pos2 = (i * 2, j)
                    case '#':
                        self.grid2[j].append('#')
                        self.grid2[j].append('#')
                    case '.':
                        self.grid2[j].append('.')
                        self.grid2[j].append('.')
                    case 'O':
                        self.grid2[j].append('[')
                        self.grid2[j].append(']')

    def _push_vertical(self, x: int, y: int, move: str) -> bool:
        direction = MOVE_TO_DIRECTION[move]
        x += direction[0]

        if self.grid[y][x] == '#':
            return False

        if self.grid[y][x] == '.':
            self.grid[y][x] = 'O'
            self.grid[y][x - direction[0]] = '.'
            return True

        if self.grid[y][x] == 'O':
            if self._push_vertical(x, y, move):
                self.grid[y][x] = 'O'
                self.grid[y][x - direction[0]] = '.'
                return True

        return False

    def _push_horizontal(self, x: int, y: int, move: str) -> bool:
        direction = MOVE_TO_DIRECTION[move]
        y += direction[1]

        if self.grid[y][x] == '#':
            return False

        if self.grid[y][x] == '.':
            self.grid[y][x] = 'O'
            self.grid[y - direction[1]][x] = '.'
            return True

        if self.grid[y][x] == 'O':
            if self._push_horizontal(x, y, move):
                self.grid[y][x] = 'O'
                self.grid[y - direction[1]][x] = '.'
                return True

        return False

    def push(self, x: int, y: int, move: str) -> bool:
        match move:
            case '>':
                return self._push_vertical(x, y, move)
            case 'v':
                return self._push_horizontal(x, y, move)
            case '<':
                return self._push_vertical(x, y, move)
            case '^':
                return self._push_horizontal(x, y, move)

    def move(self, move: str) -> None:
        dir = MOVE_TO_DIRECTION[move]
        new_pos = (self.pos[0] + dir[0], self.pos[1] + dir[1])

        if (new_pos[0], new_pos[1], move) in self.illegal_moves:
            return

        match self.grid[new_pos[1]][new_pos[0]]:
            case '#':
                self.illegal_moves.add((new_pos[0], new_pos[1], move))
                return
            case '.':
                self.grid[self.pos[1]][self.pos[0]] = '.'
                self.grid[new_pos[1]][new_pos[0]] = '@'
                self.pos = new_pos
                return
            case 'O':
                if self.push(new_pos[0], new_pos[1], move):
                    self.grid[self.pos[1]][self.pos[0]] = '.'
                    self.grid[new_pos[1]][new_pos[0]] = '@'
                    self.pos = new_pos
                return

        raise Exception('What?')

    def _push_vertical2(self, x: int, y: int, move: str) -> bool:
        direction = MOVE_TO_DIRECTION[move]
        x1, x2 = x - direction[0], x - 2 * direction[0]

        if self.grid2[y][x1] == '#' or self.grid2[y][x2] == '#':
            return False

        if self.grid2[y][x1] == '.' and self.grid2[y][x2] == '.':
            if move == '>':
                self.grid2[y][x1] = '['
                self.grid2[y][x2] = ']'
            else:
                self.grid2[y][x1] = ']'
                self.grid2[y][x2] = '['
            self.grid2[y][x1 - direction[0]] = '.'
            self.grid2[y][x2 - 2 * direction[0]] = '.'
            return True

        if self.grid2[y][x1] in ('[', ']'):
            if self._push_vertical2(x1, y, move):
                if move == '>':
                    self.grid2[y][x1] = '['
                    self.grid2[y][x2] = ']'
                else:
                    self.grid2[y][x1] = ']'
                    self.grid2[y][x2] = '['
                self.grid2[y][x1 - direction[0]] = '.'
                self.grid2[y][x2 - 2 * direction[0]] = '.'
                return True

        return False

    def _can_push_horizontal(self, x: int, y: int, move: str) -> bool:
        direction = MOVE_TO_DIRECTION[move]
        if self.grid2[y][x] == '[':
            x1, x2 = x, x + 1
        else:
            x1, x2 = x - 1, x
        y += direction[1]

        if self.grid2[y][x1] == '#' or self.grid2[y][x2] == '#':
            return False

        if self.grid2[y][x1] == '.' and self.grid2[y][x2] == '.':
            return True

        if self.grid2[y][x1] in ('[', ']') or self.grid2[y][x2] in ('[', ']'):
            return self._can_push_horizontal(x1, y, move) and self._can_push_horizontal(x2, y, move)

        return False

    def _push_horizontal2(self, x: int, y: int, move: str) -> bool:
        direction = MOVE_TO_DIRECTION[move]
        if self.grid2[y][x] == '[':
            x1, x2 = x, x + 1
        else:
            x1, x2 = x - 1, x
        y += direction[1]

        if self.grid2[y][x1] == '#' or self.grid2[y][x2] == '#':
            return False

        if self.grid2[y][x1] == '.' and self.grid2[y][x2] == '.':
            self.grid2[y - direction[1]][x1] = '.'
            self.grid2[y - direction[1]][x2] = '.'
            self.grid2[y][x1] = '['
            self.grid2[y][x2] = ']'
            return True

        if self.grid2[y][x1] in ('[', ']') or self.grid2[y][x2] in ('[', ']'):
            if self._can_push_horizontal(x1, y, move) and self._can_push_horizontal(x2, y, move):
                self._push_horizontal2(x1, y, move)
                self._push_horizontal2(x2, y, move)
                self.grid2[y - direction[1]][x1] = '.'
                self.grid2[y - direction[1]][x2] = '.'
                self.grid2[y][x1] = '['
                self.grid2[y][x2] = ']'
                return True

        return False

    def push2(self, x: int, y: int, move: str) -> bool:
        match move:
            case '>':
                return self._push_vertical2(x, y, move)
            case 'v':
                return self._push_horizontal2(x, y, move)
            case '<':
                return self._push_vertical2(x, y, move)
            case '^':
                return self._push_horizontal2(x, y, move)

    def move2(self, move: str) -> None:
        dir = MOVE_TO_DIRECTION[move]
        new_pos = (self.pos2[0] + dir[0], self.pos2[1] + dir[1])

        if (new_pos[0], new_pos[1], move) in self.illegal_moves:
            return

        match self.grid2[new_pos[1]][new_pos[0]]:
            case '#':
                self.illegal_moves.add((new_pos[0], new_pos[1], move))
                return
            case '.':
                self.grid2[self.pos2[1]][self.pos2[0]] = '.'
                self.grid2[new_pos[1]][new_pos[0]] = '@'
                self.pos2 = new_pos
                return
            case '[' | ']':
                if self.push2(new_pos[0], new_pos[1], move):
                    self.grid2[self.pos2[1]][self.pos2[0]] = '.'
                    self.grid2[new_pos[1]][new_pos[0]] = '@'
                    self.pos2 = new_pos
                return

        raise Exception('What?')

    def _solve_part1(self) -> int:
        res = 0
        for move in self.moves:
            self.move(move)

        for j in range(len(self.grid)):
            for i in range(len(self.grid[j])):
                if self.grid[j][i] == 'O':
                    res += 100 * j + i

        return res

    def _solve_part2(self) -> int:
        self.illegal_moves = set()
        res = 0
        for move in self.moves:
            self.move2(move)

        for j in range(len(self.grid2)):
            print(''.join(self.grid2[j]))
            for i in range(len(self.grid2[j])):
                if self.grid2[j][i] == '[':
                    res += 100 * j + i

        return res
