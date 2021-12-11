import typing


class Fish:
    def __init__(self, days: int = 8):
        self.days = days

    def next_day(self) -> typing.Optional[typing.Any]:
        if self.days == 0:
            self.days = 6
            return Fish()
        self.days -= 1


def _simulate_time(days: int, fish_list: typing.List[Fish]):
    for i in range(days):
        for j in range(len(fish_list)):
            child = fish_list[j].next_day()
            if child:
                fish_list.append(child)
    return fish_list


def _main():
    file_name = input('Enter input path: ')

    with open(file_name, 'r') as f:
        content = f.read().splitlines()

    fish_list = []
    for days in content[0].split(','):
        fish_list.append(Fish(days=int(days)))

    print(len(_simulate_time(fish_list=fish_list, days=80)))
    print(len(_simulate_time(fish_list=fish_list, days=256)))


if __name__ == '__main__':
    _main()
