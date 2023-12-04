import time
import typing


class Card(object):
    def __init__(self, id: int, numbers: typing.List[int], winning_numbers: typing.List[int]):
        self.id = id
        self.numbers = numbers
        self.winning_numbers = winning_numbers

    @classmethod
    def parse(cls, raw: str) -> 'Card':
        all_numbers = raw.split(': ')[1].split(' | ')
        return cls(
            id=int(raw.split(':')[0].split()[1]),
            numbers=list(map(int, all_numbers[1].split())),
            winning_numbers=list(map(int, all_numbers[0].split())),
        )

    @property
    def point_value(self) -> int:
        return int(2 ** (self.number_of_matches - 1))

    @property
    def number_of_matches(self) -> int:
        return len(set(self.numbers).intersection(set(self.winning_numbers)))


if __name__ == '__main__':
    all_cards: typing.List[Card] = []
    with open('2023/day4/input.txt', 'r') as input_file:
        raw_cards = [line.strip() for line in input_file]
        for raw_card in raw_cards:
            all_cards.append(Card.parse(raw_card))

    start = time.time()
    print(f'Part 1: {sum([card.point_value for card in all_cards])}')
    print(f'Took {round((time.time() - start)*1000)}ms')

    start = time.time()
    counts = [1] * len(all_cards)
    for card in all_cards:
        for i in range(card.id, card.id + card.number_of_matches):
            counts[i] += counts[card.id - 1]
    print(f'Part 2: {sum(counts)}')
    print(f'Took {round((time.time() - start)*1000)}ms')
