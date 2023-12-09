import typing


if __name__ == '__main__':
    histories: typing.List[typing.List[int]] = []
    with open('2023/day9/input.txt', 'r') as input_file:
        for line in input_file:
            histories.append(list(map(int, line.strip().split())))

    result1 = 0
    result2 = 0
    for history in histories:
        diffs = [history]
        while not all([diff == 0 for diff in diffs[-1]]):
            diffs.append([j - i for i, j in zip(diffs[-1][:-1], diffs[-1][1:])])
        temp_res1 = diffs[-1][-1]
        temp_res2 = diffs[-1][0]
        for i in range(len(diffs) - 2, -1, -1):
            temp_res1 += diffs[i][-1]
            temp_res2 = diffs[i][0] - temp_res2
        result1 += temp_res1
        result2 += temp_res2

    print(f'Part 1: {result1}')
    print(f'Part 2: {result2}')
