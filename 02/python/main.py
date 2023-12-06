from dataclasses import dataclass


@dataclass(frozen=True)
class CubeSet:
    red: int = 0
    green: int = 0
    blue: int = 0


@dataclass(frozen=True)
class Game:
    game_id: int
    sets: list[CubeSet]


def parse_game(line: str) -> Game:
    game_header, sets = line.split(":")
    game_id = int(game_header.split()[1])
    sets = sets.split(";")
    cubesets = []
    for set in sets:
        tokens = [s for s in set.replace(",", "").split() if s]
        counts = tokens[::2]
        colors = tokens[1::2]
        args = {color: int(count) for color, count in zip(colors, counts)}
        cubeset = CubeSet(**args)
        cubesets.append(cubeset)
    return Game(game_id=game_id, sets=cubesets)


def part1(games: list[Game]) -> int:
    def possible(game: Game) -> bool:
        return all(
            cubes.blue <= 14 and cubes.red <= 12 and cubes.green <= 13
            for cubes in game.sets
        )

    return sum(game.game_id for game in games if possible(game))


def part2(games: list[Game]) -> int:
    def power(game: Game):
        return (
            max(cubes.red for cubes in game.sets)
            * max(cubes.green for cubes in game.sets)
            * max(cubes.blue for cubes in game.sets)
        )

    return sum(power(game) for game in games)


with open("../input.txt") as f:
    games = []
    for line in f:
        game = parse_game(line.strip())
        games.append(game)
    print(f"part 1: {part1(games)}")
    print(f"part 2: {part2(games)}")


def test_parse_game():
    line = "Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green"
    game = parse_game(line)
    assert game == Game(
        1, [CubeSet(blue=3, red=4), CubeSet(red=1, green=2, blue=6), CubeSet(green=2)]
    )
