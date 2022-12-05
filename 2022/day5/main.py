import typing


def parse_input(inp: typing.List[str]):
    stacks = [[] for i in range(int(inp[-1][-2]))]
    for line in inp:
        step = 0
        for i in range(1, len(line), 4):
            if line[i] == '1':
                return stacks
            if 65 <= ord(line[i]) <= 90:
                stacks[step].insert(0, line[i])
            step += 1
    return stacks


def move(stacks: typing.List[typing.List[str]], n: int, f: int, t: int):
    for i in range(n):
        stacks[t - 1].append(stacks[f - 1].pop())


def move_v2(stacks: typing.List[typing.List[str]], n: int, f: int, t: int):
    to_add = [stacks[f - 1].pop() for _ in range(n)]
    to_add.reverse()
    stacks[t - 1] += to_add


with open('2022/day5/input.txt') as file:
    inp = file.read()

unparsed, instructions = inp.split('\n\n')

stacks = parse_input(unparsed.split('\n'))

for instruction in instructions.strip().split('\n'):
    instruction = instruction.split(' ')
    move(
        stacks=stacks,
        n=int(instruction[1]),
        f=int(instruction[3]),
        t=int(instruction[5]),
    )

result = ''
for stack in stacks:
    result += stack[-1]
print(f'Part 1: {result}')

stacks = parse_input(unparsed.split('\n'))

for instruction in instructions.strip().split('\n'):
    instruction = instruction.split(' ')
    move_v2(
        stacks=stacks,
        n=int(instruction[1]),
        f=int(instruction[3]),
        t=int(instruction[5]),
    )

result = ''
for stack in stacks:
    result += stack[-1]
print(f'Part 2: {result}')
