import typing


class Policy:
    def __init__(self, _min: int, _max: int, char: str):
        self._min = _min
        self._max = _max
        self.char = char

    @staticmethod
    def parse(rules: str) -> typing.Any:
        min_max, char = rules.split()
        _min, _max = map(int, min_max.split('-'))
        return Policy(_min=_min, _max=_max, char=char)

    def is_valid(self, password: str) -> bool:
        return self._min <= password.count(self.char) <= self._max

    def is_valid_v2(self, password: str) -> bool:
        return (password[self._min - 1] == self.char) ^ (
            password[self._max - 1] == self.char
        )


def main():
    file_name = input('Enter input path: ')

    with open(file_name, 'r') as f:
        content = f.read().splitlines()

    count_v1 = 0
    count_v2 = 0
    for line in content:
        rules, password = line.split(': ')
        policy = Policy.parse(rules=rules.strip())
        if policy.is_valid(password=password.strip()):
            count_v1 += 1
        if policy.is_valid_v2(password=password.strip()):
            count_v2 += 1
    print(f'Part 1: {count_v1}')
    print(f'Part 2: {count_v2}')


if __name__ == '__main__':
    main()
