import sys
import typing


class Interval(object):
    def __init__(self, start: int, end: int, count: int):
        self.start = start
        self.end = end
        self.count = count

    def map_num(self, num: int) -> int:
        if self.start <= num < self.start + self.count:
            return self.end + (num - self.start)
        return num

    def __str__(self) -> str:
        return f'({self.start}, {self.start + self.count}), {self.end}'

    def __repr__(self) -> str:
        return str(self)


def dfs(curr_key: int, curr_val: int, intervals: typing.List[typing.List[Interval]]) -> int:
    res = curr_val
    if curr_key >= len(intervals):
        return res

    for interval in intervals[curr_key]:
        mapped = interval.map_num(num=res)
        if res != mapped:
            res = mapped
            break

    return dfs(curr_key=curr_key + 1, curr_val=res, intervals=intervals)


if __name__ == '__main__':
    with open('2023/day5/input.txt', 'r') as input_file:
        intervals: typing.List[typing.List[Interval]] = [[]]
        seeds: typing.List[int] = []
        idx = -1
        for i, line in enumerate(input_file):
            if i == 0:
                seeds = list(map(int, line.strip().split(': ')[1].split()))
            elif line:
                if 'map:' in line:
                    idx += 1
                elif line[0].isdigit():
                    digits = list(map(int, line.split()))
                    if idx >= len(intervals):
                        intervals.append([])
                    intervals[idx].append(Interval(start=digits[1], end=digits[0], count=digits[2]))
    min_location = sys.maxsize
    for seed in seeds:
        res = dfs(curr_key=0, curr_val=seed, intervals=intervals)
        if res < min_location:
            min_location = res

    print(f'Part 1: {min_location}')

    seed_intervals: typing.List[Interval] = []
    for i in range(0, len(seeds), 2):
        seed_intervals.append(Interval(start=seeds[i], end=seeds[i], count=seeds[i + 1]))

    min_location = sys.maxsize
    for seed in seed_intervals:
        ranges = [(seed.start, seed.start + seed.count)]
        for i in range(len(intervals)):
            new_intervals = []
            while ranges:
                current = ranges.pop()
                for interval in intervals[i]:
                    start = max(interval.start, current[0])
                    end = min(interval.start + interval.count, current[1])
                    if start < end:
                        offset = interval.end - interval.start
                        new_intervals.append((start + offset, end + offset))

                        if start > current[0]:
                            ranges.append((current[0], start))
                        if end < current[1]:
                            ranges.append((end, current[1]))
                        break
                else:
                    new_intervals.append(current)
            ranges = new_intervals

        min_location = min(min_location, min([seed[0] for seed in ranges]))

    print(f'Part 2: {min_location}')
