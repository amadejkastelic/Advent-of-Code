import typing


def main():
    file_name = input('Enter input path: ')
    steps = int(input('Enter the number of steps: '))

    with open(file_name, 'r') as f:
        content = f.readlines()

    energies = [[int(num) for num in line.strip()] for line in content]

    result = 0
    count = 0
    while sum(sum(energies, [])) != 0:
        result += _next_step(energies=energies)
        count += 1
        if count == steps:
            print(f'Part 1: {result}')
    print(f'Part 2: {count}')


def _next_step(energies: typing.List[typing.List[int]]) -> int:
    flashes = 0
    cooldown = set()
    for y in range(len(energies)):
        for x in range(len(energies[y])):
            flashes += _flash(x=x, y=y, energies=energies, cooldown=cooldown)
    return flashes


def _flash(
    x: int,
    y: int,
    energies: typing.List[typing.List[int]],
    cooldown: typing.Set[typing.Tuple[int, int]],
) -> int:
    if (x, y) in cooldown:
        energies[y][x] = 0
        return 0

    if y < 0 or y >= len(energies) or x < 0 or x >= len(energies[0]):
        return 0

    energies[y][x] += 1

    if energies[y][x] != 10:
        return 0

    energies[y][x] = 0
    cooldown.add((x, y))

    flashes = 1
    for j in range(-1, 2, 1):
        for i in range(-1, 2, 1):
            flashes += _flash(x=x + i, y=y + j, energies=energies, cooldown=cooldown)
    return flashes


def _print_energies(energies: typing.List[typing.List[int]]):
    for line in energies:
        for energy in line:
            print(energy, end='')
        print()
    print()


if __name__ == '__main__':
    main()
