import math
import time
import typing

INSTRUCTION_TO_INDEX = {
    'L': 0,
    'R': 1,
}


if __name__ == '__main__':
    network: typing.Dict[str, typing.Tuple[str, str]] = {}
    instructions = ''

    with open('2023/day8/input.txt', 'r') as input_file:
        for i, line in enumerate(input_file):
            line = line.strip()
            if i == 0:
                instructions = line
            elif line:
                node, lr = line.split(' = ')
                l, r = lr.strip('()').split(', ')
                network[node] = (l, r)

    start = time.time()
    current = 'AAA'
    if current in network:
        steps = 0
        while current != 'ZZZ':
            for instruction in instructions:
                current = network[current][INSTRUCTION_TO_INDEX[instruction]]
                steps += 1

        print(f'Part 1: {steps}')
        print(f'Took {round((time.time() - start)*1000)}ms')

    start = time.time()
    steps = 0
    curr_pos = list(filter(lambda pos: pos[-1] == 'A', network.keys()))
    steps_to_find = [[0, False] for _ in range(len(curr_pos))]
    while not all([step[1] for step in steps_to_find]):
        for instruction in instructions:
            for i, pos in enumerate(curr_pos):
                curr_pos[i] = network[curr_pos[i]][INSTRUCTION_TO_INDEX[instruction]]
                if not steps_to_find[i][1]:
                    steps_to_find[i][0] += 1
                if curr_pos[i][-1] == 'Z':
                    steps_to_find[i][1] = True
            steps += 1
    print(f'Part 2: {math.lcm(*[step[0] for step in steps_to_find])}')
    print(f'Took {round((time.time() - start)*1000)}ms')
