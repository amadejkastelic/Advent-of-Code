import typing


def get_compartments(rucksack: str) -> typing.Tuple[str, str]:
    n = int(len(rucksack) / 2)
    return rucksack[:n], rucksack[n:]


def get_priority(c: str) -> int:
    if c.isupper():
        return ord(c) - 38
    return ord(c) - 96


with open('2022/day3/input.txt') as file:
    rucksacks = file.readlines()

priorities = []
for rucksack in rucksacks:
    x, y = get_compartments(rucksack)
    x, y = set(x), set(y)

    priorities.append(get_priority(list(x & y)[0]))

print('Part 1: {}'.format(sum(priorities)))

priorities = []
for group in range(int(len(rucksacks) / 3)):
    i = 3 * group
    priorities.append(
        get_priority(
            list(
                set(rucksacks[i].strip())
                & set(rucksacks[i + 1].strip())
                & set(rucksacks[i + 2].strip())
            )[0]
        )
    )

print('Part 2: {}'.format(sum(priorities)))
