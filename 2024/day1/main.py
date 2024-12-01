l1, l2 = [], []
with open("2024/day1/input.txt") as f:
    for line in f:
        l1.append(int(line.split()[0]))
        l2.append(int(line.split()[1]))

print(sum([max(a, b) - min(a, b) for a, b in zip(sorted(l1), sorted(l2))]))
print(sum([num * l2.count(num) for num in l1]))
