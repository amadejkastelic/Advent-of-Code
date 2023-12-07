import enum
import typing


ALL_CARDS = {
    '2': 0, '3': 1, '4': 2, '5': 3, '6': 4, '7': 5, '8': 6, '9': 7, 'T': 8, 'J': 9, 'Q': 10, 'K': 11, 'A': 12
}


class HandType(enum.Enum):
    HIGH_CARD = 1
    ONE_PAIR = 2
    TWO_PAIR = 3
    THREE_OF_A_KIND = 4
    FULL_HOUSE = 5
    FOUR_OF_A_KIND = 6
    FIVE_OF_A_KIND = 7


class Hand(object):
    def __init__(self, cards: str, bid: int) -> None:
        self.cards = cards
        self.bid = bid
        self.type = self._type()

    def __eq__(self, other: 'Hand') -> bool:
        return self.cards == other.cards

    def __gt__(self, other: 'Hand') -> bool:
        if self.type.value > other.type.value:
            return True
        elif self.type.value < other.type.value:
            return False

        for my_card, their_card in zip(self.cards, other.cards):
            if my_card == their_card:
                continue
            return self._card_strength(my_card) > self._card_strength(their_card)

    def __lt__(self, other: 'Hand') -> bool:
        return other > self

    @staticmethod
    def _card_strength(card: str) -> int:
        return ALL_CARDS[card]

    def _type(self) -> HandType:
        unique_cards = set(self.cards)
        if len(unique_cards) == 1:
            return HandType.FIVE_OF_A_KIND
        elif len(unique_cards) == 2 and all([self.cards.count(c) in (1, 4) for c in self.cards]):
            return HandType.FOUR_OF_A_KIND
        elif len(unique_cards) == 2 and all([self.cards.count(c) in (2, 3) for c in self.cards]):
            return HandType.FULL_HOUSE
        elif len(unique_cards) == 3 and all([self.cards.count(c) in (1, 3) for c in self.cards]):
            return HandType.THREE_OF_A_KIND
        elif len(unique_cards) == 3:
            return HandType.TWO_PAIR
        elif len(unique_cards) == 4:
            return HandType.ONE_PAIR
        return HandType.HIGH_CARD


if __name__ == '__main__':
    hands: typing.List[Hand] = []

    with open('2023/day7/input.txt', 'r') as input_file:
        for line in input_file:
            cards, bid = line.strip().split()
            hands.append(Hand(cards=cards, bid=int(bid)))

    result = 0
    for i, hand in enumerate(sorted(hands)):
        result += (i + 1) * hand.bid
    print(f'Part 1: {result}')
