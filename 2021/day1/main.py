import typing


def main():
    file_name = input('Enter input path: ')

    with open(file_name, 'r') as f:
        content = f.read().splitlines()

    depths = list(map(int, content))

    print(_count_increases(depths=depths))
    print(_count_increases(depths=depths, sliding_window=3))


def _count_increases(depths: typing.List[int], sliding_window: int = 1) -> int:
    return sum([1 for i, x in enumerate(depths[sliding_window:]) if x > depths[i]])


if __name__ == '__main__':
    main()
