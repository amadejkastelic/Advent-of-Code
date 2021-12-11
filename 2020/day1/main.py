import typing


def main():
    file_name = input('Enter input path: ')

    with open(file_name, 'r') as f:
        content = f.read().splitlines()

    numbers = list(map(int, content))

    print(_find_expense(numbers=numbers))
    print(_find_expense_2(numbers=numbers))


def _find_expense(numbers: typing.List[int]) -> int:
    for i in range(len(numbers)):
        for j in range(len(numbers)):
            if i == j:
                continue
            if numbers[i] + numbers[j] == 2020:
                return numbers[i] * numbers[j]
    return 0


def _find_expense_2(numbers: typing.List[int]) -> int:
    for i in range(len(numbers)):
        for j in range(len(numbers)):
            if i == j:
                continue
            for k in range(len(numbers)):
                if i == k or j == k:
                    continue
                if numbers[i] + numbers[j] + numbers[k] == 2020:
                    return numbers[i] * numbers[j] * numbers[k]
    return 0


if __name__ == '__main__':
    main()
