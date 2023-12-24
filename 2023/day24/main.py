import typing

import sympy


class Hailstone(object):
    def __init__(
        self,
        alias: str,
        initial_position: typing.Tuple[int, int, int],
        velocity: typing.Tuple[int, int, int],
    ) -> None:
        self.alias = alias
        self.x, self.y, self.z = initial_position
        self.velocity_x, self.velocity_y, self.velocity_z = velocity

    def intersects_in_area(self, other: 'Hailstone', area: typing.Tuple[float, float] = (7.0, 27.0)) -> bool:
        if self.velocity_x * other.velocity_y - self.velocity_y * other.velocity_x == 0:
            return self.velocity_x * (self.y - other.y) + self.velocity_y * (other.x - self.x) == 0

        t2 = (self.velocity_x * (self.y - other.y) + self.velocity_y * (other.x - self.x)) / (
            self.velocity_x * other.velocity_y - self.velocity_y * other.velocity_x
        )
        t1 = (other.x - self.x + other.velocity_x * t2) / self.velocity_x

        if t1 < 0 or t2 < 0:
            return False

        intersection = (other.x + other.velocity_x * t2, other.y + other.velocity_y * t2)
        return area[0] <= intersection[0] <= area[1] and area[0] <= intersection[1] <= area[1]


def find_rock(hailstones: typing.List[Hailstone]) -> typing.Tuple[int, int, int]:
    posx, posy, posz, vx, vy, vz, t1, t2, t3 = sympy.symbols("posx posy posz vx vy vz t1 t2 t3", real=True)
    equations = [
        sympy.Eq(posx + vx * t1, hailstones[0].x + hailstones[0].velocity_x * t1),
        sympy.Eq(posy + vy * t1, hailstones[0].y + hailstones[0].velocity_y * t1),
        sympy.Eq(posz + vz * t1, hailstones[0].z + hailstones[0].velocity_z * t1),
        sympy.Eq(posx + vx * t2, hailstones[1].x + hailstones[1].velocity_x * t2),
        sympy.Eq(posy + vy * t2, hailstones[1].y + hailstones[1].velocity_y * t2),
        sympy.Eq(posz + vz * t2, hailstones[1].z + hailstones[1].velocity_z * t2),
        sympy.Eq(posx + vx * t3, hailstones[2].x + hailstones[2].velocity_x * t3),
        sympy.Eq(posy + vy * t3, hailstones[2].y + hailstones[2].velocity_y * t3),
        sympy.Eq(posz + vz * t3, hailstones[2].z + hailstones[2].velocity_z * t3),
    ]
    solution = sympy.solve(equations)[0]
    return (solution[posx], solution[posy], solution[posz])


if __name__ == '__main__':
    hailstones: typing.List[Hailstone] = []
    with open('2023/day24/input.txt', 'r') as input_file:
        for i, line in enumerate(input_file):
            position, velocity = line.strip().split(' @ ')
            hailstones.append(
                Hailstone(
                    alias=chr(i + 65),
                    initial_position=tuple(map(int, position.split(', '))),
                    velocity=tuple(map(int, velocity.split(', '))),
                )
            )

    result = 0
    for i, hailstone in enumerate(hailstones):
        for j in range(i + 1, len(hailstones)):
            if hailstone.intersects_in_area(other=hailstones[j], area=(200000000000000, 400000000000000)):
                result += 1

    print(f'Part 1: {result}')

    print(f'Part 2: {sum(find_rock(hailstones=hailstones))}')
