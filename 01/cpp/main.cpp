#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <ctype.h>
#include <algorithm>

int part1(const std::vector<std::string> &lines)
{
    int res = 0;
    for (const auto &line : lines)
    {
        auto isdigit = [](char c)
        { return std::isdigit(c); };
        auto first_digit = std::find_if(line.begin(), line.end(), isdigit);
        auto last_digit = std::find_if(line.rbegin(), line.rend(), isdigit);
        int x = {*first_digit - '0'};
        int y = {*last_digit - '0'};
        int value = {10 * x + y};
        res += value;
    }
    return res;
}

int part2(const std::vector<std::string> &lines)
{
    std::vector<std::string> numbers{"one", "two", "three", "four", "five", "six", "seven", "eight", "nine"};
    int res{0};
    for (const auto &line : lines)
    {
        // find first number from left
        size_t first_left_num_idx{std::string::npos};
        int left_digit{0};
        for (size_t numeric_value = 1; numeric_value <= numbers.size(); numeric_value++)
        {
            const std::string &number{numbers[numeric_value - 1]};
            size_t idx = line.find(number);
            if (idx < first_left_num_idx)
            {
                first_left_num_idx = idx;
                left_digit = numeric_value;
            }
        }
        for (size_t i = 0; i < std::min(line.length(), first_left_num_idx); i++)
        {
            if (std ::isdigit(line[i]))
            {
                left_digit = {line[i] - '0'};
                break;
            }
        }

        // find first number from the right
        size_t last_right_num_idx{0};
        int right_digit{0};
        for (size_t numeric_value = 1; numeric_value <= numbers.size(); numeric_value++)
        {
            const std::string &number{numbers[numeric_value - 1]};
            size_t idx = line.rfind(number);
            if (idx != std::string::npos && idx > last_right_num_idx)
            {
                last_right_num_idx = idx;
                right_digit = numeric_value;
            }
        }
        for (size_t i = line.length() - 1; i >= last_right_num_idx; i--)
        {
            if (std ::isdigit(line[i]))
            {
                right_digit = {line[i] - '0'};
                break;
            }
        }
        res += (left_digit * 10) + right_digit;
    }
    return res;
}

int main()
{
    std::ifstream input("../input.txt");
    if (!input)
    {
        std::cerr << "Error opening file." << std::endl;
        return 1;
    }
    std::vector<std::string> lines;
    std::string line;
    while (std::getline(input, line))
    {
        lines.push_back(line);
    }
    std::cout << "part 1: " << part1(lines) << '\n';
    std::cout << "part 2: " << part2(lines) << '\n';
    return 0;
}
