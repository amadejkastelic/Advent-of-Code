import enum
import typing
from functools import reduce


class Color(enum.Enum):
    RED = 'red'
    GREEN = 'green'
    BLUE = 'blue'


class Set(object):
    def __init__(self, red: int, green: int, blue: int):
        self.red = red
        self.green = green
        self.blue = blue

    def is_legal(self, available_cubes: typing.Dict[Color, int]) -> bool:
        return (
            available_cubes[Color.RED] >= self.red
            and available_cubes[Color.BLUE] >= self.blue
            and available_cubes[Color.GREEN] >= self.green
        )

class Game(object):
    def __init__(self, game: str):
        game_id, _, sets = game.partition(': ')
        self.id = int(game_id.split(' ')[1])
        self.sets: typing.List[Set] = []
        for s in sets.split('; '):
            new_set = Set(0, 0, 0)
            for cube in s.split(', '):
                num, _, color = cube.strip().partition(' ')
                new_set.__setattr__(color, int(num))
            self.sets.append(new_set)

    def is_legal(self, available_cubes: typing.Dict[Color, int]) -> bool:
        return all(
            s.is_legal(available_cubes=available_cubes)
            for s in self.sets
        )

    def max_of_each_color(self) -> typing.Dict[Color, int]:
        result = {
            Color.RED: 0,
            Color.GREEN: 0,
            Color.BLUE: 0,
        }
        for s in self.sets:
            if s.red > result[Color.RED]:
                result[Color.RED] = s.red
            if s.green > result[Color.GREEN]:
                result[Color.GREEN] = s.green
            if s.blue > result[Color.BLUE]:
                result[Color.BLUE] = s.blue
        return result


if __name__ == '__main__':
    with open('input.txt', 'r') as input_file:
        games: typing.List[Game] = []
        for line in input_file:
            line = line.strip()
            if line:
                games.append(Game(line))

    res = 0
    for game in games:
        if game.is_legal(available_cubes={
            Color.RED: 12,
            Color.GREEN: 13,
            Color.BLUE: 14,
        }):
            res += game.id
    print(f'Part 1: {res}')

    res = sum([reduce(lambda x, y: x*y, game.max_of_each_color().values()) for game in games])
    print(f'Part 2: {res}')
