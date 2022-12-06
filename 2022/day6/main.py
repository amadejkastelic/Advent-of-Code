def find_unique(datastream: str, n: int) -> int:
    for i in range(len(datastream)):
        seen = {datastream[i]}
        for j in range(i + 1, i + n):
            if j >= len(datastream) - 1:
                break
            if datastream[j] in seen:
                break
            seen.add(datastream[j])
            if len(seen) == n:
                return j + 1

with open('2022/day6/input.txt') as file:
    datastream = file.read()

print('Part 1: {}'.format(find_unique(datastream, 4)))
print('Part 2: {}'.format(find_unique(datastream, 14)))
