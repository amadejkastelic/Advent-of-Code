with open('2022/day4/input.txt') as file:
    pairs = file.readlines()

result_1 = 0
result_2 = 0
for pair in pairs:
    x, y = pair.strip().split(',')
    x, y = list(map(int, x.split('-'))), list(map(int, y.split('-')))
    x, y = set(range(x[0], x[1] + 1)), set(range(y[0], y[1] + 1))

    if x.issubset(y) or y.issubset(x):
        result_1 += 1

    if x & y:
        result_2 += 1

print(f'Part 1: {result_1}')
print(f'Part 2: {result_2}')
