#include <algorithm>
#include <fstream>
#include <iostream>
#include <numeric>
#include <sstream>
#include <string>
#include <vector>

struct CubeSet
{
    const int r;
    const int g;
    const int b;
    CubeSet(int r, int g, int b) : r{r}, g{g}, b{b} {}
};

struct Game
{
    const int id;
    const std::vector<CubeSet> cube_sets;

    Game(int id, std::vector<CubeSet> &&cube_sets)
        : id{id}, cube_sets{cube_sets} {};

    static Game parse(const std::string &line)
    {
        auto colon_loc = line.find(':');
        int game_id{std::stoi(line.substr(5, colon_loc))};
        std::string rest = line.substr(colon_loc + 2);
        std::istringstream input_stream{rest};
        std::string segment;
        std::vector<CubeSet> cube_sets;
        while (std::getline(input_stream, segment, ';'))
        {
            std::istringstream segment_stream{segment};
            std::string pair;
            int r{0};
            int g{0};
            int b{0};
            while (std::getline(segment_stream, pair, ','))
            {
                std::istringstream pair_stream{pair};
                int count;
                std::string color;
                pair_stream >> count >> color;
                if (color == "red")
                {
                    r = count;
                }
                else if (color == "green")
                {
                    g = count;
                }
                else
                {
                    b = count;
                }
            }
            CubeSet cube_set{r, g, b};
            cube_sets.push_back(std::move(cube_set));
        }
        return Game{game_id, std::move(cube_sets)};
    }
};

std::ostream &operator<<(std::ostream &out, const CubeSet &cubes)
{
    out << "CubeSet {" << cubes.r << ", " << cubes.g << ", " << cubes.b << "}";
    return out;
}

std::ostream &operator<<(std::ostream &out, const Game &game)
{
    out << "Game {" << game.id << ", [";
    std::string sep{""};
    for (const auto &cubes : game.cube_sets)
    {
        out << sep << cubes;
        sep = ", ";
    }
    out << "]}";
    return out;
}

auto part1(const std::vector<Game> &games) -> int
{
    // filter less than 12 red cubes, 13 green cubes, and 14 blue cubes
    auto can_make_set = [](const CubeSet &cubes)
    {
        auto [r, g, b] = cubes;
        return r <= 12 and g <= 13 and b <= 14;
    };

    return std::accumulate(
        games.begin(), games.end(), 0, [&](int id_sum, const Game &game)
        {
        if (std::all_of(game.cube_sets.begin(), game.cube_sets.end(),
                        can_make_set)) {
          return game.id + id_sum;
        } else {
          return id_sum;
        } });
}
auto part2(const std::vector<Game> &games) -> int
{
    auto required_cubes = [](const Game &game)
    {
        return std::accumulate(game.cube_sets.begin(), game.cube_sets.end(),
                               CubeSet{0, 0, 0}, [](auto acc, auto set)

                               { return CubeSet{std::max(acc.r, set.r),
                                                std::max(acc.g, set.g),
                                                std::max(acc.b, set.b)}; });
    };
    return std::accumulate(games.begin(), games.end(), 0,
                           [&](int power_sum, const Game &game)
                           {
                               auto [r, g, b] = required_cubes(game);
                               auto power = r * g * b;
                               return power + power_sum;
                           });
}

int main()
{
    std::ifstream input{"../input.txt"};
    if (!input)
    {
        std::cerr << "Error opening file." << std::endl;
        return 1;
    }
    std::vector<Game> games;
    std::string line;
    while (std::getline(input, line))
    {
        games.push_back(Game::parse(line));
    }
    std::cout << "part 1: " << part1(games) << std::endl;
    std::cout << "part 2: " << part2(games) << std::endl;
}