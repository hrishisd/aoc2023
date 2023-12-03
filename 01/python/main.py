def part1(lines: list[str]) -> int:
    res = 0
    for line in lines:
        digits = [int(d) for d in line if d.isnumeric()]
        calibration_value = digits[0] * 10 + digits[-1]
        res += calibration_value
    return res


def part2(lines: list[str]) -> int:
    res = 0
    for line in lines:
        digits = []
        for i in range(len(line)):
            if line[i].isnumeric():
                digits.append(int(line[i]))
                continue
            remaining = line[i:]
            for digit_str, value in [
                ("one", 1),
                ("two", 2),
                ("three", 3),
                ("four", 4),
                ("five", 5),
                ("six", 6),
                ("seven", 7),
                ("eight", 8),
                ("nine", 9),
            ]:
                if remaining.startswith(digit_str):
                    digits.append(value)
                    continue
        res += digits[0] * 10 + digits[-1]
    return res


with open("../input.txt") as f:
    lines = [line.strip() for line in f]
print(f"part 1: {part1(lines)}")
print(f"part 2: {part2(lines)}")
