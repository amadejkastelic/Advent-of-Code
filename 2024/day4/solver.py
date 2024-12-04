import solver


class Solver(solver.Solver):
    def _init(self):
        with open(self.input_file_path) as f:
            self.word_map = []
            for line in f.readlines():
                self.word_map.append(line.strip())

    def get_char(self, x: int, y: int) -> str:
        if x < 0 or y < 0 or y >= len(self.word_map) or x >= len(self.word_map[0]):
            return '.'
        return self.word_map[y][x]

    def search(self, x: int, y: int) -> int:
        if self.get_char(x=x, y=y) != 'X':
            return 0

        words = ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X']
        for i in range(1, 4):
            words[0] += self.get_char(x=x + i, y=y)
            words[1] += self.get_char(x=x - i, y=y)
            words[2] += self.get_char(x=x, y=y + i)
            words[3] += self.get_char(x=x, y=y - i)
            words[4] += self.get_char(x=x + i, y=y + i)
            words[5] += self.get_char(x=x + i, y=y - i)
            words[6] += self.get_char(x=x - i, y=y + i)
            words[7] += self.get_char(x=x - i, y=y - i)
        return words.count('XMAS')

    def search_2(self, x: int, y: int) -> int:
        if self.get_char(x=x, y=y) != 'A':
            return 0
        dia1 = self.get_char(x=x - 1, y=y - 1) + 'A' + self.get_char(x=x + 1, y=y + 1)
        dia2 = self.get_char(x=x - 1, y=y + 1) + 'A' + self.get_char(x=x + 1, y=y - 1)
        return 1 if dia1 in ('MAS', 'SAM') and dia2 in ('MAS', 'SAM') else 0

    def _solve_part1(self) -> int:
        res = 0
        for j in range(len(self.word_map)):
            for i in range(len(self.word_map[j])):
                res += self.search(x=i, y=j)
        return res

    def _solve_part2(self) -> int:
        res = 0
        for j in range(len(self.word_map)):
            for i in range(len(self.word_map[j])):
                res += self.search_2(x=i, y=j)
        return res
