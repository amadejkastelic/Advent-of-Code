import typing
from collections import defaultdict


def main():
    file_name = input('Enter input path: ')

    with open(file_name, 'r') as f:
        polymer, insertions = f.read().split('\n\n')

    insertions = dict(
        insertion.strip().split(' -> ') for insertion in insertions.split('\n')
    )

    #result = _execute_steps(polymer=polymer, insertions=insertions, steps=10)
    #print(f'Part 1: {max(result.values()) - min(result.values())}')

    result = _execute_steps(polymer=polymer, insertions=insertions, steps=40)
    print(f'Part 2: {max(result.values()) - min(result.values())}')


def _execute_steps(
    polymer: str, insertions: typing.Dict[str, str], steps: int = 10
) -> typing.Dict[str, int]:
    # Build a dict that will contain all our pairs and their counts
    pairs = defaultdict(int)
    # Build a dict that will contain all our characters and their count, to easily calculate the final result.
    chars = defaultdict(int)

    for i in range(1, len(polymer)):
        # Add pair appearance counts
        pairs[polymer[i - 1] + polymer[i]] += 1
    for char in polymer:
        # Add char appearance counts
        chars[char] += 1

    for i in range(steps):
        #print(f'Executing step {i + 1}...')
        # For each step, go through all pairs
        for pair, count in pairs.copy().items():
            char = insertions[pair]
            # Remove old pair
            pairs[pair] -= count
            # Add two new pairs (insert new char between them)
            pairs[pair[0] + char] += count
            pairs[char + pair[1]] += count
            # Add new char to our count dict
            chars[char] += count
        #print(chars)
        #print(pairs)

    return chars


if __name__ == '__main__':
    main()
