from dataclasses import dataclass


@dataclass
class Card:
    winning_nums: set[int]
    our_nums: set[int]

    def num_matches(self) -> int:
        return sum(int(n in self.winning_nums) for n in self.our_nums)


def parse_card(line: str) -> Card:
    colon_pos = line.find(":")
    bar_pos = line.find("|", colon_pos)
    winning_nums = line[colon_pos + 1 : bar_pos - 1].split()
    our_nums = line[bar_pos + 1 :].split()
    return Card(
        winning_nums={int(n) for n in winning_nums},
        our_nums={int(n) for n in our_nums},
    )


def part1(cards: list[Card]) -> int:
    def count_points(card: Card) -> int:
        matches = card.num_matches()
        if matches == 0:
            return 0
        return 1 << (matches - 1)

    return sum(count_points(card) for card in cards)


def part2(cards: list[Card]) -> int:
    """
    graph: card i has edge to j if i < j <= i + num_matches(i)
    want to count number of times we visit an node
    """
    n = len(cards)
    copies = [1] * n
    for i, card in enumerate(cards):
        copies[i]
        for j in range(i + 1, i + 1 + card.num_matches()):
            copies[j] += copies[i]
    return sum(copies)


def main():
    with open("input.txt") as f:
        cards = [parse_card(line) for line in f]
        print(f"part 1: {part1(cards)}")
        print(f"part 2: {part2(cards)}")


if __name__ == "__main__":
    main()
