import fileinput
import string
from collections import defaultdict
from pprint import pprint


def edges(c, i, j):
    if c == '-':
        return [(i, j - 1), (i, j + 1)]
    elif c == '|':
        return [(i - 1, j), (i + 1, j)]
    elif c == 'L':
        return [(i - 1, j), (i, j + 1)]
    elif c == 'J':
        return [(i - 1, j), (i, j - 1)]
    elif c == 'F':
        return [(i, j + 1), (i + 1, j)]
    elif c == '7':
        return [(i, j - 1), (i + 1, j)]
    else:
        raise ValueError("impossible")


T = (-1, 0)
R = (0, 1)
B = (1, 0)
L = (0, -1)
TURNS = {
    'L': {T: R, R: T, B: L, L: B},
    'F': {L: T, T: L, B: R, R: B},
    'J': {B: R, R: B, T: L, L: T},
    '7': {T: R, R: T, B: L, L: B}
}


def new_view_direction(dir, tile):
    if tile in '-|':
        return dir
    return TURNS[tile][dir]


def fill_region_containing(i, j, map, cycle):
    region = {(i, j)}
    queue = [(i, j)]
    while queue:
        i, j = queue.pop(0)
        for di, dj in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
            ci, cj = i + di, j + dj
            if (ci, cj) in map and (ci, cj) not in cycle and (ci, cj) not in region:
                queue.append((ci, cj))
                region.add((ci, cj))
    return region


def main():
    # read map
    graph = defaultdict(set)
    map = {}
    si, sj = None, None
    N, M = 0, 0
    for i, line in enumerate(fileinput.input()):
        line = line.strip()
        M = len(line)
        N += 1
        for j, c in enumerate(line):
            map[(i, j)] = c
            if c == '.':
                continue
            elif c == 'S':
                si = i
                sj = j
            else:
                for e in edges(c, i, j):
                    graph[(i, j)].add(e)

    # derive starting symbol
    candidates = set('|-7JFL')
    if (si, sj) in graph.get((si - 1, sj), set()):
        candidates = candidates & set('|JL')
    if (si, sj) in graph.get((si + 1, sj), set()):
        candidates = candidates & set('|7F')
    if (si, sj) in graph.get((si, sj - 1), set()):
        candidates = candidates & set('-7J')
    if (si, sj) in graph.get((si, sj + 1), set()):
        candidates = candidates & set('-FL')
    assert len(candidates) == 1
    s = candidates.pop()
    for e in edges(s, si, sj):
        graph[(si, sj)].add(e)
    map[si, sj] = s

    # find cycle
    i, j = si, sj
    steps = 0
    cycle_seen = set()
    cycle_path = []
    while True:
        cycle_seen.add((i, j))
        cycle_path.append((i, j))
        cands = (graph[(i, j)] - cycle_seen)
        if not cands:
            break
        i, j = cands.pop()
        steps += 1

    upd_map = []
    for i in range(N):
        line = []
        upd_map.append(line)
        for j in range(M):
            c = map[(i, j)]
            if (i, j) in cycle_seen:
                c = '@'
            else:
                c = ','
            line.append(c)

    fi, fj = cycle_path[0]
    si, sj = cycle_path[1]
    if si - fi == 0:
        dir = (0, 1)
    else:
        dir = (1, 0)
    combined_region = set()
    is_outside = False
    for n, (i, j) in enumerate(cycle_path):
        old_dir = dir
        dir = new_view_direction(dir, map[(i, j)])
        for (di, dj) in (old_dir, dir):
            si, sj = i + di, j + dj
            if not ((0 <= si < N) and (0 <= sj < M)):
                is_outside = True
                continue
            if (si, sj) in cycle_path:
                continue
            region = fill_region_containing(si, sj, map, cycle_seen)
            combined_region = combined_region | region

    if is_outside:
        inside = {(i, j) for i in range(N) for j in range(M)} - cycle_seen - combined_region
    else:
        inside = combined_region

    for (si, sj) in inside:
        upd_map[si][sj] = 'x'

    print('\n'.join([''.join(line) for line in upd_map]))
    print(len(inside))


if __name__ == '__main__':
    main()
