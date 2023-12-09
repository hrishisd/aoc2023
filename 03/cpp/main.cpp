#include <algorithm>
#include <cctype>
#include <fstream>
#include <functional>
#include <iostream>
#include <numeric>
#include <unordered_map>
#include <unordered_set>
#include <utility>
#include <vector>

struct Number {
  const unsigned long value;
  const std::vector<std::pair<int, int>> positions;
  Number(const unsigned long value,
         std::vector<std::pair<int, int>> &&positions)
      : value{value}, positions{positions} {}
};

std::ostream &operator<<(std::ostream &os, const Number &number) {
  os << "Number {" << number.value << ", [";
  auto sep{""};
  for (const auto &[row, col] : number.positions) {
    os << sep << "(" << row << "," << col << ")";
    sep = ", ";
  }
  os << ']';
  return os;
}

struct PairHash {
  std::size_t operator()(const std::pair<int, int> &p) const {
    auto hash1 = std::hash<int>{}(p.first);
    auto hash2 = std::hash<int>{}(p.second);
    return hash1 ^ (hash2 << 1);
  }
};

auto digits_to_number(const std::vector<int> &digits) -> unsigned long {
  return std::accumulate(
      digits.begin(), digits.end(), 0,
      [](unsigned long acc, int digit) { return acc * 10 + digit; });
}

auto neighbors(int r, int c, size_t n_rows, size_t n_cols)
    -> std::vector<std::pair<int, int>> {
  std::vector<std::pair<int, int>> res;
  for (int dr = -1; dr <= 1; dr++) {
    for (int dc = -1; dc <= 1; dc++) {
      if (r + dr >= 0 && r + dr < static_cast<int>(n_rows) && c + dc >= 0 and
          c + dc < static_cast<int>(n_cols)) {
        res.emplace_back(r + dr, c + dc);
      }
    }
  }
  return res;
}

auto part1(
    const std::vector<Number> &numbers,
    const std::unordered_set<std::pair<int, int>, PairHash> &symbol_positions,
    size_t n_rows, size_t n_cols) -> unsigned long {

  auto is_adj_to_symbol = [&](std::pair<int, int> position) {
    auto [r, c] = position;
    auto adj = neighbors(r, c, n_rows, n_cols);
    return std::any_of(adj.begin(), adj.end(), [&](auto pos) {
      return symbol_positions.contains(pos);
    });
  };

  auto res = 0;
  for (const auto &num : numbers) {
    if (std::any_of(num.positions.begin(), num.positions.end(),
                    is_adj_to_symbol)) {
      res += num.value;
    }
  }
  return res;
}

auto part2(
    const std::vector<Number> &numbers,
    const std::unordered_set<std::pair<int, int>, PairHash> &star_positions,
    size_t n_rows, size_t n_cols) -> int {
  std::unordered_map<std::pair<int, int>, int, PairHash> pos_to_num;
  for (const auto &num : numbers) {
    for (const auto &pos : num.positions) {
      pos_to_num[pos] = num.value;
    }
  }
  int res = 0;
  for (const auto &star_pos : star_positions) {
    auto adj_positions =
        neighbors(star_pos.first, star_pos.second, n_rows, n_cols);
    std::unordered_set<int> adjacent_numbers;
    for (const auto &pos : adj_positions) {
      auto entry_ptr = pos_to_num.find(pos);
      if (entry_ptr != pos_to_num.end()) {
        auto [_, value] = *entry_ptr;
        adjacent_numbers.insert(value);
      }
    }
    if (adjacent_numbers.size() == 2) {
      res += std::accumulate(adjacent_numbers.begin(), adjacent_numbers.end(),
                             1, std::multiplies<int>());
    }
  }
  return res;
}

int main() {
  auto input = std::ifstream{"../example.txt"};
  if (!input) {
    std::cerr << "Error opening file." << '\n';
    return 1;
  }

  std::string line;
  int row_idx = 0;

  std::vector<Number> numbers;
  std::unordered_set<std::pair<int, int>, PairHash> star_positions;
  std::unordered_set<std::pair<int, int>, PairHash> symbol_positions;

  while (std::getline(input, line)) {
    std::vector<int> accumulated_digits{};
    std::vector<std::pair<int, int>> digit_positions;
    for (int col_idx = 0; col_idx < static_cast<int>(line.length());
         col_idx++) {
      char c = line.at(col_idx);
      if (std::isdigit(c)) {
        accumulated_digits.push_back(c - '0');
        digit_positions.push_back(std::make_pair(row_idx, col_idx));
      } else {
        if (!accumulated_digits.empty()) {
          auto value = digits_to_number(accumulated_digits);
          numbers.push_back(Number{value, std::move(digit_positions)});
          accumulated_digits = {};
          digit_positions = {};
        }
        if (c == '*') {
          star_positions.insert(std::make_pair(row_idx, col_idx));
        }
        if (c != '.') {
          symbol_positions.insert(std::make_pair(row_idx, col_idx));
        }
      }
    }
    row_idx += 1;
  }

  auto n_cols = line.length();
  std::cout << "part 1: " << part1(numbers, symbol_positions, row_idx, n_cols)
            << '\n';
  std::cout << "part 2: " << part2(numbers, star_positions, row_idx, n_cols)
            << '\n';
  return 0;
}