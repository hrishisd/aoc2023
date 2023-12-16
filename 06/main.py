from dataclasses import dataclass
from functools import reduce
import operator as op


@dataclass
class Race:
    time: int
    record_dist: int


def num_ways_to_win(race: Race) -> int:
    def dist_traveled(button_press: int) -> int:
        speed = button_press
        time = race.time - button_press
        return speed * time

    return sum(
        1
        for button_press in range(1, race.time)
        if dist_traveled(button_press) > race.record_dist
    )


def part1(races: list[Race]) -> int:
    return reduce(op.mul, map(num_ways_to_win, races), 1)


def part2(race: Race) -> int:
    return num_ways_to_win(race)


with open("input.txt") as f:
    times = next(f).split(": ")[1].strip().split()
    dists = next(f).split(": ")[1].strip().split()
    combined_time = int("".join(times))
    combined_dist = int("".join(dists))
    races = [Race(int(t), int(d)) for t, d in zip(times, dists)]
    print(f"part 1: {part1(races)}")
    print(f"part 2: {part2(Race(combined_time, combined_dist))}")
