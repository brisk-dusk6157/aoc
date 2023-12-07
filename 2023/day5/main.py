from pprint import pprint
import typing as t
import fileinput
import itertools
import string
from collections import defaultdict


def apply_map(intervals, map):
    translated = []
    remaining = intervals[:]
    for d_start, s1, s2 in map:
        shift = d_start - s1
        new_remaining = []
        for i1, i2 in remaining:
            if i1 <= s2 and s1 <= i2:
                u1, u2 = max(i1, s1), min(i2, s2)
                translated.append((u1 + shift, u2 + shift))
                if i1 < u1-1:
                    new_remaining.append((i1, u1-1))
                if u2+1 < i2:
                    new_remaining.append((u2+1, i2))
            else:
                new_remaining.append((i1, i2))
        remaining = merge(new_remaining)
    result = merge(translated + remaining)
    print(intervals, result, sorted(translated), sorted(remaining))
    return result


def merge(intervals):
    intervals = list(sorted(intervals))
    if len(intervals) < 2:
        return intervals
    else:
        first, second = intervals[:2]
        if first[1] + 1>= second[0]:
            return merge([(first[0], second[1])] + intervals[2:])
        else:
            return [first] + merge(intervals[1:])


def part2():
    intervals = []
    maps = []
    map = []
    for i, line in enumerate(fileinput.input()):
        line = line.strip()
        if i == 0:
            seed_inp = [int(x) for x in line.split(':')[1].split()]
            intervals = [(x, x + n - 1) for (x, n) in zip(seed_inp[::2], seed_inp[1::2])]
        elif i == 1:
            continue
        elif not line:
            maps.append(map)
            map = []
        elif line[0] in string.ascii_lowercase:
            continue
        else:
            d_start, s_start, n = line.split()
            d_start, s_start, n = int(d_start), int(s_start), int(n)
            map.append((d_start, s_start, s_start + n - 1))

    for map in maps:
        intervals = apply_map(intervals, map)

    pprint(list(sorted(intervals)))
    print(min(intervals))


if __name__ == '__main__':
    part2()
