from dataclasses import dataclass
import itertools


@dataclass(frozen=True)
class Number:
    value: int
    positions: set[tuple[int, int]]


def is_symbol(c: str) -> bool:
    return not c.isalnum() and c != "."


def main():
    def neighbors(r: int, c: int) -> list[tuple[int, int]]:
        return [
            (r + dr, c + dc)
            for dr in (-1, 0, 1)
            for dc in (-1, 0, 1)
            if (dr, dc) != (0, 0) and 0 <= r + dr < n_rows and 0 <= c + dc < n_cols
        ]

    def parse_nums(line: str, row: int) -> list[Number]:
        nums = []
        groups = itertools.groupby(
            enumerate(line), key=lambda idx_c: idx_c[1].isdigit()
        )
        for isnum, group in groups:
            if isnum:
                group = list(group)
                positions = {(row, col) for col, _ in group}
                value = int("".join(d for _, d in group))
                nums.append(Number(value, positions))
        return nums

    def part1() -> int:
        def is_adj_to_symbol(r, c):
            return any(is_symbol(grid[rr][cc]) for rr, cc in neighbors(r, c))

        return sum(
            num.value
            for num in nums
            if any(is_adj_to_symbol(r, c) for r, c in num.positions)
        )

    def part2() -> int:
        pos_to_num: dict[tuple[int, int], int] = {}
        for num in nums:
            for pos in num.positions:
                pos_to_num[pos] = num.value
        res = 0
        for r in range(n_rows):
            for c in range(n_cols):
                if grid[r][c] == "*":
                    neighboring_nums = {
                        pos_to_num[pos] for pos in neighbors(r, c) if pos in pos_to_num
                    }
                    if len(neighboring_nums) == 2:
                        n1, n2 = neighboring_nums
                        res += n1 * n2
        return res

    with open("../input.txt") as f:
        grid = [line.strip() for line in f]
        n_rows = len(grid)
        n_cols = len(grid[0])
        nums = [num for row, line in enumerate(grid) for num in parse_nums(line, row)]
        print(f"part 1: {part1()}")
        print(f"part 2: {part2()}")


if __name__ == "__main__":
    main()


def test_is_symbol():
    assert not is_symbol(".")
    assert not is_symbol("9")
    assert is_symbol("$")
