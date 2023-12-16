from dataclasses import dataclass
import collections

LABEL_TO_STRENGTH = {
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "T": 10,
    "J": 11,
    "Q": 12,
    "K": 13,
    "A": 14,
}


@dataclass(frozen=True, order=True)
class HandScore:
    kind: int
    high_cards: tuple[int, ...]


@dataclass(frozen=True)
class Card:
    label: str

    def strength(self) -> int:
        return LABEL_TO_STRENGTH[self.label]

    def __repr__(self) -> str:
        return self.label


@dataclass(frozen=True)
class Hand:
    cards: list[Card]
    bid: int

    def __repr__(self) -> str:
        card_str = "".join(str(c) for c in self.cards)
        return f"cards={card_str}, bid={self.bid}"

    def score(self) -> HandScore:
        card_to_count = collections.Counter(self.cards)
        cards_by_count_desc = sorted(
            card_to_count.keys(),
            key=lambda c: (card_to_count[c], c.strength()),
            reverse=True,
        )
        card_weights_by_count_desc = tuple(
            (card.strength() for card in cards_by_count_desc)
        )
        counts = set(card_to_count.values())
        if counts == {5}:
            return HandScore(6, card_weights_by_count_desc)
        elif counts == {4, 1}:
            return HandScore(5, card_weights_by_count_desc)
        elif counts == {3, 2}:
            return HandScore(4, card_weights_by_count_desc)
        elif counts == {3, 1, 1}:
            return HandScore(3, card_weights_by_count_desc)
        elif counts == {2, 1, 1, 1}:
            return HandScore(2, card_weights_by_count_desc)
        else:
            return HandScore(1, card_weights_by_count_desc)


def test_score():
    assert parse_hand("AAAAA 0").score() == HandScore(6, (14,))
    assert parse_hand("KKKAA 0").score() == HandScore(4, (13, 14))
    assert parse_hand("AKKAK 0").score() == HandScore(4, (13, 14))
    assert parse_hand("Q4A5J 0").score() == HandScore(1, (14, 12, 11, 5, 4))


def parse_cards(cards: str) -> list[Card]:
    return [Card(c) for c in cards]


def parse_hand(s: str) -> Hand:
    cards, bid = s.split()
    return Hand(parse_cards(cards), int(bid))


def part1(hands: list[Hand]) -> int:
    ranked_hands = sorted(hands, key=lambda h: h.score())
    acc = 0
    print("Ranking: \n")
    for rank, hand in enumerate(ranked_hands, start=1):
        acc += rank * hand.bid
        print(f"{rank}: {hand}, {hand.score()}")
    return acc


with open("input.txt") as f:
    lines = [line.strip().split() for line in f]
    hands = [Hand(parse_cards(cards), int(bid)) for cards, bid in lines]
    print(f"part 1: {part1(hands)}")
