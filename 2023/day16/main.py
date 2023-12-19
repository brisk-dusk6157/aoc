import fileinput
from collections import deque


def print_map(m, N, M):
    print_m = []
    for i in range(N):
        print_m.append([])
        for j in range(M):
            print_m[-1].append(m[i,j])
    print('\n'.join([''.join(xs) for xs in print_m]))
    print(N, M)


changes = {
    ((0, 1), '|'): [(-1, 0), (1, 0)],
    ((0, -1), '|'): [(-1, 0), (1, 0)],
    ((1, 0), '|'): [(1, 0)],
    ((-1, 0), '|'): [(-1, 0)],
    ((0, 1), '-'): [(0, 1)],
    ((0, -1), '-'): [(0, -1)],
    ((1, 0), '-'): [(0, -1), (0, 1)],
    ((-1, 0), '-'): [(0, -1), (0, 1)],
    ((0, 1), '/'): [(-1, 0)],
    ((0, -1), '/'): [(1, 0)],
    ((1, 0), '/'): [(0, -1)],
    ((-1, 0), '/'): [(0, 1)],
    ((0, 1), '\\'): [(1, 0)],
    ((0, -1), '\\'): [(-1, 0)],
    ((1, 0), '\\'): [(0, 1)],
    ((-1, 0), '\\'): [(0, -1)],
}


def main():
    m = {}
    N, M = 0, 0
    for i, line in enumerate(fileinput.input()):
        line = line.strip()
        N += 1
        M = len(line)
        for j, c in enumerate(line):
            m[i, j] = c

    def energize(start):
        lifo = deque([start])
        seen = set()
        energized = set()

        while lifo:
            tile, direction = state = lifo.popleft()
            if state in seen:
                continue
            seen.add(state)
            energized.add(tile)
            i, j = tile
            for di, dj in changes.get((direction, m[tile]), [direction]):
                ni = i + di
                nj = j + dj
                new_state = (i + di, j + dj), (di, dj)
                if new_state not in seen and 0 <= ni < N and 0 <= nj < M:
                    lifo.append(new_state)

        return len(energized)

    maxes = []
    for i in range(N):
        maxes.append(energize(((i, 0), (0, 1))))
        maxes.append(energize(((i, M-1), (0, -1))))
    for i in range(M):
        maxes.append(energize(((0, i), (1, 0))))
        maxes.append(energize(((N-1, i), (-1, 0))))

    print(max(maxes))


if __name__ == '__main__':
    main()
