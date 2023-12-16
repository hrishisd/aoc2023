def get_layers(seq: list[int]) -> list[list[int]]:
    layers = [seq]
    while any(n != 0 for n in layers[-1]):
        prev = layers[-1]
        next_layer = [prev[i] - prev[i - 1] for i in range(1, len(prev))]
        layers.append(next_layer)
    return layers


def predict(seq: list[int]) -> int:
    layers = get_layers(seq)
    next_item = 0
    for layer in reversed(layers):
        next_item += layer[-1]
    return next_item


def predict_prev(seq: list[int]) -> int:
    layers = get_layers(seq)
    next_item = 0
    for layer in reversed(layers):
        next_item = layer[0] - next_item
    return next_item


def test_predict():
    assert predict([0, 3, 6, 9, 12, 15]) == 18
    assert predict([1, 3, 6, 10, 15, 21]) == 28
    assert predict([10, 13, 16, 21, 30, 45]) == 68


def test_predict_prev():
    assert predict_prev([0, 3, 6, 9, 12, 15]) == -3
    assert predict_prev([1, 3, 6, 10, 15, 21]) == 0
    assert predict_prev([10, 13, 16, 21, 30, 45]) == 5


def part1(seqs: list[list[int]]) -> int:
    return sum(map(predict, seqs))


def part2(seqs: list[list[int]]) -> int:
    return sum(map(predict_prev, seqs))


with open("input.txt") as f:
    seqs = [[int(n) for n in line.split()] for line in f]
    print("part 1:", part1(seqs))
    print("part 1:", part2(seqs))
