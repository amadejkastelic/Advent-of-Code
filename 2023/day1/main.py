str_num = {
    'one': 1,
    'two': 2,
    'three': 3,
    'four': 4,
    'five': 5,
    'six': 6,
    'seven': 7,
    'eight': 8,
    'nine': 9,
}


def part1() -> int:
    res = 0
    with open('input.txt', 'r') as inp:
        for line in inp:
            line = line.strip()
            left, right = '', ''
            for i in range(len(line)):
                if left and right:
                    break
                if not left and line[i].isdigit():
                    left = line[i]
                if not right and line[-i - 1].isdigit():
                    right = line[-i - 1]
            res += int(left + right)
    return res


def part2() -> int:
    res = 0
    with open('input.txt', 'r') as inp:
        for line in inp:
            line = line.strip()
            left, right = '', ''
            for i in range(len(line)):
                if left and right:
                    break
                if not left and line[i].isdigit():
                    left = line[i]
                elif not left:
                    for key in str_num.keys():
                        if line[i:].startswith(key):
                            left = str(str_num[key])
                if not right and line[-i-1].isdigit():
                    right = line[-i-1]
                elif not right:
                    for key in str_num.keys():
                        if line[::-1][i:].startswith(key[::-1]):
                            right = str(str_num[key])
            res += int(left + right)
            print(left + right)
    return res


print(part2())
