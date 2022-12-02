import enum
import typing


class RPS(enum.Enum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3

    def loses_to(self):
        if self == RPS.ROCK:
            return RPS.PAPER
        elif self == RPS.PAPER:
            return RPS.SCISSORS
        else:
            return RPS.ROCK

    def wins_vs(self):
        if self == RPS.ROCK:
            return RPS.SCISSORS
        elif self == RPS.PAPER:
            return RPS.ROCK
        else:
            return RPS.PAPER


def parse(c: str) -> typing.Tuple[RPS]:
    if c in ['A', 'X']:
        return RPS.ROCK
    elif c in ['B', 'Y']:
        return RPS.PAPER
    elif c in ['C', 'Z']:
        return RPS.SCISSORS


def rps(a: RPS, b: RPS) -> typing.Optional[bool]:
    if a == b:
        return None

    return (
        (a == RPS.PAPER and b == RPS.ROCK)
        or (a == RPS.ROCK and b == RPS.SCISSORS)
        or (a == RPS.SCISSORS and b == RPS.PAPER)
    )


def calculate(a: RPS, b: RPS) -> typing.Tuple[int, int]:
    result = rps(a, b)
    if result is True:
        return a.value + 6, b.value
    elif result is False:
        return a.value, b.value + 6

    return a.value + 3, b.value + 3


def reverse_rps(a: RPS, result: typing.Optional[bool]) -> RPS:
    if result is True:
        return a.wins_vs()
    elif result is False:
        return a.loses_to()
    return a


with open('2022/day2/input.txt') as file:
    duels = file.readlines()

score_p1 = [0, 0]
score_p2 = [0, 0]
for duel in duels:
    a, b = duel.strip().split(' ')

    x, y = calculate(parse(a), parse(b))
    score_p1[0] += x
    score_p1[1] += y

    if b == 'X':
        outcome = True
    elif b == 'Y':
        outcome = None
    else:
        outcome = False
    b = reverse_rps(parse(a), outcome)
    x, y = calculate(parse(a), b)
    score_p2[0] += x
    score_p2[1] += y
    print(y)


print(f'Part 1: {score_p1}')
print(f'Part 2: {score_p2}')
