import fileinput
import itertools
from collections import defaultdict


def main():
    numbers = []
    symbols = {}
    for i, line in enumerate(fileinput.input()):
        line = line.strip()
        number = 0
        j_start = 0
        c: str
        for j, c in enumerate(line):
            if c.isdigit():
                if number == 0:
                    j_start = j
                number = 10 * number + int(c)
            else:
                if number != 0:
                    numbers.append((number, i, j_start, j-1))
                number = 0
                if c != '.':
                    symbols[i,j] = c
        if number > 0:
            numbers.append((number, i, j_start, len(line)-1))

    sum_numbers = []
    for k, (n, i, j_start, j_end) in enumerate(numbers):
        for (vi, vj) in itertools.product([i-1, i, i+1], range(j_start-1, j_end+2)):
            if (vi,vj) in symbols:
                sum_numbers.append(n)
                break

    candidates = defaultdict(set)
    for k, (n, i, j_start, j_end) in enumerate(numbers):
        for (vi, vj) in itertools.product([i-1, i, i+1], range(j_start-1, j_end+2)):
            if (vi,vj) in symbols and symbols[vi,vj] == "*":
                candidates[vi,vj].add(k)

    print(sum(sum_numbers))

    s = 0
    for part_ids in candidates.values():
        part_ids = list(part_ids)
        if len(part_ids) == 2:
            s += (numbers[part_ids[0]][0] * numbers[part_ids[1]][0])

    print(s)


if __name__ == '__main__':
    main()