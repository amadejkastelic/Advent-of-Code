import typing


def _main():
    file_name = input("Enter input path: ")

    with open(file_name, 'r') as f:
        content = f.read().splitlines()

    ages = [0] * 9
    for age in content[0].split(','):
        ages[int(age)] = ages[int(age)] + 1

    print(_simulate(ages=ages, days=80))
    print(_simulate(ages=ages, days=256))


def _simulate(ages: typing.List[int], days: int):
    fish = [1] * 9
    for i in range(days):
        fish = [fish[6] + fish[8]] + fish[:-1]

    result = 0
    for i in range(9):
        result += fish[i] * ages[i]
    return result


if __name__ == '__main__':
    _main()
