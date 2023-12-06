import typing


class Boat(object):
    def __init__(self, starting_speed: int = 0, acceleration: int = 1, time_frame: int = 1) -> None:
        self.starting_speed = starting_speed
        self.acceleration = acceleration
        self.time_frame = time_frame

    def speed_for_held_time(self, t: int) -> int:
        return self.starting_speed + (self.acceleration * t)

    def beat(self, t: int, distance: int) -> typing.List[int]:
        possible_times_held = []
        for i in range(t + 1):
            moved = self.starting_speed + (self.speed_for_held_time(t=i)) * (t - i)
            if moved > distance:
                possible_times_held.append(i)
        return possible_times_held


if __name__ == '__main__':
    with open('2023/day6/input.txt', 'r') as input_file:
        lines = input_file.readlines()
        times = list(map(int, lines[0].split(':')[1].split()))
        distances = list(map(int, lines[1].split(':')[1].split()))

    result = 1
    my_boat = Boat()
    for t, d in zip(times, distances):
        result *= len(my_boat.beat(t=t, distance=d))

    print(f'Part 1: {result}')

    time = int(''.join(map(str, times)))
    distance = int(''.join(map(str, distances)))

    print(f'Part 2: {len(my_boat.beat(t=time, distance=distance))}')
