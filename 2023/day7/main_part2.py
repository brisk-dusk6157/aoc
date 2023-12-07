import fileinput
from collections import Counter

M = {
    'A': 14,
    'K': 13,
    'Q': 12,
    'T': 10,
    'J': 1,
}

def parse(hand):
    result = []
    for c in hand:
        result.append(M.get(c, None) or int(c))
    return tuple(result)


def hand_type(hand):
    counter = Counter(hand)
    jokers = counter.pop(1, 0)
    pattern = sorted(counter.values())
    if pattern:
        pattern[-1] += jokers
    else:
        return 7
    if pattern == [5]:
        return 7
    elif pattern == [1, 4]:
        return 6
    elif pattern == [2, 3]:
        return 5
    elif pattern == [1, 1, 3]:
        return 4
    elif pattern == [1, 2, 2]:
        return 3
    elif pattern == [1, 1, 1, 2]:
        return 2
    else:
        assert pattern == [1,1,1,1,1], "Unknown pattern"
        return 1


def is_higher(h1, h2):
    ht1, ht2 = hand_type(h1), hand_type(h2)
    if ht1 == ht2:
        for c1, c2 in zip(h1, h2):
            if c1 > c2:
                return True
            elif c1 < c2:
                return False
        raise ValueError("Impossible")
    return ht1 > ht2


def sort(tuples):
    for i in range(0, len(tuples)):
        for j in range(i+1, len(tuples)):
            if is_higher(tuples[i][0], tuples[j][0]):
                tuples[i], tuples[j] = tuples[j], tuples[i]

def main():
    tuples = []
    for i, line in enumerate(fileinput.input()):
        hand, bid = line.split()
        tuples.append((parse(hand), int(bid)))
    sort(tuples)
    result = 0
    for i, (_, bid) in enumerate(tuples):
        result += (i+1)*bid
    print(result)


if __name__ == '__main__':
    main()