PIPES = {
    "|": ((1, 0), (-1, 0)),
    "-": ((0, 1), (0, -1)),
    "L": ((-1, 0), (0, 1)),
    "J": ((-1, 0), (0, -1)),
    "7": ((1, 0), (0, -1)),
    "F": ((1, 0), (0, 1)),
}


def add(t1: tuple[int, int], t2: tuple[int, int]) -> tuple[int, int]:
    return t1[0] + t2[0], t1[1] + t2[1]


def explore(
    grid: list[str], start_row: int, start_col: int, start_pipe: str
) -> list[tuple[int, int]]:
    def get_dirs(pipe: str) -> tuple[tuple[int, int], tuple[int, int]]:
        if pipe == "S":
            return PIPES[start_pipe]
        return PIPES[pipe]

    loop = [(start_row, start_col)]
    while True:
        if loop[-1] == loop[0] and len(loop) > 1:
            break

        # print(f"{loop=}")
        r, c = loop[-1]
        nxt_dir, prev_dir = get_dirs(grid[r][c])
        nxt = add(loop[-1], nxt_dir)
        prev = add(loop[-1], prev_dir)
        if nxt in loop[-2:]:
            nxt, prev = prev, nxt
        loop.append(nxt)

    return loop


def test_explore():
    small_square = """
F7
LJ
""".split()
    explore(small_square, 0, 0, "F")
    square_loop = """
.....
.S-7.
.|.|.
.L-J.
.....
""".split()
    # explore(square_loop, 1, 1, "F")
    print(square_loop)


def part1(grid: list[str], start_pipe: str) -> int:
    start_row, start_col = next(
        (r, c)
        for r in range(len(grid))
        for c in range(len(grid[0]))
        if grid[r][c] == "S"
    )
    cells = explore(grid, start_row, start_col, start_pipe)
    return len(cells) // 2


def test_part1():
    grid1 = """.....
.S-7.
.|.|.
.L-J.
.....""".split()
    assert part1(grid1, "F") == 4

    grid2 = """..F7.
.FJ|.
SJ.L7
|F--J
LJ...
""".split()
    assert (part1(grid2, "F")) == 8


if __name__ == "__main__":
    with open("input.txt") as f:
        grid = [line.strip() for line in f]
        print("part 1:", part1(grid, "L"))
