from functools import cache


@cache
def find_solutions(springs, sizes, group_size=0):
    if not springs:
        return not sizes and not group_size
    num_solutions = 0
    symbol = ['.', '#'] if springs[0] == '?' else springs[0]
    for sym in symbol:
        if sym == '#':
            num_solutions += find_solutions(springs[1:], sizes, group_size + 1)
        else:
            if group_size:
                if sizes and sizes[0] == group_size:
                    num_solutions += find_solutions(springs[1:], sizes[1:])
            else:
                num_solutions += find_solutions(springs[1:], sizes)
    return num_solutions


if __name__ == "__main__":
    with open('2023/day12/input.txt', "r") as f:
        parsed_data = [[line.split()[0], tuple(map(int, line.split()[1].split(',')))] for line in f.read().splitlines()]

    print('Part 1: ' + str(sum(find_solutions((springs + '.'), sizes) for springs, sizes in parsed_data)))
    print(
        'Part 2: '
        + str(sum(find_solutions(('?'.join([springs] * 5) + '.'), (sizes * 5)) for springs, sizes in parsed_data))
    )
