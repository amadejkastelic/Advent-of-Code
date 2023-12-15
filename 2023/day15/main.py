import typing
from collections import defaultdict


class String(object):
    def __init__(self, value: str):
        self.value = value

    def __hash__(self) -> int:
        result = 0
        for char in self.value:
            result += ord(char)
            result *= 17
            result %= 256
        return result


if __name__ == '__main__':
    with open('2023/day15/input.txt', 'r') as input_file:
        steps = input_file.read().strip().split(',')

    result = 0
    for step in steps:
        result += hash(String(step))
    print(f'Part 1: {result}')

    boxes: typing.Dict[int, typing.Dict[str, int]] = defaultdict(lambda: {})
    for step in steps:
        box = hash(String(step.split('-')[0].split('=')[0]))
        if '=' in step:
            key, value = step.split('=')
            boxes[box][key] = int(value)
        else:
            key = step[:-1]
            if key in boxes[box]:
                boxes[box].pop(key)

    result = 0
    for box, contents in boxes.items():
        for i, (key, value) in enumerate(contents.items()):
            result += (box + 1) * (i + 1) * value
    print(f'Part 2: {result}')
