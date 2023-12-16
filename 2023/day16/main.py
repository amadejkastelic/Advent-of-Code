import enum
import typing


class Direction(enum.Enum):
    RIGHT = 0
    LEFT = 1
    UP = 2
    DOWN = 3


class Beam(object):
    def __init__(self, x: int = 0, y: int = 0, direction: Direction = Direction.RIGHT):
        self.x = x
        self.y = y
        self.direction = direction

    def __str__(self) -> str:
        return f'{self.direction.name.capitalize()} ({self.x}, {self.y})'

    def cycle(self) -> bool:
        for direction in self.directions:
            match direction:
                case Direction.RIGHT:
                    self.x += 1
                case Direction.LEFT:
                    self.x -= 1
                case Direction.UP:
                    pass
                case Direction.DOWN:
                    pass

    def duplicate(self, direction: Direction) -> 'Beam':
        return Beam(
            x=self.x,
            y=self.y,
            direction=direction,
        )


class Grid(object):
    def __init__(self, grid: typing.List[typing.List[str]], beam: Beam) -> None:
        self.beams = {beam}
        self.grid = grid
        self.visited: typing.Dict[typing.Tuple[int, int], typing.Set[Direction]] = {}

    def count_energized(self) -> int:
        return len(self.visited)

    def cycle(self) -> bool:
        if not self.beams:
            return False

        for beam in list(self.beams):
            match beam.direction:
                case Direction.RIGHT:
                    beam.x += 1
                case Direction.LEFT:
                    beam.x -= 1
                case Direction.UP:
                    beam.y -= 1
                case Direction.DOWN:
                    beam.y += 1

            if beam.y < 0 or beam.y >= len(self.grid) or beam.x < 0 or beam.x >= len(self.grid[beam.y]):
                self.beams.remove(beam)
                continue

            if beam.direction in self.visited.get((beam.x, beam.y), []):
                self.beams.remove(beam)
                continue

            if (beam.x, beam.y) not in self.visited:
                self.visited[(beam.x, beam.y)] = {beam.direction}
            else:
                self.visited[(beam.x, beam.y)].add(beam.direction)

            match self.grid[beam.y][beam.x]:
                case '/':
                    match beam.direction:
                        case Direction.RIGHT:
                            beam.direction = Direction.UP
                        case Direction.LEFT:
                            beam.direction = Direction.DOWN
                        case Direction.UP:
                            beam.direction = Direction.RIGHT
                        case Direction.DOWN:
                            beam.direction = Direction.LEFT
                case '\\':
                    match beam.direction:
                        case Direction.RIGHT:
                            beam.direction = Direction.DOWN
                        case Direction.LEFT:
                            beam.direction = Direction.UP
                        case Direction.UP:
                            beam.direction = Direction.LEFT
                        case Direction.DOWN:
                            beam.direction = Direction.RIGHT
                case '|':
                    match beam.direction:
                        case Direction.RIGHT | Direction.LEFT:
                            beam.direction = Direction.UP
                            self.beams.add(beam.duplicate(Direction.DOWN))
                case '-':
                    match beam.direction:
                        case Direction.UP | Direction.DOWN:
                            beam.direction = Direction.LEFT
                            self.beams.add(beam.duplicate(Direction.RIGHT))

        return True


if __name__ == '__main__':
    g: typing.List[typing.List[str]] = []
    with open('2023/day16/input.txt', 'r') as input_file:
        for line in input_file:
            g.append(list(line.strip()))

    grid = Grid(grid=g, beam=Beam(x=-1))
    while grid.cycle():
        pass

    print(f'Part 1: {grid.count_energized()}')

    results = []
    for i in range(len(g)):
        grid = Grid(grid=g, beam=Beam(x=-1, y=i, direction=Direction.RIGHT))
        while grid.cycle():
            pass
        results.append(grid.count_energized())

        grid = Grid(grid=g, beam=Beam(x=len(g), y=i, direction=Direction.LEFT))
        while grid.cycle():
            pass
        results.append(grid.count_energized())

    for i in range(len(g[0])):
        grid = Grid(grid=g, beam=Beam(x=i, y=-1, direction=Direction.DOWN))
        while grid.cycle():
            pass
        results.append(grid.count_energized())

        grid = Grid(grid=g, beam=Beam(x=i, y=len(g[0]), direction=Direction.UP))
        while grid.cycle():
            pass
        results.append(grid.count_energized())

    print(f'Part 2: {max(results)}')
