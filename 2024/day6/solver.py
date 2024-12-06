import solver


DIRECTIONS = {
    (0, -1): (1, 0),  # up
    (1, 0): (0, 1),  # right
    (0, 1): (-1, 0),  # down
    (-1, 0): (0, -1),  # left
}


class Solver(solver.Solver):
    def _init(self):
        with open(self.input_file_path) as f:
            self.map = [list(line) for line in f.read().splitlines()]
        for j in range(len(self.map)):
            for i in range(len(self.map[j])):
                if self.map[j][i] == '^':
                    self.pos = (i, j)
                    return

    def _solve_part1(self, max_cycle: int = 1000) -> int:
        res = 1
        self.visited = {self.pos}
        pos = self.pos
        direction = (0, -1)  # (x, y)
        cycle = 0
        while pos[1] > 0 and pos[1] < len(self.map) and pos[0] > 0 and pos[0] < len(self.map[0]):
            next_pos = (pos[0] + direction[0], pos[1] + direction[1])
            if (
                next_pos[0] < 0
                or next_pos[0] > len(self.map[0]) - 1
                or next_pos[1] < 0
                or next_pos[1] > len(self.map) - 1
            ):
                return res
            next_ch = self.map[next_pos[1]][next_pos[0]]
            if next_ch == '.' or next_ch == '^':
                pos = next_pos
                if pos not in self.visited:
                    res += 1
                    self.visited.add(pos)
                else:
                    cycle += 1
            elif next_ch == '#':
                direction = DIRECTIONS[direction]

            if cycle >= max_cycle:
                return -1
        return res

    def _solve_part2(self) -> int:
        res = 0
        visited = frozenset(self.visited)
        for vis in visited:
            i = vis[0]
            j = vis[1]
            if (
                self.map[j][i] == '.'
                and '#' in set(self.map[j])
                and '#' in {self.map[j][i] for i in range(len(self.map[j]))}
            ):
                self.map[j][i] = '#'
                if self._solve_part1() == -1:
                    res += 1
                self.map[j][i] = '.'
        return res
