import typing

CYCLES = 1000000000


class BeamMap(object):
    def __init__(self, beam_map: typing.List[typing.List[str]]) -> None:
        self.beam_map = beam_map

    def __str__(self) -> str:
        res = ''
        for line in self.beam_map:
            res += ''.join(line) + '\n'
        return res

    def __hash__(self) -> int:
        return hash(str(self))

    def tilt_north(self) -> None:
        for y in range(1, len(self.beam_map)):
            for x in range(len(self.beam_map[y])):
                if self.beam_map[y][x] != 'O':
                    continue

                for i in range(y - 1, -1, -1):
                    if self.beam_map[i][x] != '.':
                        self.beam_map[y][x], self.beam_map[i + 1][x] = '.', 'O'
                        break
                    elif i == 0:
                        self.beam_map[y][x], self.beam_map[i][x] = '.', 'O'
                        break

    def tilt_south(self) -> None:
        for y in range(len(self.beam_map) - 2, -1, -1):
            for x in range(len(self.beam_map[y])):
                if self.beam_map[y][x] != 'O':
                    continue

                for i in range(y + 1, len(self.beam_map)):
                    if self.beam_map[i][x] != '.':
                        self.beam_map[y][x], self.beam_map[i - 1][x] = '.', 'O'
                        break
                    elif i == len(self.beam_map) - 1:
                        self.beam_map[y][x], self.beam_map[i][x] = '.', 'O'
                        break

    def tilt_west(self) -> None:
        for x in range(1, len(self.beam_map[0])):
            for y in range(len(self.beam_map)):
                if self.beam_map[y][x] != 'O':
                    continue

                for i in range(x - 1, -1, -1):
                    if self.beam_map[y][i] != '.':
                        self.beam_map[y][x], self.beam_map[y][i + 1] = '.', 'O'
                        break
                    elif i == 0:
                        self.beam_map[y][x], self.beam_map[y][i] = '.', 'O'
                        break

    def tilt_east(self) -> None:
        for x in range(len(self.beam_map[0]) - 1, -1, -1):
            for y in range(len(self.beam_map)):
                if self.beam_map[y][x] != 'O':
                    continue

                for i in range(x + 1, len(self.beam_map[0])):
                    if self.beam_map[y][i] != '.':
                        self.beam_map[y][x], self.beam_map[y][i - 1] = '.', 'O'
                        break
                    elif i == len(self.beam_map[0]) - 1:
                        self.beam_map[y][x], self.beam_map[y][i] = '.', 'O'
                        break

    @property
    def total_load(self) -> int:
        result = 0
        for y in range(len(self.beam_map) - 1, -1, -1):
            result += self.beam_map[y].count('O') * (len(self.beam_map) - y)
        return result

    def cycle(self) -> None:
        self.tilt_north()
        self.tilt_west()
        self.tilt_south()
        self.tilt_east()


if __name__ == '__main__':
    with open('2023/day14/input.txt', 'r') as input_file:
        positions: typing.List[typing.List[str]] = []
        for line in input_file:
            positions.append(list(line.strip()))

    beam_map = BeamMap(beam_map=positions)
    beam_map.tilt_north()

    print(f'Part 1: {beam_map.total_load}')

    beam_map = BeamMap(beam_map=positions)

    cache: typing.Dict[typing.Tuple[str, int], int] = {(str(beam_map), beam_map.total_load): 0}
    for i in range(1, CYCLES):
        beam_map.cycle()
        k = (str(beam_map), beam_map.total_load)
        if k not in cache:
            cache[k] = i
        else:
            cycle = i - cache[k]
            idx = cache[k] + (CYCLES - cache[k]) % cycle
            for key, value in cache.items():
                if value == idx:
                    print(f'Part 2: {key[1]}')
                    exit(0)
