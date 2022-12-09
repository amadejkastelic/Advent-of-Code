import typing
from dataclasses import dataclass


@dataclass
class Knot:
    x: int
    y: int
    tail: bool


def fix_knots(head: Knot, body: Knot) -> typing.Optional[typing.Tuple[int, int]]:
    if abs(head.x - body.x) == 2:
        if body.x < head.x:
            body.x += 1
        else:
            body.x -= 1

        if body.y < head.y:
            body.y += 1
        elif body.y > head.y:
            body.y -= 1
    elif abs(head.y - body.y) == 2:
        if body.y < head.y:
            body.y += 1
        else:
            body.y -= 1

        if body.x < head.x:
            body.x += 1
        elif body.x > head.x:
            body.x -= 1
    else:
        return None

    if body.tail:
        return (body.x, body.y)


with open('2022/day9/input.txt') as file:
    commands = file.read().strip().split('\n')

rope_length = int(input('Set rope length: '))

visited = {(0, 0)}
rope = [Knot(0, 0, i == rope_length - 1) for i in range(rope_length)]

for command in commands:
    direction, steps = command.split(' ')
    for i in range(int(steps)):
        if direction == 'R':
            rope[0].x += 1
        elif direction == 'L':
            rope[0].x -= 1
        elif direction == 'U':
            rope[0].y += 1
        elif direction == 'D':
            rope[0].y -= 1

        for head, body in zip(rope, rope[1:]):
            point = fix_knots(head=head, body=body)
            if point is not None:
                visited.add(point)

print(f'Result: {len(visited)}')
