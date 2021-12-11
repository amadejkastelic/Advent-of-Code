import sys
import typing


def main():
    file_name = input('Enter input path: ')

    with open(file_name, 'r') as f:
        content = f.read()

    positions = list(map(int, content.split(',')))

    print(_least_fuel(positions=positions))
    print(_least_fuel_2(positions=positions))


def _least_fuel(positions: typing.List[int]) -> int:
    previous = sys.maxsize
    for i in range(min(positions), max(positions) + 1):
        current = 0
        for position in positions:
            current += abs(i - position)
        if current < previous:
            previous = current
    return previous


def _least_fuel_2(positions: typing.List[int]) -> int:
    previous = sys.maxsize
    for i in range(min(positions), max(positions) + 1):
        current = 0
        for position in positions:
            current += sum(range(1, abs(i - position) + 1))
        if current < previous:
            previous = current
    return previous


if __name__ == '__main__':
    main()
