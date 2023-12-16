import itertools
import math
from typing import Iterator


def part1(graph: dict[str, tuple[str, str]], commands: Iterator[str]) -> int:
    curr = "AAA"
    path_len = 0
    while curr != "ZZZ":
        cmd = next(commands)
        left, right = graph[curr]
        if cmd == "L":
            curr = left
        else:
            curr = right
        path_len += 1
    return path_len


def part2(graph: dict[str, tuple[str, str]], commands: str) -> int:
    k = len(commands)

    def steps_to_z(node: str) -> int:
        command_idx = 0
        while node[-1] != "Z":
            if commands[command_idx % k] == "L":
                node = graph[node][0]
            else:
                node = graph[node][1]
            command_idx += 1
        return command_idx

    return math.lcm(*(steps_to_z(node) for node in graph if node[-1] == "A"))


with open("input.txt") as f:

    def parse_line(s: str) -> tuple[str, str, str]:
        node, _, left, right = s.split()
        left = left[1:-1]
        right = right[:-1]
        return node, left, right

    header = next(f).strip()
    next(f)  # skip blank line
    graph = {}
    for line in f:
        node, left, right = parse_line(line)
        graph[node] = (left, right)

    print(f"part 1: {part1(graph, itertools.cycle(header))}")
    print(f"part 2: {part2(graph, header)}")
